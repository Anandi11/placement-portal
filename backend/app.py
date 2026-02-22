from flask import Flask
from config import Config
from extensions import db, cache, celery
from flask_cors import CORS
from routes.auth_routes import auth_bp
from routes.admin_routes import admin_bp
from routes.student_routes import student_bp
from routes.company_routes import company_bp
from routes.drive_routes import drive_bp

from models import User, Company, PlacementDrive, Application


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app)
    db.init_app(app)
    cache.init_app(app)

    init_celery(app)

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(admin_bp, url_prefix="/api/admin")
    app.register_blueprint(student_bp, url_prefix="/api/student")
    app.register_blueprint(company_bp, url_prefix="/api/company")
    app.register_blueprint(drive_bp, url_prefix="/api/drive")

    with app.app_context():
        db.create_all()
        create_admin_user()

    return app


def init_celery(app):
    celery.conf.update(
        broker_url=app.config["CELERY_BROKER_URL"],
        result_backend=app.config["CELERY_RESULT_BACKEND"]
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


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
