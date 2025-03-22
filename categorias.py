import json
import os

def carregar_categorias():
    """
    Carrega as categorias do arquivo categorias.json.

    Returns:
        dict: Um dicionário com as categorias e suas palavras-chave.
    """
    if not os.path.exists('categorias.json'):
        raise FileNotFoundError("Arquivo categorias.json não encontrado.")

    try:
        with open('categorias.json', 'r', encoding='utf-8') as f:
            categorias = json.load(f)
            return categorias
    except json.JSONDecodeError:
        raise ValueError("Erro ao ler o arquivo categorias.json. Verifique o formato do arquivo.")

# Carrega as categorias
categorias = carregar_categorias()

def mapear_categoria(descricao):
    """
    Mapeia uma descrição para uma categoria com base nas palavras-chave.

    Args:
        descricao (str): A descrição do gasto ou ganho.

    Returns:
        str: A categoria correspondente ou "outros" se não houver correspondência.
    """
    descricao = descricao.lower()  # Converte a descrição para minúsculas

    for categoria, palavras_chave in categorias.items():
        # Verifica se alguma palavra-chave está na descrição
        if any(palavra.lower() in descricao for palavra in palavras_chave):
            return categoria

    return "outros"  # Se não encontrar nenhuma correspondência, retorna "outros"