import tkinter as tk
from tkinter import ttk, messagebox
from bson import ObjectId
from datetime import datetime
from controllers.paciente_controller import (
    cadastrar_paciente,
    listar_pacientes,
    atualizar_paciente,
    excluir_paciente
)


class PacienteView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(fill="both", expand=True)

        form_frame = tk.LabelFrame(
            self,
            text="Cadastro de Paciente",
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

        tk.Label(form_frame, text="Data de Nascimento:", font=("Segoe UI", 10)).grid(
            row=3, column=0, padx=5, pady=8, sticky="e"
        )
        self.entry_data_nasc = ttk.Entry(form_frame, width=40, justify="center")
        self.entry_data_nasc.grid(row=3, column=1, padx=5, pady=8, sticky="w")
        self.entry_data_nasc.bind("<KeyRelease>", self.formatar_data)

        btn_frame = tk.Frame(form_frame)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=15)
        for i in range(3):
            btn_frame.grid_columnconfigure(i, weight=1)

        ttk.Button(btn_frame, text="Cadastrar", command=self.cadastrar).grid(row=0, column=0, padx=10)
        ttk.Button(btn_frame, text="Editar", command=self.editar).grid(row=0, column=1, padx=10)
        ttk.Button(btn_frame, text="Excluir", command=self.excluir).grid(row=0, column=2, padx=10)

        list_frame = tk.LabelFrame(
            self,
            text="Pacientes Cadastrados",
            padx=10,
            pady=10,
            font=("Segoe UI", 10, "bold")
        )
        list_frame.pack(fill="both", expand=True, padx=20, pady=15)

        self.tree = ttk.Treeview(
            list_frame,
            columns=("Nome", "Telefone", "Email", "Data Nasc"),
            show="headings",
            height=10
        )
        self.tree.pack(fill="both", expand=True)

        for col in ("Nome", "Telefone", "Email", "Data Nasc"):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)

        self.tree.bind("<<TreeviewSelect>>", self.preencher_campos)
        self.carregar_pacientes()

    def validar_campos(self):
        data_texto = self.entry_data_nasc.get().strip()
        if not all([
            self.entry_nome.get().strip(),
            self.entry_telefone.get().strip(),
            self.entry_email.get().strip(),
            data_texto
        ]):
            return False

        try:
            data = datetime.strptime(data_texto, "%d/%m/%Y")
            if data > datetime.now():
                return False
        except ValueError:
            return False
        return True

    def limpar_campos(self):
        self.entry_nome.delete(0, tk.END)
        self.entry_telefone.delete(0, tk.END)
        self.entry_email.delete(0, tk.END)
        self.entry_data_nasc.delete(0, tk.END)

    def carregar_pacientes(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        pacientes = listar_pacientes()
        for paciente in pacientes:
            self.tree.insert(
                "",
                "end",
                iid=paciente["_id"],
                values=(paciente["nome"], paciente["telefone"], paciente["email"], paciente["data_nasc"])
            )

    def formatar_data(self, event):
        texto = self.entry_data_nasc.get()
        numeros = ''.join(filter(str.isdigit, texto))
        numeros = numeros[:8]
        nova_data = ""
        for i, c in enumerate(numeros):
            nova_data += c
            if i == 1 or i == 3:
                nova_data += "/"
        self.entry_data_nasc.delete(0, tk.END)
        self.entry_data_nasc.insert(0, nova_data)

    def cadastrar(self):
        if not self.validar_campos():
            messagebox.showwarning("Atenção", "Preencha todos os campos corretamente! Data deve ser válida e antes do ano atual.")
            return
        cadastrar_paciente({
            "nome": self.entry_nome.get(),
            "telefone": self.entry_telefone.get(),
            "email": self.entry_email.get(),
            "data_nasc": self.entry_data_nasc.get()
        })
        self.carregar_pacientes()
        self.limpar_campos()
        messagebox.showinfo("Sucesso", "Paciente cadastrado com sucesso!")

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
            self.entry_data_nasc.delete(0, tk.END)
            self.entry_data_nasc.insert(0, valores[3])

    def editar(self):
        selecionado = self.tree.selection()
        if not selecionado:
            messagebox.showwarning("Atenção", "Selecione um paciente para editar!")
            return
        if not self.validar_campos():
            messagebox.showwarning("Atenção", "Preencha todos os campos corretamente!")
            return
        atualizar_paciente(
            {"_id": ObjectId(selecionado[0])},
            {
                "nome": self.entry_nome.get(),
                "telefone": self.entry_telefone.get(),
                "email": self.entry_email.get(),
                "data_nasc": self.entry_data_nasc.get()
            }
        )
        self.carregar_pacientes()
        self.limpar_campos()
        messagebox.showinfo("Sucesso", "Paciente atualizado com sucesso!")

    def excluir(self):
        selecionado = self.tree.selection()
        if not selecionado:
            messagebox.showwarning("Atenção", "Selecione um paciente para excluir!")
            return
        excluir_paciente({"_id": ObjectId(selecionado[0])})
        self.carregar_pacientes()
        self.limpar_campos()
        messagebox.showinfo("Sucesso", "Paciente excluído com sucesso!")
