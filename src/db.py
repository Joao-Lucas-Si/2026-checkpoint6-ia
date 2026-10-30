import json
import os
from typing import Literal, Self, TypedDict


class Mensagem(TypedDict):
   role: Literal["usuario", "chat"]
   conteudo: str
   arquivos: list[str]

class Database:
    caminho="data/db/db.json"
    def __init__(self) -> None:
        self.mensagens: list[Mensagem] = []
    
    @staticmethod
    def read():
        if os.path.exists(Database.caminho):
            singleton = Database.get_singleton()
            salvo = json.loads(open(Database.caminho, "r", encoding="utf-8").read())
            # print(salvo)
            singleton.mensagens = salvo["mensagens"]
            # print(singleton.mensagens)
        
    def write(self):
        if not os.path.exists("data/db"):
            os.mkdir("data/db")
        with open(Database.caminho, "w", encoding="utf-8") as file:
            file.write(f"""{{
                "mensagens": {json.dumps(self.mensagens)}
            }}""")
            
    def salvar_conversa(self, mensagem: Mensagem):
        self.mensagens.append(mensagem)
    
    singleton: "Database|None" = None
    @staticmethod
    def get_singleton():
        if not Database.singleton:
            Database.singleton = Database()
        return Database.singleton