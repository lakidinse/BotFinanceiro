import matplotlib.pyplot as plt
import io
from datetime import datetime

def gerar_grafico_gastos(gastos_por_categoria, mes_ano):
    """
    Gera um gráfico de barras com os gastos por categoria.
    """
    categorias = [gasto[0] for gasto in gastos_por_categoria]
    valores = [gasto[1] for gasto in gastos_por_categoria]

    # Cria o gráfico de barras
    plt.figure(figsize=(10, 6))
    bars = plt.bar(categorias, valores, color='skyblue')

    # Adiciona valores nas barras
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, height,
                 f'R$ {height:.2f}', ha='center', va='bottom')

    plt.xlabel('Categorias', fontsize=12)
    plt.ylabel('Valor (R$)', fontsize=12)
    plt.title(f'Gastos por Categoria em {mes_ano}', fontsize=14, fontweight='bold')
    plt.xticks(rotation=45, ha='right')  # Rotaciona os rótulos para melhor legibilidade
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # Salva o gráfico em um buffer de memória
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    plt.close()

    return buf

def gerar_grafico_pizza(gastos_por_categoria, mes_ano):
    """
    Gera um gráfico de pizza com a distribuição de gastos por categoria.
    """
    categorias = [gasto[0] for gasto in gastos_por_categoria]
    valores = [gasto[1] for gasto in gastos_por_categoria]

    # Cria o gráfico de pizza
    plt.figure(figsize=(8, 8))
    plt.pie(valores, labels=categorias, autopct='%1.1f%%', startangle=140,
            colors=plt.cm.Paired.colors, textprops={'fontsize': 12})
    plt.title(f'Distribuição de Gastos em {mes_ano}', fontsize=14, fontweight='bold')

    # Salva o gráfico em um buffer de memória
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    plt.close()

    return buf

def gerar_grafico_linha(gastos_por_dia, mes_ano):
    """
    Gera um gráfico de linha com a evolução dos gastos ao longo do mês.
    """
    dias = [int(dia) for dia, _ in gastos_por_dia]  # Extrai os dias
    valores = [valor for _, valor in gastos_por_dia]  # Extrai os valores

    # Cria o gráfico de linha
    plt.figure(figsize=(10, 6))
    plt.plot(dias, valores, marker='o', color='orange', linestyle='-', linewidth=2, markersize=8)

    # Adiciona valores nos pontos
    for dia, valor in zip(dias, valores):
        plt.text(dia, valor, f'R$ {valor:.2f}', ha='center', va='bottom', fontsize=10)

    plt.xlabel('Dia do Mês', fontsize=12)
    plt.ylabel('Valor (R$)', fontsize=12)
    plt.title(f'Evolução dos Gastos em {mes_ano}', fontsize=14, fontweight='bold')
    plt.grid(linestyle='--', alpha=0.7)
    plt.xticks(range(1, 32))  # Dias do mês (1 a 31)

    # Salva o gráfico em um buffer de memória
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    plt.close()

    return buf