from telegram import Update
from telegram.ext import CommandHandler, CallbackContext
from database import cursor
from utils.graficos import gerar_grafico_gastos, gerar_grafico_pizza, gerar_grafico_linha
from datetime import datetime
from unidecode import unidecode  # Para normalizar categorias

async def relatorio_mensal(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    mes_ano = datetime.now().strftime("%Y-%m")  # Formato YYYY-MM

    try:
        # Consulta os gastos do mês
        cursor.execute('''
        SELECT categoria, SUM(valor) FROM gastos
        WHERE user_id = ? AND strftime('%Y-%m', data) = ?
        GROUP BY categoria
        ''', (user_id, mes_ano))

        gastos_por_categoria = cursor.fetchall()

        # Normaliza as categorias (remove acentos e converte para minúsculas)
        gastos_normalizados = {}
        for categoria, valor in gastos_por_categoria:
            categoria_normalizada = unidecode(categoria).lower()  # Remove acentos e converte para minúsculas
            if categoria_normalizada in gastos_normalizados:
                gastos_normalizados[categoria_normalizada] += valor
            else:
                gastos_normalizados[categoria_normalizada] = valor

        # Converte o dicionário de volta para uma lista de tuplas
        gastos_por_categoria = [(categoria, valor) for categoria, valor in gastos_normalizados.items()]

        # Consulta os ganhos do mês
        cursor.execute('''
        SELECT descricao, SUM(valor) FROM ganhos
        WHERE user_id = ? AND strftime('%Y-%m', data) = ?
        GROUP BY descricao
        ''', (user_id, mes_ano))

        ganhos_por_descricao = cursor.fetchall()

        # Consulta os gastos diários do mês
        cursor.execute('''
        SELECT strftime('%d', data) as dia, SUM(valor) 
        FROM gastos 
        WHERE user_id = ? AND strftime('%Y-%m', data) = ?
        GROUP BY dia
        ORDER BY dia
        ''', (user_id, mes_ano))

        gastos_por_dia = cursor.fetchall()

        # Preenche os dias faltantes com zero (opcional)
        dias_completos = {f"{dia:02d}": 0.0 for dia in range(1, 32)}  # Dias de 01 a 31
        for dia, valor in gastos_por_dia:
            dias_completos[dia] = valor
        gastos_por_dia = [(dia, valor) for dia, valor in dias_completos.items()]

        # Calcula totais
        total_gastos = sum(gasto[1] for gasto in gastos_por_categoria)
        total_ganhos = sum(ganho[1] for ganho in ganhos_por_descricao)
        saldo_final = total_ganhos - total_gastos

        # Monta a mensagem do relatório
        mensagem = f"📅 *Relatório Mensal ({mes_ano})*:\n\n"
        mensagem += f"💸 *Total de Gastos:* R$ {total_gastos:.2f}\n"
        mensagem += f"💰 *Total de Ganhos:* R$ {total_ganhos:.2f}\n"
        mensagem += f"💳 *Saldo Final:* R$ {saldo_final:.2f}\n\n"

        if not gastos_por_categoria and not ganhos_por_descricao:
            mensagem += "Nenhum dado registrado este mês."
        else:
            if gastos_por_categoria:
                mensagem += "📉 *Gastos por Categoria:*\n"
                for categoria, total in gastos_por_categoria:
                    mensagem += f"- {categoria}: R$ {total:.2f}\n"
            else:
                mensagem += "📉 Nenhum gasto registrado este mês.\n"

            if ganhos_por_descricao:
                mensagem += "\n📈 *Ganhos por Descrição:*\n"
                for descricao, total in ganhos_por_descricao:
                    mensagem += f"- {descricao}: R$ {total:.2f}\n"
            else:
                mensagem += "\n📈 Nenhum ganho registrado este mês.\n"

        # Envia o relatório textual
        await update.message.reply_text(mensagem, parse_mode='Markdown')

        # Gera e envia gráficos (se houver dados)
        if gastos_por_categoria:
            # Gráfico de barras (gastos por categoria)
            grafico_barras = gerar_grafico_gastos(gastos_por_categoria, mes_ano)
            await update.message.reply_photo(photo=grafico_barras, caption="📊 Gráfico de Gastos por Categoria")
            grafico_barras.close()

            # Gráfico de pizza (distribuição dos gastos)
            grafico_pizza = gerar_grafico_pizza(gastos_por_categoria, mes_ano)
            await update.message.reply_photo(photo=grafico_pizza, caption="🍕 Distribuição dos Gastos por Categoria")
            grafico_pizza.close()

            # Gráfico de linha (evolução dos gastos ao longo do mês)
            if gastos_por_dia:  # Verifica se há dados diários
                grafico_linha = gerar_grafico_linha(gastos_por_dia, mes_ano)
                await update.message.reply_photo(photo=grafico_linha, caption="📈 Evolução dos Gastos ao Longo do Mês")
                grafico_linha.close()

    except Exception as e:
        await update.message.reply_text(f"❌ Erro ao gerar o relatório: {str(e)}")

# Handler para o comando /relatorio_mensal
relatorio_handler = CommandHandler("relatorio_mensal", relatorio_mensal)