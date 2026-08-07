from dotenv import load_dotenv
load_dotenv()  # reads .env and loads values into os.environ before anything else runs

from flask import Flask
from flask_cors import CORS
from routes.auth import auth_bp
from routes.tasks import tasks_bp
from routes.categories import categories_bp

app = Flask(__name__)

# Allow the HTML/CSS frontend (served from a different origin/port) to call this API
CORS(app)

# Register each set of routes
app.register_blueprint(auth_bp)
app.register_blueprint(tasks_bp)
app.register_blueprint(categories_bp)


@app.route("/health", methods=["GET"])
def health_check():
    # Simple endpoint to confirm the service is up — useful for Docker/K8s health checks later
    return {"status": "ok"}, 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)