import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler, RobustScaler
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
import joblib
import os
import warnings
from datetime import datetime
from typing import Dict, List, Tuple, Optional, Union
import logging

# Import advanced ML libraries
try:
    import xgboost as xgb
    XGBOOST_AVAILABLE = True
except ImportError:
    XGBOOST_AVAILABLE = False
    warnings.warn("XGBoost not available. Installing XGBoost recommended for better performance.")

try:
    import lightgbm as lgb
    LIGHTGBM_AVAILABLE = True
except ImportError:
    LIGHTGBM_AVAILABLE = False
    warnings.warn("LightGBM not available. Installing LightGBM recommended for better performance.")

try:
    from imblearn.over_sampling import SMOTE
    from imblearn.pipeline import Pipeline as ImbPipeline
    IMBALANCED_LEARN_AVAILABLE = True
except ImportError:
    IMBALANCED_LEARN_AVAILABLE = False
    warnings.warn("Imbalanced-learn not available. Installing recommended for handling class imbalance.")

try:
    import shap
    SHAP_AVAILABLE = True
except ImportError:
    SHAP_AVAILABLE = False
    warnings.warn("SHAP not available. Installing SHAP recommended for model interpretability.")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AdvancedRiskPredictor:
    """
    Advanced Risk Predictor with multiple ML algorithms and comprehensive feature engineering.
    
    Features:
    - Multiple ML algorithms (Logistic Regression, Random Forest, XGBoost, LightGBM)
    - Advanced feature engineering
    - Model comparison and selection
    - Cross-validation and hyperparameter tuning
    - Model interpretability with SHAP
    - Handling class imbalance
    """
    
    def __init__(self, algorithm='auto', random_state=42):
        self.algorithm = algorithm
        self.random_state = random_state
        self.models = {}
        self.best_model = None
        self.best_model_name = None
        self.scaler = RobustScaler()  # More robust to outliers
        self.feature_names = None
        self.is_trained = False
        self.model_performance = {}
        
        # Initialize available algorithms
        self._initialize_algorithms()
        
    def _initialize_algorithms(self):
        """Initialize available ML algorithms"""
        self.available_algorithms = {
            'logistic': LogisticRegression(random_state=self.random_state, max_iter=1000),
            'random_forest': RandomForestClassifier(random_state=self.random_state, n_estimators=100),
            'gradient_boosting': GradientBoostingClassifier(random_state=self.random_state)
        }
        
        # Add XGBoost if available
        if XGBOOST_AVAILABLE:
            self.available_algorithms['xgboost'] = xgb.XGBClassifier(
                random_state=self.random_state,
                eval_metric='logloss'
            )
            
        # Add LightGBM if available
        if LIGHTGBM_AVAILABLE:
            self.available_algorithms['lightgbm'] = lgb.LGBMClassifier(
                random_state=self.random_state,
                verbose=-1
            )
    
    def create_advanced_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Create comprehensive feature engineering"""
        features = df.copy()
        
        # Basic features
        features['fees_paid'] = features['fees_status'].map({'paid': 1, 'pending': 0})
        
        # Risk factors (inverted percentages)
        features['attendance_risk'] = (100 - features['attendance_percentage']) / 100
        features['marks_risk'] = (100 - features['marks_percentage']) / 100
        features['fees_risk'] = 1 - features['fees_paid']
        
        # Combined risk scores
        features['academic_risk'] = (features['attendance_risk'] + features['marks_risk']) / 2
        features['overall_risk'] = (features['attendance_risk'] * 0.4 + 
                                   features['marks_risk'] * 0.4 + 
                                   features['fees_risk'] * 0.2)
        
        # Performance categories
        features['attendance_category'] = pd.cut(
            features['attendance_percentage'], 
            bins=[0, 60, 75, 85, 100], 
            labels=['poor', 'below_avg', 'good', 'excellent']
        ).astype(str)
        
        features['marks_category'] = pd.cut(
            features['marks_percentage'], 
            bins=[0, 40, 60, 75, 100], 
            labels=['failing', 'below_avg', 'good', 'excellent']
        ).astype(str)
        
        # Interaction features
        features['attendance_marks_product'] = features['attendance_percentage'] * features['marks_percentage'] / 10000
        features['attendance_marks_ratio'] = features['attendance_percentage'] / (features['marks_percentage'] + 1)
        
        # Polynomial features for non-linear relationships
        features['attendance_squared'] = features['attendance_percentage'] ** 2
        features['marks_squared'] = features['marks_percentage'] ** 2
        
        # Distance from ideal performance
        features['distance_from_ideal'] = np.sqrt(
            (features['attendance_percentage'] - 100) ** 2 + 
            (features['marks_percentage'] - 100) ** 2
        )
        
        # Performance consistency (if we had historical data, this would be variance)
        # For now, use a proxy based on how close to average performance
        avg_performance = (features['attendance_percentage'] + features['marks_percentage']) / 2
        features['performance_consistency'] = 100 - abs(features['attendance_percentage'] - features['marks_percentage'])
        
        # Binary flags
        features['high_attendance'] = (features['attendance_percentage'] >= 85).astype(int)
        features['high_marks'] = (features['marks_percentage'] >= 75).astype(int)
        features['excellent_student'] = ((features['attendance_percentage'] >= 85) & 
                                       (features['marks_percentage'] >= 75)).astype(int)
        features['at_risk_student'] = ((features['attendance_percentage'] < 75) | 
                                     (features['marks_percentage'] < 60)).astype(int)
        
        # One-hot encode categorical features
        categorical_features = ['attendance_category', 'marks_category']
        for feature in categorical_features:
            if feature in features.columns:
                dummies = pd.get_dummies(features[feature], prefix=feature)
                features = pd.concat([features, dummies], axis=1)
                features.drop(feature, axis=1, inplace=True)
        
        return features
    
    def get_feature_columns(self, df: pd.DataFrame) -> List[str]:
        """Get numerical feature columns for ML model"""
        # Core numerical features
        base_features = [
            'attendance_percentage', 'marks_percentage', 'fees_paid',
            'attendance_risk', 'marks_risk', 'fees_risk', 'academic_risk', 'overall_risk',
            'attendance_marks_product', 'attendance_marks_ratio',
            'attendance_squared', 'marks_squared', 'distance_from_ideal',
            'performance_consistency', 'high_attendance', 'high_marks',
            'excellent_student', 'at_risk_student'
        ]
        
        # Add one-hot encoded features
        categorical_features = [col for col in df.columns if 
                              col.startswith(('attendance_category_', 'marks_category_'))]
        
        all_features = base_features + categorical_features
        
        # Filter to only include columns that exist in the dataframe
        return [col for col in all_features if col in df.columns]
    
    def create_risk_labels(self, df: pd.DataFrame, method='weighted') -> np.ndarray:
        """Create risk labels using different methods"""
        if method == 'weighted':
            return self._create_weighted_risk_labels(df)
        elif method == 'threshold':
            return self._create_threshold_risk_labels(df)
        else:
            raise ValueError(f"Unknown method: {method}")
    
    def _create_weighted_risk_labels(self, df: pd.DataFrame) -> np.ndarray:
        """Create risk labels using weighted approach"""
        labels = []
        for _, row in df.iterrows():
            risk_score = 0
            
            # Attendance factor (40% weight)
            if row['attendance_percentage'] < 60:
                risk_score += 0.4
            elif row['attendance_percentage'] < 75:
                risk_score += 0.2
            elif row['attendance_percentage'] < 85:
                risk_score += 0.1
                
            # Marks factor (40% weight)  
            if row['marks_percentage'] < 40:
                risk_score += 0.4
            elif row['marks_percentage'] < 60:
                risk_score += 0.2
            elif row['marks_percentage'] < 75:
                risk_score += 0.1
                
            # Fees factor (20% weight)
            if row['fees_status'] == 'pending':
                risk_score += 0.2
                
            # Classify risk with more granular thresholds
            if risk_score >= 0.6:
                labels.append(2)  # High Risk
            elif risk_score >= 0.3:
                labels.append(1)  # Medium Risk
            else:
                labels.append(0)  # Low Risk
                
        return np.array(labels)
    
    def _create_threshold_risk_labels(self, df: pd.DataFrame) -> np.ndarray:
        """Create risk labels using hard thresholds"""
        labels = []
        for _, row in df.iterrows():
            high_risk_conditions = [
                row['attendance_percentage'] < 60,
                row['marks_percentage'] < 40,
                (row['attendance_percentage'] < 70 and row['marks_percentage'] < 50)
            ]
            
            medium_risk_conditions = [
                row['attendance_percentage'] < 75,
                row['marks_percentage'] < 60,
                row['fees_status'] == 'pending'
            ]
            
            if any(high_risk_conditions):
                labels.append(2)  # High Risk
            elif any(medium_risk_conditions):
                labels.append(1)  # Medium Risk
            else:
                labels.append(0)  # Low Risk
                
        return np.array(labels)
    
    def train_single_model(self, X: pd.DataFrame, y: np.ndarray, algorithm: str) -> Dict:
        """Train a single model and return performance metrics"""
        if algorithm not in self.available_algorithms:
            raise ValueError(f"Algorithm {algorithm} not available")
        
        # Split data for validation
        X_train, X_val, y_train, y_val = train_test_split(
            X, y, test_size=0.2, random_state=self.random_state, stratify=y
        )
        
        # Handle class imbalance with SMOTE if available
        if IMBALANCED_LEARN_AVAILABLE and len(np.unique(y_train)) > 1:
            smote = SMOTE(random_state=self.random_state)
            try:
                X_train_balanced, y_train_balanced = smote.fit_resample(X_train, y_train)
            except ValueError:
                # If SMOTE fails, use original data
                X_train_balanced, y_train_balanced = X_train, y_train
        else:
            X_train_balanced, y_train_balanced = X_train, y_train
        
        # Create pipeline
        model = self.available_algorithms[algorithm]
        pipeline = Pipeline([
            ('scaler', self.scaler),
            ('classifier', model)
        ])
        
        # Train model
        pipeline.fit(X_train_balanced, y_train_balanced)
        
        # Evaluate model
        y_pred = pipeline.predict(X_val)
        y_pred_proba = pipeline.predict_proba(X_val)
        
        # Calculate metrics
        cv_scores = cross_val_score(pipeline, X_train, y_train, cv=5, scoring='f1_weighted')
        
        performance = {
            'algorithm': algorithm,
            'cv_mean': cv_scores.mean(),
            'cv_std': cv_scores.std(),
            'val_accuracy': (y_pred == y_val).mean(),
            'val_f1_weighted': cross_val_score(pipeline, X_val.values.reshape(-1, X_val.shape[1]) if len(X_val.shape) == 1 else X_val, y_val, cv=3, scoring='f1_weighted').mean() if len(X_val) > 0 else 0,
            'model': pipeline
        }
        
        # Add AUC score for multi-class
        try:
            if len(np.unique(y)) > 2:
                auc_score = roc_auc_score(y_val, y_pred_proba, multi_class='ovr', average='weighted')
            else:
                auc_score = roc_auc_score(y_val, y_pred_proba[:, 1])
            performance['auc_score'] = auc_score
        except Exception:
            performance['auc_score'] = 0.0
        
        return performance
    
    def train(self, df: pd.DataFrame, target_method='weighted') -> 'AdvancedRiskPredictor':
        """Train the model with comprehensive approach"""
        logger.info("Starting advanced model training...")
        
        # Feature engineering
        features_df = self.create_advanced_features(df)
        
        # Get feature columns
        feature_columns = self.get_feature_columns(features_df)
        self.feature_names = feature_columns
        
        # Prepare features and target
        X = features_df[feature_columns]
        y = self.create_risk_labels(df, method=target_method)
        
        logger.info(f"Training with {len(feature_columns)} features and {len(df)} samples")
        logger.info(f"Feature columns: {feature_columns}")
        logger.info(f"Class distribution: {np.bincount(y)}")
        
        # Train multiple models if algorithm is 'auto'
        if self.algorithm == 'auto':
            logger.info("Training multiple algorithms for comparison...")
            
            for algo_name in self.available_algorithms.keys():
                try:
                    logger.info(f"Training {algo_name}...")
                    performance = self.train_single_model(X, y, algo_name)
                    self.model_performance[algo_name] = performance
                    self.models[algo_name] = performance['model']
                    logger.info(f"{algo_name} - CV Score: {performance['cv_mean']:.3f} (+/- {performance['cv_std']:.3f})")
                except Exception as e:
                    logger.warning(f"Failed to train {algo_name}: {str(e)}")
            
            # Select best model based on cross-validation score
            if self.model_performance:
                best_algo = max(self.model_performance.keys(), 
                              key=lambda x: self.model_performance[x]['cv_mean'])
                self.best_model = self.models[best_algo]
                self.best_model_name = best_algo
                logger.info(f"Best algorithm: {best_algo} with CV score: {self.model_performance[best_algo]['cv_mean']:.3f}")
            else:
                # Fallback to simple logistic regression
                logger.warning("No models trained successfully, using simple logistic regression")
                self.best_model = Pipeline([
                    ('scaler', self.scaler),
                    ('classifier', LogisticRegression(random_state=self.random_state))
                ])
                self.best_model.fit(X, y)
                self.best_model_name = 'logistic_fallback'
        else:
            # Train specific algorithm
            logger.info(f"Training specific algorithm: {self.algorithm}")
            performance = self.train_single_model(X, y, self.algorithm)
            self.models[self.algorithm] = performance['model']
            self.model_performance[self.algorithm] = performance
            self.best_model = performance['model']
            self.best_model_name = self.algorithm
        
        self.is_trained = True
        logger.info("Model training completed successfully!")
        
        return self
    
    def predict_risk(self, df: pd.DataFrame) -> np.ndarray:
        """Predict risk for students"""
        if not self.is_trained:
            logger.warning("Model not trained. Using rule-based approach.")
            return self.create_risk_labels(df)
        
        # Feature engineering
        features_df = self.create_advanced_features(df)
        
        # Get features
        X = features_df[self.feature_names]
        
        # Predict
        predictions = self.best_model.predict(X)
        
        return predictions
    
    def predict_risk_proba(self, df: pd.DataFrame) -> np.ndarray:
        """Predict risk probabilities"""
        if not self.is_trained:
            logger.warning("Model not trained. Cannot provide probabilities.")
            return None
        
        # Feature engineering
        features_df = self.create_advanced_features(df)
        
        # Get features
        X = features_df[self.feature_names]
        
        # Predict probabilities
        probabilities = self.best_model.predict_proba(X)
        
        return probabilities
    
    def get_feature_importance(self) -> Optional[pd.DataFrame]:
        """Get feature importance from the best model"""
        if not self.is_trained or self.best_model is None:
            return None
        
        try:
            # Get the classifier from pipeline
            classifier = self.best_model.named_steps['classifier']
            
            # Get feature importance based on model type
            if hasattr(classifier, 'feature_importances_'):
                importance = classifier.feature_importances_
            elif hasattr(classifier, 'coef_'):
                importance = abs(classifier.coef_[0]) if len(classifier.coef_.shape) == 2 else abs(classifier.coef_)
            else:
                return None
            
            # Create DataFrame
            feature_importance_df = pd.DataFrame({
                'feature': self.feature_names,
                'importance': importance
            }).sort_values('importance', ascending=False)
            
            return feature_importance_df
            
        except Exception as e:
            logger.warning(f"Could not extract feature importance: {str(e)}")
            return None
    
    def explain_prediction(self, df: pd.DataFrame, student_index: int = 0) -> Optional[Dict]:
        """Explain individual prediction using SHAP (if available)"""
        if not SHAP_AVAILABLE or not self.is_trained:
            return None
        
        try:
            # Feature engineering
            features_df = self.create_advanced_features(df)
            X = features_df[self.feature_names]
            
            # Create explainer
            explainer = shap.Explainer(self.best_model)
            shap_values = explainer(X.iloc[[student_index]])
            
            # Return explanation
            return {
                'shap_values': shap_values.values[0],
                'feature_names': self.feature_names,
                'feature_values': X.iloc[student_index].values,
                'expected_value': shap_values.base_values[0] if hasattr(shap_values, 'base_values') else None
            }
            
        except Exception as e:
            logger.warning(f"Could not create SHAP explanation: {str(e)}")
            return None
    
    def get_model_performance_summary(self) -> pd.DataFrame:
        """Get summary of all model performances"""
        if not self.model_performance:
            return pd.DataFrame()
        
        summary_data = []
        for algo, perf in self.model_performance.items():
            summary_data.append({
                'Algorithm': algo,
                'CV_Mean': perf['cv_mean'],
                'CV_Std': perf['cv_std'],
                'Val_Accuracy': perf['val_accuracy'],
                'AUC_Score': perf.get('auc_score', 0),
                'Is_Best': algo == self.best_model_name
            })
        
        return pd.DataFrame(summary_data).sort_values('CV_Mean', ascending=False)
    
    def get_risk_category(self, risk_score: Union[int, np.ndarray]) -> Union[Tuple[str, str], List[Tuple[str, str]]]:
        """Convert numeric risk to category"""
        def _convert_single(score):
            if score == 2:
                return "High Risk", "🔴"
            elif score == 1:
                return "Medium Risk", "🟠"
            else:
                return "Safe", "🟢"
        
        if isinstance(risk_score, (list, np.ndarray)):
            return [_convert_single(score) for score in risk_score]
        else:
            return _convert_single(risk_score)
    
    def save_model(self, filepath: str = 'advanced_risk_model.pkl'):
        """Save trained model with all components"""
        if self.is_trained:
            model_data = {
                'best_model': self.best_model,
                'models': self.models,
                'model_performance': self.model_performance,
                'feature_names': self.feature_names,
                'best_model_name': self.best_model_name,
                'algorithm': self.algorithm,
                'scaler': self.scaler,
                'timestamp': datetime.now().isoformat()
            }
            joblib.dump(model_data, filepath)
            logger.info(f"Model saved to {filepath}")
    
    def load_model(self, filepath: str = 'advanced_risk_model.pkl'):
        """Load trained model"""
        if os.path.exists(filepath):
            model_data = joblib.load(filepath)
            self.best_model = model_data['best_model']
            self.models = model_data.get('models', {})
            self.model_performance = model_data.get('model_performance', {})
            self.feature_names = model_data['feature_names']
            self.best_model_name = model_data.get('best_model_name', 'unknown')
            self.algorithm = model_data.get('algorithm', 'auto')
            self.scaler = model_data.get('scaler', self.scaler)
            self.is_trained = True
            logger.info(f"Model loaded from {filepath}")
        else:
            logger.warning(f"Model file {filepath} not found")


# Backward compatibility class
class RiskPredictor(AdvancedRiskPredictor):
    """Backward compatible version of the risk predictor"""
    
    def __init__(self):
        super().__init__(algorithm='logistic')
        # Override with simple scaler for backward compatibility
        self.scaler = StandardScaler()
    
    def prepare_features(self, df):
        """Legacy method for backward compatibility"""
        features = df.copy()
        
        # Convert fees_status to numeric
        features['fees_paid'] = features['fees_status'].map({'paid': 1, 'pending': 0})
        
        # Create risk factors
        features['attendance_risk'] = (100 - features['attendance_percentage']) / 100
        features['marks_risk'] = (100 - features['marks_percentage']) / 100
        features['fees_risk'] = 1 - features['fees_paid']
        
        # Select final features
        feature_cols = ['attendance_percentage', 'marks_percentage', 'fees_paid', 
                       'attendance_risk', 'marks_risk', 'fees_risk']
        
        return features[feature_cols]
    
    def train(self, df):
        """Legacy training method"""
        X = self.prepare_features(df)
        y = self.create_risk_labels(df, method='weighted')
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        
        # Train simple model for backward compatibility
        self.model = LogisticRegression(random_state=42)
        self.model.fit(X_scaled, y)
        self.is_trained = True
        
        # Set up for advanced predictor compatibility
        self.best_model = Pipeline([
            ('scaler', self.scaler),
            ('classifier', self.model)
        ])
        self.feature_names = X.columns.tolist()
        
        return self

# Enhanced sample data generator for testing
def generate_sample_data(n_students=50, include_patterns=True, random_seed=42):
    """Generate realistic sample student data with various patterns"""
    np.random.seed(random_seed)
    
    students = []
    
    # Define student patterns for more realistic data
    patterns = {
        'excellent': 0.15,    # 15% excellent students
        'good': 0.35,         # 35% good students  
        'average': 0.30,      # 30% average students
        'struggling': 0.15,   # 15% struggling students
        'at_risk': 0.05       # 5% at-risk students
    }
    
    pattern_configs = {
        'excellent': {'attendance_mean': 95, 'attendance_std': 3, 'marks_mean': 85, 'marks_std': 8, 'fees_prob': 0.95},
        'good': {'attendance_mean': 85, 'attendance_std': 8, 'marks_mean': 75, 'marks_std': 10, 'fees_prob': 0.90},
        'average': {'attendance_mean': 75, 'attendance_std': 10, 'marks_mean': 65, 'marks_std': 12, 'fees_prob': 0.80},
        'struggling': {'attendance_mean': 65, 'attendance_std': 12, 'marks_mean': 50, 'marks_std': 15, 'fees_prob': 0.70},
        'at_risk': {'attendance_mean': 45, 'attendance_std': 15, 'marks_mean': 35, 'marks_std': 12, 'fees_prob': 0.50}
    }
    
    student_names = [
        'Alice Johnson', 'Bob Smith', 'Carol Davis', 'David Wilson', 'Emma Brown',
        'Frank Miller', 'Grace Lee', 'Henry Taylor', 'Ivy Chen', 'Jack Anderson',
        'Kate Williams', 'Liam Jones', 'Maya Patel', 'Noah Garcia', 'Olivia Martinez',
        'Paul Rodriguez', 'Quinn Thompson', 'Ruby Clark', 'Sam Lewis', 'Tina Walker',
        'Uma Singh', 'Victor Hall', 'Wendy Allen', 'Xavier Young', 'Yara King',
        'Zoe Wright', 'Adam Scott', 'Bella Green', 'Chris Adams', 'Diana Baker',
        'Ethan Nelson', 'Fiona Carter', 'George Mitchell', 'Hannah Perez', 'Ian Roberts',
        'Julia Turner', 'Kevin Phillips', 'Luna Campbell', 'Mason Parker', 'Nora Evans',
        'Oscar Edwards', 'Penny Collins', 'Quinn Stewart', 'Rosa Sanchez', 'Sean Morris',
        'Tara Rogers', 'Ulysses Reed', 'Vera Cook', 'Wade Morgan', 'Xara Bell'
    ]
    
    for i in range(n_students):
        # Determine student pattern
        if include_patterns:
            rand_val = np.random.random()
            cumulative_prob = 0
            pattern = 'average'  # default
            
            for pattern_name, prob in patterns.items():
                cumulative_prob += prob
                if rand_val <= cumulative_prob:
                    pattern = pattern_name
                    break
            
            config = pattern_configs[pattern]
        else:
            # Generate completely random data
            config = {
                'attendance_mean': np.random.uniform(60, 90),
                'attendance_std': np.random.uniform(5, 15),
                'marks_mean': np.random.uniform(50, 80),
                'marks_std': np.random.uniform(8, 15),
                'fees_prob': np.random.uniform(0.6, 0.95)
            }
        
        # Generate attendance with some correlation to base performance
        attendance = max(30, min(100, np.random.normal(config['attendance_mean'], config['attendance_std'])))
        
        # Generate marks with some correlation to attendance
        marks_base = config['marks_mean']
        if attendance < 60:
            marks_base *= 0.8  # Lower marks if very low attendance
        elif attendance > 90:
            marks_base *= 1.1  # Bonus for high attendance
            
        marks = max(20, min(100, np.random.normal(marks_base, config['marks_std'])))
        
        # Generate fees status
        fees_status = 'paid' if np.random.random() < config['fees_prob'] else 'pending'
        
        # Add some noise and edge cases
        if i < 5:  # First few students have some specific patterns
            if i == 0:  # Perfect student
                attendance, marks, fees_status = 98, 95, 'paid'
            elif i == 1:  # High risk student
                attendance, marks, fees_status = 45, 30, 'pending'
            elif i == 2:  # Medium risk - attendance issue
                attendance, marks, fees_status = 65, 75, 'paid'
            elif i == 3:  # Medium risk - marks issue
                attendance, marks, fees_status = 85, 45, 'paid'
            elif i == 4:  # Edge case - good marks but poor attendance
                attendance, marks, fees_status = 55, 80, 'pending'
        
        # Select name
        if i < len(student_names):
            name = student_names[i]
        else:
            name = f"Student {i+1}"
        
        students.append({
            'student_id': f'STU{i+1:03d}',
            'name': name,
            'attendance_percentage': round(attendance, 1),
            'marks_percentage': round(marks, 1),
            'fees_status': fees_status
        })
    
    return pd.DataFrame(students)


def analyze_student_data(df: pd.DataFrame, predictor: AdvancedRiskPredictor = None) -> Dict:
    """Comprehensive analysis of student data"""
    analysis = {}
    
    # Basic statistics
    analysis['total_students'] = len(df)
    analysis['attendance_stats'] = {
        'mean': df['attendance_percentage'].mean(),
        'median': df['attendance_percentage'].median(),
        'std': df['attendance_percentage'].std(),
        'min': df['attendance_percentage'].min(),
        'max': df['attendance_percentage'].max()
    }
    analysis['marks_stats'] = {
        'mean': df['marks_percentage'].mean(),
        'median': df['marks_percentage'].median(),
        'std': df['marks_percentage'].std(),
        'min': df['marks_percentage'].min(),
        'max': df['marks_percentage'].max()
    }
    
    # Fees analysis
    fees_counts = df['fees_status'].value_counts()
    analysis['fees_analysis'] = {
        'paid_count': fees_counts.get('paid', 0),
        'pending_count': fees_counts.get('pending', 0),
        'paid_percentage': (fees_counts.get('paid', 0) / len(df)) * 100
    }
    
    # Risk analysis
    if predictor and predictor.is_trained:
        risk_predictions = predictor.predict_risk(df)
        risk_counts = pd.Series(risk_predictions).value_counts()
        
        analysis['risk_analysis'] = {
            'safe_count': risk_counts.get(0, 0),
            'medium_risk_count': risk_counts.get(1, 0),
            'high_risk_count': risk_counts.get(2, 0),
            'high_risk_percentage': (risk_counts.get(2, 0) / len(df)) * 100
        }
        
        # Feature importance
        feature_importance = predictor.get_feature_importance()
        if feature_importance is not None:
            analysis['top_risk_factors'] = feature_importance.head(5).to_dict('records')
    
    # Performance categories
    attendance_categories = pd.cut(
        df['attendance_percentage'], 
        bins=[0, 60, 75, 85, 100], 
        labels=['poor', 'below_avg', 'good', 'excellent']
    ).value_counts()
    
    marks_categories = pd.cut(
        df['marks_percentage'], 
        bins=[0, 40, 60, 75, 100], 
        labels=['failing', 'below_avg', 'good', 'excellent']
    ).value_counts()
    
    analysis['performance_categories'] = {
        'attendance': attendance_categories.to_dict(),
        'marks': marks_categories.to_dict()
    }
    
    return analysis


def print_analysis_report(analysis: Dict):
    """Print a formatted analysis report"""
    print("\n" + "="*60)
    print("           STUDENT DATA ANALYSIS REPORT")
    print("="*60)
    
    print(f"\n📊 OVERALL STATISTICS")
    print(f"Total Students: {analysis['total_students']}")
    
    print(f"\n📅 ATTENDANCE ANALYSIS")
    att_stats = analysis['attendance_stats']
    print(f"  Mean: {att_stats['mean']:.1f}%")
    print(f"  Median: {att_stats['median']:.1f}%")
    print(f"  Range: {att_stats['min']:.1f}% - {att_stats['max']:.1f}%")
    print(f"  Standard Deviation: {att_stats['std']:.1f}%")
    
    print(f"\n📊 MARKS ANALYSIS")
    marks_stats = analysis['marks_stats']
    print(f"  Mean: {marks_stats['mean']:.1f}%")
    print(f"  Median: {marks_stats['median']:.1f}%")
    print(f"  Range: {marks_stats['min']:.1f}% - {marks_stats['max']:.1f}%")
    print(f"  Standard Deviation: {marks_stats['std']:.1f}%")
    
    print(f"\n💰 FEES ANALYSIS")
    fees = analysis['fees_analysis']
    print(f"  Paid: {fees['paid_count']} ({fees['paid_percentage']:.1f}%)")
    print(f"  Pending: {fees['pending_count']}")
    
    if 'risk_analysis' in analysis:
        print(f"\n🚨 RISK ANALYSIS")
        risk = analysis['risk_analysis']
        print(f"  🟢 Safe: {risk['safe_count']}")
        print(f"  🟠 Medium Risk: {risk['medium_risk_count']}")
        print(f"  🔴 High Risk: {risk['high_risk_count']} ({risk['high_risk_percentage']:.1f}%)")
        
        if 'top_risk_factors' in analysis:
            print(f"\n📈 TOP RISK FACTORS")
            for factor in analysis['top_risk_factors']:
                print(f"  {factor['feature']}: {factor['importance']:.3f}")
    
    print(f"\n📊 PERFORMANCE CATEGORIES")
    att_cat = analysis['performance_categories']['attendance']
    marks_cat = analysis['performance_categories']['marks']
    
    print(f"  Attendance Categories:")
    for category, count in att_cat.items():
        print(f"    {category}: {count}")
    
    print(f"  Marks Categories:")
    for category, count in marks_cat.items():
        print(f"    {category}: {count}")
    
    print("\n" + "="*60)


if __name__ == "__main__":
    print("🚀 Starting DropSafe Advanced ML Risk Assessment System...")
    
    # Generate comprehensive sample data
    print("\n📊 Generating sample student data...")
    sample_df = generate_sample_data(100, include_patterns=True)
    sample_df.to_csv('sample_students.csv', index=False)
    print(f"✅ Generated {len(sample_df)} student records and saved to sample_students.csv")
    
    # Initialize and train advanced predictor
    print("\n🤖 Training Advanced Risk Prediction Model...")
    predictor = AdvancedRiskPredictor(algorithm='auto')
    predictor.train(sample_df)
    
    # Save the trained model
    predictor.save_model('advanced_risk_model.pkl')
    print("✅ Advanced model trained and saved!")
    
    # Show model performance
    print("\n📈 Model Performance Summary:")
    performance_df = predictor.get_model_performance_summary()
    if not performance_df.empty:
        print(performance_df.to_string(index=False))
    
    # Make predictions
    print("\n🔍 Making Risk Predictions...")
    risks = predictor.predict_risk(sample_df)
    probabilities = predictor.predict_risk_proba(sample_df)
    
    # Add predictions to dataframe
    results_df = sample_df.copy()
    results_df['risk_score'] = risks
    risk_categories = predictor.get_risk_category(risks)
    results_df['risk_category'] = [cat[0] for cat in risk_categories]
    results_df['risk_emoji'] = [cat[1] for cat in risk_categories]
    
    # Save results
    results_df.to_csv('student_risk_predictions.csv', index=False)
    print("✅ Predictions saved to student_risk_predictions.csv")
    
    # Show feature importance
    print("\n🎯 Feature Importance:")
    feature_importance = predictor.get_feature_importance()
    if feature_importance is not None:
        print(feature_importance.head(10).to_string(index=False))
    
    # Comprehensive analysis
    print("\n📊 Performing Comprehensive Analysis...")
    analysis = analyze_student_data(sample_df, predictor)
    print_analysis_report(analysis)
    
    # Show some example predictions
    print("\n🎯 SAMPLE PREDICTIONS:")
    print("-" * 80)
    for i in range(min(10, len(sample_df))):
        student = sample_df.iloc[i]
        risk_cat, emoji = predictor.get_risk_category(risks[i])
        print(f"{emoji} {student['name']} (ID: {student['student_id']})")
        print(f"    Attendance: {student['attendance_percentage']}%, Marks: {student['marks_percentage']}%, Fees: {student['fees_status']}")
        print(f"    Risk Level: {risk_cat}")
        if probabilities is not None:
            probs = probabilities[i]
            print(f"    Probabilities - Safe: {probs[0]:.2f}, Medium: {probs[1]:.2f}, High: {probs[2]:.2f}")
        print()
    
    # Test backward compatibility
    print("\n🔄 Testing Backward Compatibility...")
    legacy_predictor = RiskPredictor()
    legacy_predictor.train(sample_df)
    legacy_risks = legacy_predictor.predict_risk(sample_df)
    
    compatibility_check = np.mean(risks == legacy_risks) * 100
    print(f"✅ Backward compatibility: {compatibility_check:.1f}% agreement with legacy model")
    
    print("\n🎉 All systems ready! The DropSafe ML environment is fully set up and tested.")
    print("\n📋 Next Steps:")
    print("   1. Run 'streamlit run teacher_dashboard.py' for the teacher interface")
    print("   2. Run 'streamlit run student_dashboard.py' for the student portal")
    print("   3. Use 'run.bat' (Windows) or 'run.sh' (Linux/Mac) for the launcher")