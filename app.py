from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

DATABASE = 'database.db'

def conectar():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def criar_tabela():
    conn = conectar()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS links (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            url TEXT NOT NULL,
            categoria TEXT
        )
    """)
    conn.commit()
    conn.close()

@app.route('/')
def index():
    busca = request.args.get('busca', '')

    conn = conectar()

    if busca:
        links = conn.execute("""
            SELECT * FROM links
            WHERE nome LIKE ?
            ORDER BY categoria,nome
        """, (f'%{busca}%',)).fetchall()
    else:
        links = conn.execute("""
            SELECT * FROM links
            ORDER BY categoria,nome
        """).fetchall()

    conn.close()

    return render_template(
        'index.html',
        links=links,
        busca=busca
    )

@app.route('/adicionar', methods=['POST'])
def adicionar():
    nome = request.form['nome']
    url = request.form['url']
    categoria = request.form['categoria']

    conn = conectar()

    conn.execute("""
        INSERT INTO links(nome,url,categoria)
        VALUES(?,?,?)
    """, (nome, url, categoria))

    conn.commit()
    conn.close()

    return redirect('/')

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):

    conn = conectar()

    if request.method == 'POST':

        nome = request.form['nome']
        url = request.form['url']
        categoria = request.form['categoria']

        conn.execute("""
            UPDATE links
            SET nome=?, url=?, categoria=?
            WHERE id=?
        """, (nome, url, categoria, id))

        conn.commit()
        conn.close()

        return redirect('/')

    link = conn.execute(
        'SELECT * FROM links WHERE id=?',
        (id,)
    ).fetchone()

    conn.close()

    return render_template('editar.html', link=link)

@app.route('/excluir/<int:id>')
def excluir(id):
    conn = conectar()

    conn.execute(
        'DELETE FROM links WHERE id=?',
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect('/')

if __name__ == '__main__':
    criar_tabela()
    app.run(debug=True)