import tkinter as tk
from tkinter import ttk
from pynput.keyboard import Key, Controller

TITLE_FONT = ('Helvetica', 17, 'bold')
BUTTON_FONT = ('Helvetica', 12, 'bold')

global state
state = 0

class App(tk.Tk):
    """Destinada criar a página, herda o Tkinter"""
    def __init__(self, *args, **kwargs):
        """App. Inicializa a todas as páginas da GUI e todos os seus atributos

        :param self: acessar os atributos e métodos da classe
        :param *args: variaveis a ser passadas
        :param **kwargs: dicionarios a ser passados
        """
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, "Sistema Inteligente para Deteção de Contornos em Imagens")

        container = tk.Frame(self) # popular o frame
        container.pack(side="top", fill="both", expand=True) # configuração do pack
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {} # define um dicionario de frames

        for F in (HomePage, TrainPage, TestPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        frame = HomePage(container, self)
        self.frames[HomePage] = frame
        frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(HomePage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class HomePage(tk.Frame):
    """A página principal da GUI"""
    def __init__(self, parent, controller):
        """Home Page. Inicializa a página principal e todos os seus atributos

        :param self: acessar os atributos e métodos da classe
        :param *args: variaveis a ser passadas
        :param **kwargs: dicionarios a ser passados
        """
        tk.Frame.__init__(self, parent)
        tk.Tk.configure(self, bg='#121212')
        controller.resizable(False, False)
        controller.geometry("1000x600+250+100")

        label = tk.Label(self, text="Sistema Inteligente para Deteção de Contornos em Imagens", font=TITLE_FONT, bg='#121212', fg='#ffffff')
        label.place(x=180, y=150)

        button1 = tk.Button(self, text="Treinar", font=BUTTON_FONT, padx=40, pady=15, fg="white", bg="#363636", command=lambda: controller.show_frame(TrainPage))
        button1.place(x=300, y=350)

        button2 = tk.Button(self, text="Testar", font=BUTTON_FONT, padx=40, pady=15, fg="white", bg="#363636", command=lambda: controller.show_frame(TestPage))
        button2.place(x=550, y=350)

class TrainPage(tk.Frame):
    """A página de treinos da GUI"""
    def __init__(self, parent, controller):
        """Train Page. Inicializa a página de treinos e todos os seus atributos

        :param self: acessar os atributos e métodos da classe em python
        :param *args: variaveis a ser passadas
        :param **kwargs: dicionarios a ser passados
        """
        tk.Frame.__init__(self, parent)
        tk.Tk.configure(self, bg='#121212')
        controller.resizable(False, False)
        controller.geometry("1000x600+250+100")

        label = tk.Label(self, text="Treino", font=TITLE_FONT, bg='#121212', fg='#ffffff')
        label.pack(padx=40, pady=50)

        button1 = tk.Button(self, text="Página Inicial", font=BUTTON_FONT, padx=10, pady=10, fg="white", bg="#363636",
                            command=lambda: controller.show_frame(HomePage))
        button1.place(x=30, y=30)

        n_iterations_label = tk.Label(self, text='Introduza o número de iterações: -> X', font=BUTTON_FONT, fg="white", bg="#121212")
        n_iterations_label.place(x=160, y=200)
        n_iterations_entry = tk.Entry(self, font=BUTTON_FONT, width=30)
        n_iterations_entry.insert(0, "10")
        n_iterations_entry.place(x=160, y=230)

        n_population_label = tk.Label(self, text='Introduza o número de população: -> Y', font=BUTTON_FONT, fg="white", bg="#121212")
        n_population_label.place(x=160, y=275)
        n_population_entry = tk.Entry(self, font=BUTTON_FONT, width=30)
        n_population_entry.insert(0, "1000")
        n_population_entry.place(x=160, y=305)

        choose_operator_label = tk.Label(self, text='Escolha um operador base: -> Z', font=BUTTON_FONT, fg="white", bg="#121212")
        choose_operator_label.place(x=160, y=345)
        choose_operator = tk.StringVar()
        operator_options = tk.ttk.Combobox(self, width=42, textvariable=choose_operator)
        operator_options['values'] = ("Sobel Operator", "Prewitt Operator")
        operator_options.place(x=160, y=375)

        buttonTraining = tk.Button(self, text="Iniciar Treino", font=BUTTON_FONT, padx=40, pady=20, fg="white", bg="#363636",
                            command=lambda: press_train_start(n_iterations_entry.get(), n_population_entry.get(), get_operator(operator_options.get())))
        buttonTraining.place(x=400, y=440)

        script_details = tk.Label(self, text='Resumo do treino: ', font=BUTTON_FONT, fg="white", bg="#121212")
        script_details.place(x=550, y=190)

        script_details = "O treino tem como objetivo gerar um modelo/genoma óptimo para deteção de contornos, consoante a sua base.\n\nO treino correrá 'X' iterações.\nCom população de tamanho 'Y'.\nCom base o operador 'Z'."
        script_details_widget = tk.Text(self, height=8, width=40)
        script_details_widget.insert(tk.END, script_details)
        script_details_widget.configure(state='disabled')
        script_details_widget.place(x=550, y=230)




class TestPage(tk.Frame):
    """A página de testes da GUI"""
    def __init__(self, parent, controller):
        """Test Page. Inicializa a página de testes e todos os seus atributos

        :param self: acessar os atributos e métodos da classe
        :param *args: variaveis a ser passadas
        :param **kwargs: dicionarios a ser passados
        """
        tk.Frame.__init__(self, parent)
        tk.Tk.configure(self, bg='#121212')
        controller.resizable(False, False)
        controller.geometry("1000x600+250+100")

        label = tk.Label(self, text="Testar", font=TITLE_FONT, bg='#121212', fg='#ffffff')
        label.place(x=430, y=40)

        button1 = tk.Button(self, text="Página Inicial", font=BUTTON_FONT, padx=10, pady=10, fg="white", bg="#363636",
                            command=lambda: controller.show_frame(HomePage))
        button1.place(x=30, y=30)

        buttonTesting = tk.Button(self, text="Iniciar Teste ", font=BUTTON_FONT, padx=40, pady=20, fg="white", bg="#363636", command=lambda: press_test_start())
        buttonTesting.place(x=140, y=260)

        script_details = tk.Label(self, text='Resumo do teste: ', font=BUTTON_FONT, fg="white", bg="#121212")
        script_details.place(x=550, y=190)

        script_details = "O teste irá aplicar a todas as imagens  presentes na diretoria 'TestImages/Test', o melhor genoma obtido pelo treino."
        script_details_widget = tk.Text(self, height=8, width=40)
        script_details_widget.insert(tk.END, script_details)
        script_details_widget.configure(state='disabled')
        script_details_widget.place(x=550, y=230)


def get_operator(operator_options):
    """Get operator. Obtem o número operador selecinado pelo utilizador

    :param operator_options: string
    :return: número do operador a ser utilizado: int
    """
    if operator_options == "Sobel Operator":
        return 0
    elif operator_options == "Prewitt Operator":
        return 1
    else:
        pass


def get_operator_string(operator):
    """Get operator string. Obtem o nome operador selecinado pelo utilizador

    :param operator: int
    :return: nome do operador: string
    """
    if operator == 0:
        return "Sobel Operator"
    elif operator == 1:
        return "Prewitt Operator"
    else:
        pass


def close_gui():
    """Close GUI. Fecha a GUI"""

    keyboard = Controller()
    keyboard.press(Key.alt)
    keyboard.press(Key.f4)
    keyboard.release(Key.alt)
    keyboard.release(Key.f4)


def press_train_start(iterations, size_of_pop, operator):
    """Press train start. Apresenta os parametros selecionados e escreve os parametros num ficheiro

    :param iterations: int
    :param size_of_pop: int
    :param operator: int
    """
    print("Iterations: {} | Size of population: {} | Base Operator: {}".format(iterations, size_of_pop, get_operator_string(operator)))
    f = open("parameters.txt", "w+")
    f.write("{}\n{}\n{}\n{}".format(iterations, size_of_pop, operator, 1))
    f.close()
    close_gui()


def press_test_start():
    """Press test start. Escreve os parametros num ficheiro"""
    f = open("parameters.txt", "w+")
    f.write("{}\n{}\n{}\n{}".format(0, 0, 0, 2))
    f.close()
    close_gui()


def start():
    """Start. Executa a GUI"""
    f = open("parameters.txt", "w+")
    f.write("{}\n{}\n{}\n{}".format(0, 0, 0, 0))
    f.close()
    app = App()
    app.mainloop()

#if __name__ == "__main__":
#    start()