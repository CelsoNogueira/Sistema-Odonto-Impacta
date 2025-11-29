import tkinter as tk
from tkinter import ttk
from views.dentista_view import DentistaView
from views.paciente_view import PacienteView
from views.login_view import LoginView
from views.agendamento_view import AgendamentoView
from views.fatura_view import FaturaView

def centralizar_janela(root, largura, altura):
    tela_largura = root.winfo_screenwidth()
    tela_altura = root.winfo_screenheight()
    x = (tela_largura // 2) - (largura // 2)
    y = (tela_altura // 2) - (altura // 2)
    root.geometry(f"{largura}x{altura}+{x}+{y}")

def abrir_sistema(root):
    for widget in root.winfo_children():
        widget.destroy()

    root.title("Sistema Clínica Odontológica")
    centralizar_janela(root, 1000, 700)
    root.minsize(900, 600)

    notebook = ttk.Notebook(root)
    notebook.pack(fill="both", expand=True)

    aba_dentista = DentistaView(notebook)
    notebook.add(aba_dentista, text="Dentistas")

    aba_paciente = PacienteView(notebook)
    notebook.add(aba_paciente, text="Pacientes")

    aba_agendamento = AgendamentoView(notebook)
    notebook.add(aba_agendamento, text="Agendamentos")

    aba_fatura = FaturaView(notebook)
    notebook.add(aba_fatura, text="Faturas / Pagamentos")

    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)

def main():
    root = tk.Tk()
    root.title("Login - Sistema Clínica")
    centralizar_janela(root, 400, 300)
    root.resizable(False, False)

    try:
        root.iconbitmap("assets/dente.ico")
    except Exception as e:
        print("Ícone não encontrado:", e)

   
    def login_sucesso():
        abrir_sistema(root)


    LoginView(root, login_sucesso)

    root.mainloop()

if __name__ == "__main__":
    main()
