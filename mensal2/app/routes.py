from flask import json, request, jsonify
import flask
from bson import json_util
from app import app
from app import db
from bson.objectid import ObjectId

@app.route('/')
@app.route('/index')
def index():
	return flask.jsonify(json.loads(json_util.dumps(db.notafiscal.find({}).sort("_id", 1))))

@app.route("/create")
def create():
	return flask.render_template('create.html')

@app.route('/createAction', methods=['POST'])
def createAction():
	json_data = request.form.to_dict()
	if json_data is not None:
		if db.notafiscal.insert_one(json_data).inserted_id is not None:
			return jsonify(mensagem='Inserido')
		else:
			return jsonify(mensagem='Não inserido')
	else:
		return jsonify(mensagem='Nada a inserir')

@app.route("/update/<string:comprador>")
def update(comprador):
	notafiscal = db.notafiscal.find_one({"comprador": comprador})
	if notafiscal is not None:
		return flask.render_template('update.html', notafiscal=notafiscal)
	else:
		return jsonify(mensagem='Comprador não existe')

@app.route('/updateAction', methods=['POST'])
def updateAction():
	json_data = request.form.to_dict()
	if json_data is not None:
		if db.notafiscal.update_one({'_id': ObjectId(json_data["_id"])}, {"$set": {'numero': json_data["numero"], 'comprador': json_data["comprador"],'cnpj': json_data["cnpj"],'endereco': json_data["endereco"],'telefone': json_data["telefone"],'data': json_data["data"],'valor': json_data["valor"],'itens': json_data["itens"]}}).modified_count > 0:
			return jsonify(mensagem='Alterado')
		else:
			return jsonify(mensagem='Não alterado')
	else:
		return jsonify(mensagem='Nada a alterar')

@app.route("/delete/<string:comprador>")
def delete(comprador):
    result = db.notafiscal.delete_one({"comprador": comprador})
    if(result.deleted_count > 0):
        return jsonify(mensagem='Removido')
    else:
        return jsonify(mensagem='Não removido')
