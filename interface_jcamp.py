import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import os

# Importa seu script principal
import processar_espectros_jcamp as proc


class App:
    def __init__(self, root):
        self.root = root
        root.title("Conversor de Espectros JCAMP")
        root.geometry("500x420")

        # Variáveis
        self.caminho = tk.StringVar()

        # Frame principal
        frame = tk.Frame(root, padx=10, pady=10)
        frame.pack(fill="both", expand=True)

        # Selecionar arquivo/pasta
        tk.Label(frame, text="Selecione um arquivo ZIP ou uma pasta com JDX:").pack(anchor="w")
        entry = tk.Entry(frame, textvariable=self.caminho, width=45)
        entry.pack(side="left", padx=5)

        tk.Button(frame, text="Selecionar", command=self.selecionar_caminho).pack(side="left")

        # Botão de processamento
        tk.Button(root, text="\nPROCESSAR ESPECTROS\n",
                  command=self.iniciar_processamento,
                  bg="#4CAF50", fg="white").pack(pady=12)

        # Log
        tk.Label(root, text="Log:").pack(anchor="w")
        self.log = tk.Text(root, height=12, width=60)
        self.log.pack()

    def selecionar_caminho(self):
        caminho_zip = filedialog.askopenfilename(
            filetypes=[("Zip Files", "*.zip"), ("Todos os arquivos", "*.*")]
        )

        if caminho_zip:
            self.caminho.set(caminho_zip)
            return

        # Também permite selecionar pastas
        caminho_pasta = filedialog.askdirectory()
        if caminho_pasta:
            self.caminho.set(caminho_pasta)

    def iniciar_processamento(self):
        caminho = self.caminho.get()

        if not os.path.exists(caminho):
            messagebox.showerror("Erro", "Selecione um arquivo ou pasta válida.")
            return

        # Rodar em thread separada
        threading.Thread(target=self.processar, args=(caminho,), daemon=True).start()

    def processar(self, caminho):
        try:
            # Envia o caminho para o script principal
            proc.CAMINHO = caminho

            self.log.insert("end", f"🔍 Processando: {caminho}\n")
            self.log.insert("end", "⏳ Isso pode levar alguns segundos...\n")

            # Chama o main() do seu script
            proc.main()

            self.log.insert("end", "\n✅ Processamento concluído!\n")
            messagebox.showinfo("Sucesso", "Espectros processados com sucesso!")

        except Exception as e:
            self.log.insert("end", f"\n❌ ERRO: {e}\n")
            messagebox.showerror("Erro", str(e))


# Roda a interface
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
