from telegram import Update
from telegram.ext import CommandHandler, CallbackContext
from database import cursor, conn
from utils.validacao import validacao_valor
from datetime import datetime

async def gasto(update: Update, context: CallbackContext) -> None:
    valor, descricao, categoria = await validacao_valor(update, context, 'gasto')
    if valor is None:
        return

    user_id = update.effective_user.id
    data_atual = datetime.now().strftime("%Y-%m-%d")  # Formato YYYY-MM-DD

    try:
        cursor.execute('''
        INSERT INTO gastos (user_id, valor, descricao, data, categoria)
        VALUES (?, ?, ?, ?, ?)
        ''', (user_id, valor, descricao, data_atual, categoria))
        conn.commit()
        await update.message.reply_text(f"💸 Gasto de R${valor:.2f} registrado: {descricao} (Categoria: {categoria})")
    except Exception as e:
        await update.message.reply_text(f"⚠️ Erro ao registrar gasto: {e}")

# Handler para o comando /gasto
gasto_handler = CommandHandler("gasto", gasto)