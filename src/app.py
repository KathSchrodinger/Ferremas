import hashlib
from flask import Flask, jsonify, request
from flask_jwt_extended import jwt_required, create_access_token, JWTManager, get_jwt_identity
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = 'shikanokonokonokokoshitantan'
jwt = JWTManager(app)

# MongoDB
client = MongoClient("mongodb+srv://Kath:U6JyKLiHYMd4qMNc@cluster0.opmhnpl.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client['Cluster0']
user_collection = db["users"]

@app.route("/api/ferremas/createuser", methods=["POST"])
def create_user():
    new_user = request.get_json()
    new_user["password"] = hashlib.sha256(new_user["password"].encode("utf-8")).hexdigest()
    new_user["is_admin"] = False
    doc = user_collection.find_one({"username" : new_user["username"]})
    if not doc:
         user_collection.insert_one(new_user)
         return jsonify({"status" : "Usuario creado con exito"})
    else:
         return jsonify({"status" : "Usuario ya existe"})

@app.route("/api/ferremas/createadmin", methods=["POST"])
@jwt_required()
def create_admin():
    current_user = get_jwt_identity()
    user = user_collection.find_one({"username": current_user})
    if not user or not user.get("is_admin", False):
        return jsonify({"msg": "Acceso denegado. Solo los administradores pueden crear nuevos administradores."}), 403

    new_admin = request.get_json()
    new_admin["password"] = hashlib.sha256(new_admin["password"].encode("utf-8")).hexdigest()
    new_admin["is_admin"] = True
    doc = user_collection.find_one({"username": new_admin["username"]})
    if not doc:
        user_collection.insert_one(new_admin)
        return jsonify({"status": "Administrador creado con éxito"})
    else:
        return jsonify({"status": "Usuario ya existe"})

@app.route("/api/ferremas/viewuser", methods=["GET"])
@jwt_required()
def get_all_users():
    current_user = get_jwt_identity()
    user = user_collection.find_one({"username": current_user})

    if not user or not user.get("is_admin", False):
        return jsonify({"msg": "Acceso denegado. Solo los administradores pueden ver la lista de usuarios."}), 403

    users = user_collection.find()
    data=[]
    for user in users:
        user["_id"] = str(user["_id"])
        data.append(user) 
    return jsonify(data)

@app.route("/api/ferremas/login", methods=["POST"])
def login():
     login_details = request.get_json()
     user = user_collection.find_one({"username" : login_details["username"]})
     if user:
          enc_pass = hashlib.sha256(login_details['password'].encode("utf-8")).hexdigest()
          if enc_pass == user["password"]:
               access_token = create_access_token(identity = user["username"])
               return jsonify(access_token= access_token),200

     return jsonify({'msg':'Credenciales incorrectas'}),401

@app.route("/api/ferremas/deleteuser/<user_id>",methods=["DELETE"])
@jwt_required()
def delete(user_id):
    current_user = get_jwt_identity()
    user = user_collection.find_one({"username": current_user})

    if not user or not user.get("is_admin", False):
        return jsonify({"msg": "Acceso denegado. Solo los administradores pueden eliminar usuarios."}), 403
   
    delete_user = user_collection.delete_one({'_id':ObjectId(user_id)})
    if delete_user.deleted_count>0:
        return jsonify({"status" : "Usuario eliminado con exito"}),204
    else:
        return "",404

if __name__ == "__main__":
    app.run(debug=True)