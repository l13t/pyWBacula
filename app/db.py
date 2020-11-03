from sqlalchemy import create_engine
import config

db = create_engine(config.DB_URI, echo=True)
