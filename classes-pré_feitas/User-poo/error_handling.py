class EstoqueError(Exception):
    """
    Classe base para excecoes relacionadas ao estoque.
    """
    pass

class ProdutoNaoEncontradoError(EstoqueError):
    """
    Excecao levantada quando um produto nao e encontrado no estoque.
    """
    def __init__(self, codigo):
        super().__init__(f"Produto com código {codigo} nao encontrado no estoque.")

class EstoqueInsuficienteError(EstoqueError):
    """
    Excecao levantada quando nao ha estoque suficiente para retirada
    """
    def __init__(self, quantidade_disponivel, quantidade_solicitada):
        super().__init__(f"Estoque insuficiente!! Disponivel: {quantidade_disponivel}, solicitado: {quantidade_solicitada}.")


