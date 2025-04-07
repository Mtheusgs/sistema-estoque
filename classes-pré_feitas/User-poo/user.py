class User:
    user_list = []

    def __init__(self, UserId: str, UserName: str, Cargo: str, Login: str, Senha: str):
        self.UserId = UserId
        self.UserName = UserName
        self.Cargo = Cargo
        self.Login = Login
        self.Senha = Senha
        User.user_list.append(self)

    @classmethod
    def listar_usuarios(cls):
        """ Exibe todos os usuários cadastrados """
        for user in cls.user_list:
            print(f"ID: {user.UserId}, Nome: {user.UserName}, Cargo: {user.Cargo}, Login: {user.Login}")

    @classmethod
    def login(cls, login, senha):
        """ Realiza o login do usuário """
        for user in cls.user_list:
            if user.Login == login and user.Senha == senha: 
                print(f"Usuário {user.UserName} logado com sucesso!")
                return  # Sai da função após um login bem-sucedido
        
        print("Usuário ou senha incorretos!")  # Se não encontrou o usuário

    @classmethod
    def alterarSenha(cls): 
        login = input("Digite o login: ")
        senha = input("Digite a senha: ")
        """ Permite alterar a senha do usuário autenticado """
        for user in cls.user_list:
            if user.Login == login and user.Senha == senha:
                nova_senha = input("Digite a nova senha: ")
                user.Senha = nova_senha
                print("Senha alterada com sucesso!")
                return
        
        print("Usuário ou senha incorretos!")  # Se não encontrou o usuário

    @staticmethod
    def autenticarUser():
        """ Método estático para autenticar usuário """
        login = input("Digite o login: ")
        senha = input("Digite a senha: ")
        User.login(login, senha) 


class Gerente(User):
    def __init__(self, UserId: str, UserName: str, Cargo: str, Senha: str, Login: str):
        super().__init__(UserId, UserName, Cargo, Senha, Login)
        self.cargo = "Gerente" 
    
    def removerUser(self):
        """ Remove um usuário da lista """
        user_id = input("Digite o ID do usuário que deseja remover: ")
        for user in User.user_list:
            if user.UserId == user_id:
                User.user_list.remove(user)
                print(f"Usuário {user.UserName} removido com sucesso!")
                return
        
        print("Usuário não encontrado!")

    

class Funcionario(User): 
    pass


def registrar(): 
    """ Registra um novo usuário """
    userid = input("Digite o ID do usuário: ")
    username = input("Digite o nome do usuário: ")    
    cargo = input("Digite o cargo do usuário: ")
    login = input("Digite o login do usuário: ")
    senha = input("Digite a senha do usuário: ")  
    
    # Criando o usuário corretamente (corrigindo a ordem dos argumentos)
    novo_usuario = User(userid, username, cargo, senha, login)  
    print(f"Usuário {username} cadastrado com sucesso!")


def mostrarAtributo(escolha):
    switcher = {
        1: "UserId",
        2: "UserName",
        3: "Cargo",
        4: "Login",
        5: "Senha"
    }
    user= User.user_list[1]
    print(f"ID: {user.UserId}, Nome: {user.UserName}, Cargo: {user.Cargo}, Login: {user.Login}, Senha: {user.Senha}")
    atributo = int(input("Digite o número do atributo que deseja visualizar: "))
    print(getattr(user, switcher.get(atributo)))
       




    

