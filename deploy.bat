@echo off
echo 🚀 Resume Scanner Deployment Script
echo ==================================

REM Check if git is initialized
if not exist ".git" (
    echo 📁 Initializing git repository...
    git init
    git add .
    git commit -m "Initial commit"
    echo ✅ Git repository initialized
) else (
    echo 📁 Git repository already exists
)

echo.
echo 🎯 Choose deployment option:
echo 1) Render (Recommended - Free)
echo 2) Railway (Alternative - Free)
echo 3) Heroku (Classic)
echo 4) Docker (Local)
echo 5) Docker Compose (Local)
echo 6) Show all options
echo.

set /p choice="Enter your choice (1-6): "

if "%choice%"=="1" goto render
if "%choice%"=="2" goto railway
if "%choice%"=="3" goto heroku
if "%choice%"=="4" goto docker
if "%choice%"=="5" goto docker_compose
if "%choice%"=="6" goto all_options
goto invalid

:render
echo 🎯 Deploying to Render...
echo 📝 Steps:
echo 1. Go to https://render.com
echo 2. Sign up with GitHub
echo 3. Click "New +" → "Web Service"
echo 4. Connect your GitHub repository
echo 5. Configure:
echo    - Name: resume-scanner
echo    - Environment: Python
echo    - Build Command: pip install -r requirements.txt ^&^& python -m spacy download en_core_web_sm
echo    - Start Command: gunicorn app:app
echo 6. Click "Create Web Service"
echo.
echo 🌐 Your app will be live at: https://resume-scanner.onrender.com
goto end

:railway
echo 🎯 Deploying to Railway...
echo 📝 Steps:
echo 1. Go to https://railway.app
echo 2. Sign up with GitHub
echo 3. Click "New Project" → "Deploy from GitHub repo"
echo 4. Select your repository
echo 5. Railway will auto-detect Python and deploy
echo.
echo 🌐 Your app will be live at: https://your-app-name.railway.app
goto end

:heroku
echo 🎯 Deploying to Heroku...
echo 📝 Steps:
echo 1. Install Heroku CLI: winget install --id=Heroku.HerokuCLI
echo 2. Open command prompt and run:
echo    heroku login
echo    heroku create resume-scanner-app
echo    git push heroku main
echo    heroku open
echo.
echo 🌐 Your app will be live at: https://resume-scanner-app.herokuapp.com
goto end

:docker
echo 🐳 Building Docker image...
docker build -t resume-scanner .
echo 🚀 Running Docker container...
docker run -d -p 5000:5000 --name resume-scanner-app resume-scanner
echo 🌐 Your app is running at: http://localhost:5000
echo 📋 To stop: docker stop resume-scanner-app
echo 📋 To remove: docker rm resume-scanner-app
goto end

:docker_compose
echo 🐳 Deploying with Docker Compose...
docker-compose up -d
echo 🌐 Your app is running at: http://localhost:5000
echo 📋 To stop: docker-compose down
echo 📋 To view logs: docker-compose logs -f
goto end

:all_options
echo 📋 All deployment options:
echo.
call :render
echo.
call :railway
echo.
call :heroku
echo.
call :docker
echo.
call :docker_compose
goto end

:invalid
echo ❌ Invalid choice. Please run the script again.
goto end

:end
echo.
echo 🎉 Deployment script completed!
echo 📖 For detailed instructions, see DEPLOYMENT.md
pause
