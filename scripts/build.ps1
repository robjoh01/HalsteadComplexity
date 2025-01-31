# 1. Activate the virtual environment
& .\.venv\Scripts\Activate.ps1

# 2. Run PyInstaller to create the .exe file with the required dependencies
pyinstaller --onefile --clean --name HalsteadComplexity --icon=img\icon.ico --add-data "requirements.txt;." --copy-metadata readchar src\main.py

# 3. Deactivate the virtual environment
deactivate