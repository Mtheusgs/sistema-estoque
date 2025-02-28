from flask_sqlalchemy import SQLAlchemy 
from Models import db


class Produto(db.Model):
    __tablename__ = 'produtos'
    
    id = db.Column(db.Integer, primary_key=True)  # Chave primária
    nome = db.Column(db.String(100), nullable=False)
    codigo = db.Column(db.String(80), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    peso = db.Column(db.Float, nullable=False)
    categoria = db.Column(db.Integer, nullable=False)
    preco = db.Column(db.Float, nullable=False)
    fornecedor = db.Column(db.Integer, nullable=False)
    
    def __init__(self, nome, codigo, quantidade, peso, categoria, preco, fornecedor):
        self.nome = nome
        self.codigo = codigo
        self.quantidade = quantidade
        self.peso = peso
        self.categoria = categoria
        self.preco = preco
        self.fornecedor = fornecedor