from telegram import Update
from telegram.ext import CommandHandler, CallbackContext
from database import cursor

async def saldo(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id

    # Consulta os gastos e ganhos do usuário
    cursor.execute('SELECT SUM(valor) FROM gastos WHERE user_id = ?', (user_id,))
    total_gastos = cursor.fetchone()[0] or 0

    cursor.execute('SELECT SUM(valor) FROM ganhos WHERE user_id = ?', (user_id,))
    total_ganhos = cursor.fetchone()[0] or 0

    saldo_final = total_ganhos - total_gastos

    await update.message.reply_text(
        f"📊 Seu saldo atual:\n\n"
        f"💰 Ganhos totais: R${total_ganhos:.2f}\n"
        f"💸 Gastos totais: R${total_gastos:.2f}\n"
        f"🔹 Saldo final: R${saldo_final:.2f}"
    )

# Handler para o comando /saldo
saldo_handler = CommandHandler("saldo", saldo)