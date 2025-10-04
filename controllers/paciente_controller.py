from database.mongo_connection import get_db
from bson import ObjectId

db = get_db()
paciente_collection = db["pacientes"]

def cadastrar_paciente(dados):
    paciente_collection.insert_one(dados)

def listar_pacientes():
    pacientes = list(paciente_collection.find())
    for p in pacientes:
        p["_id"] = str(p["_id"])
    return pacientes

def atualizar_paciente(filtro, novos_dados):
    paciente_collection.update_one(filtro, {"$set": novos_dados})

def excluir_paciente(filtro):
    paciente_collection.delete_one(filtro)
