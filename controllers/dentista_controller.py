from database.mongo_connection import get_db
from bson import ObjectId

db = get_db()
dentista_collection = db["dentistas"]

def cadastrar_dentista(dados):
    return dentista_collection.insert_one(dados)

def listar_dentistas():
    return list(dentista_collection.find())

def atualizar_dentista(id_dentista, novos_dados):
    return dentista_collection.update_one(
        {"_id": ObjectId(id_dentista)},
        {"$set": novos_dados}
    )

def excluir_dentista(id_dentista):
    return dentista_collection.delete_one({"_id": ObjectId(id_dentista)})
