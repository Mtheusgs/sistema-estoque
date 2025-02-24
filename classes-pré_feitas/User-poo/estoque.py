from produto import Produtos
from pedidos import Pedidos

class Estoque:
    def __init__(self):
        self.listaDeProdutos = self.carregarProdutos()
        self.listaDePedidos = self.carregarPedidos()

    def salvarProdutos(self):
        """
        Salva a lista de produtos no arquivo produtos.txt.
        """
        with open("produtos.txt", "w") as f:
            for produto in self.listaDeProdutos:
                f.write(produto.to_string() + "\n")

    def salvarPedidos(self):
        """
        Salva a lista de pedidos no arquivo pedidos.txt.
        """
        with open("pedidos.txt", "w") as f:
            for pedido in self.listaDePedidos:
                f.write(pedido.to_string() + "\n")

    def carregarPedidos(self):
        """
        Carrega a lista de pedidos do arquivo pedidos.txt.
        """
        try:
            with open("pedidos.txt", "r") as f:
                return [Pedidos.from_string(linha, self) for linha in f.readlines()]
        except FileNotFoundError:
            return []

    def carregarProdutos(self):
        """
        Carrega a lista de produtos do arquivo produtos.txt.
        """
        try:
            with open("produtos.txt", "r") as f:
                return [Produtos.from_string(linha) for linha in f.readlines()]
        except FileNotFoundError:
            return []

    def adicionarProduto(self, produto):
        """
        Adiciona um produto ao estoque ou atualiza um produto existente.
        """
        # Verifica se o produto já existe na lista
        produto_existente = next((p for p in self.listaDeProdutos if p.codigo == produto.codigo), None)
        
        if produto_existente:
            # Se o produto já existe, atualiza seus dados
            produto_existente.nome = produto.nome
            produto_existente.quantidade = produto.quantidade
            produto_existente.peso = produto.peso
            produto_existente.categoria = produto.categoria
            produto_existente.preco = produto.preco
            produto_existente.fornecedor = produto.fornecedor
            print(f"Produto '{produto.nome}' (código: {produto.codigo}) atualizado com sucesso.")
        else:
            # Se o produto não existe, adiciona à lista
            self.listaDeProdutos.append(produto)
            print(f"Produto '{produto.nome}' (código: {produto.codigo}) adicionado com sucesso.")
        
        # Salva a lista atualizada no arquivo
        self.salvar_produtos()

    def adicionarPedido(self, pedido):
        """Adiciona um pedido e salva no arquivo."""
        self.listaDePedidos.append(pedido)
        self.salvar_pedidos()

    def finalizarPedidos(self):
        """
        Finaliza todos os pedidos, atualizando o estoque e limpando a lista de pedidos.
        """
        for pedido in self.listaDePedidos:
            for produto, quantidade in pedido.itens.items():
                # Procura o produto no estoque
                for prod in self.listaDeProdutos:
                    if prod.codigo == produto.codigo:
                        try:
                            prod.retirada(quantidade)  # Atualiza o estoque
                        except ValueError as e:
                            print(f"Erro ao finalizar pedido {pedido.id}: {e}")
                            break  # Interrompe a finalização do pedido atual
            print(f"Pedido #{pedido.id} finalizado com sucesso.")

        # Salva o estoque atualizado no arquivo
        self.salvarProdutos()

        # Limpa a lista de pedidos e o arquivo de pedidos
        self.listaDePedidos = []
        self.salvarPedidos()

        print("Todos os pedidos foram finalizados e o estoque foi atualizado.")