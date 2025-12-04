from app.core.app_factory import create_app

# Gunicorn will look for `app` here
app = create_app()
