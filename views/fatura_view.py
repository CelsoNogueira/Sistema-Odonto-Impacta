import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from pymongo import MongoClient
from bson import ObjectId
from fpdf import FPDF
from datetime import datetime

class FaturaView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(fill="both", expand=True)

        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client["clinica"]
        self.collection = self.db["faturas"]

        form_frame = tk.LabelFrame(
            self,
            text="Registro de Fatura / Pagamento",
            padx=15, pady=15,
            font=("Segoe UI", 10, "bold")
        )
        form_frame.pack(fill="x", padx=20, pady=15)

        form_frame.grid_columnconfigure(0, weight=1)
        form_frame.grid_columnconfigure(1, weight=3)

        tk.Label(form_frame, text="Paciente:", font=("Segoe UI", 10)).grid(row=0, column=0, padx=5, pady=8, sticky="e")
        self.combo_paciente = ttk.Combobox(form_frame, width=37, state="readonly")
        self.combo_paciente.grid(row=0, column=1, padx=5, pady=8, sticky="w")
        self.carregar_pacientes()
        self.combo_paciente.bind("<<ComboboxSelected>>", self.puxar_dados_paciente)

        tk.Label(form_frame, text="Dentista:", font=("Segoe UI", 10)).grid(row=1, column=0, padx=5, pady=8, sticky="e")
        self.entry_dentista = ttk.Entry(form_frame, width=40, justify="center")
        self.entry_dentista.grid(row=1, column=1, padx=5, pady=8, sticky="w")

        tk.Label(form_frame, text="Procedimento:", font=("Segoe UI", 10)).grid(row=2, column=0, padx=5, pady=8, sticky="e")
        self.entry_procedimento = ttk.Entry(form_frame, width=40, justify="center")
        self.entry_procedimento.grid(row=2, column=1, padx=5, pady=8, sticky="w")

        tk.Label(form_frame, text="Valor (R$):", font=("Segoe UI", 10)).grid(row=3, column=0, padx=5, pady=8, sticky="e")
        self.entry_valor = ttk.Entry(form_frame, width=40)
        self.entry_valor.insert(0, "R$ ")
        self.entry_valor.grid(row=3, column=1, padx=5, pady=8, sticky="w")

        btn_frame = tk.Frame(form_frame)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=15)
        for i in range(4):
            btn_frame.grid_columnconfigure(i, weight=1)

        ttk.Button(btn_frame, text="Gerar Fatura", command=self.cadastrar).grid(row=0, column=0, padx=10)
        ttk.Button(btn_frame, text="Editar Fatura", command=self.editar).grid(row=0, column=1, padx=10)
        ttk.Button(btn_frame, text="Imprimir Fatura", command=self.imprimir_fatura).grid(row=0, column=2, padx=10)
        ttk.Button(btn_frame, text="Atualizar", command=self.atualizar).grid(row=0, column=3, padx=10)

        list_frame = tk.LabelFrame(self, text="Faturas Registradas", padx=10, pady=10, font=("Segoe UI", 10, "bold"))
        list_frame.pack(fill="both", expand=True, padx=20, pady=15)

        self.tree = ttk.Treeview(list_frame, columns=("Paciente", "Dentista", "Procedimento", "Valor"), show="headings", height=10)
        self.tree.pack(fill="both", expand=True)

        for col in ("Paciente", "Dentista", "Procedimento", "Valor"):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)

        self.tree.bind("<<TreeviewSelect>>", self.preencher_campos)
        self.carregar_faturas()

    def carregar_pacientes(self):
        pacientes = self.db["pacientes"].find()
        self.combo_paciente["values"] = [p["nome"] for p in pacientes]

    def puxar_dados_paciente(self, event=None):
        paciente = self.combo_paciente.get()
        agendamento = self.db["agendamentos"].find_one({"paciente": paciente}, sort=[("_id", -1)])
        if agendamento:
            self.entry_dentista.delete(0, tk.END)
            self.entry_dentista.insert(0, agendamento["dentista"])
            self.entry_procedimento.delete(0, tk.END)
            self.entry_procedimento.insert(0, agendamento["procedimento"])
            self.entry_valor.delete(0, tk.END)
            self.entry_valor.insert(0, agendamento["preco"])

    def validar_campos(self):
        return all([
            self.combo_paciente.get().strip(),
            self.entry_dentista.get().strip(),
            self.entry_procedimento.get().strip(),
            self.entry_valor.get().strip()
        ])

    def limpar_campos(self):
        self.combo_paciente.set("")
        self.entry_dentista.delete(0, tk.END)
        self.entry_procedimento.delete(0, tk.END)
        self.entry_valor.delete(0, tk.END)
        self.entry_valor.insert(0, "R$ ")

    def carregar_faturas(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for fatura in self.collection.find():
            self.tree.insert("", "end", iid=str(fatura["_id"]),
                             values=(fatura["paciente"], fatura["dentista"], fatura["procedimento"], fatura["valor"]))

    def cadastrar(self):
        if not self.validar_campos():
            messagebox.showwarning("Atenção", "Preencha todos os campos!")
            return
        self.collection.insert_one({
            "paciente": self.combo_paciente.get(),
            "dentista": self.entry_dentista.get(),
            "procedimento": self.entry_procedimento.get(),
            "valor": self.entry_valor.get()
        })
        self.atualizar()
        self.limpar_campos()
        messagebox.showinfo("Sucesso", "Fatura gerada com sucesso!")

    def preencher_campos(self, event):
        selecionado = self.tree.selection()
        if selecionado:
            valores = self.tree.item(selecionado[0], "values")
            self.combo_paciente.set(valores[0])
            self.entry_dentista.delete(0, tk.END)
            self.entry_dentista.insert(0, valores[1])
            self.entry_procedimento.delete(0, tk.END)
            self.entry_procedimento.insert(0, valores[2])
            self.entry_valor.delete(0, tk.END)
            self.entry_valor.insert(0, valores[3])

    def editar(self):
        selecionado = self.tree.selection()
        if not selecionado:
            messagebox.showwarning("Atenção", "Selecione uma fatura para editar!")
            return
        if not self.validar_campos():
            messagebox.showwarning("Atenção", "Preencha todos os campos!")
            return
        self.collection.update_one(
            {"_id": ObjectId(selecionado[0])},
            {"$set": {
                "paciente": self.combo_paciente.get(),
                "dentista": self.entry_dentista.get(),
                "procedimento": self.entry_procedimento.get(),
                "valor": self.entry_valor.get()
            }}
        )
        self.atualizar()
        self.limpar_campos()
        messagebox.showinfo("Sucesso", "Fatura atualizada com sucesso!")

    def atualizar(self):
        self.carregar_pacientes()
        self.carregar_faturas()

    def imprimir_fatura(self):
        selecionado = self.tree.selection()
        if not selecionado:
            messagebox.showwarning("Atenção", "Selecione uma fatura para imprimir!")
            return
        fatura = self.collection.find_one({"_id": ObjectId(selecionado[0])})
        if not fatura:
            messagebox.showerror("Erro", "Fatura não encontrada!")
            return

        arquivo = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("Arquivos PDF", "*.pdf")],
            title="Salvar fatura como",
            initialfile=f"fatura_{self.combo_paciente.get()}.pdf"
        )
        if not arquivo:
            return

        pdf = FPDF()
        pdf.add_page()


        try:
            pdf.image("assets/logo.png", x=10, y=8, w=30)
        except:
            pass 

        pdf.set_font("Arial", "B", 18)
        pdf.set_text_color(40, 40, 120)
        pdf.cell(0, 12, "Clínica Odontológica Impacta", ln=True, align="C")
        pdf.set_font("Arial", "I", 12)
        pdf.set_text_color(100, 100, 100)
        pdf.cell(0, 10, "Fatura / Recibo de Pagamento", ln=True, align="C")
        pdf.ln(5)
        pdf.set_draw_color(0, 0, 0)
        pdf.line(10, 40, 200, 40)
        pdf.ln(20)

        pdf.set_font("Arial", "", 12)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(0, 10, f"Paciente: {fatura['paciente']}", ln=True)
        pdf.cell(0, 10, f"Dentista: {fatura['dentista']}", ln=True)
        pdf.ln(10)

        pdf.set_font("Arial", "B", 12)
        pdf.cell(100, 10, "Procedimento", border=1, align="C")
        pdf.cell(50, 10, "Valor (R$)", border=1, align="C")
        pdf.ln()
        pdf.set_font("Arial", "", 12)
        pdf.cell(100, 10, fatura["procedimento"], border=1, align="C")
        pdf.cell(50, 10, fatura["valor"], border=1, align="C")
        pdf.ln(20)

        pdf.set_font("Arial", "I", 10)
        data_atual = datetime.now().strftime("%d/%m/%Y %H:%M")
        pdf.cell(0, 10, f"Emitido em: {data_atual}", ln=True, align="L")
        pdf.ln(15)
        pdf.cell(0, 10, "__________________________________", ln=True, align="C")
        pdf.cell(0, 10, "Assinatura do Responsável", ln=True, align="C")

        pdf.output(arquivo)
        messagebox.showinfo("Sucesso", f"Fatura salva em:\n{arquivo}")
