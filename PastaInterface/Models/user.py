from flask_sqlalchemy import SQLAlchemy 
from Models import db


class User(db.Model):
    __tablename__ = 'users'

    UserId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    UserName = db.Column(db.String(80), nullable=False)
    Cargo = db.Column(db.String(80), nullable=False)
    Login = db.Column(db.String(80), unique=True, nullable=False)
    Senha = db.Column(db.String(120), nullable=False)

    def __init__(self, nome, cargo, login, senha):
        self.UserName = nome
        self.Cargo = cargo
        self.Login = login
        self.Senha = senha

    @staticmethod
    def login(login, senha):
        """ Realiza o login do usuário e retorna o usuário se autenticado """
        return User.query.filter_by(Login=login, Senha=senha).first()

    @staticmethod
    def listarUsers():
        """ Lista todos os usuários cadastrados """ 
        return User.query.all()
        

    



class Gerente(User):
    def __init__(self, UserId: str, UserName: str, Cargo: str, Senha: str, Login: str):
        super().__init__(UserId, UserName, Cargo, Senha, Login)
        self.cargo = "Gerente" 
    
    def removerUser(self):
        """ Remove um usuário da lista """
        user_id = input("Digite o ID do usuário que deseja remover: ")
        for user in User.user_list:
            if user.UserId == user_id:
                User.user_list.remove(user)
                print(f"Usuário {user.UserName} removido com sucesso!")
                return
        
        print("Usuário não encontrado!")

    






       




    

