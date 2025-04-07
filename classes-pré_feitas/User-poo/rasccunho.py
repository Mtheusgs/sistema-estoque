class User:
    user_list = []  # Lista para armazenar os usuários criados

    def __init__(self, UserId: str, UserName: str, Cargo: str, Senha: str, Login: str):
        self.UserId = UserId
        self.UserName = UserName
        self.Cargo = Cargo
        self.Login = Login
        self.Senha = Senha
        User.user_list.append(self)  # Adiciona o usuário à lista

    @classmethod
    def login(cls, login, senha):
        """ Realiza o login do usuário """
        for user in cls.user_list:
            if user.Login == login and user.Senha == senha:
                print(f"Usuário {user.UserName} logado com sucesso!")
                return  # Sai da função após um login bem-sucedido
        
        # Se não encontrou o usuário na lista, exibe erro
        print("Usuário ou senha incorretos!")

# Criando usuários
user1 = User("1", "Alice", "Admin", "1234", "alice_admin")
user2 = User("2", "Bob", "User", "5678", "bob_user")

# Testando login
User.login("alice_admin", "134")  # Sucesso
User.login("bob_user", "5678")  # Sucesso
User.login("bob_user", "0000")  # Erro