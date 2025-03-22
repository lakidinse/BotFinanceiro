from telegram import Update
from telegram.ext import CommandHandler, CallbackContext
from database import cursor, conn
from datetime import datetime

async def definir_meta(update: Update, context: CallbackContext) -> None:
    try:
        valor = float(context.args[0])
        descricao = " ".join(context.args[1:]) if len(context.args) > 1 else "Sem descrição"
    except (IndexError, ValueError):
        await update.message.reply_text("⚠️ Formato inválido. Use /definir_meta <valor> <descrição>.")
        return

    user_id = update.effective_user.id
    data_atual = datetime.now().strftime("%m/%Y")

    # Insere a meta no banco de dados
    cursor.execute('''
    INSERT INTO metas (user_id, descricao, valor, data)
    VALUES (?, ?, ?, ?)
    ''', (user_id, descricao, valor, data_atual))

    conn.commit()
    await update.message.reply_text(f"🎯 Meta definida: {descricao} (R${valor:.2f})")

# Handler para o comando /definir_meta
meta_handler = CommandHandler("definir_meta", definir_meta)