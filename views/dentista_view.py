import tkinter as tk
from tkinter import ttk, messagebox
from bson import ObjectId
from controllers.dentista_controller import (
    cadastrar_dentista, listar_dentistas,
    atualizar_dentista, excluir_dentista
)

class DentistaView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(fill="both", expand=True)

        # Frame de formulário
        form_frame = tk.LabelFrame(
            self,
            text="Cadastro de Dentista",
            padx=15, pady=15,
            font=("Segoe UI", 10, "bold")
        )
        form_frame.pack(fill="x", padx=20, pady=15)

        form_frame.grid_columnconfigure(0, weight=1)
        form_frame.grid_columnconfigure(1, weight=3)

        # Campos
        self.entry_nome = self._criar_campo(form_frame, "Nome:", 0)
        self.entry_telefone = self._criar_campo(form_frame, "Telefone:", 1)
        self.entry_email = self._criar_campo(form_frame, "Email:", 2)
        self.entry_especialidade = self._criar_campo(form_frame, "Especialidade:", 3)

        # Botões
        btn_frame = tk.Frame(form_frame)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=15)
        for i in range(3):
            btn_frame.grid_columnconfigure(i, weight=1)

        ttk.Button(btn_frame, text="Cadastrar", command=self.cadastrar).grid(row=0, column=0, padx=10)
        ttk.Button(btn_frame, text="Editar", command=self.editar).grid(row=0, column=1, padx=10)
        ttk.Button(btn_frame, text="Excluir", command=self.excluir).grid(row=0, column=2, padx=10)

        # Tabela
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

    def _criar_campo(self, frame, label, row):
        tk.Label(frame, text=label, font=("Segoe UI", 10)).grid(
            row=row, column=0, padx=5, pady=8, sticky="e"
        )
        entry = ttk.Entry(frame, width=40, justify="center")
        entry.grid(row=row, column=1, padx=5, pady=8, sticky="w")
        return entry

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
        for dentista in listar_dentistas():
            self.tree.insert(
                "", "end",
                iid=str(dentista["_id"]),
                values=(dentista["nome"], dentista["telefone"], dentista["email"], dentista["especialidade"])
            )

    def cadastrar(self):
        if not self.validar_campos():
            messagebox.showwarning("Atenção", "Preencha todos os campos!")
            return
        cadastrar_dentista({
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
        atualizar_dentista(
            selecionado[0],
            {
                "nome": self.entry_nome.get(),
                "telefone": self.entry_telefone.get(),
                "email": self.entry_email.get(),
                "especialidade": self.entry_especialidade.get()
            }
        )
        self.carregar_dentistas()
        self.limpar_campos()
        messagebox.showinfo("Sucesso", "Dentista atualizado com sucesso!")

    def excluir(self):
        selecionado = self.tree.selection()
        if not selecionado:
            messagebox.showwarning("Atenção", "Selecione um dentista para excluir!")
            return
        excluir_dentista(selecionado[0])
        self.carregar_dentistas()
        self.limpar_campos()
        messagebox.showinfo("Sucesso", "Dentista excluído com sucesso!")
