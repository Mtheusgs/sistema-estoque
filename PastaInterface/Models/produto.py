from flask_sqlalchemy import SQLAlchemy 
from Models import db


class Produto(db.Model):
    __tablename__ = 'produtos'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    codigo = db.Column(db.String(80), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    peso = db.Column(db.Float, nullable=False)
    categoria = db.Column(db.String(100), nullable=False)  # Alterado para String
    preco = db.Column(db.Float, nullable=False)
    fornecedor = db.Column(db.String(100), nullable=False)  # Alterado para String
    
    def __init__(self, nome, codigo, quantidade, peso, categoria, preco, fornecedor):
        self.nome = nome
        self.codigo = codigo
        self.quantidade = quantidade
        self.peso = peso
        self.categoria = categoria
        self.preco = preco
        self.fornecedor = fornecedor
    
    @staticmethod 
    def buscarProduto(criterio, valor_busca):
        """ Busca um produto no banco de dados """
        if criterio == 'codigo':
            return Produto.query.filter(Produto.codigo == valor_busca).all()
        elif criterio == 'nome':
            return Produto.query.filter(Produto.nome.ilike(f'%{valor_busca}%')).all()
        elif criterio == 'categoria':
            return Produto.query.filter_by(categoria=valor_busca).all()
        elif criterio == 'fornecedor':
            return Produto.query.filter_by(fornecedor=valor_busca).all()
        else:
            return [] 
        
    @staticmethod
    def apagarProduto(codigo, quantidade):
        """ Apaga um produto do banco de dados baseado no código """
        print(f"Código buscado: {codigo}")
        produto = Produto.query.filter(Produto.codigo == codigo).first()
        print(f"Produto encontrado: {produto}")
        
        if produto: 
            produto.quantidade -= int(quantidade)
            if produto.quantidade <= 0:
                db.session.delete(produto) 
            db.session.commit()
            return True
        else:
            return False
        
    

        

        
