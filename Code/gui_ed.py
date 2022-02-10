import glob
import tkinter as tk
from tkinter import *
from PIL import ImageTk, Image
from tkinter import ttk
import train

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

        frame = HomePage(container, self)
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

        label = tk.Label(self, text="Treino", font=TITLE_FONT, bg='#121212', fg='#ffffff')
        label.pack(padx=40, pady=50)

        button1 = tk.Button(self, text="Página Inicial", font=BUTTON_FONT, padx=10, pady=10, fg="white", bg="#363636",
                            command=lambda: controller.show_frame(HomePage))
        button3 = tk.Button(self, text="Parar Treino", font=BUTTON_FONT, padx=40, pady=20, fg="white", bg="#363636",
                            command=lambda: stop_execution())
        button1.place(x=30, y=30)
        button3.place(x=550, y=440)


        n_iterations_label = tk.Label(self, text='Introduza o número de iterações: ', font=BUTTON_FONT, fg="white", bg="#121212")
        n_iterations_entry = tk.Entry(self, font=BUTTON_FONT, width=30)
        n_population_label = tk.Label(self, text='Introduza o número de população: ', font=BUTTON_FONT, fg="white", bg="#121212")
        n_population_entry = tk.Entry(self, font=BUTTON_FONT, width=30)
        choose_operator_label = tk.Label(self, text='Escolha um operador base: ', font=BUTTON_FONT, fg="white", bg="#121212")
        n_iterations_label.place(x=160, y=200)
        n_iterations_entry.place(x=160, y=230)
        n_population_label.place(x=160, y=275)
        n_population_entry.place(x=160, y=305)
        choose_operator_label.place(x=160, y=345)
        n_iterations_entry.insert(0, "10")
        n_population_entry.insert(0, "1000")
        #def get_input_dir():
        #print("O diretorio escolhido foi: ", dir_entry.get())

        n = tk.StringVar()
        operator_options = ttk.Combobox(self, width=42, textvariable=n)
        operator_options['values'] = ("Sobel Operator", "Robinson Operator", "Fri-Chen Operator")
        operator_options.place(x=160, y=375)

        button2 = tk.Button(self, text="Iniciar Treino", font=BUTTON_FONT, padx=40, pady=20, fg="white", bg="#363636",
                            command=lambda: press_start_button(n_iterations_entry.get(), n_population_entry.get(), get_operator(operator_options.get())))
        button2.place(x=250, y=440)


        #button2 = tk.Button(self, text="Iniciar Treino", font=BUTTON_FONT, padx=40, pady=20, fg="white", bg="#363636",
          #                  command=lambda: hold(n_iterations_entry.get(), n_population_entry.get(), operator_options.get()))
        #button2.place(x=250, y=440)


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
        button2 = tk.Button(self, text="Iniciar Teste ", font=BUTTON_FONT, padx=40, pady=20, fg="white", bg="#363636")
        button3 = tk.Button(self, text="Parar Teste", font=BUTTON_FONT, padx=40, pady=20, fg="white", bg="#363636",
                            command=lambda: stop_execution())
        button1.place(x=30, y=30)
        button2.place(x=140, y=220)
        button3.place(x=140, y=360)

        result_photo_label = tk.Label(self, text='Melhor resultado: ', font=BUTTON_FONT, fg="white", bg="#121212")
        result_photo_label.place(x=550, y=105)

        #result_image = ImageTk.PhotoImage(Image.open(image_path).resize((300, 225), Image.ANTIALIAS))
        #img_label = Label(self, image=result_image)
        #img_label.image = result_image
        #img_label.place(x=550, y=130)

        result_photo_label = tk.Label(self, text='Média Resultado: ', font=BUTTON_FONT, fg="white", bg="#121212")
        result_photo_label.place(x=550, y=380)

        result_text = "Isto é um exemplo de resultado"
        result_text_widget = Text(self, height=8, width=40)
        result_text_widget.insert(tk.END, result_text)
        result_text_widget.configure(state='disabled')
        result_text_widget.place(x=550, y=420)

#def get_iterations(n_iterations_entry):
#    return n_iterations_entry

#def get_size_of_pop(n_population_entry):
#    return n_population_entry

def get_operator(operator_options):
    if operator_options == "Sobel Operator":
        return 0
    elif operator_options == "Robinson Operator":
        return 1
    elif operator_options == "Fri-Chen Operator":
        return 2
    else:
        pass


def stop_execution():
    import sys
    sys.exit()

def press_start_button(iterations, size_of_pop, operator):
    print("iterations: ", iterations, "| size_of_pop:", size_of_pop, "| operator:", operator)
    train.training(int(iterations), int(size_of_pop), int(operator))


def start():
    app = App()
    app.mainloop()

if __name__ == "__main__":
    start()