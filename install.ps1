# 1. Create virtual environment with Python
python -m venv venv

# 2. Activate virtual environment
.\venv\Scripts\Activate.ps1 &

# 3. Install dependencies
pip install -r requirements.txt

# 4. Build executable
pyinstaller 

# 5. Deactivate virtual environment
deactivate