from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('postgresql://postgres:postgres@127.0.0.1:5430/flask')
Session = sessionmaker(bind=engine)
