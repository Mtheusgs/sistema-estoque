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
    if User.query.filter_by(Login=usuario).first():
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


    # Recupera informações da sessão
    nome = session.get('nome', 'Usuário')  # Se não houver, usa 'Usuário' como default
    cargo = session.get('cargo', 'Cargo')  # Se não houver, usa 'Cargo' como default


    if request.method == 'POST':
        # Verifica se estamos realizando uma busca ou adicionando um produto
        if 'Busca' in request.form:
            # Captura o critério de busca
            criterio = request.form.get('Busca')  # Agora o nome correto é 'Busca'
            valor_busca = request.form.get('valor_busca')  # Certifique-se de ter um campo adicional para inserir o valor da busca, como um input de texto ou algo similar

            # Realiza a consulta no banco de dados com base no critério selecionado
            if criterio == 'cod':
                produtos = Produto.query.filter_by(codigo=valor_busca).all()
            elif criterio == 'nome':
                produtos = Produto.query.filter(Produto.nome.ilike(f'%{valor_busca}%')).all()
            elif criterio == 'categoria':
                produtos = Produto.query.filter_by(categoria=valor_busca).all()
            elif criterio == 'fornecedor':
                produtos = Produto.query.filter_by(fornecedor=valor_busca).all()
            else:
                produtos = []  # Caso nenhum critério válido seja selecionado

            if produtos:
                flash("Encontrado", "success") 
            else:
                flash("Não encontrado", "error")


            
            
        
        if 'nome' in request.form:  # Caso o formulário seja para adicionar um produto
            nome = request.form.get("nome")
            codigo = request.form.get("codigo")
            quantidade = request.form.get("quantidade")
            peso = request.form.get("peso")
            categoria = request.form.get("categoria")
            preco = request.form.get("preco")
            fornecedor = request.form.get("fornecedor")

            # Verifica se o produto já existe baseado no código
            produto_existente = Produto.query.filter_by(codigo=codigo).first()

            if produto_existente:
                flash("Produto com esse código já existe", "error")  # Mensagem flash de erro
            else:
                # Cria um novo produto
                novo_produto = Produto(
                nome=nome,
                codigo=codigo,
                quantidade=int(quantidade),  # Converte para inteiro
                peso=float(peso),  # Converte para float
                categoria=categoria,
                preco=float(preco),  # Converte para float
                fornecedor=fornecedor
                 )

                # Adiciona o produto no banco de dados
                db.session.add(novo_produto)
                db.session.commit()
            
                flash("Produto adicionado com sucesso!", "success")  # Mensagem flash de sucesso
            


    # Consulta todos os produtos no banco de dados
    produtos = Produto.query.all()  # Pode ser uma lista de objetos Produto

    return render_template("dashboard.html", nome=nome, cargo=cargo, produtos=produtos)



@app.route("/logout")
def logout():
    session.clear()  # Limpa todos os dados da sessão
    flash("Você saiu com sucesso!","success")
    return redirect(url_for("index"))  # Redireciona para a página de login





if __name__ == "__main__":  
    with app.app_context():
        db.create_all()  # Cria as tabelas no banco de dados

        # Teste de acesso às tabelas
        users = User.query.all()  # Tenta buscar todos os usuários
        print(users)  # Imprime os resultados para ver se há dados no banco de dados 
        for usuario in users:
            print(f'ID: {usuario.UserId}, Nome: {usuario.UserName}, Cargo: {usuario.Cargo}')
    app.run(debug=True)
