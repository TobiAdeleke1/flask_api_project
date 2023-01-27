from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, MetaData
import os


FILE_DIR =  os.path.dirname(__file__)
os.chdir(FILE_DIR)

#connect to existing db
engine = create_engine("sqlite:///db.sqlite3", connect_args={"check_same_thread": False})

# reflect the tables
metadata = MetaData()
metadata.reflect(engine)

LocalSession = sessionmaker(engine)

Base = automap_base(metadata=metadata)
Base.prepare()

# Get models from db
Orders = Base.classes.orders
Products = Base.classes.products