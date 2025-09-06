import tkinter as tk
from tkinter import ttk, messagebox
from pymongo import MongoClient
from bson import ObjectId


class DentistaView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(fill="both", expand=True)

        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client["clinica"]
        self.collection = self.db["dentistas"]

        form_frame = tk.LabelFrame(
            self,
            text="Cadastro de Dentista",
            padx=15, pady=15,
            font=("Segoe UI", 10, "bold")
        )
        form_frame.pack(fill="x", padx=20, pady=15)

        form_frame.grid_columnconfigure(0, weight=1)
        form_frame.grid_columnconfigure(1, weight=3)

        tk.Label(form_frame, text="Nome:", font=("Segoe UI", 10)).grid(
            row=0, column=0, padx=5, pady=8, sticky="e"
        )
        self.entry_nome = ttk.Entry(form_frame, width=40, justify="center")
        self.entry_nome.grid(row=0, column=1, padx=5, pady=8, sticky="w")

        tk.Label(form_frame, text="Telefone:", font=("Segoe UI", 10)).grid(
            row=1, column=0, padx=5, pady=8, sticky="e"
        )
        self.entry_telefone = ttk.Entry(form_frame, width=40, justify="center")
        self.entry_telefone.grid(row=1, column=1, padx=5, pady=8, sticky="w")

        tk.Label(form_frame, text="Email:", font=("Segoe UI", 10)).grid(
            row=2, column=0, padx=5, pady=8, sticky="e"
        )
        self.entry_email = ttk.Entry(form_frame, width=40, justify="center")
        self.entry_email.grid(row=2, column=1, padx=5, pady=8, sticky="w")

        tk.Label(form_frame, text="Especialidade:", font=("Segoe UI", 10)).grid(
            row=3, column=0, padx=5, pady=8, sticky="e"
        )
        self.entry_especialidade = ttk.Entry(form_frame, width=40, justify="center")
        self.entry_especialidade.grid(row=3, column=1, padx=5, pady=8, sticky="w")

        btn_frame = tk.Frame(form_frame)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=15)
        for i in range(3):
            btn_frame.grid_columnconfigure(i, weight=1)

        ttk.Button(btn_frame, text="Cadastrar", command=self.cadastrar).grid(row=0, column=0, padx=10)
        ttk.Button(btn_frame, text="Editar", command=self.editar).grid(row=0, column=1, padx=10)
        ttk.Button(btn_frame, text="Excluir", command=self.excluir).grid(row=0, column=2, padx=10)

        list_frame = tk.LabelFrame(
            self,
            text="Dentistas Cadastrados",
            padx=10, pady=10,
            font=("Segoe UI", 10, "bold")
        )
        list_frame.pack(fill="both", expand=True, padx=20, pady=15)

        self.tree = ttk.Treeview(
            list_frame,
            columns=("Nome", "Telefone", "Email", "Especialidade"),
            show="headings",
            height=10
        )
        self.tree.pack(fill="both", expand=True)

        for col in ("Nome", "Telefone", "Email", "Especialidade"):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)

        self.tree.bind("<<TreeviewSelect>>", self.preencher_campos)

        self.carregar_dentistas()

    def validar_campos(self):
        return all([
            self.entry_nome.get().strip(),
            self.entry_telefone.get().strip(),
            self.entry_email.get().strip(),
            self.entry_especialidade.get().strip()
        ])

    def limpar_campos(self):
        self.entry_nome.delete(0, tk.END)
        self.entry_telefone.delete(0, tk.END)
        self.entry_email.delete(0, tk.END)
        self.entry_especialidade.delete(0, tk.END)

    def carregar_dentistas(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for dentista in self.collection.find():
            self.tree.insert(
                "", "end",
                iid=str(dentista["_id"]),
                values=(dentista["nome"], dentista["telefone"], dentista["email"], dentista["especialidade"])
            )

    def cadastrar(self):
        if not self.validar_campos():
            messagebox.showwarning("Atenção", "Preencha todos os campos!")
            return
        self.collection.insert_one({
            "nome": self.entry_nome.get(),
            "telefone": self.entry_telefone.get(),
            "email": self.entry_email.get(),
            "especialidade": self.entry_especialidade.get()
        })
        self.carregar_dentistas()
        self.limpar_campos()
        messagebox.showinfo("Sucesso", "Dentista cadastrado com sucesso!")

    def preencher_campos(self, event):
        selecionado = self.tree.selection()
        if selecionado:
            valores = self.tree.item(selecionado[0], "values")
            self.entry_nome.delete(0, tk.END)
            self.entry_nome.insert(0, valores[0])
            self.entry_telefone.delete(0, tk.END)
            self.entry_telefone.insert(0, valores[1])
            self.entry_email.delete(0, tk.END)
            self.entry_email.insert(0, valores[2])
            self.entry_especialidade.delete(0, tk.END)
            self.entry_especialidade.insert(0, valores[3])

    def editar(self):
        selecionado = self.tree.selection()
        if not selecionado:
            messagebox.showwarning("Atenção", "Selecione um dentista para editar!")
            return
        if not self.validar_campos():
            messagebox.showwarning("Atenção", "Preencha todos os campos!")
            return
        self.collection.update_one(
            {"_id": ObjectId(selecionado[0])},
            {"$set": {
                "nome": self.entry_nome.get(),
                "telefone": self.entry_telefone.get(),
                "email": self.entry_email.get(),
                "especialidade": self.entry_especialidade.get()
            }}
        )
        self.carregar_dentistas()
        self.limpar_campos()
        messagebox.showinfo("Sucesso", "Dentista atualizado com sucesso!")

    def excluir(self):
        selecionado = self.tree.selection()
        if not selecionado:
            messagebox.showwarning("Atenção", "Selecione um dentista para excluir!")
            return
        self.collection.delete_one({"_id": ObjectId(selecionado[0])})
        self.carregar_dentistas()
        self.limpar_campos()
        messagebox.showinfo("Sucesso", "Dentista excluído com sucesso!")
