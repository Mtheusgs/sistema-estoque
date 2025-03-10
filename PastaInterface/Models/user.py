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
    
    @staticmethod
    def mostrarUser(userNome): 
        """ Mostra um usuário específico """
        return User.query.filter_by(UserName=userNome).first()
    
    @staticmethod  
    def apagarUser(cargo,id):
        """ Apaga um usuário do banco de dados """ 
        if cargo == 'Gerente' or "Criador":
            user = User.query.filter_by(UserId=id).first()
            if user:
                db.session.delete(user)
                db.session.commit()
                return True 
            else:
                return False
        else:
            return False    

    





    






       




    

