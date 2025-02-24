from estoque import Estoque

class Relatorio:
    def __init__(self):
        """
        Inicializa a classe Relatorio.
        """
        pass

    def procurarProduto(self, id: int, estoque: Estoque):
        """
        Procura um produto no estoque pelo ID.

        Args:
            id (int): ID do produto a ser procurado.
            estoque (Estoque): Objeto da classe Estoque.

        Returns:
            Produto: O produto encontrado ou None se não existir.
        """
        for produto in estoque.listaDeProdutos:
            if id == produto.codigo:  
                return produto
        return None

    def consultarEstoquePorProduto(self, estoque: Estoque, id: int):
        """
        Consulta a quantidade em estoque de um produto específico.

        Args:
            estoque (Estoque): Objeto da classe Estoque.
            id (int): ID do produto.

        Returns:
            int: Quantidade do produto em estoque.
        """
        produto = self.procurarProduto(id, estoque)
        if produto:
            return produto.quantidade
        return 0

    def consultarEstoque(self, estoque: Estoque):
        """
        Exibe o estoque completo.
        """
        print("=== Estoque ===")
        for produto in estoque.listaDeProdutos:
            print(f"{produto.codigo} - {produto.nome} : {produto.quantidade} unidades")

    def consultarPedidos(self, estoque: Estoque):
        """
        Exibe todos os pedidos.
        """
        print("=== Pedidos ===")
        for pedido in estoque.listaDePedidos:
            print(f"#{pedido.id} - {pedido.descricao} ({pedido.status})")
            for produto, quantidade in pedido.itens.items():
                print(f"  {produto.codigo} - {produto.nome} : {quantidade} unidades")
            print(f"  Peso total: {pedido.pesoTotal()} kg")
            print(f"  Valor total: R$ {pedido.valorTotal():.2f}")
