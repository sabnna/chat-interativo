import tkinter as tk
from tkinter import ttk

class ConversaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Assistente Virtual - Bate-papo")
        self.root.geometry("520x600")
        self.root.minsize(450, 500)
        self.root.configure(bg="#1e1e2e")

        # Estado da conversa
        self.etapa = 0
        self.dados = {
            "nome": "",
            "origem": "",
            "local": ""
        }

        # Configurar Estilos
        self.configurar_estilos()

        # Criar Elementos Visuais
        self.criar_layout()

        # Iniciar conversa
        self.mensagem_bot("Olá! 👋 Seja muito bem-vindo(a)!\nQual o seu nome?")

    def configurar_estilos(self):
        style = ttk.Style()
        style.theme_use("clam")

    def criar_layout(self):
        # Cabeçalho
        header = tk.Frame(self.root, bg="#2b2b3d", height=60)
        header.pack(fill="x", side="top")
        
        titulo = tk.Label(
            header,
            text="💬 Chat Interativo",
            font=("Segoe UI", 14, "bold"),
            fg="#cdd6f4",
            bg="#2b2b3d"
        )
        titulo.pack(side="left", padx=20, pady=15)

        btn_reiniciar = tk.Button(
            header,
            text="🔄 Reiniciar",
            command=self.reiniciar_conversa,
            bg="#45475a",
            fg="#cdd6f4",
            activebackground="#585b70",
            activeforeground="#ffffff",
            relief="flat",
            font=("Segoe UI", 9, "bold"),
            padx=10,
            pady=4,
            cursor="hand2"
        )
        btn_reiniciar.pack(side="right", padx=20, pady=15)

        # Área de Mensagens (Chat History)
        frame_chat = tk.Frame(self.root, bg="#1e1e2e")
        frame_chat.pack(fill="both", expand=True, padx=20, pady=15)

        self.canvas = tk.Canvas(frame_chat, bg="#1e1e2e", highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(frame_chat, orient="vertical", command=self.canvas.yview)
        
        self.chat_container = tk.Frame(self.canvas, bg="#1e1e2e")
        self.chat_container.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.chat_container, anchor="nw", width=460)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Rodapé / Entrada de Texto
        footer = tk.Frame(self.root, bg="#2b2b3d", height=70)
        footer.pack(fill="x", side="bottom")

        self.entrada = tk.Entry(
            footer,
            font=("Segoe UI", 11),
            bg="#181825",
            fg="#cdd6f4",
            insertbackground="#cdd6f4",
            relief="flat",
            highlightthickness=1,
            highlightbackground="#45475a",
            highlightcolor="#89b4fa"
        )
        self.entrada.pack(side="left", fill="x", expand=True, padx=(20, 10), pady=15, ipady=8)
        self.entrada.bind("<Return>", lambda event: self.processar_envio())
        self.entrada.focus_set()

        self.btn_enviar = tk.Button(
            footer,
            text="Enviar ➤",
            command=self.processar_envio,
            bg="#89b4fa",
            fg="#11111b",
            activebackground="#b4befe",
            activeforeground="#11111b",
            relief="flat",
            font=("Segoe UI", 10, "bold"),
            padx=15,
            pady=7,
            cursor="hand2"
        )
        self.btn_enviar.pack(side="right", padx=(0, 20), pady=15)

    def rolar_para_fim(self):
        self.root.update_idletasks()
        self.canvas.yview_moveto(1.0)

    def mensagem_bot(self, texto):
        msg_frame = tk.Frame(self.chat_container, bg="#1e1e2e")
        msg_frame.pack(fill="x", pady=6, anchor="w")

        lbl = tk.Label(
            msg_frame,
            text=texto,
            font=("Segoe UI", 10),
            bg="#313244",
            fg="#cdd6f4",
            wraplength=350,
            justify="left",
            padx=14,
            pady=10
        )
        lbl.pack(anchor="w")
        self.rolar_para_fim()

    def mensagem_usuario(self, texto):
        msg_frame = tk.Frame(self.chat_container, bg="#1e1e2e")
        msg_frame.pack(fill="x", pady=6, anchor="e")

        lbl = tk.Label(
            msg_frame,
            text=texto,
            font=("Segoe UI", 10),
            bg="#89b4fa",
            fg="#11111b",
            wraplength=350,
            justify="right",
            padx=14,
            pady=10
        )
        lbl.pack(anchor="e")
        self.rolar_para_fim()

    def processar_envio(self):
        texto = self.entrada.get().strip()
        if not texto:
            return

        self.mensagem_usuario(texto)
        self.entrada.delete(0, tk.END)

        # Lógica do script original:
        if self.etapa == 0:
            self.dados["nome"] = texto
            self.etapa = 1
            resposta = f"Olá {self.dados['nome']}, é um prazer te conhecer! Seja bem-vindo(a)!\n\nDe onde você é?"
            self.root.after(400, lambda: self.mensagem_bot(resposta))

        elif self.etapa == 1:
            self.dados["origem"] = texto
            self.etapa = 2
            resposta = f"Que legal que você é de {self.dados['origem']}! 🗺️ Onde fica essa cidade?"
            self.root.after(400, lambda: self.mensagem_bot(resposta))

        elif self.etapa == 2:
            self.dados["local"] = texto
            self.etapa = 3
            resposta = f"Show! Nunca tive a chance de conhecer {self.dados['local']}, espero ir lá um dia! ✨"
            self.root.after(400, lambda: self.mensagem_bot(resposta))
            self.entrada.config(state="disabled")
            self.btn_enviar.config(state="disabled")

    def reiniciar_conversa(self):
        for widget in self.chat_container.winfo_children():
            widget.destroy()
        self.etapa = 0
        self.dados = {"nome": "", "origem": "", "local": ""}
        self.entrada.config(state="normal")
        self.btn_enviar.config(state="normal")
        self.entrada.delete(0, tk.END)
        self.entrada.focus_set()
        self.mensagem_bot("Olá! 👋 Seja muito bem-vindo(a)!\nQual o seu nome?")

if __name__ == "__main__":
    janela = tk.Tk()
    app = ConversaApp(janela)
    janela.mainloop()

