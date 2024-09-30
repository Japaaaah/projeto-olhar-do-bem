import sqlite3
from tkinter import Tk, Label, Entry, Button, Listbox, END, messagebox, Toplevel
import os 

if os.path.exists('doacoes.db'):
    os.remove('doacoes.db')
if os.path.exists('itens_ja_doados.db'):
    os.remove('itens_ja_doados.db')
if os.path.exists('necessidades.db'):
    os.remove('necessidades.db')

conn_doacoes = sqlite3.connect('doacoes.db')
cursor_doacoes = conn_doacoes.cursor()

cursor_doacoes.execute('''
CREATE TABLE IF NOT EXISTS doacoes (
    id INTEGER PRIMARY KEY,
    tipo TEXT NOT NULL,
    itens TEXT NOT NULL,
    doador TEXT NOT NULL
)
''')
conn_doacoes.commit()

conn_ja_doados = sqlite3.connect('itens_ja_doados.db')
cursor_ja_doados = conn_ja_doados.cursor()

cursor_ja_doados.execute('''
CREATE TABLE IF NOT EXISTS itens_removidos (
    id INTEGER PRIMARY KEY,
    tipo TEXT NOT NULL,
    itens TEXT NOT NULL,
    doador TEXT NOT NULL
)
''')
conn_ja_doados.commit()

conn_necessidades = sqlite3.connect('necessidades.db')
cursor_necessidades = conn_necessidades.cursor()

cursor_necessidades.execute('''
CREATE TABLE IF NOT EXISTS necessidades (
    id INTEGER PRIMARY KEY,
    descricao TEXT NOT NULL
)
''')
conn_necessidades.commit()

def adicionar_doacao():
    tipo = entry_tipo.get()
    itens = entry_itens.get()
    doador = entry_doador.get()
    
    if tipo and itens and doador:
        cursor_doacoes.execute('INSERT INTO doacoes (tipo, itens, doador) VALUES (?, ?, ?)', (tipo, itens, doador))
        conn_doacoes.commit()
        messagebox.showinfo("Sucesso", "Doação adicionada com sucesso!")
        entry_tipo.delete(0, END)
        entry_itens.delete(0, END)
        entry_doador.delete(0, END)
        listar_doacoes()
    else:
        messagebox.showwarning("Atenção", "Por favor, preencha todos os campos.")

def listar_doacoes():
    listbox.delete(0, END)
    cursor_doacoes.execute('SELECT * FROM doacoes')
    for row in cursor_doacoes.fetchall():
        listbox.insert(END, f"ID: {row[0]}, Tipo: {row[1]}, Itens: {row[2]}, Doador: {row[3]}")

def remover_doacao():
    selected_item = listbox.curselection()
    if selected_item:
        doacao_id = listbox.get(selected_item).split(",")[0].split(":")[1].strip()
        
        cursor_doacoes.execute('SELECT * FROM doacoes WHERE id = ?', (doacao_id,))
        doacao = cursor_doacoes.fetchone()
        
        cursor_ja_doados.execute('INSERT INTO itens_removidos (tipo, itens, doador) VALUES (?, ?, ?)', (doacao[1], doacao[2], doacao[3]))
        conn_ja_doados.commit()
        
        cursor_doacoes.execute('DELETE FROM doacoes WHERE id = ?', (doacao_id,))
        conn_doacoes.commit()
        messagebox.showinfo("Sucesso", "Item de doação removido e registrado como doado!")
        listar_doacoes()
    else:
        messagebox.showwarning("Atenção", "Selecione um item de doação para remover.")

def visualizar_itens_ja_doados():
    top = Toplevel()
    top.title("Itens Já Doados")
    
    global listbox_ja_doados 
    listbox_ja_doados = Listbox(top, width=70)
    listbox_ja_doados.pack()
    
    cursor_ja_doados.execute('SELECT * FROM itens_removidos')
    for row in cursor_ja_doados.fetchall():
        listbox_ja_doados.insert(END, f"ID: {row[0]}, Tipo: {row[1]}, Itens: {row[2]}, Doador: {row[3]}")
    
    Button(top, text="Remover Permanentemente", command=remover_item_permanentemente).pack()
    Button(top, text="Fechar", command=top.destroy).pack()

def remover_item_permanentemente():
    global listbox_ja_doados
    if listbox_ja_doados:
        selected_item = listbox_ja_doados.curselection()
        if selected_item:
            doacao_id = listbox_ja_doados.get(selected_item).split(",")[0].split(":")[1].strip()
            
            cursor_ja_doados.execute('DELETE FROM itens_removidos WHERE id = ?', (doacao_id,))
            conn_ja_doados.commit()
            
            listbox_ja_doados.delete(selected_item)
            messagebox.showinfo("Sucesso", "Item removido permanentemente!")
        else:
            messagebox.showwarning("Atenção", "Selecione um item para remover permanentemente.")
    else:
        messagebox.showwarning("Atenção", "Nenhum item disponível para remover.")

def adicionar_necessidade():
    descricao = entry_necessidade.get()
    
    if descricao:
        cursor_necessidades.execute('INSERT INTO necessidades (descricao) VALUES (?)', (descricao,))
        conn_necessidades.commit()
        messagebox.showinfo("Sucesso", "Necessidade adicionada com sucesso!")
        entry_necessidade.delete(0, END)
        listar_necessidades()
    else:
        messagebox.showwarning("Atenção", "Por favor, preencha o campo de necessidade.")

def listar_necessidades():
    listbox_necessidades.delete(0, END)
    cursor_necessidades.execute('SELECT * FROM necessidades')
    for row in cursor_necessidades.fetchall():
        listbox_necessidades.insert(END, f"ID: {row[0]}, Descrição: {row[1]}")

def remover_necessidade():
    selected_item = listbox_necessidades.curselection()
    if selected_item:
        necessidade_id = listbox_necessidades.get(selected_item).split(",")[0].split(":")[1].strip()
        cursor_necessidades.execute('DELETE FROM necessidades WHERE id = ?', (necessidade_id,))
        conn_necessidades.commit()
        messagebox.showinfo("Sucesso", "Necessidade removida com sucesso!")
        listar_necessidades()
    else:
        messagebox.showwarning("Atenção", "Selecione uma necessidade para remover.")

def visualizar_necessidades():
    top = Toplevel()
    top.title("Lista de Necessidades")
    
    global listbox_necessidades
    listbox_necessidades = Listbox(top, width=70)
    listbox_necessidades.pack()
    
    listar_necessidades()
    
    Label(top, text="Adicionar Necessidade:").pack()
    global entry_necessidade
    entry_necessidade = Entry(top)
    entry_necessidade.pack()
    
    Button(top, text="Adicionar", command=adicionar_necessidade).pack()
    Button(top, text="Remover Necessidade", command=remover_necessidade).pack()
    Button(top, text="Fechar", command=top.destroy).pack()

root = Tk()
root.title("Gerenciador de Doações")

Label(root, text="Tipo de Doação:").pack()
entry_tipo = Entry(root)
entry_tipo.pack()

Label(root, text="Quantidade de itens:").pack()
entry_itens = Entry(root)
entry_itens.pack()

Label(root, text="Doador:").pack()
entry_doador = Entry(root)
entry_doador.pack()

Button(root, text="Adicionar Doação", command=adicionar_doacao).pack()

listbox = Listbox(root, width=70)
listbox.pack()

Button(root, text="Adicionar a doado", command=remover_doacao).pack()
Button(root, text="Visualizar itens doados", command=visualizar_itens_ja_doados).pack()
Button(root, text="Excluir doação", command=remover_item_permanentemente).pack()  
Button(root, text="Visualizar Necessidades", command=visualizar_necessidades).pack()

listar_doacoes()

root.mainloop()

conn_doacoes.close()
conn_ja_doados.close()
conn_necessidades.close()
