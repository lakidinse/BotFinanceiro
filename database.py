import sqlite3

# Conecta ao banco de dados (ou cria se não existir)
conn = sqlite3.connect('financeiro.db', check_same_thread=False)
cursor = conn.cursor()

def criar_tabelas():
    # Tabela de usuários
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER UNIQUE
    )
    ''')

    # Tabela de gastos
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS gastos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        valor REAL,
        descricao TEXT,
        data TEXT,
        categoria TEXT,
        FOREIGN KEY (user_id) REFERENCES usuarios (user_id)
    )
    ''')

    # Adiciona a coluna 'categoria' se não existir
    cursor.execute('PRAGMA table_info(gastos)')
    colunas = [info[1] for info in cursor.fetchall()]
    if 'categoria' not in colunas:
        cursor.execute('ALTER TABLE gastos ADD COLUMN categoria TEXT')

    # Tabela de ganhos
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS ganhos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        valor REAL,
        descricao TEXT,
        data TEXT,  -- Adicionando a coluna 'data'
        categoria TEXT,
        FOREIGN KEY (user_id) REFERENCES usuarios (user_id)
    )
    ''')

    # Adiciona a coluna 'categoria' se não existir
    cursor.execute('PRAGMA table_info(ganhos)')
    colunas = [info[1] for info in cursor.fetchall()]
    if 'categoria' not in colunas:
        cursor.execute('ALTER TABLE ganhos ADD COLUMN categoria TEXT')

    # Adiciona a coluna 'data' se não existir
    cursor.execute('PRAGMA table_info(ganhos)')
    colunas = [info[1] for info in cursor.fetchall()]
    if 'data' not in colunas:
        cursor.execute('ALTER TABLE ganhos ADD COLUMN data TEXT')

    # Tabela de metas
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS metas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        descricao TEXT,
        valor REAL,
        data TEXT,
        FOREIGN KEY (user_id) REFERENCES usuarios (user_id)
    )
    ''')

    conn.commit()
    
criar_tabelas()