"""
Data Validation and Preprocessing Utilities for DropSafe
========================================================

This module provides comprehensive data validation, cleaning, and preprocessing
utilities for the DropSafe student risk assessment system.

Features:
- Input data validation and sanitization
- Data quality checks and reporting
- Missing data handling strategies
- Outlier detection and treatment
- Data transformation and normalization
- Export validation reports

Author: DropSafe Development Team
Date: 2024
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional, Union, Any
import warnings
from datetime import datetime
import logging
from pathlib import Path

# Import validation libraries if available
try:
    from pydantic import BaseModel, Field, validator
    from pydantic.dataclasses import dataclass
    PYDANTIC_AVAILABLE = True
except ImportError:
    PYDANTIC_AVAILABLE = False
    warnings.warn("Pydantic not available. Basic validation will be used.")

try:
    import pandera as pa
    from pandera import Column, DataFrameSchema, Check
    PANDERA_AVAILABLE = True
except ImportError:
    PANDERA_AVAILABLE = False
    warnings.warn("Pandera not available. Schema validation will be limited.")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class StudentDataValidator:
    """
    Comprehensive validator for student data in the DropSafe system.
    
    Provides validation, cleaning, and quality assessment for student records.
    """
    
    def __init__(self, strict_mode: bool = False):
        """
        Initialize the validator.
        
        Args:
            strict_mode: If True, validation errors will raise exceptions.
                        If False, warnings will be logged and data will be cleaned.
        """
        self.strict_mode = strict_mode
        self.validation_errors = []
        self.validation_warnings = []
        self.cleaned_data = None
        
        # Define expected data schema
        self.required_columns = ['student_id', 'name', 'attendance_percentage', 'marks_percentage', 'fees_status']
        self.optional_columns = ['email', 'phone', 'department', 'year', 'gender']
        
        # Define validation rules
        self.validation_rules = {
            'student_id': {
                'type': str,
                'required': True,
                'unique': True,
                'pattern': r'^STU\d{3,}$',
                'description': 'Student ID must follow pattern STU### (e.g., STU001)'
            },
            'name': {
                'type': str,
                'required': True,
                'min_length': 2,
                'max_length': 100,
                'description': 'Student name must be 2-100 characters'
            },
            'attendance_percentage': {
                'type': (int, float),
                'required': True,
                'min_value': 0,
                'max_value': 100,
                'description': 'Attendance must be between 0 and 100'
            },
            'marks_percentage': {
                'type': (int, float),
                'required': True,
                'min_value': 0,
                'max_value': 100,
                'description': 'Marks must be between 0 and 100'
            },
            'fees_status': {
                'type': str,
                'required': True,
                'allowed_values': ['paid', 'pending'],
                'description': 'Fees status must be either "paid" or "pending"'
            }
        }
    
    def create_pandera_schema(self) -> Optional['pa.DataFrameSchema']:
        """Create a Pandera schema for validation if available."""
        if not PANDERA_AVAILABLE:
            return None
        
        try:
            schema = pa.DataFrameSchema({
                'student_id': Column(
                    pa.String,
                    checks=[
                        Check.str_matches(r'^STU\d{3,}$'),
                        Check(lambda x: x.nunique() == len(x), error="Student IDs must be unique")
                    ],
                    nullable=False
                ),
                'name': Column(
                    pa.String,
                    checks=[
                        Check.str_length(2, 100)
                    ],
                    nullable=False
                ),
                'attendance_percentage': Column(
                    pa.Float,
                    checks=[
                        Check.in_range(0, 100)
                    ],
                    nullable=False
                ),
                'marks_percentage': Column(
                    pa.Float,
                    checks=[
                        Check.in_range(0, 100)
                    ],
                    nullable=False
                ),
                'fees_status': Column(
                    pa.String,
                    checks=[
                        Check.isin(['paid', 'pending'])
                    ],
                    nullable=False
                )
            })
            return schema
        except Exception as e:
            logger.warning(f"Could not create Pandera schema: {e}")
            return None
    
    def validate_dataframe_structure(self, df: pd.DataFrame) -> bool:
        """Validate the basic structure of the DataFrame."""
        errors = []
        warnings = []
        
        # Check if DataFrame is empty
        if df.empty:
            errors.append("DataFrame is empty")
        
        # Check required columns
        missing_columns = [col for col in self.required_columns if col not in df.columns]
        if missing_columns:
            errors.append(f"Missing required columns: {missing_columns}")
        
        # Check for completely empty columns
        empty_columns = [col for col in df.columns if df[col].isna().all()]
        if empty_columns:
            warnings.append(f"Completely empty columns found: {empty_columns}")
        
        # Check for duplicate columns
        duplicate_columns = df.columns[df.columns.duplicated()].tolist()
        if duplicate_columns:
            errors.append(f"Duplicate column names found: {duplicate_columns}")
        
        # Store results
        self.validation_errors.extend(errors)
        self.validation_warnings.extend(warnings)
        
        return len(errors) == 0
    
    def validate_data_types(self, df: pd.DataFrame) -> pd.DataFrame:
        """Validate and convert data types."""
        df_clean = df.copy()
        
        for column, rules in self.validation_rules.items():
            if column not in df_clean.columns:
                continue
            
            expected_type = rules['type']
            
            # Handle numeric columns
            if expected_type in [(int, float), int, float]:
                try:
                    # Try to convert to numeric
                    df_clean[column] = pd.to_numeric(df_clean[column], errors='coerce')
                    
                    # Check for invalid values that became NaN
                    invalid_mask = df_clean[column].isna() & df[column].notna()
                    if invalid_mask.any():
                        invalid_values = df.loc[invalid_mask, column].unique()
                        self.validation_warnings.append(
                            f"Invalid numeric values in {column}: {invalid_values}"
                        )
                    
                except Exception as e:
                    self.validation_errors.append(f"Could not convert {column} to numeric: {e}")
            
            # Handle string columns
            elif expected_type == str:
                df_clean[column] = df_clean[column].astype(str)
                
                # Clean string data
                df_clean[column] = df_clean[column].str.strip()
                df_clean[column] = df_clean[column].replace(['nan', 'None', ''], np.nan)
        
        return df_clean
    
    def validate_data_ranges(self, df: pd.DataFrame) -> pd.DataFrame:
        """Validate data ranges and constraints."""
        df_clean = df.copy()
        
        for column, rules in self.validation_rules.items():
            if column not in df_clean.columns:
                continue
            
            # Check min/max values
            if 'min_value' in rules:
                min_val = rules['min_value']
                invalid_mask = df_clean[column] < min_val
                if invalid_mask.any():
                    count = invalid_mask.sum()
                    self.validation_warnings.append(
                        f"{count} values in {column} are below minimum {min_val}"
                    )
                    # Clip values to minimum
                    df_clean.loc[invalid_mask, column] = min_val
            
            if 'max_value' in rules:
                max_val = rules['max_value']
                invalid_mask = df_clean[column] > max_val
                if invalid_mask.any():
                    count = invalid_mask.sum()
                    self.validation_warnings.append(
                        f"{count} values in {column} are above maximum {max_val}"
                    )
                    # Clip values to maximum
                    df_clean.loc[invalid_mask, column] = max_val
            
            # Check allowed values
            if 'allowed_values' in rules:
                allowed = rules['allowed_values']
                invalid_mask = ~df_clean[column].isin(allowed + [np.nan])
                if invalid_mask.any():
                    invalid_values = df_clean.loc[invalid_mask, column].unique()
                    self.validation_warnings.append(
                        f"Invalid values in {column}: {invalid_values}. Allowed: {allowed}"
                    )
                    # Replace invalid values with NaN
                    df_clean.loc[invalid_mask, column] = np.nan
            
            # Check string length
            if rules['type'] == str and 'min_length' in rules:
                min_len = rules['min_length']
                invalid_mask = df_clean[column].str.len() < min_len
                if invalid_mask.any():
                    count = invalid_mask.sum()
                    self.validation_warnings.append(
                        f"{count} values in {column} are shorter than minimum length {min_len}"
                    )
            
            if rules['type'] == str and 'max_length' in rules:
                max_len = rules['max_length']
                invalid_mask = df_clean[column].str.len() > max_len
                if invalid_mask.any():
                    count = invalid_mask.sum()
                    self.validation_warnings.append(
                        f"{count} values in {column} exceed maximum length {max_len}"
                    )
                    # Truncate long strings
                    df_clean.loc[invalid_mask, column] = df_clean.loc[invalid_mask, column].str[:max_len]
        
        return df_clean
    
    def validate_uniqueness(self, df: pd.DataFrame) -> bool:
        """Validate uniqueness constraints."""
        for column, rules in self.validation_rules.items():
            if column not in df.columns or not rules.get('unique', False):
                continue
            
            duplicated_mask = df[column].duplicated()
            if duplicated_mask.any():
                duplicate_values = df.loc[duplicated_mask, column].tolist()
                self.validation_errors.append(
                    f"Duplicate values found in {column}: {duplicate_values}"
                )
                return False
        
        return True
    
    def detect_outliers(self, df: pd.DataFrame, method: str = 'iqr') -> Dict[str, List[int]]:
        """Detect outliers in numeric columns."""
        outliers = {}
        numeric_columns = ['attendance_percentage', 'marks_percentage']
        
        for column in numeric_columns:
            if column not in df.columns:
                continue
            
            if method == 'iqr':
                Q1 = df[column].quantile(0.25)
                Q3 = df[column].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                
                outlier_mask = (df[column] < lower_bound) | (df[column] > upper_bound)
                outliers[column] = df.index[outlier_mask].tolist()
            
            elif method == 'zscore':
                z_scores = np.abs((df[column] - df[column].mean()) / df[column].std())
                outlier_mask = z_scores > 3
                outliers[column] = df.index[outlier_mask].tolist()
        
        return outliers
    
    def handle_missing_data(self, df: pd.DataFrame, strategy: str = 'smart') -> pd.DataFrame:
        """Handle missing data using various strategies."""
        df_clean = df.copy()
        
        missing_counts = df_clean.isnull().sum()
        missing_columns = missing_counts[missing_counts > 0]
        
        if not missing_columns.empty:
            logger.info(f"Missing data found in columns: {missing_columns.to_dict()}")
        
        for column in missing_columns.index:
            missing_count = missing_counts[column]
            total_count = len(df_clean)
            missing_pct = (missing_count / total_count) * 100
            
            self.validation_warnings.append(
                f"Missing data in {column}: {missing_count}/{total_count} ({missing_pct:.1f}%)"
            )
            
            # Choose strategy based on column and missing percentage
            if column in ['student_id', 'name']:
                # Critical columns - flag as error if too many missing
                if missing_pct > 5:
                    self.validation_errors.append(
                        f"Too much missing data in critical column {column}: {missing_pct:.1f}%"
                    )
                # For critical columns, remove rows with missing data
                df_clean = df_clean.dropna(subset=[column])
            
            elif column in ['attendance_percentage', 'marks_percentage']:
                if strategy == 'smart':
                    # Use median imputation for numeric columns
                    median_value = df_clean[column].median()
                    df_clean[column] = df_clean[column].fillna(median_value)
                    logger.info(f"Imputed missing {column} with median value: {median_value}")
                elif strategy == 'forward_fill':
                    df_clean[column] = df_clean[column].fillna(method='ffill')
                elif strategy == 'drop':
                    df_clean = df_clean.dropna(subset=[column])
            
            elif column == 'fees_status':
                # For fees status, assume 'pending' if missing
                df_clean[column] = df_clean[column].fillna('pending')
                logger.info(f"Imputed missing fees_status with 'pending'")
        
        return df_clean
    
    def validate_business_rules(self, df: pd.DataFrame) -> bool:
        """Validate business-specific rules."""
        is_valid = True
        
        # Rule 1: Students with very low attendance should have proportionally low marks
        suspicious_mask = (df['attendance_percentage'] < 50) & (df['marks_percentage'] > 80)
        if suspicious_mask.any():
            suspicious_students = df.loc[suspicious_mask, 'student_id'].tolist()
            self.validation_warnings.append(
                f"Suspicious pattern: Students with low attendance but high marks: {suspicious_students}"
            )
        
        # Rule 2: Students with pending fees and excellent performance
        excellent_unpaid_mask = (df['marks_percentage'] > 90) & (df['attendance_percentage'] > 90) & (df['fees_status'] == 'pending')
        if excellent_unpaid_mask.any():
            students = df.loc[excellent_unpaid_mask, 'student_id'].tolist()
            self.validation_warnings.append(
                f"High-performing students with pending fees: {students}"
            )
        
        # Rule 3: Check for impossible combinations
        impossible_mask = (df['attendance_percentage'] == 0) & (df['marks_percentage'] > 0)
        if impossible_mask.any():
            students = df.loc[impossible_mask, 'student_id'].tolist()
            self.validation_errors.append(
                f"Impossible combination: 0% attendance with marks > 0 for students: {students}"
            )
            is_valid = False
        
        return is_valid
    
    def generate_data_quality_report(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Generate a comprehensive data quality report."""
        report = {
            'timestamp': datetime.now().isoformat(),
            'total_records': len(df),
            'total_columns': len(df.columns),
            'validation_errors': self.validation_errors.copy(),
            'validation_warnings': self.validation_warnings.copy(),
            'data_completeness': {},
            'data_quality_scores': {},
            'outliers': {},
            'summary_statistics': {}
        }
        
        # Data completeness
        for column in df.columns:
            non_null_count = df[column].notna().sum()
            completeness = (non_null_count / len(df)) * 100
            report['data_completeness'][column] = {
                'non_null_count': int(non_null_count),
                'completeness_percentage': round(completeness, 2)
            }
        
        # Data quality scores
        for column in self.required_columns:
            if column in df.columns:
                # Calculate quality score based on completeness and validity
                completeness = report['data_completeness'][column]['completeness_percentage']
                
                # Check validity based on rules
                validity_score = 100
                if column in self.validation_rules:
                    rules = self.validation_rules[column]
                    
                    if 'min_value' in rules and 'max_value' in rules:
                        valid_range_mask = (df[column] >= rules['min_value']) & (df[column] <= rules['max_value'])
                        validity_score = (valid_range_mask.sum() / len(df)) * 100
                    
                    elif 'allowed_values' in rules:
                        valid_values_mask = df[column].isin(rules['allowed_values'])
                        validity_score = (valid_values_mask.sum() / len(df)) * 100
                
                overall_quality = (completeness + validity_score) / 2
                report['data_quality_scores'][column] = {
                    'completeness': round(completeness, 2),
                    'validity': round(validity_score, 2),
                    'overall_quality': round(overall_quality, 2)
                }
        
        # Outliers
        report['outliers'] = self.detect_outliers(df)
        
        # Summary statistics for numeric columns
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        for column in numeric_columns:
            if column in df.columns:
                stats = df[column].describe()
                report['summary_statistics'][column] = {
                    'mean': round(stats['mean'], 2),
                    'median': round(stats['50%'], 2),
                    'std': round(stats['std'], 2),
                    'min': round(stats['min'], 2),
                    'max': round(stats['max'], 2),
                    'skewness': round(df[column].skew(), 2),
                    'kurtosis': round(df[column].kurtosis(), 2)
                }
        
        return report
    
    def validate(self, df: pd.DataFrame, 
                missing_data_strategy: str = 'smart',
                generate_report: bool = True) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """
        Perform comprehensive validation and cleaning of student data.
        
        Args:
            df: Input DataFrame to validate
            missing_data_strategy: Strategy for handling missing data ('smart', 'drop', 'forward_fill')
            generate_report: Whether to generate a quality report
        
        Returns:
            Tuple of (cleaned_dataframe, quality_report)
        """
        logger.info("Starting comprehensive data validation...")
        
        # Reset validation results
        self.validation_errors = []
        self.validation_warnings = []
        
        # Step 1: Validate DataFrame structure
        if not self.validate_dataframe_structure(df):
            if self.strict_mode:
                raise ValueError(f"Structure validation failed: {self.validation_errors}")
        
        # Step 2: Validate and convert data types
        df_clean = self.validate_data_types(df)
        
        # Step 3: Handle missing data
        df_clean = self.handle_missing_data(df_clean, strategy=missing_data_strategy)
        
        # Step 4: Validate data ranges and constraints
        df_clean = self.validate_data_ranges(df_clean)
        
        # Step 5: Validate uniqueness constraints
        if not self.validate_uniqueness(df_clean):
            if self.strict_mode:
                raise ValueError(f"Uniqueness validation failed: {self.validation_errors}")
        
        # Step 6: Validate business rules
        if not self.validate_business_rules(df_clean):
            if self.strict_mode:
                raise ValueError(f"Business rule validation failed: {self.validation_errors}")
        
        # Step 7: Use Pandera schema validation if available
        if PANDERA_AVAILABLE:
            schema = self.create_pandera_schema()
            if schema:
                try:
                    df_clean = schema.validate(df_clean)
                    logger.info("Pandera schema validation passed")
                except Exception as e:
                    self.validation_warnings.append(f"Pandera validation warning: {str(e)}")
        
        # Store cleaned data
        self.cleaned_data = df_clean
        
        # Generate quality report
        quality_report = None
        if generate_report:
            quality_report = self.generate_data_quality_report(df_clean)
        
        logger.info(f"Data validation completed. {len(self.validation_errors)} errors, {len(self.validation_warnings)} warnings")
        
        return df_clean, quality_report
    
    def save_quality_report(self, report: Dict[str, Any], filepath: str = 'data_quality_report.json'):
        """Save data quality report to file."""
        import json
        
        try:
            with open(filepath, 'w') as f:
                json.dump(report, f, indent=2, default=str)
            logger.info(f"Quality report saved to {filepath}")
        except Exception as e:
            logger.error(f"Failed to save quality report: {e}")
    
    def print_validation_summary(self):
        """Print a summary of validation results."""
        print("\n" + "="*60)
        print("           DATA VALIDATION SUMMARY")
        print("="*60)
        
        if self.validation_errors:
            print(f"\n❌ ERRORS ({len(self.validation_errors)}):")
            for i, error in enumerate(self.validation_errors, 1):
                print(f"  {i}. {error}")
        
        if self.validation_warnings:
            print(f"\n⚠️  WARNINGS ({len(self.validation_warnings)}):")
            for i, warning in enumerate(self.validation_warnings, 1):
                print(f"  {i}. {warning}")
        
        if not self.validation_errors and not self.validation_warnings:
            print("\n✅ No validation issues found!")
        
        print("\n" + "="*60)


def validate_csv_file(filepath: str, 
                     strict_mode: bool = False,
                     save_cleaned: bool = True,
                     save_report: bool = True) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """
    Convenience function to validate a CSV file.
    
    Args:
        filepath: Path to the CSV file
        strict_mode: Whether to use strict validation
        save_cleaned: Whether to save the cleaned data
        save_report: Whether to save the quality report
    
    Returns:
        Tuple of (cleaned_dataframe, quality_report)
    """
    # Load CSV file
    try:
        df = pd.read_csv(filepath)
        logger.info(f"Loaded {len(df)} records from {filepath}")
    except Exception as e:
        logger.error(f"Failed to load CSV file: {e}")
        raise
    
    # Initialize validator
    validator = StudentDataValidator(strict_mode=strict_mode)
    
    # Validate data
    df_clean, report = validator.validate(df)
    
    # Print summary
    validator.print_validation_summary()
    
    # Save cleaned data
    if save_cleaned:
        cleaned_filepath = filepath.replace('.csv', '_cleaned.csv')
        df_clean.to_csv(cleaned_filepath, index=False)
        logger.info(f"Cleaned data saved to {cleaned_filepath}")
    
    # Save quality report
    if save_report and report:
        report_filepath = filepath.replace('.csv', '_quality_report.json')
        validator.save_quality_report(report, report_filepath)
    
    return df_clean, report


if __name__ == "__main__":
    # Example usage
    print("🔍 Testing Data Validation System...")
    
    # Create sample test data with some issues
    test_data = {
        'student_id': ['STU001', 'STU002', 'STU003', 'STU001', 'STU004'],  # Duplicate
        'name': ['Alice', 'Bob', '', 'David', 'Emma'],  # Missing name
        'attendance_percentage': [95, 85, 120, 65, -10],  # Out of range
        'marks_percentage': [90, 75, 85, np.nan, 95],  # Missing mark
        'fees_status': ['paid', 'pending', 'unknown', 'paid', 'paid']  # Invalid status
    }
    
    test_df = pd.DataFrame(test_data)
    print(f"Created test data with {len(test_df)} records")
    
    # Test validation
    validator = StudentDataValidator(strict_mode=False)
    clean_df, report = validator.validate(test_df)
    
    print(f"\nOriginal data shape: {test_df.shape}")
    print(f"Cleaned data shape: {clean_df.shape}")
    
    # Print validation summary
    validator.print_validation_summary()
    
    print("\n✅ Data validation system is working correctly!")