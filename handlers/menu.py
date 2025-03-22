from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CommandHandler, CallbackContext, MessageHandler, filters

async def menu(update: Update, context: CallbackContext) -> None:
    # Cria o teclado com as opções
    keyboard = [
        ['Registrar Gasto', 'Registrar Ganho'],
        ['Ver Saldo', 'Gastos por Mês'],
        ['Relatório Mensal', 'Definir Meta'],
        ['Ativar Lembretes']
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)

    # Mensagem personalizada com as opções
    mensagem = (
        "💰 Olá! Eu sou seu bot financeiro. Use as opções abaixo para registrar seus dados financeiros:\n\n"
        "📊 /gasto <valor> <descrição> <categoria> - Registrar um gasto\n"
        "💵 /ganho <valor> <descrição> <categoria> - Registrar um ganho\n"
        "💳 /saldo - Ver o seu saldo atual\n"
        "📅 /gastos_mes <MM/AAAA> - Ver gastos de um mês específico\n"
        "📊 /relatorio_mensal - Gerar relatório mensal\n"
        "🎯 /definir_meta <valor> <descrição> - Definir uma meta financeira"
    )

    # Envia a mensagem com o teclado de opções
    await update.message.reply_text(mensagem, reply_markup=reply_markup)

async def handle_menu_selection(update: Update, context: CallbackContext) -> None:
    # Captura o texto da mensagem enviada pelo usuário
    text = update.message.text

    # Mapeia o texto para os comandos correspondentes
    if text == "Registrar Gasto":
        await update.message.reply_text("Executando /gasto...")
        # Aqui você pode chamar a função que executa o comando /gasto
    elif text == "Registrar Ganho":
        await update.message.reply_text("Executando /ganho...")
        # Aqui você pode chamar a função que executa o comando /ganho
    elif text == "Ver Saldo":
        await update.message.reply_text("Executando /saldo...")
        # Aqui você pode chamar a função que executa o comando /saldo
    elif text == "Gastos por Mês":
        await update.message.reply_text("Executando /gastos_mes...")
        # Aqui você pode chamar a função que executa o comando /gastos_mes
    elif text == "Relatório Mensal":
        await update.message.reply_text("Executando /relatorio_mensal...")
        # Aqui você pode chamar a função que executa o comando /relatorio_mensal
    elif text == "Definir Meta":
        await update.message.reply_text("Executando /definir_meta...")
        # Aqui você pode chamar a função que executa o comando /definir_meta
    elif text == "Ativar Lembretes":
        await update.message.reply_text("Executando /ativar_lembretes...")
        # Aqui você pode chamar a função que executa o comando /ativar_lembretes
    else:
        await update.message.reply_text("Opção inválida. Use /menu para ver as opções.")

# Handler para o comando /menu
menu_handler = CommandHandler("menu", menu)

# Handler para capturar as seleções do menu
menu_selection_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, handle_menu_selection)