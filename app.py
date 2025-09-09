from flask import Flask, session, request
from datetime import datetime
from config import Config
from models import db
from routes.auth import auth_bp
from routes.main import main_bp
from routes.admin import admin_bp
from routes.dept import dept_bp
from routes.staff import staff_bp
from routes.task_setup import task_bp
from routes.project import project_bp

app = Flask(__name__)
app.config.from_object(Config)

# Init DB
db.init_app(app)
with app.app_context():
    # db.drop_all()
    db.create_all()

# Register Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(main_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(dept_bp)
app.register_blueprint(staff_bp, url_prefix="/staff")
app.register_blueprint(task_bp, url_prefix="/task")
app.register_blueprint(project_bp, url_prefix="/project")

@app.context_processor
def inject_user_info():
    return dict(
        email=session.get('email'),
        role=session.get('role'),
        user_ip=request.headers.get('X-Forwarded-For', request.remote_addr),
        current_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    )

if __name__ == "__main__":
    app.run(debug=True)
