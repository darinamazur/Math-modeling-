import database
import tkinter as tk
from tkinter import*
from tkinter import ttk
from tkinter.ttk import Combobox
from PIL import ImageTk, Image
from tkinter import ttk, messagebox
from tkinter.messagebox import showinfo
import matplotlib.pyplot as plt
import matplotlib.widgets as wdg
import mplcursors
import numpy as np

import process


class GUI:
    def __init__(self):
        self.process = process.Process()
        self.window1 = None
        #for dim 1 -> to new class. We split this 2 cases because 3d and 2d graphics -
        # in 2d using 3d is not too attractive
        self.arrS01 = []
        self.arrG1 = []
        self.subS01 = []
        self.M01 = []
        self.MG1 = []
        #for dim 2

    fontEx = lambda: "Times 14"

    def Window_1(self):
        self.window1 = Tk()
        width = 700
        height = 580
        self.window1.geometry(f'{width}x{height}')
        self.window1.resizable(width=False, height=False)
        self.window1.title('Вхідні дані')
        chapter_label = Label(text='Задача математичного моделювання лiнiйно-розподiлених систем з '
                                   'неперервними початково-крайовими спостереженнями i дискретними '
                                   'моделюючими функцiями', fg="indigo",
                              bg="white", font='Times 14', wraplength=width, background = 'floralwhite')
        chapter_label.pack()

        image = Image.open("back1.png")
        resized = image.resize((width, height), Image.ANTIALIAS)
        image2 = ImageTk.PhotoImage(resized)
        canvas = Canvas(self.window1, width=width, height=height)
        canvas.pack(fill=BOTH, expand=True)
        canvas.create_image(0, 0, image=image2, anchor='nw')

        dim_label = Label(text="1. Оберіть розмірність просторової складової:", fg="purple",
                          bg="white", font=GUI.fontEx())
        dim_label.place(x = 30, y = 60)

        cbox_dim = ttk.Combobox(self.window1, width=11, height=5,
                                font=GUI.fontEx(), state="readonly", values=(1, 2))
        cbox_dim.option_add('*TCombobox*Listbox.font', GUI.fontEx())
        cbox_dim.place(x = 442, y = 60)

        def callbackFuncDim(event):
            cbox_proc.set('')
            cbox_modelfunc.set('')
            self.process.dimension = int(cbox_dim.get())
            cbox_proc['values'] = database.DataBase().SelectProcessName(self.process.dimension)
            if self.process.dimension == 1:
                cbox_modelfunc['values'] = database.DataBase().SelectFunc1()
            else:
                cbox_modelfunc['values'] = database.DataBase().SelectFunc2()

        cbox_dim.bind("<<ComboboxSelected>>", callbackFuncDim)


        proc_label = Label(text="2. Оберіть процес:", fg="purple",
                          bg="white", font=GUI.fontEx())
        proc_label.place(x = 30, y = 100)

        cbox_proc = ttk.Combobox(self.window1, width=36, height=5,
                                font=GUI.fontEx(), state="readonly", values = ())
        cbox_proc.option_add('*TCombobox*Listbox.font', GUI.fontEx())
        cbox_proc.place(x = 216, y = 100)

        def callbackFuncProc(event):
            self.process.name = cbox_proc.get()
            self.process.green = database.DataBase().SelectGreenFunction(self.process.name, str(self.process.dimension))[0]
            self.process.oper = database.DataBase().SelectDiffOperator(self.process.name, str(self.process.dimension))[0]
            if self.process.oper.find('c') != -1:
                GUI.ConstantWindow(self)


        cbox_proc.bind("<<ComboboxSelected>>", callbackFuncProc)


        def check():
            if(cbox_dim.get()==''):
                messagebox.showwarning(title="Увага", message="Оберіть розмірність!")
                return

            if (cbox_proc.get() == ''):
                messagebox.showwarning(title="Увага", message="Оберіть процес!")
                return

            msg = f'Розмірність: {self.process.dimension}\n' \
                  f'Процес: {self.process.name}\n'\
                  f'Функція Гріна: {self.process.green}\n' \
                  f'Диференціальний оператор: {self.process.oper}\n'
            if self.process.const:
                msg+= f'c = {self.process.const}'
            showinfo(title='Уведені дані', message=msg)



        but_check_proc = Button(self.window1, text=" Перевірити ", fg="purple",
                          bg="white", font="Times 11",
                          activeforeground='black', command = lambda: check())
        but_check_proc.place(x = 578, y = 100)




        modelfunc_label = Label(text="3. Оберіть функцію для моделювання спостережень:", fg="purple",
                           bg="white", font=GUI.fontEx())
        modelfunc_label.place(x=30, y=140)

        cbox_modelfunc = ttk.Combobox(self.window1, width=17, height=5,
                                 font=GUI.fontEx(), state="readonly", values = ())
        cbox_modelfunc.option_add('*TCombobox*Listbox.font', GUI.fontEx())
        cbox_modelfunc.place(x=493, y=140)

        def callbackFuncModel(event):
            self.process.func = cbox_modelfunc.get()

        cbox_modelfunc.bind("<<ComboboxSelected>>", callbackFuncModel)



        T_label = Label(text="4. Оберіть значення Т, t є [0, Т]:", fg="purple",
                                bg="white", font=GUI.fontEx())
        T_label.place(x=30, y=200)


        T_scale = Scale(self.window1, from_=0, to=100, orient='horizontal', resolution=0.1,
                        activebackground = 'indigo', bd = 2, background ='white', font = GUI.fontEx(),
                        length = 343, highlightcolor = 'pink', fg = 'purple', troughcolor = 'floralwhite')
        T_scale.place(x = 320, y = 190)

        def callbackFuncScale(event):
            self.process.T = T_scale.get()

        T_scale.bind("<ButtonRelease-1>", callbackFuncScale)


        def setS0():
            if self.process.dimension == 2:
                return
            else:
                self.arrS01 = []
                fig, ax = plt.subplots()
                lines = ax.hlines(y=0, xmin=-10, xmax=10, linewidth=2, color='r')
                mplcursors.cursor(lines)
                plt.xlabel("просторова змінна x")
                plt.ylabel("час t")
                plt.title('Оберіть 2 точки для задання області на осі Х')
                def onclick(event):
                    if len(self.arrS01) == 2:
                       return
                    x1, y1 = event.xdata, event.ydata
                    if abs(y1) <= 0.001:
                        plt.plot([x1], [0], marker='o', markersize=7, color="green")
                        self.arrS01.append(x1)
                fig.canvas.mpl_connect('button_press_event', onclick)
                plt.show()


        but_S0 = Button(self.window1, text="5. Уведіть контур просторової області", fg="purple",
                                bg="white", font=GUI.fontEx(),
                                activeforeground='black', command = lambda: setS0())
        but_S0.place(x=30, y=270)


        def setsubS0():
            if self.process.dimension == 2:
                return
            else:
                self.subS01 = []
                fig, ax = plt.subplots()
                lines = ax.hlines(y=0, xmin=-10, xmax=10, linewidth=2, color='r')
                mplcursors.cursor(lines)
                plt.xlabel("просторова змінна x")
                plt.ylabel("час t")
                plt.title('Оберіть 2 точки для задання підобласті на осі Х')
                plt.plot(self.arrS01, [0,0], marker='o', markersize=7, color="green")

                def onclick(event):
                    if len(self.subS01) == 2:
                        return
                    x1, y1 = event.xdata, event.ydata
                    if abs(y1) <= 0.001:
                        if x1 >= self.arrS01[0] and x1 <= self.arrS01[1]:
                            plt.plot([x1], [0], marker='*', markersize=7, color="blue")
                            self.subS01.append(x1)

                fig.canvas.mpl_connect('button_press_event', onclick)
                plt.show()


        but_subS0 = Button(self.window1, text="6. Уведіть контур області "
                                              "початкового спостереження", fg="purple",
                        bg="white", font=GUI.fontEx(),
                        activeforeground='black', command = lambda: setsubS0())
        but_subS0.place(x=30, y=320)

        but_G = Button(self.window1, text="7. Уведіть контур крайового спостереження", fg="purple",
                        bg="white", font=GUI.fontEx(),
                        activeforeground='black')
        but_G.place(x=30, y=370)

        but_M0 = Button(self.window1, text="8. Уведіть точки моделювання зовнішнього впливу на початковий стан області", fg="purple",
                       bg="white", font=GUI.fontEx(),
                       activeforeground='black')
        but_M0.place(x=30, y=420)

        but_Mg = Button(self.window1, text="9. Уведіть точки моделювання зовнішнього впливу на контур області",
                        fg="purple",
                        bg="white", font=GUI.fontEx(),
                        activeforeground='black')
        but_Mg.place(x=30, y=470)

        but_res = Button(self.window1, text="Отримати результат",
                        fg="purple",
                        bg="white", font='Times 15 bold italic',
                        activeforeground='black')
        but_res.place(relx = 0.5, y = 540, anchor = 'center')



        self.window1.mainloop()

    def ConstantWindow(self):
        fontExample = ("Times", 12, 'italic')
        add_win = Tk()
        add_win.geometry("300x200")
        add_win.resizable(width=False, height=False)
        add_win.title(f'Введіть константу С')
        add_win.configure(background='white')
        add_win.attributes("-topmost", True)

        def Quit():
            messagebox.showwarning(title="Увага", message="Уведіть C!")
            pass

        add_win.protocol("WM_DELETE_WINDOW", Quit)

        Label(add_win, text=f'Уведіть константу  C\n для диференціального оператора\n {self.process.oper}:',
              fg="purple", bg="white", font=fontExample).pack(pady=10)
        txt = Text(add_win, width=10, height=1, font=fontExample)
        txt.pack(pady=10)

        def update_txt():
            txt.update()
            if len(txt.get('1.0', END)) == 1:
                messagebox.showwarning(title="Увага", message="Уведіть C!")
                return
            if txt.get('1.0', END).replace('.', '', 1)[0:-1].isdigit() == False:
                messagebox.showwarning(title="Увага", message="Лише цифри!")
            else:
                self.process.const = txt.get('1.0', END)
                add_win.destroy()


        but_exit = Button(add_win, text=" Застосувати ", fg="purple",
                          bg="white", font="Times 10 bold",
                          activeforeground='black', command=lambda: update_txt())
        but_exit.pack(pady=30)
        add_win.mainloop()


gui = GUI()
gui.Window_1()





