import tkinter as tk
from tkinter import ttk, messagebox
import random, string
from controllers.usuario_controller import UsuarioController

class usuarioView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(fill="both", expand=True, padx=20, pady=20)

        self.controller = UsuarioController()

        form_frame = tk.LabelFrame(
            self,
            text="Gerenciamento de Usuários",
            padx=15, pady=15,
            font=("Segoe UI", 10, "bold")
        )
        form_frame.pack(fill="x", pady=10)

        form_frame.grid_columnconfigure(0, weight=1)
        form_frame.grid_columnconfigure(1, weight=3)

        tk.Label(form_frame, text="Nome:").grid(row=0, column=0, padx=5, pady=8, sticky="e")
        self.entry_nome = ttk.Entry(form_frame, width=40, justify="center")
        self.entry_nome.grid(row=0, column=1, padx=5, pady=8, sticky="w")

        tk.Label(form_frame, text="Email:").grid(row=1, column=0, padx=5, pady=8, sticky="e")
        self.entry_email = ttk.Entry(form_frame, width=40, justify="center")
        self.entry_email.grid(row=1, column=1, padx=5, pady=8, sticky="w")

        tk.Label(form_frame, text="Senha:").grid(row=2, column=0, padx=5, pady=8, sticky="e")
        self.entry_senha = ttk.Entry(form_frame, width=40, justify="center", show="*")
        self.entry_senha.grid(row=2, column=1, padx=5, pady=8, sticky="w")

        btn_frame = tk.Frame(form_frame)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=15)
        for i in range(2):
            btn_frame.grid_columnconfigure(i, weight=1)

        ttk.Button(btn_frame, text="Cadastrar", command=self.cadastrar_usuario).grid(row=0, column=0, padx=10)
        ttk.Button(btn_frame, text="Redefinir Senha", command=self.redefinir_senha).grid(row=0, column=1, padx=10)

        list_frame = tk.LabelFrame(
            self,
            text="Usuários Cadastrados",
            padx=10, pady=10,
            font=("Segoe UI", 10, "bold")
        )
        list_frame.pack(fill="both", expand=True, pady=10)

        self.tree = ttk.Treeview(list_frame, columns=("Nome", "Email", "Senha"), show="headings", height=8)
        self.tree.pack(fill="both", expand=True)

        for col in ("Nome", "Email", "Senha"):
            self.tree.heading(col, text=col)

        self.carregar_usuarios()

    def carregar_usuarios(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for user in self.controller.listar_usuarios():
            self.tree.insert("", "end", values=(user["nome"], user["email"], user.get("senha", "—")))

    def cadastrar_usuario(self):
        nome = self.entry_nome.get().strip()
        email = self.entry_email.get().strip()
        senha = self.entry_senha.get().strip()
        if not nome or not email or not senha:
            messagebox.showwarning("Atenção", "Preencha todos os campos!")
            return
        sucesso, msg = self.controller.cadastrar_usuario(nome, email, senha)
        if sucesso:
            messagebox.showinfo("Sucesso", msg)
            self.entry_nome.delete(0, tk.END)
            self.entry_email.delete(0, tk.END)
            self.entry_senha.delete(0, tk.END)
            self.carregar_usuarios()
        else:
            messagebox.showerror("Erro", msg)

    def redefinir_senha(self):
        email = self.entry_email.get().strip()
        if not email:
            messagebox.showwarning("Atenção", "Digite o email para redefinir a senha!")
            return
        temp_senha = "".join(random.choices("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=8))
        sucesso, msg = self.controller.redefinir_senha(email, temp_senha)
        if sucesso:
            messagebox.showinfo("Senha redefinida", f"{msg}\nNova senha temporária: {temp_senha}")
            self.carregar_usuarios()
        else:
            messagebox.showerror("Erro", msg)
