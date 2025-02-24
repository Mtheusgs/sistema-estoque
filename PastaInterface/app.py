from flask import Flask, render_template, request, redirect, url_for, flash, session
from user import User

app = Flask(__name__) 
app.secret_key= "12345"

# Lista de usuários
User.user_list = [ 
    User('0', 'admin', 'Criador', 'admin', 'admin'),
    User("1", "Matheus", "Gerente", "thg", "12345"),
    User("2", "Maria", "Funcionário", "Mah", "123")
]


@app.route("/", methods=["GET", "POST"])
def index():
    mensagem = ""
    if request.method == "POST":
        usuario = request.form.get("usuario")
        senha = request.form.get("senha") 

        usuario_autenticado = User.login(usuario, senha)  # Aqui chamamos o método de classe corretamente
        if usuario_autenticado: 
            session['nome'] = usuario_autenticado.UserName
            session['cargo'] = usuario_autenticado.Cargo
            return redirect(url_for("dashboard"))
        else:
            mensagem = "Usuário ou senha incorretos!"


    
    return render_template("index.html", mensagem=mensagem)

@app.route("/register", methods=["POST"])
def register():   
    Usercast = True
    iden = request.form.get("iden")
    nome = request.form.get("nome")
    cargo = request.form.get("cargo")
    usuario = request.form.get("usuario")
    senha = request.form.get("senha")
    
    # Verifica se o usuário já existe
    for user in User.user_list:
        if user.Login == usuario or user.UserId == iden:
            Usercast = False
            break  # Quando encontrar o usuário, não precisa continuar a busca
    
    if Usercast == False:
        flash("Usuário já está cadastrado no sistema!")
        return redirect(url_for("index"))
    else:
        # Criação do novo usuário
        novo_usuario = User(iden, nome, cargo, usuario, senha) 
        flash("Usuário cadastrado com sucesso!")
        
        return redirect(url_for("index"))
    

@app.route("/dashboard")
def dashboard():
    nome = session.get('nome', 'Usuário')
    cargo = session.get('cargo', 'Cargo')
    return render_template("dashboard.html", nome=nome, cargo=cargo) 


@app.route("/logout")
def logout():
    session.clear()  # Limpa todos os dados da sessão
    flash("Você saiu com sucesso!")
    return redirect(url_for("index"))  # Redireciona para a página de login


if __name__ == "__main__":
    app.run(debug=True)
