import sqlite3 as sq

base = sq.connect('users.db')
cursor = base.cursor()


async def sql_start():
    global base, cursor
    if base:
        print('Database connected successfully!')
    base.execute('CREATE TABLE IF NOT EXISTS task(id INTEGER PRIMARY KEY)')
    base.commit()


async def sql_add_command(state):
    cursor.execute('INSERT INTO task VALUES(?)', (state,))
    base.commit()


async def sql_read(message):
    return cursor.execute('SELECT * FROM task WHERE id = ?', (message,)).fetchall()
