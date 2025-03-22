import asyncio
import nest_asyncio
from telegram.ext import Application
from handlers import gastos, ganhos, saldo, relatorio, metas, lembretes
from handlers.menu import menu_handler, menu_selection_handler  # Importa os handlers do menu

# Aplica o nest_asyncio para evitar problemas de loop
nest_asyncio.apply()

# Token do bot (substitua pelo seu token válido)
TOKEN = "8016303871:AAFMRUErJ7x-vuTPt4cjkvosVwzpPzUBa0o"

async def main():
    # Cria a aplicação do bot
    application = Application.builder().token(TOKEN).build()

    # Adiciona os handlers
    application.add_handler(menu_handler)  # Adiciona o menu
    application.add_handler(menu_selection_handler)  # Adiciona o handler das seleções do menu
    application.add_handler(gastos.gasto_handler)
    application.add_handler(ganhos.ganho_handler)
    application.add_handler(saldo.saldo_handler)
    application.add_handler(relatorio.relatorio_handler)
    application.add_handler(metas.meta_handler)
    application.add_handler(lembretes.lembrete_handler)

    print("Bot iniciado...")
    await application.run_polling()

if __name__ == "__main__":
    asyncio.run(main())