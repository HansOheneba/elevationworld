from flask import Flask
from routes import main_routes
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Set secret key from .env
app.secret_key = os.getenv("SECRET_KEY", "fallback-secret-key")

# Register routes
app.register_blueprint(main_routes)

if __name__ == "__main__":
    app.run(debug=True, port=5001)
