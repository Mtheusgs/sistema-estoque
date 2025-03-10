from flask import Flask, render_template, request, redirect, url_for, flash, session
import os 
from Models import db
from Models.user import User  # Importamos depois do db para evitar erros 
from Models.produto import Produto  # Importamos depois do db para evitar erros



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
    
        print(f"Action: {action}")
        print(f"Código para apagar: {codigo_apag}")

        # Se for uma busca de produto
        if action == 'buscar' and criterio and valor_busca: 
            print("foi!")
            Resultado = Produto.buscarProduto(criterio, valor_busca)
            if Resultado:
                flash("Produto encontrado!", "success")
            else:    
                flash("Produto não encontrado!", "error")
            return render_template("dashboard.html", nome=nome, cargo=cargo, produtos=produtos, usuarios=usuarios, Resultado=Resultado)

        # Se for um cadastro de produto
        if action == 'adicionar' and request.form.get('nome'):  # Verifica se o campo 'nome' está presente
            nome = request.form.get("nome")
            codigo = request.form.get("codigo")
            quantidade = request.form.get("quantidade")
            peso = request.form.get("peso")
            categoria = request.form.get("categoria")
            preco = request.form.get("preco")
            fornecedor = request.form.get("fornecedor")

            produto_existente = Produto.query.filter_by(codigo=codigo).first()
            
            if produto_existente:
                flash("Produto com esse código já existe", "error")
            else:
                novo_produto = Produto(
                    nome=nome,
                    codigo=codigo,
                    quantidade=int(quantidade),
                    peso=float(peso),
                    categoria=categoria,
                    preco=float(preco),
                    fornecedor=fornecedor
                )
                db.session.add(novo_produto)
                db.session.commit()
                flash("Produto adicionado com sucesso!", "success") 

        # Se for uma exclusão de produto
        if action == "apagar" and codigo_apag: 
            print("Chegou")
            codigo = request.form.get("codigoApagar")  
            print(codigo)
            sucesso = Produto.apagarProduto(codigo)  
            if sucesso:
                flash("Produto apagado com sucesso!", "success") 
                
            else:
                flash("Produto não encontrado", "error")

    # Recarrega a lista de produtos após a exclusão
    produtos = Produto.query.all()  
    usuarios = User.listarUsers()

    UserLogado = User.mostrarUser(nome)  # Mostra o usuário logado
    return render_template("dashboard.html", nome=nome, cargo=cargo, produtos=produtos, usuarios=usuarios, Resultado=produtos, UserLogado=UserLogado)




@app.route("/logout")
def logout():
    session.clear()  # Limpa todos os dados da sessão
    flash("Você saiu com sucesso!","success")
    return redirect(url_for("index"))  # Redireciona para a página de login





if __name__ == "__main__":  
    with app.app_context():
        db.create_all()  # Cria as tabelas no banco de dados 

    app.run(debug=True)
