from pymongo import MongoClient

class UsuarioController:
    def __init__(self):
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client["clinica"]
        self.collection = self.db["usuarios"]

    def cadastrar_usuario(self, nome, email, senha):
        if self.collection.find_one({"email": email}):
            return False, "Usuário já existe."
        self.collection.insert_one({"nome": nome, "email": email, "senha": senha})
        return True, "Usuário cadastrado com sucesso!"

    def autenticar_usuario(self, email, senha):
        user = self.collection.find_one({"email": email, "senha": senha})
        if user:
            return True, user
        return False, "Usuário ou senha inválidos."

    def redefinir_senha(self, email, nova_senha):
        user = self.collection.find_one({"email": email})
        if not user:
            return False, "Usuário não encontrado."
        self.collection.update_one({"email": email}, {"$set": {"senha": nova_senha}})
        return True, "Senha atualizada com sucesso!"

    def listar_usuarios(self):
        return list(self.collection.find({}, {"_id": 0}))
