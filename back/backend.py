import json
import jsonpickle
from pessoa import Pessoa

from bottle import request, response
from bottle import route, post, get, put, delete, hook
from bottle import hook, run

pessoas = [Pessoa('Fabiano'), Pessoa('Diego'), Pessoa('Felipinho'), Pessoa('Fenomeno'), Pessoa('teste')]    

_allow_origin = '*'
_allow_methods = 'PUT, GET, POST, DELETE, OPTIONS'
_allow_headers = 'Authorization, Origin, Accept, Content-Type, X-Requested-With'

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
	nome = request.forms.get('nome')
	pessoas.append(Pessoa(nome))
	return read()
    

@get("/read")
def read():
    response.content_type = 'application/json'
    # json_string = json.dumps(pessoas, default=obj_dict)
    json_string = JsonTransformer().transform(pessoas)
    return json_string


@put("/update")
def update():
    id = request.forms.get('id')
    nome = request.forms.get('nome')
    for pessoa in pessoas:
        if pessoa.id == int(id):
            index = pessoas.index(pessoa)
            pessoa.nome = nome
            pessoas[index] = pessoa

    return read()

@delete("/delete/<id>")
def delete(id):
    # id = request.forms.get('id')
    for pessoa in pessoas:
        if pessoa.id == int(id):
            index = pessoas.index(pessoa)
            del pessoas[index]

    return read()

run(host='localhost', port=8080, debug=True)
