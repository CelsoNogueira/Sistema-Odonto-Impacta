from database.mongo_connection import get_db
from bson import ObjectId

db = get_db()
fatura_collection = db["faturas"]
agendamento_collection = db["agendamentos"]

def cadastrar_fatura(dados):
    return fatura_collection.insert_one(dados)

def listar_faturas():
    return list(fatura_collection.find())

def atualizar_fatura(fatura_id, novos_dados):
    return fatura_collection.update_one({"_id": ObjectId(fatura_id)}, {"$set": novos_dados})

def excluir_fatura(fatura_id):
    return fatura_collection.delete_one({"_id": ObjectId(fatura_id)})

def buscar_fatura(fatura_id):
    return fatura_collection.find_one({"_id": ObjectId(fatura_id)})

def listar_pacientes():
    pacientes = agendamento_collection.distinct("paciente")
    return pacientes

def buscar_ultimo_agendamento(nome_paciente):
    ags = list(agendamento_collection.find({"paciente": nome_paciente}).sort("_id", -1))
    if ags:
        return ags[0]
    return None
