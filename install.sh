#!/bin/bash

# 1. Create virtual environment with Python
python3 -m venv venv

# 2. Activate virtual environment
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Deactivate virtual environment
deactivate