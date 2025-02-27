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
    

@app.route("/dashboard")
def dashboard():  
     
    #produtos = Produto.query.all()

    produtos = [
    {"nome": "Notebook Dell", "codigo": "NB123", "quantidade": 10, "peso": 2.5, "categoria": "Eletrônicos", "preco": 4500.00, "fornecedor": "Dell"},
    {"nome": "Mouse Gamer", "codigo": "MG456", "quantidade": 50, "peso": 0.3, "categoria": "Acessórios", "preco": 150.00, "fornecedor": "Razer"},
    {"nome": "Teclado Mecânico", "codigo": "TM789", "quantidade": 30, "peso": 1.2, "categoria": "Acessórios", "preco": 350.00, "fornecedor": "HyperX"},
    {"nome": "Monitor 24''", "codigo": "MN012", "quantidade": 20, "peso": 4.5, "categoria": "Eletrônicos", "preco": 1200.00, "fornecedor": "Samsung"},
    {"nome": "Impressora HP", "codigo": "IP345", "quantidade": 5, "peso": 8.0, "categoria": "Periféricos", "preco": 800.00, "fornecedor": "HP"},
    {"nome": "SSD 1TB", "codigo": "SD678", "quantidade": 40, "peso": 0.2, "categoria": "Armazenamento", "preco": 600.00, "fornecedor": "Kingston"},
    {"nome": "Cadeira Gamer", "codigo": "CG901", "quantidade": 15, "peso": 15.0, "categoria": "Móveis", "preco": 1500.00, "fornecedor": "DXRacer"},
    {"nome": "Placa de Vídeo RTX 3060", "codigo": "PV234", "quantidade": 8, "peso": 1.8, "categoria": "Hardware", "preco": 2800.00, "fornecedor": "NVIDIA"},
    {"nome": "Processador Ryzen 5", "codigo": "PR567", "quantidade": 25, "peso": 0.5, "categoria": "Hardware", "preco": 1200.00, "fornecedor": "AMD"},
    {"nome": "Memória RAM 16GB", "codigo": "MR890", "quantidade": 60, "peso": 0.1, "categoria": "Hardware", "preco": 400.00, "fornecedor": "Corsair"},
    {"nome": "HD Externo 2TB", "codigo": "HD123", "quantidade": 35, "peso": 0.8, "categoria": "Armazenamento", "preco": 500.00, "fornecedor": "Seagate"},
    {"nome": "Fonte 600W", "codigo": "FN456", "quantidade": 20, "peso": 2.0, "categoria": "Hardware", "preco": 350.00, "fornecedor": "EVGA"},
    {"nome": "Gabinete Gamer", "codigo": "GB789", "quantidade": 18, "peso": 7.0, "categoria": "Hardware", "preco": 700.00, "fornecedor": "NZXT"},
    {"nome": "Webcam Full HD", "codigo": "WC012", "quantidade": 22, "peso": 0.4, "categoria": "Periféricos", "preco": 250.00, "fornecedor": "Logitech"},
    {"nome": "Microfone USB", "codigo": "MC345", "quantidade": 14, "peso": 0.6, "categoria": "Periféricos", "preco": 300.00, "fornecedor": "Blue Yeti"},
    {"nome": "Headset Gamer", "codigo": "HS678", "quantidade": 27, "peso": 0.9, "categoria": "Acessórios", "preco": 450.00, "fornecedor": "SteelSeries"},
    {"nome": "Controle Xbox", "codigo": "CX901", "quantidade": 12, "peso": 0.7, "categoria": "Acessórios", "preco": 500.00, "fornecedor": "Microsoft"},
    {"nome": "Joystick para PC", "codigo": "JP234", "quantidade": 9, "peso": 1.1, "categoria": "Acessórios", "preco": 600.00, "fornecedor": "Thrustmaster"},
    {"nome": "Placa-Mãe B450", "codigo": "PM567", "quantidade": 13, "peso": 1.5, "categoria": "Hardware", "preco": 850.00, "fornecedor": "ASUS"},
    {"nome": "Cooler para CPU", "codigo": "CL890", "quantidade": 19, "peso": 0.8, "categoria": "Hardware", "preco": 200.00, "fornecedor": "Cooler Master"},
    {"nome": "Smartphone Samsung", "codigo": "SP123", "quantidade": 30, "peso": 0.4, "categoria": "Eletrônicos", "preco": 2500.00, "fornecedor": "Samsung"},
    {"nome": "Smartwatch Xiaomi", "codigo": "SW456", "quantidade": 40, "peso": 0.2, "categoria": "Eletrônicos", "preco": 700.00, "fornecedor": "Xiaomi"},
    {"nome": "Tablet Apple", "codigo": "TB789", "quantidade": 10, "peso": 0.5, "categoria": "Eletrônicos", "preco": 5000.00, "fornecedor": "Apple"},
    {"nome": "Carregador Universal", "codigo": "CU012", "quantidade": 50, "peso": 0.3, "categoria": "Acessórios", "preco": 120.00, "fornecedor": "Anker"},
]



    nome = session.get('nome', 'Usuário')
    cargo = session.get('cargo', 'Cargo')
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
