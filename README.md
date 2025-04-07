# Sistema de Estoque 📦

Este projeto consiste em um sistema de controle de estoque desenvolvido para fins acadêmicos. O sistema permite o gerenciamento de produtos em estoque, com funcionalidades para adicionar, editar, excluir e visualizar produtos. Além disso, possibilita realizar pedidos, obter relatórios, gerir fornecedores e entre outras aplicabilidades.

## Tecnologias Utilizadas 🛠️

- **HTML**: Estruturação das páginas da aplicação.
- **Tailwind CSS**: Framework CSS para estilização rápida e responsiva.
- **Flask**: Framework Python para desenvolvimento web.
- **Python**: Linguagem utilizada para lógica de programação e manipulação de dados.
- **JavaScript**: Linguagem para reorganizar atributos no HTML.
- **POO (Programação Orientada a Objetos)**: Estruturação do código utilizando conceitos de classes e objetos.
- **SQLite**: Banco de dados relacional utilizado para armazenar e gerenciar dados de forma eficiente.

## Funcionalidades Principais ⚙️

- **Cadastro de Produtos** 📝: Permite adicionar novos produtos ao estoque, com nome, descrição, quantidade e preço.
- **Edição de Produtos** ✏️: Permite editar as informações dos produtos existentes.
- **Exclusão de Produtos** 🗑️: Permite remover produtos do estoque.
- **Listagem de Produtos** 📋: Exibe todos os produtos registrados no estoque com a opção de visualização detalhada.
- **Pedidos**: Permite realizar pedidos conforme disponibilidade de produtos.
- **Gerenciar Fornecedores**: Possibilita realizar cadastro de fornecedores, bem como, gerir os fornecedores já existentes.
- **Gerenciar Perfis**: Permite ao gerente administrar os perfis de usuário no sistema.
- **Obter Relatório**: Permite gerar relatórios com informes relevantes como entrada e saída de produtos, estoque, pedidos realizados e entre outros setores. 

## Como Rodar o Projeto 🚀

### Pré-requisitos 📋

1. Python 3.x instalado na sua máquina.
2. Gerenciador de pacotes `pip` instalado.

### Instalação 🛠️

- Clone o repositório:

```bash
git clone https://github.com/Mtheusgs/sistema-estoque.git
cd sistema-estoque
````

- Instale as dependências necessárias:

```bash
pip install SQLAlchemy
pip install flask
```
- Em caso de erro de ModuleNotFoundError realize esse comando:
  
```bash
pip install flask-sqlalchemy
```
- Com as dependências instaladas agora execute:

```bash
python app.py
```
## Estrutura do Repositório 📂

```
sistema-estoque/ 📂
│
├── PastaInterface
│    ├── Models/
│    ├── __pycache__                                                                     
│    ├── instance                                 
│    ├── static/img                  
│    ├── templates/                      
│    ├── app.py             
│    └── database.db
├── classes-pré_feitas/User-poo
│    c error_handling.py  
│    ├── error_handling_user.py  
│    ├── estoque.py  
│    ├── pedidos.py  
│    ├── produto.py  
│    ├── rasccunho.py  
│    ├── relatorio.py  
│    └── user.py
├── docs
│    ├── Sprints 
│    ├── Apresentação_Final_Sistema_de_Estoque.pdf 
│    └── Descrição_Sistema_POO_GPTECOS.pdf
└── README.md        
```
---
Esse projeto foi desenvolvido para aplicar na prática os conceitos de Programação Orientada a Objetos (POO), Desenvolvimento Web e entre outros conhecimentos relacionados.
