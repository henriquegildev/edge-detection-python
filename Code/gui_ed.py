import tkinter as tk
from tkinter import ttk
from pynput.keyboard import Key, Controller

TITLE_FONT = ('Helvetica', 17, 'bold')
BUTTON_FONT = ('Helvetica', 12, 'bold')

global state
state = 0

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

        frame = HomePage(container, self)
        self.frames[HomePage] = frame
        frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(HomePage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class HomePage(tk.Frame):
    def __init__(self, parent, controller):
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
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        tk.Tk.configure(self, bg='#121212')
        controller.resizable(False, False)
        controller.geometry("1000x600+250+100")

        label = tk.Label(self, text="Treino", font=TITLE_FONT, bg='#121212', fg='#ffffff')
        label.pack(padx=40, pady=50)

        button1 = tk.Button(self, text="Página Inicial", font=BUTTON_FONT, padx=10, pady=10, fg="white", bg="#363636",
                            command=lambda: controller.show_frame(HomePage))
        button1.place(x=30, y=30)

        n_iterations_label = tk.Label(self, text='Introduza o número de iterações: ', font=BUTTON_FONT, fg="white", bg="#121212")
        n_iterations_label.place(x=160, y=200)
        n_iterations_entry = tk.Entry(self, font=BUTTON_FONT, width=30)
        n_iterations_entry.insert(0, "10")
        n_iterations_entry.place(x=160, y=230)

        n_population_label = tk.Label(self, text='Introduza o número de população: ', font=BUTTON_FONT, fg="white", bg="#121212")
        n_population_label.place(x=160, y=275)
        n_population_entry = tk.Entry(self, font=BUTTON_FONT, width=30)
        n_population_entry.insert(0, "1000")
        n_population_entry.place(x=160, y=305)

        choose_operator_label = tk.Label(self, text='Escolha um operador base: ', font=BUTTON_FONT, fg="white", bg="#121212")
        choose_operator_label.place(x=160, y=345)
        choose_operator = tk.StringVar()
        operator_options = ttk.Combobox(self, width=42, textvariable=choose_operator)
        operator_options['values'] = ("Sobel Operator", "Robinson Operator", "Fri-Chen Operator")
        operator_options.place(x=160, y=375)

        buttonTraining = tk.Button(self, text="Iniciar Treino", font=BUTTON_FONT, padx=40, pady=20, fg="white", bg="#363636",
                            command=lambda: press_train_start(n_iterations_entry.get(), n_population_entry.get(), get_operator(operator_options.get())))
        buttonTraining.place(x=250, y=440)

class TestPage(tk.Frame):
    def __init__(self, parent, controller):
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
        buttonTesting.place(x=140, y=220)

"""
Nome: get_operator
Desc.: Obtem o número operador selecinado pelo utilizador
Input: operator_options: string
Returns: 0, 1, 2
"""

def get_operator(operator_options):
    if operator_options == "Sobel Operator":
        return 0
    elif operator_options == "Robinson Operator":
        return 1
    elif operator_options == "Fri-Chen Operator":
        return 2
    else:
        pass

"""
Nome: get_operator_string
Desc.: Obtem o nome do operador selecinado pelo utilizador
Input: operator: int
Returns: "Sobel Operator" / "Robinson Operator" / "Fri-Chen Operator"
"""
def get_operator_string(operator):
    if operator == 0:
        return "Sobel Operator"
    elif operator == 1:
        return "Robinson Operator"
    elif operator == 2:
        return "Fri-Chen Operator"
    else:
        pass


"""
Nome: close_gui
Desc.: Fecha a GUI
"""

def close_gui():
    keyboard = Controller()
    keyboard.press(Key.alt)
    keyboard.press(Key.f4)
    keyboard.release(Key.alt)
    keyboard.release(Key.f4)


"""
Nome: press_train_start
Desc.: Obtem o nome do operador selecinado pelo utilizador
Input: iterations = int, size_of_pop = int, operator = int
"""

def press_train_start(iterations, size_of_pop, operator):
    print("Iterations: {} | Size of population: {} | Base Operator: {}".format(iterations, size_of_pop, get_operator_string(operator)))
    f = open("parameters.txt", "w+")
    f.write("{}\n{}\n{}\n{}".format(iterations, size_of_pop, operator, 1))
    f.close()
    close_gui()


"""
Nome: press_test_start
Desc.: Corre a opção teste selecionada pelo utilizador
"""

def press_test_start():
    f = open("parameters.txt", "w+")
    f.write("{}\n{}\n{}\n{}".format(0, 0, 0, 2))
    f.close()
    close_gui()


"""
Nome: start
Desc.: Executa a GUI
"""

def start():
    app = App()
    app.mainloop()

#if __name__ == "__main__":
#    start()