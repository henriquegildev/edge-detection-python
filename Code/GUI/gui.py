import tkinter as tk

TITLE_FONT = ('Helvetica', 17, 'bold')
BUTTON_FONT = ('Helvetica', 12, 'bold')

class App(tk.Tk): #inherit tkinter
    def __init__(self, *args, **kwargs): #automatic startup fuction
        tk.Tk.__init__(self, *args, **kwargs) #args - varibles being passed / #kwargs - dictionaries passed
        tk.Tk.wm_title(self, "Sistema Inteligente para Deteção de Contornos em Imagens")

        container = tk.Frame(self) #used populate the frame
        container.pack(side="top", fill="both", expand=True) #pack configuration
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {} #define a dictionary frame

        for F in (HomePage, TrainPage, TestPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        frame = HomePage (container, self)
        self.frames[HomePage] = frame
        frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(HomePage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

def qf(param):
    print(param)

class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        tk.Tk.configure(self, bg='#121212')
        controller.resizable(False, False)
        controller.geometry("1000x600+250+100")

        label = tk.Label(self, text="Sistema Inteligente para Deteção de Contornos em Imagens", font=TITLE_FONT, bg='#121212', fg='#ffffff')
        label.place(x=180, y=150)

        button1 = tk.Button(self, text="Treinar", font=BUTTON_FONT, padx=40, pady=15, fg="white", bg="#363636", command=lambda: controller.show_frame(TrainPage))
        button2 = tk.Button(self, text="Testar", font=BUTTON_FONT, padx=40, pady=15, fg="white", bg="#363636", command=lambda: controller.show_frame(TestPage))
        button1.place(x=300, y=350)
        button2.place(x=550, y=350)

class TrainPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        tk.Tk.configure(self, bg='#121212')
        controller.resizable(False, False)
        controller.geometry("1000x600+250+100")

        label = tk.Label(self, text="Train Page", font=TITLE_FONT, bg='#121212', fg='#ffffff')
        label.pack(padx=40, pady=20)

        button1 = tk.Button(self, text="Home Page", font=BUTTON_FONT, padx=40, pady=20, fg="white", bg="#363636", command=lambda: controller.show_frame(HomePage))
        button1.pack()
        button2 = tk.Button(self, text="Test Page", font=BUTTON_FONT, padx=40, pady=20, fg="white", bg="#363636", command=lambda: controller.show_frame(TestPage))
        button2.pack()

class TestPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        tk.Tk.configure(self, bg='#121212')
        controller.resizable(False, False)
        controller.geometry("1000x600+250+100")

        label = tk.Label(self, text="Testar", font=TITLE_FONT, bg='#121212', fg='#ffffff')

        button1 = tk.Button(self, text="Página Inicial", font=BUTTON_FONT, padx=10, pady=10, fg="white", bg="#363636", command=lambda: controller.show_frame(HomePage))
        button2 = tk.Button(self, text="Apagar Fotos", font=BUTTON_FONT, padx=40, pady=20, fg="white", bg="#363636", command=lambda: controller.show_frame(TrainPage))
        button3 = tk.Button(self, text="Iniciar Teste", font=BUTTON_FONT, padx=40, pady=20, fg="white", bg="#363636", command=lambda: controller.show_frame(TrainPage))

        dir_label = tk.Label(self, text='Introduza o nome do diretorio com as novas fotos de treino: ', font=('calibre', 12), fg="white", bg="#121212")
        dir_var = tk.StringVar()
        dir_var.set("")
        dir_entry = tk.Entry(self, textvariable=dir_var, font=('calibre', 10, 'normal'), width=70)
        button4 = tk.Button(self, text="Selecionar Diretorio", font=BUTTON_FONT, padx=40, pady=5, fg="white", bg="#363636")

        dir_label.place(x=250, y=230)
        dir_entry.place(x=250, y=260)
        button4.place(x=375, y=315)

        label.place(x=430, y=100)
        button1.place(x=30, y=30)
        button2.place(x=250, y=400)
        button3.place(x=550, y=400)


app = App()
app.mainloop()

