class UsuarioError(Exception):
    """
    Classe base para excecoes relacionadas ao usuario.
    """
    pass

class UsuarioNaoEncontradoError(UsuarioError):
    """
    Excecao levantada quando um usuario nao e encontrado.
    """
    def __init__(self, login):
        super().__init__(f"Usuario com login '{login}' não encontrado.")

class SenhaIncorretaError(UsuarioError):
    """
    Excecao levantada quando a senha fornecida esta incorreta.
    """
    def __init__(self):
        super().__init__("Senha Incorreta!")