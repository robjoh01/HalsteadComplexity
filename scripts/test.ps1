# 1. Activate the virtual environment
.\.venv\Scripts\Activate

# 2. Install the dependencies from requirements.txt
pip install -r .\requirements\test.txt

# 3. Run the unit tests with coverage
coverage run -m pytest

# 4. Generate the coverage report
coverage report

# 5. Lint the code
pylint .\src

# 6. Deactivate the virtual environment
deactivate