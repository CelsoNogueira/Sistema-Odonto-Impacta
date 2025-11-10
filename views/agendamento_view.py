import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import datetime
from pymongo import MongoClient
from bson import ObjectId

class AgendamentoView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(fill="both", expand=True)

        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client["clinica"]
        self.collection = self.db["agendamentos"]

        form_frame = tk.LabelFrame(
            self,
            text="Agendamento",
            padx=15, pady=15,
            font=("Segoe UI", 10, "bold")
        )
        form_frame.pack(fill="x", padx=20, pady=15)
        form_frame.grid_columnconfigure(0, weight=1)
        form_frame.grid_columnconfigure(1, weight=3)

        tk.Label(form_frame, text="Paciente:", font=("Segoe UI", 10)).grid(row=0, column=0, sticky="e", padx=5, pady=8)
        self.combo_paciente = ttk.Combobox(form_frame, width=37, state="readonly")
        self.combo_paciente.grid(row=0, column=1, sticky="w", padx=5, pady=8)
        self.carregar_pacientes()

        tk.Label(form_frame, text="Dentista:", font=("Segoe UI", 10)).grid(row=1, column=0, sticky="e", padx=5, pady=8)
        self.combo_dentista = ttk.Combobox(form_frame, width=37, state="readonly")
        self.combo_dentista.grid(row=1, column=1, sticky="w", padx=5, pady=8)
        self.carregar_dentistas()

        tk.Label(form_frame, text="Data:", font=("Segoe UI", 10)).grid(row=2, column=0, sticky="e", padx=5, pady=8)
        self.entry_data = DateEntry(form_frame, width=37, date_pattern="dd/mm/yyyy")
        self.entry_data.set_date(datetime.date.today())
        self.entry_data.grid(row=2, column=1, sticky="w", padx=5, pady=8)

        tk.Label(form_frame, text="Procedimento:", font=("Segoe UI", 10)).grid(row=3, column=0, sticky="e", padx=5, pady=8)
        self.combo_procedimento = ttk.Combobox(form_frame, width=37, state="readonly")
        self.combo_procedimento.grid(row=3, column=1, sticky="w", padx=5, pady=8)
        self.combo_procedimento["values"] = ["Cirurgia", "Canal", "Restauração", "Clareamento"]
        self.combo_procedimento.bind("<<ComboboxSelected>>", self.verificar_procedimento)

        tk.Label(form_frame, text="Detalhes:", font=("Segoe UI", 10)).grid(row=4, column=0, sticky="e", padx=5, pady=8)
        self.entry_detalhes = ttk.Entry(form_frame, width=40)
        self.entry_detalhes.grid(row=4, column=1, sticky="w", padx=5, pady=8)

        tk.Label(form_frame, text="Preço:", font=("Segoe UI", 10)).grid(row=5, column=0, sticky="e", padx=5, pady=8)
        self.entry_preco = ttk.Entry(form_frame, width=40)
        self.entry_preco.grid(row=5, column=1, sticky="w", padx=5, pady=8)
        self.entry_preco.insert(0, "R$ ")
        self.entry_preco.bind("<KeyRelease>", self.formatar_preco)

        btn_frame = tk.Frame(form_frame)
        btn_frame.grid(row=6, column=0, columnspan=2, pady=15)
        for i in range(4):
            btn_frame.grid_columnconfigure(i, weight=1)

        ttk.Button(btn_frame, text="Cadastrar", command=self.cadastrar).grid(row=0, column=0, padx=10)
        ttk.Button(btn_frame, text="Editar", command=self.editar).grid(row=0, column=1, padx=10)
        ttk.Button(btn_frame, text="Excluir", command=self.excluir).grid(row=0, column=2, padx=10)
        ttk.Button(btn_frame, text="Atualizar", command=self.atualizar).grid(row=0, column=3, padx=10)

        list_frame = tk.LabelFrame(self, text="Agendamentos", padx=10, pady=10, font=("Segoe UI", 10, "bold"))
        list_frame.pack(fill="both", expand=True, padx=20, pady=15)

        self.tree = ttk.Treeview(
            list_frame,
            columns=("Paciente", "Dentista", "Data", "Procedimento", "Detalhes", "Preço"),
            show="headings",
            height=10
        )
        self.tree.pack(fill="both", expand=True)

        for col in ("Paciente", "Dentista", "Data", "Procedimento", "Detalhes", "Preço"):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)

        self.tree.bind("<<TreeviewSelect>>", self.preencher_campos)
        self.carregar_agendamentos()


    def formatar_preco(self, event):
        valor = self.entry_preco.get().replace("R$ ", "").replace(",", "").replace(".", "")
        if valor.isdigit():
            numero = int(valor)
            valor_formatado = f"{numero/100:,.2f}".replace(".", ",")
            self.entry_preco.delete(0, tk.END)
            self.entry_preco.insert(0, f"R$ {valor_formatado}")
        else:
            self.entry_preco.delete(0, tk.END)
            self.entry_preco.insert(0, "R$ ")
            self.entry_preco.icursor(tk.END)


    def carregar_pacientes(self):
        pacientes = self.db["pacientes"].find()
        self.combo_paciente["values"] = [p["nome"] for p in pacientes]

    def carregar_dentistas(self):
        dentistas = self.db["dentistas"].find()
        self.combo_dentista["values"] = [d["nome"] for d in dentistas]

    def verificar_procedimento(self, event=None):
        proc = self.combo_procedimento.get()
        if proc == "Clareamento":
            self.entry_detalhes.delete(0, tk.END)
            self.entry_detalhes.insert(0, "Consultório")
            self.entry_detalhes.config(state="readonly")
        else:
            self.entry_detalhes.config(state="normal")
            self.entry_detalhes.delete(0, tk.END)

    def validar_campos(self):
        return all([
            self.combo_paciente.get().strip(),
            self.combo_dentista.get().strip(),
            self.combo_procedimento.get().strip(),
            self.entry_preco.get().strip() != "R$ ",
            isinstance(self.entry_data.get_date(), datetime.date)
        ])

    def limpar_campos(self):
        self.combo_paciente.set("")
        self.combo_dentista.set("")
        self.combo_procedimento.set("")
        self.entry_detalhes.config(state="normal")
        self.entry_detalhes.delete(0, tk.END)
        self.entry_preco.delete(0, tk.END)
        self.entry_preco.insert(0, "R$ ")
        self.entry_data.set_date(datetime.date.today())

    def carregar_agendamentos(self):
        self.tree.delete(*self.tree.get_children())
        for ag in self.collection.find():
            self.tree.insert("", "end", iid=str(ag["_id"]), values=(
                ag["paciente"],
                ag["dentista"],
                ag["data"],
                ag["procedimento"],
                ag.get("detalhes", ""),
                ag["preco"]
            ))

    def preencher_campos(self, event):
        selecionado = self.tree.selection()
        if selecionado:
            ag = self.tree.item(selecionado[0], "values")
            self.combo_paciente.set(ag[0])
            self.combo_dentista.set(ag[1])
            self.entry_data.set_date(datetime.datetime.strptime(ag[2], "%d/%m/%Y").date())
            self.combo_procedimento.set(ag[3])
            self.entry_detalhes.config(state="normal")
            self.entry_detalhes.delete(0, tk.END)
            self.entry_detalhes.insert(0, ag[4])
            if ag[3] == "Clareamento":
                self.entry_detalhes.config(state="readonly")
            self.entry_preco.delete(0, tk.END)
            self.entry_preco.insert(0, ag[5])

    def cadastrar(self):
        if not self.validar_campos():
            messagebox.showwarning("Atenção", "Preencha todos os campos!")
            return
        self.collection.insert_one({
            "paciente": self.combo_paciente.get(),
            "dentista": self.combo_dentista.get(),
            "data": self.entry_data.get_date().strftime("%d/%m/%Y"),
            "procedimento": self.combo_procedimento.get(),
            "detalhes": self.entry_detalhes.get(),
            "preco": self.entry_preco.get()
        })
        self.carregar_agendamentos()
        self.limpar_campos()
        messagebox.showinfo("Sucesso", "Agendamento feito com sucesso!")

    def editar(self):
        selecionado = self.tree.selection()
        if not selecionado:
            messagebox.showwarning("Atenção", "Selecione um agendamento para editar!")
            return
        ag_id = selecionado[0]
        self.collection.update_one(
            {"_id": ObjectId(ag_id)},
            {"$set": {
                "paciente": self.combo_paciente.get(),
                "dentista": self.combo_dentista.get(),
                "data": self.entry_data.get_date().strftime("%d/%m/%Y"),
                "procedimento": self.combo_procedimento.get(),
                "detalhes": self.entry_detalhes.get(),
                "preco": self.entry_preco.get()
            }}
        )
        self.atualizar()
        self.limpar_campos()
        messagebox.showinfo("Sucesso", "Agendamento atualizado com sucesso!")

    def excluir(self):
        selecionado = self.tree.selection()
        if not selecionado:
            messagebox.showwarning("Atenção", "Selecione um agendamento para excluir!")
            return
        ag_id = selecionado[0]
        self.collection.delete_one({"_id": ObjectId(ag_id)})
        self.atualizar()
        self.limpar_campos()
        messagebox.showinfo("Sucesso", "Agendamento excluído com sucesso!")

    def atualizar(self):
        self.carregar_pacientes()
        self.carregar_dentistas()
        self.carregar_agendamentos()
