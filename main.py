import tkinter as tk
from tkinter import ttk
from views.dentista_view import DentistaView

def centralizar_janela(root, largura, altura):
    tela_largura = root.winfo_screenwidth()
    tela_altura = root.winfo_screenheight()
    x = (tela_largura // 2) - (largura // 2)
    y = (tela_altura // 2) - (altura // 2)
    root.geometry(f"{largura}x{altura}+{x}+{y}")

def main():
    root = tk.Tk()
    root.title("Sistema Dentista")

    centralizar_janela(root, 1000, 700)
    root.minsize(900, 600)

    try:
        root.iconbitmap("assets/dente.ico")
    except Exception as e:
        print("Ícone não encontrado:", e)

    notebook = ttk.Notebook(root)
    notebook.pack(fill="both", expand=True)

    aba_dentista = DentistaView(notebook)
    notebook.add(aba_dentista, text="Dentistas")
    
    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)

    root.mainloop()

if __name__ == "__main__":
    main()
