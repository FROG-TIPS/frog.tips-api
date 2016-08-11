export FLASK_CONFIG=$(pwd)/src/frog/config/test.py
export FLASK_MASTER_AUTH_PHRASE=CROAKING

source .python/Scripts/activate
pip install -e .
pip install waitress

echo "Authorization header phrase is: '$FLASK_MASTER_AUTH_PHRASE'"

waitress-serve --port=5000 frog:app
