from produto import Produto
from estoque import Estoque

class Pedidos:
    """
    Classe que representa um pedido, contendo produtos e suas respectivas quantidades.

    Atributos:
        id (int): Identificação única do pedido.
        status (str): Estado atual do pedido (ex: "Em andamento", "Concluído").
        descricao (str): Descrição detalhada do pedido.
        itens (dict): Dicionário contendo os produtos e suas respectivas quantidades.

    Métodos:
        adicionarProdutos(produto, quantidade):
            Adiciona um produto ao pedido ou atualiza a quantidade de um já existente.
        
        removerProduto(produto):
            Remove um produto do pedido, se ele estiver presente.

        valorTotal():
            Calcula e retorna o valor total do pedido, considerando os preços dos produtos e suas quantidades.
    """

    def __init__(self, IdPedido: int, descricao: str, status: str):
        """
        Inicializa um pedido com ID, descrição e status.

        Args:
            IDpedido (int): Número identificador do pedido.
            descricao (str): Descrição do pedido.
            status (str): Status atual do pedido.
        """
        self.status = status
        self.id = IdPedido
        self.descricao = descricao
        self.itens = {}  

    def adicionarProdutos(self, produto: Produto, quantidade):
        """
        Adiciona um produto ao pedido ou atualiza a quantidade de um produto existente.

        Args:
            produto (Produto): Objeto da classe Produto.
            quantidade (int): Quantidade do produto a ser adicionada.
        """
        self.itens[produto] = quantidade
    
    def removerProduto(self, produto: Produto):
        """
        Remove um produto do pedido.

        Args:
            produto (Produto): Objeto da classe Produto a ser removido.

        Raises:
            KeyError: Se o produto não estiver no pedido.
        """
        if produto in self.itens:
            del self.itens[produto]

    def valorTotal(self):
        """
        Calcula e retorna o valor total do pedido.

        Returns:
            float: Valor total do pedido, considerando o preço dos produtos e suas quantidades.
        """
        valorDoPedido = 0
        for produto in self.itens:
            valorDoPedido += produto.preco * self.itens[produto]  
        return valorDoPedido
    
    def pesoTotal(self):
        pesoDoPedido = 0
        for produto in self.itens: 
            pesoDoPedido += produto.peso * self.itens[produto]
        return pesoDoPedido
    
    def to_string(self):
        """
        Converte o pedido em uma string formatada para salvar no arquivo.
        """
        itens_str = ",".join([f"{produto.codigo}:{quantidade}" for produto, quantidade in self.itens.items()])
        return f"{self.id}|{self.descricao}|{self.status}|{itens_str}"

    @staticmethod
    def from_string(linha, estoque: Estoque):
        """
        Cria um Pedido a partir de uma string formatada.
        """
        dados = linha.strip().split("|")
        pedido = Pedidos(int(dados[0]), dados[1], dados[2])
        itens = dados[3].split(",")
        for item in itens:
            codigo, quantidade = item.split(":")
            produto = next((p for p in estoque.listaDeProdutos if p.codigo == int(codigo)), None)
            if produto:
                pedido.adicionarProdutos(produto, int(quantidade))
        return pedido