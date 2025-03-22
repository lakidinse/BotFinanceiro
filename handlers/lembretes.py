from telegram import Update
from telegram.ext import CommandHandler, CallbackContext, Application
from datetime import time

async def ativar_lembretes(update: Update, context: CallbackContext) -> None:
    # Captura o ID do usuário
    user_id = update.effective_user.id

    # Agenda um lembrete diário para o usuário
    context.job_queue.run_daily(
        enviar_lembrete,
        time=time(hour=20, minute=0),  # Horário do lembrete (20:00)
        days=(0, 1, 2, 3, 4, 5, 6),  # Todos os dias da semana
        data=user_id  # Passa o user_id como dados adicionais
    )

    await update.message.reply_text("🔔 Lembretes diários ativados! Você receberá uma mensagem todos os dias às 20:00.")

async def enviar_lembrete(context: CallbackContext):
    # Recupera o user_id dos dados adicionais
    user_id = context.job.data

    # Envia o lembrete
    await context.bot.send_message(chat_id=user_id, text="📅 Não se esqueça de registrar seus gastos de hoje!")

# Handler para ativar lembretes
lembrete_handler = CommandHandler("ativar_lembretes", ativar_lembretes)