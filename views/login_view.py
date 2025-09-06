import tkinter as tk
from tkinter import ttk, messagebox
import random, string
from controllers.usuario_controller import UsuarioController

class LoginView(tk.Frame):
    def __init__(self, parent, callback_login_sucesso):
        super().__init__(parent)
        self.callback_login_sucesso = callback_login_sucesso
        self.pack(fill="both", expand=True, padx=20, pady=20)

        self.controller = UsuarioController()

        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)

        frame_login = ttk.Frame(notebook)
        notebook.add(frame_login, text="Login")

        tk.Label(frame_login, text="Email:").pack(pady=5)
        self.entry_email_login = ttk.Entry(frame_login, width=30)
        self.entry_email_login.pack()

        tk.Label(frame_login, text="Senha:").pack(pady=5)
        self.entry_senha_login = ttk.Entry(frame_login, show="*", width=30)
        self.entry_senha_login.pack()

        ttk.Button(frame_login, text="Entrar", command=self.login).pack(pady=15)
        ttk.Button(frame_login, text="Esqueci a senha", command=self.esqueci_senha).pack(pady=5)

        frame_cadastro = ttk.Frame(notebook)
        notebook.add(frame_cadastro, text="Cadastro")

        tk.Label(frame_cadastro, text="Nome:").pack(pady=5)
        self.entry_nome_cadastro = ttk.Entry(frame_cadastro, width=30)
        self.entry_nome_cadastro.pack()

        tk.Label(frame_cadastro, text="Email:").pack(pady=5)
        self.entry_email_cadastro = ttk.Entry(frame_cadastro, width=30)
        self.entry_email_cadastro.pack()

        tk.Label(frame_cadastro, text="Senha:").pack(pady=5)
        self.entry_senha_cadastro = ttk.Entry(frame_cadastro, show="*", width=30)
        self.entry_senha_cadastro.pack()

        ttk.Button(frame_cadastro, text="Cadastrar", command=self.cadastrar).pack(pady=15)

    def login(self):
        email = self.entry_email_login.get().strip()
        senha = self.entry_senha_login.get().strip()
        if not email or not senha:
            messagebox.showwarning("Atenção", "Preencha todos os campos!")
            return

        sucesso, resultado = self.controller.autenticar_usuario(email, senha)
        if sucesso:
            messagebox.showinfo("Bem-vindo", f"Olá, {resultado['nome']}!")
            self.callback_login_sucesso()
        else:
            messagebox.showerror("Erro", resultado)

    def cadastrar(self):
        nome = self.entry_nome_cadastro.get().strip()
        email = self.entry_email_cadastro.get().strip()
        senha = self.entry_senha_cadastro.get().strip()
        if not nome or not email or not senha:
            messagebox.showwarning("Atenção", "Preencha todos os campos!")
            return

        sucesso, msg = self.controller.cadastrar_usuario(nome, email, senha)
        if sucesso:
            messagebox.showinfo("Sucesso", msg)
            self.entry_nome_cadastro.delete(0, tk.END)
            self.entry_email_cadastro.delete(0, tk.END)
            self.entry_senha_cadastro.delete(0, tk.END)
        else:
            messagebox.showerror("Erro", msg)

    def esqueci_senha(self):
        email = self.entry_email_login.get().strip()
        if not email:
            messagebox.showwarning("Atenção", "Digite seu email para redefinir a senha!")
            return
        temp_senha = "".join(random.choices("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=8))
        sucesso, msg = self.controller.redefinir_senha(email, temp_senha)
        if sucesso:
            messagebox.showinfo("Senha redefinida", f"{msg}\nNova senha temporária: {temp_senha}")
        else:
            messagebox.showerror("Erro", msg)
