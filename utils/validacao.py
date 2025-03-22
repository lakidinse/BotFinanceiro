from categorias import mapear_categoria
from telegram import Update
from telegram.ext import CallbackContext

async def validacao_valor(update: Update, context: CallbackContext, tipo: str):
    try:
        valor = float(context.args[0])
        if valor <= 0:
            await update.message.reply_text(f"⚠️ O valor do {tipo} deve ser positivo.")
            return None, None, None
        
        # Captura a descrição e a categoria
        if len(context.args) > 1:
            descricao = " ".join(context.args[1:-1])  # Descrição são todos os argumentos, exceto o último
            categoria = context.args[-1].lower()  # Último argumento é a categoria
            if not mapear_categoria(categoria):  # Verifica se a categoria existe
                await update.message.reply_text(f"⚠️ Categoria '{categoria}' não encontrada. Usando 'outros'.")
                categoria = "outros"
        else:
            descricao = "Sem descrição"
            categoria = "outros"
        
        return valor, descricao, categoria
    except (IndexError, ValueError):
        await update.message.reply_text(f"⚠️ Insira um valor válido para o {tipo}.")
        return None, None, None