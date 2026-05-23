from flask import Flask, jsonify
from sqlalchemy.exc import IntegrityError

from app.config import Config
from app.extensions import db, jwt


def create_app(config_object=Config):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_object)

    db.init_app(app)
    jwt.init_app(app)

    from app.auth.routes import auth_bp
    from app.tasks.routes import tasks_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(tasks_bp, url_prefix="/api/tasks")
    register_cli(app)
    register_error_handlers(app)

    @app.get("/health")
    def health_check():
        return {"status": "ok"}


    @app.get("/test")
    def hello_world():
        return {"message": "Hello, World!"}

    return app


def register_cli(app):
    @app.cli.command("init-db")
    def init_db():
        """Create database tables."""
        db.create_all()
        print("Database tables created.")

    @app.cli.command("create-admin")
    def create_admin():
        """Create an admin user from ADMIN_* environment variables."""
        import os

        from app.models import User

        username = os.getenv("ADMIN_USERNAME", "admin")
        email = os.getenv("ADMIN_EMAIL", "admin@example.com")
        password = os.getenv("ADMIN_PASSWORD")

        if not password:
            raise RuntimeError("Set ADMIN_PASSWORD before running create-admin.")

        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            print("Admin user already exists.")
            return

        admin = User(username=username, email=email.lower(), role="admin")
        admin.set_password(password)
        db.session.add(admin)
        db.session.commit()
        print(f"Admin user created: {email}")


def register_error_handlers(app):
    @app.errorhandler(IntegrityError)
    def handle_integrity_error(error):
        db.session.rollback()
        return jsonify({"error": "A record with that value already exists."}), 409

    @app.errorhandler(404)
    def handle_not_found(error):
        return jsonify({"error": "Resource not found."}), 404
