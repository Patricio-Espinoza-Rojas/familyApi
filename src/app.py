"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure


app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def handle_hello():

    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()


    return jsonify(members), 200

@app.route('/member/<int:member_id>', methods=['GET','DELETE'])
def get_delete_user_id(member_id):
    if request.method == 'GET':
        members = jackson_family.get_all_members()
        for member in members:
            if member_id == member['id']:
                return jsonify(member), 200

        return jsonify({"msg" : "Usuario no encontrado"}),404

    if request.method ==  'DELETE':
        members = jackson_family.get_all_members()
        for member in members:
            if member_id == member['id']:
                members.pop(members.index(member))
                return jsonify({"done" : True}),200

        return jsonify({"msg" : "Usuario no encontrado"}),404

@app.route('/member', methods=['POST'])
def post_user():
    new_member = {
        "first_name" : '',
        "last_name": "Jackson",
        "age": '',
        "lucky_numbers": [],
        "id": ''
    }

    if(request.json.get('first_name')): new_member["first_name"] = request.json.get("first_name")
    else: return jsonify({"msg" : "Nombre es requerido"}),400

    if(request.json.get("last_name")): return jsonify({"msg" : "Apellido no es requerido"}),400

    if(request.json.get("age")): new_member["age"] = request.json.get("age")
    else: return jsonify({"msg" : "Edad es requerida"}),400

    if(request.json.get("lucky_numbers")): new_member["lucky_numbers"] = request.json.get("lucky_numbers")
    else: return jsonify({"msg" : "Lucky Numbers requerido!"}),400

    if(request.json.get('id')): new_member["id"] = request.json.get("id")
    else: new_member["id"] = jackson_family._generateId()

    jackson_family.add_member(new_member)
    
    return jsonify({"msg" : "success"}),200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
