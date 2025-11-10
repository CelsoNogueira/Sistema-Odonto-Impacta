from database.mongo_connection import get_db
from bson import ObjectId

db = get_db()
agendamento_collection = db["agendamentos"]

def cadastrar_agendamento(dados):
    agendamento_collection.insert_one(dados)

def listar_agendamentos():
    agendamentos = list(agendamento_collection.find())
    for a in agendamentos:
        a["_id"] = str(a["_id"])
    return agendamentos

def atualizar_agendamento(filtro, novos_dados):
    agendamento_collection.update_one(filtro, {"$set": novos_dados})

def excluir_agendamento(filtro):
    agendamento_collection.delete_one(filtro)
