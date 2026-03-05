from flask import Flask, send_from_directory
from config import Config
from extensions import db, cache, celery, jwt, mail
from flask_cors import CORS
from flask_migrate import Migrate
from routes.auth_routes import auth_bp
from routes.admin_routes import admin_bp
from routes.student_routes import student_bp
from routes.company_routes import company_bp
from routes.drive_routes import drive_bp
from models import User, Company, PlacementDrive, Application
import os

migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app)

    db.init_app(app)
    cache.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    init_celery(app)
    mail.init_app(app)

    import tasks

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(admin_bp, url_prefix="/api/admin")
    app.register_blueprint(student_bp, url_prefix="/api/student")
    app.register_blueprint(company_bp, url_prefix="/api/company")
    app.register_blueprint(drive_bp, url_prefix="/api/drive")

    # ── Serve uploaded resumes ──
    @app.route("/uploads/resumes/<filename>")
    def serve_resume(filename):
        upload_folder = os.path.join(app.root_path, "uploads", "resumes")
        return send_from_directory(upload_folder, filename)

    with app.app_context():
        db.create_all()
        create_admin_user()

    return app


def init_celery(app):
    celery.conf.update(
        broker_url=app.config["CELERY_BROKER_URL"],
        result_backend=app.config["CELERY_RESULT_BACKEND"],
        timezone="Asia/Kolkata",
        enable_utc=True
    )

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask


def create_admin_user():
    admin = User.query.filter_by(role="admin").first()
    if not admin:
        admin = User(
            name="Placement Admin",
            email="admin@placement.com",
            role="admin",
            is_active=True
        )
        admin.set_password("admin123")
        db.session.add(admin)
        db.session.commit()
        print("Admin user created successfully!")


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)