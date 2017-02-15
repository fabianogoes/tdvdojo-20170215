from json import JSONEncoder
from sqlalchemy import Column, Boolean, Integer, String
from sqlalchemy.ext.declarative import declarative_base

class Pessoa(object):

    def __init__(self, id, nome):
        self.id = id
        self.nome = nome

Base = declarative_base()

class PessoaDB(Base):
    """
    Pessoa database class
    """
    __tablename__ = "pessoa"
    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
 
    #----------------------------------------------------------------------
    def __init__(self, nome):
        """Constructor"""
        self.nome = nome
