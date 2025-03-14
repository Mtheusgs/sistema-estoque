from flask import Flask, render_template, request, redirect, url_for, flash, session
import os 
from Models import db
from Models.user import User  # Importamos depois do db para evitar erros 
from Models.produto import Produto  # Importamos depois do db para evitar erros
from Models.produto import Produto, validar_produto, ProdutoError  # Importamos depois do db para evitar erros 
from flask import redirect, url_for  





app = Flask(__name__)  

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False    
app.config["SECRET_KEY"]="chave_secreta"  # Chave secreta para as sessões


db.init_app(app)




@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        usuario = request.form.get("usuario")
        senha = request.form.get("senha")

        user = User.login(usuario, senha)  # Verifica se o usuário existe no banco de dados 
        if user:  
            session['user_id'] = user.UserId
            session['nome'] = user.UserName
            session['cargo'] = user.Cargo
            return redirect(url_for("dashboard")) 
        else:
            flash("Usuário ou senha incorretos!", "error")

    return render_template("index.html")  # Volta para a página sem redirecionamento



@app.route("/register", methods=["POST"])
def register():   
    Usercast = True
    nome = request.form.get("nome")
    cargo = request.form.get("cargo")
    usuario = request.form.get("usuario")
    senha = request.form.get("senha")
    
    # Verifica se o usuário já existe
    if User.query.filter_by(Login=usuario).first():  # modificar 
        Usercast = False
    
    if not Usercast:  # Você pode simplificar assim
        flash("Usuário já está cadastrado no sistema!","error")
        return redirect(url_for("index"))
    else:
        # Criação do novo usuário
        novo_usuario = User(nome, cargo, usuario, senha)
 
        db.session.add(novo_usuario)
        db.session.commit()
        flash("Usuário cadastrado com sucesso!","success")
        
        return redirect(url_for("index"))
    

@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    

    active_section = request.args.get("section", "gerEstoque")


    nome = session.get('nome', 'Usuário')  
    cargo = session.get('cargo', 'Cargo')   

    UserLogado = User.mostrarUser(nome)  # Mostra o usuário logado

    # Consulta todos os produtos e usuários no banco de dados
    produtos = Produto.query.all()  
    usuarios = User.listarUsers()  

    # Lógica de busca
    criterio = request.form.get('Busca')
    valor_busca = request.form.get('valor_busca')  

    


    if request.method == 'POST':
        action = request.form.get('action')  


        
        codigo_apag = request.form.get("codigoApagar") 

        

        # Se for uma busca de produto
        if action == 'buscar':
            if not criterio: 
                flash("Por favor, selecione um critério de busca!", "error")
                return render_template("dashboard.html", nome=nome, cargo=cargo, produtos=produtos, usuarios=usuarios, Resultado=produtos, UserLogado=UserLogado,active_section="gerEstoque")

            if not valor_busca: 
                flash("Por favor, digite um valor para buscar!", "error")
                return render_template("dashboard.html", nome=nome, cargo=cargo, produtos=produtos, usuarios=usuarios, Resultado=produtos, UserLogado=UserLogado,active_section="gerEstoque")

            
            Resultado = Produto.buscarProduto(criterio, valor_busca)
            
            if Resultado:
                flash("Produto encontrado!", "success")
                return render_template("dashboard.html", nome=nome, cargo=cargo, produtos=produtos, usuarios=usuarios, Resultado=Resultado, UserLogado=UserLogado,active_section="gerEstoque")
            else:    
                flash("Produto não encontrado! Retornando à lista principal", "error")  
                return render_template("dashboard.html", nome=nome, cargo=cargo, produtos=produtos, usuarios=usuarios, Resultado=produtos, UserLogado=UserLogado,active_section="gerEstoque")
            
            
            


        # Se for um cadastro de produto
        if action == 'adicionar' and request.form.get('nome'):  # Verifica se o campo 'nome' está presente
            nome_produto = request.form.get("nome")
            quantidade = request.form.get("quantidade")
            peso = request.form.get("peso")
            categoria = request.form.get("categoria")
            preco = request.form.get("preco")
            fornecedor = request.form.get("fornecedor") 


            if nome_produto and fornecedor and preco:
                codigo = f"{nome_produto[0].upper()}{fornecedor[0].upper()}{int(float(preco))}"
            else:
                flash("Erro ao gerar código do produto. Verifique os campos!", "error-add")



            produto_existente = Produto.query.filter_by(codigo=codigo).first()
            
            if produto_existente:
                flash("Produto com esse código já existe", "error")
            else:
                try:
                    validar_produto(quantidade, peso, preco)

                    novo_produto = Produto(
                        nome=nome_produto,
                        codigo=codigo,
                        quantidade=int(quantidade),
                        peso=float(peso),
                        categoria=categoria,
                        preco=float(preco),
                        fornecedor=fornecedor
                    )
                    db.session.add(novo_produto)
                    db.session.commit()
                    flash("Produto adicionado com sucesso!", "success-add")  

                except ProdutoError as err:
                    flash(str(err), "error-add")
                produtos = Produto.query.all()    
            return render_template("dashboard.html", nome=nome, cargo=cargo, produtos=produtos, usuarios=usuarios, Resultado=produtos, UserLogado=UserLogado,active_section="gerEstoque")

        # Se for uma exclusão de produto
        if action == "apagar" and codigo_apag: 
            print("Chegou")
            codigo = request.form.get("codigoApagar")  
            print(codigo) 
            quantidade = request.form.get("quantapagar")
            try:
                validar_produto(quantidade, 1, 1)
                sucesso = Produto.apagarProduto(codigo,quantidade)  

                if sucesso:
                    flash("Produto apagado com sucesso!", "success-del") 
                    
                else:
                    flash("Produto não encontrado", "error-del")
            except ProdutoError as err:
                    flash(str(err), "error-del")



                    
        # Se for uma ação de carrinho
        if action == "carrinho":  
            active_section = request.form.get("section", "estoque") 

            print(active_section)

            codigo = request.form.get("codigoProCarrinho").upper()  
            quantidadeDesejada = request.form.get("quantidadeProcarrinho")  

            # Recupera o carrinho da sessão ou cria uma lista vazia
            carrinhodeProdutos = session.get("carrinho", [])  

            produto = Produto.addProduCarrinho(codigo,quantidadeDesejada)
            if produto:
                # Verifica se o produto já está no carrinho
                produto_encontrado = next((p for p in carrinhodeProdutos if p["codigo"] == codigo), None)

                if produto_encontrado:
                    # Converte a quantidade existente para inteiro antes de somar
                    produto_encontrado["quantidade"] = int(produto_encontrado["quantidade"]) + int(quantidadeDesejada)
                else:
                    # Se não existe, adiciona um novo item ao carrinho
                    produto_dict = {
                        "codigo": produto.codigo,
                        "nome": produto.nome,
                        "quantidade": quantidadeDesejada  # Mantendo como int
                    }
                    carrinhodeProdutos.append(produto_dict)

            # Salva o carrinho atualizado na sessão
            session["carrinho"] = carrinhodeProdutos 
            session.modified = True  # Garante que a sessão seja atualizada  


            return render_template("dashboard.html", nome=nome, cargo=cargo, produtos=produtos, usuarios=usuarios, Resultado=produtos,carrinhodeProdutos=carrinhodeProdutos,quantidadeDesejada=quantidadeDesejada,UserLogado=UserLogado, active_section=active_section)

                 

        if action == "alterar": 
            active_section = request.form.get("section", "estoque") 

            # Recupera o carrinho da sessão
            carrinhodeProdutos = session.get("carrinho", [])

            # A linha que você quer remover do carrinho
            linha = request.form.get("alterarPedido") 
            print(linha)

            # Verifica se a linha existe na lista
            if 0 <= int(linha) < len(carrinhodeProdutos):
                del carrinhodeProdutos[int(linha)]

            # Salva o carrinho atualizado na sessão
            session["carrinho"] = carrinhodeProdutos
            session.modified = True

            return render_template("dashboard.html", nome=nome, cargo=cargo, produtos=produtos, usuarios=usuarios, Resultado=produtos, carrinhodeProdutos=carrinhodeProdutos, UserLogado=UserLogado, active_section="pedidos")




        if action == "apagarUser":
            active_section = request.args.get("section", "user")
            idApagar = request.form.get("userId")  
            ocorreu=User.apagarUser(cargo, idApagar)  
            if ocorreu:
                flash("Usuário apagado com sucesso!", "apagado") 
                listaUser=User.listarUsers()
                return render_template("dashboard.html", nome=nome, cargo=cargo, produtos=produtos, usuarios=listaUser, Resultado=produtos, UserLogado=UserLogado,active_section=active_section)
            else:
                flash("Você não tem permissão para apagar usuários ou o usuário não foi encontrado", "napagado")
                return render_template("dashboard.html", nome=nome, cargo=cargo, produtos=produtos, usuarios=usuarios, Resultado=produtos, UserLogado=UserLogado,active_section=active_section)
            
        if action == "Confirmar":
            carrinhodeProdutos = session.get("carrinho", [])
            
            # Itera sobre o carrinho
            for item in carrinhodeProdutos:
                codigo = item.get('codigo')  # Código do produto
                quantidade = item.get('quantidade')  # Quantidade do produto
                
                # Verifica se o produto existe e chama o método para apagar do banco
                sucesso = Produto.apagarProduto(codigo, quantidade)
                
                # Se a remoção for bem-sucedida, você pode executar algo aqui (se necessário)
                if sucesso:
                    flash(f"Produto {codigo} removido com sucesso!", "success-del")
                else:
                    flash(f"Produto {codigo} não encontrado no banco de dados.", "error-del")
            
            # Atualiza o carrinho na sessão, removendo os produtos
            session["carrinho"] = []
            session.modified = True

            return render_template("dashboard.html", nome=nome, cargo=cargo, produtos=produtos, usuarios=usuarios, Resultado=produtos, carrinhodeProdutos=[], UserLogado=UserLogado, active_section="pedidos")

                


    # Recarrega a lista de produtos após a exclusão
    produtos = Produto.query.all()  
    usuarios = User.listarUsers()

    UserLogado = User.mostrarUser(nome)  # Mostra o usuário logado
    return render_template("dashboard.html", nome=nome, cargo=cargo, produtos=produtos, usuarios=usuarios, Resultado=produtos,carrinhodeProdutos=[], UserLogado=UserLogado, active_section=active_section)




@app.route("/logout")
def logout():
    session.clear()  # Limpa todos os dados da sessão
    flash("Você saiu com sucesso!","success")
    return redirect(url_for("index"))  # Redireciona para a página de login





if __name__ == "__main__":  
    with app.app_context():
        db.create_all()  # Cria as tabelas no banco de dados 

    app.run(debug=True)
