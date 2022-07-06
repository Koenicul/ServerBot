from sqlalchemy import Column, Float, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import create_engine

Base = declarative_base()

engine = create_engine('sqlite:///data.sqlite', echo=False)

class Server(Base):
    __tablename__ = "server"

    id = Column(Integer, primary_key=True)
    server_name = Column(String)
    server_id = Column(String)
    welcome_message_bool = Column(Boolean)
    welcome_message = Column(String)
    welcome_message_channel = Column(Integer)

    def __init__(self, server_name, server_id):
        self.server_name = server_name
        self.server_id = server_id
        self.welcome_message_bool = False
        self.welcome_message = "Welcome to {}!".format(server_name)
        self.welcome_message_channel = None

Base.metadata.create_all(engine)