python -m pip install --upgrade pip
pip install -r test_requirements.txt
pip install -r requirements.txt

python -m mypy --ignore-missing-imports hun_date_parser

python -m flake8 --max-line-length=120 --per-file-ignores='patterns.py:E501' hun_date_parser

pytest --cov hun_date_parser