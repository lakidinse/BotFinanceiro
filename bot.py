import os
import asyncio
import logging
from telegram.ext import Application
from handlers import gastos, ganhos, saldo, relatorio, metas, lembretes
from handlers.menu import menu_handler, menu_selection_handler  # Importa os handlers do menu

# Configuração de logs
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Obtém o token da variável de ambiente
TOKEN = os.getenv("TOKEN")  # Certifique-se de configurar a variável TOKEN no Heroku

async def main():
    try:
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

        logger.info("Bot iniciado...")
        await application.run_polling()

    except Exception as e:
        logger.error(f"Erro ao iniciar o bot: {e}")

if __name__ == "__main__":
    asyncio.run(main())