import json
import jsonpickle
from pessoa import Pessoa, PessoaDB, Base

from bottle import Bottle, request, response
from bottle import route, post, get, put, delete, hook
from bottle import hook, run, redirect

from sqlalchemy import create_engine, Column, Boolean, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
 
# --------------------------------
# Add SQLAlchemy app
# --------------------------------
app = Bottle()
 
#Base = declarative_base()
engine = create_engine("sqlite:///dojo.db", echo=True)
create_session = sessionmaker(bind=engine)

pessoas = [] #[Pessoa('Fabiano'), Pessoa('Diego'), Pessoa('Felipinho'), Pessoa('Fenomeno'), Pessoa('teste')]    

_allow_origin = '*'
_allow_methods = 'PUT, GET, POST, DELETE, OPTIONS'
_allow_headers = 'Authorization, Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token, Access-Control-Allow-Headers:Accept, Access-Control-Allow-Headers: X-Requested-With, Range, If-Range, X-Brad-Test, Access-Control-Allow-Origin: *'


class JsonTransformer(object):
    def transform(self, myObject):
        return jsonpickle.encode(myObject, unpicklable=False)
    
    def untransform(self, myObject):
        return jsonpickle.decode(myObject, unpicklable=False)

@hook('after_request')
def enable_cors():
    response.headers['Access-Control-Allow-Origin'] = _allow_origin
    response.headers['Access-Control-Allow-Methods'] = _allow_methods
    response.headers['Access-Control-Allow-Headers'] = _allow_headers


@route('/', method = 'OPTIONS')
@route('/<path:path>', method = 'OPTIONS')
def options_handler(path = None):
    return



@get("/")
def home():
    return read()

@post("/create")
def create():
    print("create()...")
    nome = request.forms.get('nome')
    
    session = create_session()
    pessoa = PessoaDB(nome)
    session.add(pessoa)
    session.commit()

    return read()
    

@get("/read")
def read():
    response.content_type = 'application/json'
    
    session = create_session()
    result = session.query(PessoaDB).all()

    pessoas = []
    for item in result:
        pessoas.append(Pessoa(item.id, item.nome))

    json_string = JsonTransformer().transform(pessoas) 
    print(json_string)

    return json_string

@get("/find/<id>")
def update(id):
    session = create_session()
    pessoa = session.query(PessoaDB).filter_by(id=id).one()
    pessoas = [Pessoa(pessoa.id, pessoa.nome)]

    json_string = JsonTransformer().transform(pessoas) 

    return json_string

@put("/update")
def update():
    print("update()...")
    nome = request.forms.get('nome')
    print('nome = '+nome)

    id = request.forms.get('id')
    print('id = '+id)

    session = create_session()
    pessoa = session.query(PessoaDB).filter_by(id=id).one()
    pessoa.nome = nome
    session.commit() 

    response.content_type = 'application/json'
    session = create_session()
    result = session.query(PessoaDB).all()
    pessoas = []
    for item in result:
        pessoas.append(Pessoa(item.id, item.nome))

    json_string = JsonTransformer().transform(pessoas) 
    return json_string

@delete("/delete/<id>")
def delete(id):
    
    session = create_session()
    pessoa = session.query(PessoaDB).filter_by(id=id).one()
    session.delete(pessoa)
    session.commit()

    return read()

def main():
    """
    Create the database and add data to it
    """
    Base.metadata.create_all(engine)
 
if __name__ == "__main__":
    main()

run(host='localhost', port=8080, debug=True)


