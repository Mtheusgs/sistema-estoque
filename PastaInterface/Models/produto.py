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
        """ Busca um produto no banco de dados sem diferenciar maiúsculas e minúsculas """
        if criterio == 'codigo':
            return Produto.query.filter(Produto.codigo.ilike(valor_busca)).all()
        elif criterio == 'nome':
            return Produto.query.filter(Produto.nome.ilike(valor_busca)).all()
        elif criterio == 'categoria':
            return Produto.query.filter(Produto.categoria.ilike(valor_busca)).all()
        elif criterio == 'fornecedor':
            return Produto.query.filter(Produto.fornecedor.ilike(valor_busca)).all()
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


    @staticmethod
    def addProduCarrinho(codigo,quantidade):
        """ Adiciona um produto ao carrinho """
        produtoCarrinho = Produto.query.filter(Produto.codigo == codigo).first()  
        if int(quantidade) <= 0 or int(quantidade)>produtoCarrinho.quantidade:
            return False 
        else:
            return produtoCarrinho
        
        


class ProdutoError(Exception):
    """Classe base para exceções relacionadas a produtos."""
    pass

class QuantidadeInvalidaError(ProdutoError):
    """Exceção para quando a quantidade for negativa."""
    def __init__(self, quantidade):
        super().__init__(f"A quantidade ({quantidade}) não pode ser negativa.")

class PesoInvalidoError(ProdutoError):
    """Exceção para quando o peso for negativo ou zero."""
    def __init__(self, peso):
        super().__init__(f"O peso ({peso}) deve ser maior que zero.")

class PrecoInvalidoError(ProdutoError):
    """Exceção para quando o preço for negativo ou zero."""
    def __init__(self, preco):
        super().__init__(f"O preço ({preco}) deve ser maior que zero.")

def validar_produto(quantidade, peso, preco):
    """Valida os valores do produto e levanta exceções se necessário."""
    if int(quantidade) < 0:
        raise QuantidadeInvalidaError(quantidade)
    if float(peso) <= 0:
        raise PesoInvalidoError(peso)
    if float(preco) <= 0:
        raise PrecoInvalidoError(preco)
        
        


        
