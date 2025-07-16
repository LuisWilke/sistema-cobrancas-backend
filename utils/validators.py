import re

def validar_email(email):
    """
    Valida o formato do email usando regex
    """
    if not email:
        return False
    
    padrao = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(padrao, email) is not None

def validar_senha(senha):
    """
    Valida se a senha atende aos critérios mínimos:
    - Pelo menos 6 caracteres
    """
    if not senha:
        return False
    
    return len(senha) >= 6

def validar_cpf(cpf):
    """
    Valida formato básico do CPF (apenas números e tamanho)
    """
    if not cpf:
        return True  # CPF é opcional
    
    # Remove caracteres não numéricos
    cpf_numeros = re.sub(r'\D', '', cpf)
    
    # Verifica se tem 11 dígitos
    return len(cpf_numeros) == 11

def validar_nome(nome):
    """
    Valida se o nome tem pelo menos 2 caracteres
    """
    if not nome:
        return False
    
    return len(nome.strip()) >= 2

