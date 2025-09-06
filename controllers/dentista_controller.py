from database.mongo_connection import get_db

db = get_db()
dentista_collection = db["dentistas"]

def cadastrar_dentista(dados):
    dentista_collection.insert_one(dados)

def listar_dentistas():
    return list(dentista_collection.find({}, {"_id": 0}))

def atualizar_dentista(filtro, novos_dados):
    dentista_collection.update_one(filtro, {"$set": novos_dados})

def excluir_dentista(filtro):
    dentista_collection.delete_one(filtro)
