export FLASK_CONFIG=$(pwd)/config/testing.py
export FLASK_MASTER_AUTH_PHRASE=CROAKING
export FLASK_DEBUG_SSL_CERT=$(pwd)/config/debug_ssl.crt
export FLASK_DEBUG_SSL_KEY=$(pwd)/config/debug_ssl.key

source .python/Scripts/activate
pip install -e .

echo "Authorization header phrase is: '$FLASK_MASTER_AUTH_PHRASE'"

python src/frog/__init__.py
