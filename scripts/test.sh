#!/bin/bash

# 1. Activate virtual environment
source .venv/bin/activate

# 2. Install the dependencies from requirements.txt
pip install -r .\requirements\test.txt

# 3. Run the unit tests with coverage
coverage run -m pytest

# 4. Generate the coverage report
coverage report

# 5. Lint the code
pylint .\src

# 6. Deactivate virtual environment
deactivate