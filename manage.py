import os
import logging
from flask_migrate import Migrate

from app import create_app, db
from app.models import Example

logger = logging.getLogger(__name__)

dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(dotenv_path):
    try:
        from dotenv import load_dotenv
        load_dotenv(dotenv_path)
        logger.info("Loaded environment file: {dotenv_path}")
    except Exception as e:
        logger.warn(f"{e}\nUnable to load environment file: {dotenv_path}")


app = create_app()

# Fix SQLite, `flask db migrate` fails with a DROP column unless `render_batch=True`
with app.app_context():
    if db.engine.url.drivername == "sqlite":
        migrate = Migrate(app, db, render_as_batch=True)
    else:
        migrate = Migrate(app, db)

@app.shell_context_processor
def make_shell_context():
    return dict(
        db=db,
        Example=Example
    )
