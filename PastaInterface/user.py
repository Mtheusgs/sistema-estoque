class User():
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


    def login(login, senha):
        """ Realiza o login do usuário e retorna o usuário se autenticado """
        for user in User.user_list:
            if user.Login == login and user.Senha == senha:
                return user  # Retorna o usuário autenticado
        
        return None  # Retorna None se falhar a autenticação

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




       




    

