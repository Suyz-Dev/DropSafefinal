# DropSafe - Student Risk Assessment Platform
## Deployment Guide

## 🚀 Overview
This guide provides instructions for deploying the DropSafe Student Risk Assessment Platform in various environments.

## 📋 Prerequisites
- Python 3.8 or higher
- pip package manager
- Git (for cloning the repository)
- 4GB RAM minimum (8GB recommended)
- 2GB free disk space

## 🌐 Deployment Options

### Option 1: Local Deployment (Development/Testing)

#### 1. Clone the Repository
```bash
git clone https://github.com/Suyz-Dev/DropSafe-.git
cd DropSafe-
```

#### 2. Create Virtual Environment
```bash
python -m venv dropsafe_env
source dropsafe_env/bin/activate  # On Windows: dropsafe_env\Scripts\activate
```

#### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 4. Run the Application
```bash
# Start all services
./run.sh  # On Windows: run.bat

# Or start individual services:
streamlit run main_page.py --server.port=8499
streamlit run teacher_dashboard.py --server.port=8501
streamlit run enhanced_student_dashboard.py --server.port=8502
streamlit run counsellor_dashboard.py --server.port=8504
```

#### 5. Access the Application
- Main Page: http://localhost:8499
- Teacher Dashboard: http://localhost:8501
- Student Dashboard: http://localhost:8502
- Counsellor Dashboard: http://localhost:8504

### Option 2: Docker Deployment (Recommended for Production)

#### 1. Build Docker Image
```bash
docker build -t dropsafe .
```

#### 2. Run Docker Container
```bash
docker run -p 8499:8499 -p 8501:8501 -p 8502:8502 -p 8504:8504 dropsafe
```

### Option 3: Cloud Deployment (Streamlit Cloud/AWS/Heroku/Google Cloud)

#### Streamlit Cloud (Easiest Option)
1. Fork this repository to your GitHub account
2. Go to [Streamlit Community Cloud](https://streamlit.io/cloud)
3. Create a new app and connect it to your forked repository
4. Set the main file to `streamlit_main.py` (for simplified version) or `main_page.py` (for full version)
5. Use `requirements-streamlit.txt` as the requirements file
6. Deploy and share your app!

**Note**: The full version (`main_page.py`) includes redirects to localhost services that won't work on Streamlit Cloud. For a complete experience, use the simplified version (`streamlit_main.py`) or deploy locally.

#### Heroku Deployment
1. Install Heroku CLI
2. Login to Heroku:
   ```bash
   heroku login
   ```
3. Create a new Heroku app:
   ```bash
   heroku create your-dropsafe-app-name
   ```
4. Deploy:
   ```bash
   git push heroku main
   ```

#### AWS EC2 Deployment
1. Launch an EC2 instance (Ubuntu 20.04 LTS recommended)
2. SSH into the instance
3. Install dependencies:
   ```bash
   sudo apt update
   sudo apt install python3-pip python3-venv git -y
   ```
4. Clone repository and set up:
   ```bash
   git clone https://github.com/Suyz-Dev/DropSafe-.git
   cd DropSafe-
   python3 -m venv dropsafe_env
   source dropsafe_env/bin/activate
   pip install -r requirements.txt
   ```
5. Configure firewall to allow ports 8499, 8501, 8502, 8504
6. Run the application:
   ```bash
   nohup ./run.sh > dropsafe.log 2>&1 &
   ```

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the project root with:
```env
# Streamlit Configuration
STREAMLIT_SERVER_PORT=8499
STREAMLIT_SERVER_HEADLESS=true

# Data Directory
DATA_DIR=./data

# Logging
LOG_LEVEL=INFO
```

### Reverse Proxy (Nginx - Production)
For production deployment with HTTPS, configure Nginx:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8499;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /teacher/ {
        proxy_pass http://localhost:8501;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /student/ {
        proxy_pass http://localhost:8502;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /counsellor/ {
        proxy_pass http://localhost:8504;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 🔐 Security Considerations

1. **Authentication**: The application includes basic role-based authentication
2. **Data Protection**: Student data should be encrypted at rest
3. **Network Security**: Use HTTPS in production
4. **Access Control**: Restrict access to dashboards based on user roles
5. **Regular Updates**: Keep dependencies updated

## 📊 Monitoring and Maintenance

### Health Checks
- Check service status: `./system_status.py`
- Monitor logs in `shared_data/` directory
- Set up alerts for high-risk student identification

### Backup Strategy
1. Regular backups of:
   - Student data files
   - Chat history
   - Risk assessment models
2. Store backups in secure, encrypted storage

### Performance Optimization
- Use a production WSGI server for high-traffic deployments
- Implement caching for frequently accessed data
- Monitor memory usage and optimize data loading

## 🆘 Troubleshooting

### Common Issues

1. **Port Conflicts**:
   ```bash
   # Check which process is using a port
   lsof -i :8499
   # Kill the process
   kill -9 <PID>
   ```

2. **Missing Dependencies**:
   ```bash
   pip install -r requirements.txt --force-reinstall
   ```

3. **Permission Errors**:
   ```bash
   chmod +x *.sh
   chmod +x *.py
   ```

### Logs
Check logs in:
- Application logs: `dropsafe.log`
- Streamlit logs: Check terminal output
- Error logs: `shared_data/error.log` (if exists)

## 🔄 Updates and Maintenance

### Updating the Application
```bash
git pull origin main
pip install -r requirements.txt --upgrade
```

### Adding New Features
1. Create feature branch:
   ```bash
   git checkout -b feature/new-feature
   ```
2. Implement changes
3. Test thoroughly
4. Merge to main:
   ```bash
   git checkout main
   git merge feature/new-feature
   git push origin main
   ```

## 📞 Support
For issues or questions, contact:
- Repository Owner: Suyz-Dev
- Email: suyz.dev@gmail.com

## 📄 License
This project is licensed under the MIT License - see the LICENSE file for details.