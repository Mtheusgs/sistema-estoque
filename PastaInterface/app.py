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
    mensagem = ""
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
            mensagem = "Usuário ou senha incorretos!"

    return render_template("index.html", mensagem=mensagem)


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
        flash("Usuário já está cadastrado no sistema!")
        return redirect(url_for("index"))
    else:
        # Criação do novo usuário
        novo_usuario = User(nome, cargo, usuario, senha)
 
        db.session.add(novo_usuario)
        db.session.commit()
        flash("Usuário cadastrado com sucesso!")
        
        return redirect(url_for("index"))
    

@app.route("/dashboard")
def dashboard():  
   
    produtos = Produto.query.all()
    nome = session.get('nome', 'Usuário')
    cargo = session.get('cargo', 'Cargo')
    return render_template("dashboard.html", nome=nome, cargo=cargo, produtos=produtos)


@app.route("/logout")
def logout():
    session.clear()  # Limpa todos os dados da sessão
    flash("Você saiu com sucesso!")
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
