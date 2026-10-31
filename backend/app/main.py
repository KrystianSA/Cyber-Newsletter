from app.database import DatabaseConnector
from app.factory import create_app

app = create_app(DatabaseConnector("DATABASE_URL"))
