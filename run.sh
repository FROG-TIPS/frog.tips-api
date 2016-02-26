export FLASK_CONFIG=config/testing.py
source .python/Scripts/activate
pip install -e .
python src/frog/__init__.py
