from tkinter import *
from tkinter import ttk, messagebox
from tkinter.messagebox import showinfo
from PIL import ImageTk, Image
import additional
import matplotlib.pyplot as plt
import matplotlib.widgets as widg
import numpy as np
import copy
import database
from sympy import *
from sympy.plotting import plot3d
from matplotlib import cm

import process


class GUI:
    def __init__(self):
        self.process = process.Process()
        self.window1 = None
        #for dim 1
        self.arrS01 = []#две точки ограничений области (посортированы)
        self.arrG1 = []#точка (одна), которая показывает где подконтур
        self.subS01 = []#две точки внутри главной области (посортированы)
        self.M0x1 = []#точки для зовнишнього впливу на початковий стан - иксы
        self.M0y1 = []#точки для зовнишнього впливу на початковий стан - игреки
        self.MGx1 = []#точки для зовнишнього впливу на область контуру - иксы
        self.MGy1 = []#точки для зовнишнього впливу на область контуру - игреки
        self.t1 = 0#точка для ограничения подконтура по времени нижняя
        self.t2 = 0#точка для ограничения подконтура по времени верхняя
        #for dim 2
        self.flag = None
        self.arrS0x2 = []#
        self.arrS0y2 = []#
        self.rectangle = []#если область прямоугольник - одна точка - в массиве координаты икс и игрек
        self.subrectangle = []#подобласть прямоугольника - тоже прямоугольник
        self.subx2 = []#
        self.suby2 = []#
        self.lines_eq = []#нужно чтобы попадать точно на линии при вводе подобласти
        self.contour_x = []#точки подконтура - иксы
        self.contour_y = []#точки подконтура - игреки


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
                                   'моделюючими функцiями', fg="blue",
                              bg="white", font='Times 14', wraplength=width, background = 'floralwhite')
        chapter_label.pack()

        image = Image.open("back1.png")
        resized = image.resize((width, height), Image.ANTIALIAS)
        image2 = ImageTk.PhotoImage(resized)
        canvas = Canvas(self.window1, width=width, height=height)
        canvas.pack(fill=BOTH, expand=True)
        canvas.create_image(0, 0, image=image2, anchor='nw')

        dim_label = Label(text="1. Оберіть розмірність просторової складової:", fg="blue",
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


        proc_label = Label(text="2. Оберіть процес:", fg="blue",
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



        but_check_proc = Button(self.window1, text=" Перевірити ", fg="blue",
                          bg="white", font="Times 11",
                          activeforeground='black', command = lambda: check())
        but_check_proc.place(x = 578, y = 100)




        modelfunc_label = Label(text="3. Оберіть функцію для моделювання спостережень:", fg="blue",
                           bg="white", font=GUI.fontEx())
        modelfunc_label.place(x=30, y=140)

        cbox_modelfunc = ttk.Combobox(self.window1, width=17, height=5,
                                 font=GUI.fontEx(), state="readonly", values = ())
        cbox_modelfunc.option_add('*TCombobox*Listbox.font', GUI.fontEx())
        cbox_modelfunc.place(x=493, y=140)

        def callbackFuncModel(event):
            self.process.func = cbox_modelfunc.get()

        cbox_modelfunc.bind("<<ComboboxSelected>>", callbackFuncModel)



        T_label = Label(text="4. Оберіть значення Т, t є [0, Т]:", fg="blue",
                                bg="white", font=GUI.fontEx())
        T_label.place(x=30, y=200)


        T_scale = Scale(self.window1, from_=0, to=100, orient='horizontal', resolution=0.1,
                        activebackground = 'deepskyblue', bd = 2, background ='white', font = GUI.fontEx(),
                        length = 343, highlightcolor = 'pink', fg = 'blue', troughcolor = 'floralwhite')
        T_scale.place(x = 320, y = 190)

        def callbackFuncScale(event):
            self.process.T = T_scale.get()

        T_scale.bind("<ButtonRelease-1>", callbackFuncScale)


        def setS0():
            if self.process.dimension == 2:
                if self.flag == 1:
                    self.arrS0x2 = []
                    self.arrS0y2 = []
                    fig, ax = plt.subplots()
                    major_ticks_x = np.arange(-1, 10, 1)
                    major_ticks_y = np.arange(-1, 4, 1)
                    ax.set_xticks(major_ticks_x)
                    ax.set_yticks(major_ticks_y)
                    plt.xlabel("просторова змінна Х")
                    plt.ylabel("просторова змінна Y")
                    cursor = widg.Cursor(ax,
                                         horizOn=False,
                                         vertOn=True,
                                         color='white',
                                         linewidth=0.1)

                    def onclick(event):
                        x1, y1 = event.xdata, event.ydata
                        if len(self.arrS0x2) > 0:
                            plt.scatter([x1, self.arrS0x2[-1]], [y1, self.arrS0y2[-1]], color='blue', marker='*')
                            plt.plot([x1, self.arrS0x2[-1]], [y1, self.arrS0y2[-1]], color='blue', marker='*')
                        else:
                            plt.scatter([x1], [y1], color='blue', marker='*')
                        self.arrS0x2.append(x1)
                        self.arrS0y2.append(y1)

                    fig.canvas.mpl_connect('button_press_event', onclick)
                    plt.ylim([-2, 2])
                    plt.xlim([-5, 5])
                    plt.title("Оберіть точки для задання області\n область опукла, без самоперетинів")
                    plt.show()
                    self.arrS0x2.append(self.arrS0x2[0])
                    self.arrS0y2.append(self.arrS0y2[0])
                    for i in range(0, len(self.arrS0x2) - 1):
                        k = (self.arrS0y2[i + 1] - self.arrS0y2[i]) / (self.arrS0x2[i + 1] - self.arrS0x2[i])
                        b = self.arrS0y2[i] - k * self.arrS0x2[i]
                        self.lines_eq.append(np.poly1d([k, b]))
                else:
                    self.arrS0x2 = []
                    self.arrS0y2 = []
                    self.rectangle = []
                    fig, ax = plt.subplots()
                    major_ticks_x = np.arange(-1, 10, 1)
                    major_ticks_y = np.arange(-1, 4, 1)
                    ax.set_xticks(major_ticks_x)
                    ax.set_yticks(major_ticks_y)
                    plt.xlabel("просторова змінна Х")
                    plt.ylabel("просторова змінна Y")
                    cursor = widg.Cursor(ax,
                                         horizOn=False,
                                         vertOn=True,
                                         color='white',
                                         linewidth=0.1)

                    def onclick(event):
                        if len(self.arrS0x2) == 5:
                            plt.title("Точки успішно обрано!")
                            ax.set_facecolor("red")
                            return

                        x1, y1 = event.xdata, event.ydata
                        self.rectangle.append(x1)
                        self.rectangle.append(y1)
                        self.arrS0x2.append(0)
                        self.arrS0y2.append(0)
                        self.arrS0x2.append(0)
                        self.arrS0y2.append(y1)
                        self.arrS0x2.append(x1)
                        self.arrS0y2.append(y1)
                        self.arrS0x2.append(x1)
                        self.arrS0y2.append(0)
                        self.arrS0x2.append(0)
                        self.arrS0y2.append(0)
                        plt.plot(self.arrS0x2, self.arrS0y2, color='orange')

                    fig.canvas.mpl_connect('button_press_event', onclick)
                    plt.ylim([-1, 4])
                    plt.xlim([-1, 10])
                    plt.title("Оберіть точку для задання прямокутника\n (проходить через початок координат)")
                    plt.show()

            else:
                self.arrS01 = []
                fig, ax = plt.subplots()
                major_ticks_x = np.arange(-5, 5, 1)
                major_ticks_y = np.arange(-2, 2, 1)
                ax.set_xticks(major_ticks_x)
                ax.set_yticks(major_ticks_y)
                plt.xlabel("просторова змінна Х")
                plt.ylabel("часова змінна t")
                plt.axhline(y=0, color='pink',linewidth=1.0)
                y = []
                cursor = widg.Cursor(ax,
                                     horizOn=False,
                                     vertOn=True,
                                     color='white',
                                     linewidth=0.1)
                def onclick(event):
                    x1, y1 = event.xdata, event.ydata
                    if len(self.arrS01) == 2:
                        plt.title("Точки успішно обрано!")
                        ax.set_facecolor("red")
                        return
                    if abs(y1) <= 0.05:
                        self.arrS01.append(x1)
                        y.append(0)
                        plt.scatter(x1, 0, color='green')
                        if len(self.arrS01) == 2:
                            plt.plot(self.arrS01, y, color='green',markersize=7)

                fig.canvas.mpl_connect('button_press_event', onclick)
                plt.ylim([-2, 2])
                plt.xlim([-5, 5])
                plt.title("Оберіть 2 точки для задання області на осі Х")
                plt.show()
                self.arrS01.sort()


        def choose_setS0():
            if self.process.dimension == 2 and self.flag == None:
                choose_setS0_win = Tk()
                choose_setS0_win.geometry("310x80")
                choose_setS0_win.resizable(width=False, height=False)
                choose_setS0_win.title(f'Оберіть тип області')
                choose_setS0_win.configure(background='white')
                choose_setS0_win.attributes("-topmost", True)

                def change_poly():
                    but_poly.configure(bg="skyblue")
                    self.flag = 1

                def change_rec():
                    but_rec.configure(bg="skyblue")
                    self.flag = 0

                but_rec = Button(choose_setS0_win, text=" Прямокутник ", fg="blue",
                              bg="white", font="Times 15 bold",command = change_rec,
                              activeforeground='black')
                but_rec.grid(row=1, column=0)

                but_poly = Button(choose_setS0_win, text=" Полігон точок ", fg="blue",
                                 bg="white", font="Times 15 bold", command = change_poly,
                                 activeforeground='black')
                but_poly.grid(row=1, column=1)


                but_ok = Button(choose_setS0_win, text=" Застосувати ", fg="blue",
                                  bg="white", font="Times 15 bold", command=choose_setS0_win.destroy,
                                  activeforeground='black')
                but_ok.grid(row=2, column=0, columnspan = 2)


                choose_setS0_win.mainloop()
            else:
                setS0()


        but_S0 = Button(self.window1, text="5. Уведіть контур просторової області", fg="blue",
                                bg="white", font=GUI.fontEx(),
                                activeforeground='black', command = choose_setS0)
        but_S0.place(x=30, y=270)

        def setsubS0():
            if self.process.dimension == 2:
                if self.flag == 1:
                    self.subx2 = []
                    self.suby2 = []
                    fig, ax = plt.subplots()
                    major_ticks_x = np.arange(-5, 5, 1)
                    major_ticks_y = np.arange(-2, 2, 1)
                    ax.set_xticks(major_ticks_x)
                    ax.set_yticks(major_ticks_y)
                    plt.xlabel("просторова змінна Х")
                    plt.ylabel("просторова змінна Y")
                    plt.plot(self.arrS0x2, self.arrS0y2, color='blue', marker='*')
                    cursor = widg.Cursor(ax,
                                         horizOn=False,
                                         vertOn=True,
                                         color='white',
                                         linewidth=0.1)

                    def onclick(event):
                        x1, y1 = event.xdata, event.ydata
                        if len(self.subx2) > 0:
                            plt.scatter([x1, self.subx2[-1]], [y1, self.suby2[-1]], color='green', marker='*')
                            plt.plot([x1, self.subx2[-1]], [y1, self.suby2[-1]], color='green', marker='*')
                        else:
                            plt.scatter([x1], [y1], color='green', marker='*')
                        self.subx2.append(x1)
                        self.suby2.append(y1)

                    fig.canvas.mpl_connect('button_press_event', onclick)
                    plt.ylim([-2, 2])
                    plt.xlim([-5, 5])
                    plt.title("Оберіть підобласть для поточної області\n (опуклу та без самоперетинів)")
                    plt.show()
                    self.subx2.append(self.subx2[0])
                    self.suby2.append(self.suby2[0])
                else:
                    self.subx2 = []
                    self.suby2 = []
                    self.subrectangle = []
                    fig, ax = plt.subplots()
                    major_ticks_x = np.arange(-1, 10, 1)
                    major_ticks_y = np.arange(-1, 4, 1)
                    ax.set_xticks(major_ticks_x)
                    ax.set_yticks(major_ticks_y)
                    plt.xlabel("просторова змінна Х")
                    plt.ylabel("просторова змінна Y")
                    plt.plot(self.arrS0x2, self.arrS0y2, color='blue', marker='*')
                    cursor = widg.Cursor(ax,
                                         horizOn=False,
                                         vertOn=True,
                                         color='white',
                                         linewidth=0.1)

                    def onclick(event):
                        if len(self.subx2) == 5:
                            plt.title("Точки успішно обрано!")
                            ax.set_facecolor("red")
                            return
                        x1, y1 = event.xdata, event.ydata
                        self.subrectangle.append(x1)
                        self.subrectangle.append(y1)
                        self.subx2.append(0)
                        self.suby2.append(0)
                        self.subx2.append(0)
                        self.suby2.append(y1)
                        self.subx2.append(x1)
                        self.suby2.append(y1)
                        self.subx2.append(x1)
                        self.suby2.append(0)
                        self.subx2.append(0)
                        self.suby2.append(0)
                        plt.plot(self.subx2, self.suby2, color='orange')

                    fig.canvas.mpl_connect('button_press_event', onclick)
                    plt.ylim([-1, 4])
                    plt.xlim([-1, 10])
                    plt.title("Оберіть підобласть для поточної області\n (прямокутник)")
                    plt.show()

            else:
                self.subS01 = []
                fig, ax = plt.subplots()
                major_ticks_x = np.arange(-5, 5, 1)
                major_ticks_y = np.arange(-2, 2, 1)
                ax.set_xticks(major_ticks_x)
                ax.set_yticks(major_ticks_y)
                plt.xlabel("просторова змінна Х")
                plt.ylabel("часова змінна t")
                plt.axhline(y=0, color='pink',linewidth=1.0)
                plt.plot(self.arrS01, [0,0], color='green', marker='o')
                cursor = widg.Cursor(ax,
                                     horizOn=False,
                                     vertOn=True,
                                     color='white',
                                     linewidth=0.1)
                def onclick(event):
                    x1, y1 = event.xdata, event.ydata
                    if len(self.subS01) == 2:
                        plt.title("Точки успішно обрано!")
                        ax.set_facecolor("red")
                        return
                    if abs(y1) <= 0.05:
                        if self.arrS01[0] <= x1 <= self.arrS01[1]:
                            self.subS01.append(x1)
                            plt.scatter(x1, 0, color = 'blue', marker = '*')
                        if len(self.subS01) == 2:
                            plt.plot(self.subS01, [0,0], color='blue',marker='*',markersize=7)

                fig.canvas.mpl_connect('button_press_event', onclick)
                plt.ylim([-2, 2])
                plt.xlim([-5, 5])
                plt.title("Оберіть 2 точки на відрізку для задання підобласті на осі Х")
                plt.show()


        but_subS0 = Button(self.window1, text="6. Уведіть контур області "
                                              "початкового спостереження", fg="blue",
                        bg="white", font=GUI.fontEx(),command = setsubS0,
                        activeforeground='black')
        but_subS0.place(x=30, y=320)

        def Bound():
            if self.process.dimension == 2:
                self.contour_x = []
                self.contour_y = []
                fig, ax = plt.subplots()
                if self.flag == 1:
                    major_ticks_x = np.arange(-5, 5, 1)
                    major_ticks_y = np.arange(-2, 2, 1)
                else:
                    major_ticks_x = np.arange(-1, 10, 1)
                    major_ticks_y = np.arange(-1, 4, 1)
                ax.set_xticks(major_ticks_x)
                ax.set_yticks(major_ticks_y)
                plt.xlabel("просторова змінна Х")
                plt.ylabel("просторова змінна Y")
                plt.plot(self.arrS0x2, self.arrS0y2, color='blue', marker='*')
                plt.plot(self.subx2, self.suby2, color='green', marker='o')
                cursor = widg.Cursor(ax,
                                     horizOn=False,
                                     vertOn=True,
                                     color='white',
                                     linewidth=0.1)
                lines = []
                print(self.lines_eq)
                def onclick(event):
                    if len(self.contour_x) == 3:
                        plt.title("Точки успішно обрано!")
                        ax.set_facecolor("red")
                        return
                    x1, y1 = event.xdata, event.ydata
                    if self.flag == 1:
                        for i in range(0, len(self.lines_eq)):
                            if abs(np.polyval(self.lines_eq[i], x1) - y1) <= 0.05 and len(self.contour_x) < 3:
                                lines.append(i)
                                plt.scatter([x1], [np.polyval(self.lines_eq[i], x1)], color='cyan', marker = '*')
                                self.contour_x.append(x1)
                                self.contour_y.append(np.polyval(self.lines_eq[i], x1))
                    else:
                        if len(self.contour_x) < 3:
                            if x1 <= 0.05:
                                if 0 < y1 < self.rectangle[1]:
                                    plt.scatter([0], [y1], color='cyan', marker='*')
                                    self.contour_x.append(0)
                                    self.contour_y.append(y1)
                            elif abs(x1 - self.rectangle[0]):
                                if 0 < y1 < self.rectangle[1]:
                                    plt.scatter([self.rectangle[0]], [y1], color='cyan', marker='*')
                                    self.contour_x.append(self.rectangle[0])
                                    self.contour_y.append(y1)
                            if y1 <= 0.05:
                                if 0 < x1 < self.rectangle[0]:
                                    plt.scatter([x1], [0], color='cyan', marker='*')
                                    self.contour_x.append(x1)
                                    self.contour_y.append(0)
                            elif abs(y1-self.rectangle[1]) <= 0.05:
                                if 0 < x1 < self.rectangle[0]:
                                    plt.scatter([x1], [self.rectangle[1]], color='cyan', marker='*')
                                    self.contour_x.append(x1)
                                    self.contour_y.append(self.rectangle[1])

                fig.canvas.mpl_connect('button_press_event', onclick)
                if self.flag == 1:
                    plt.ylim([-2, 2])
                    plt.xlim([-5, 5])
                else:
                    plt.ylim([-1, 4])
                    plt.xlim([-1, 10])
                plt.title("Оберіть підконтур області")
                plt.show()

                time_window = Tk()
                time_window.geometry("210x100")
                time_window.resizable(width=False, height=False)
                time_window.title(f'Оберіть часові обмеження для крайової області')
                time_window.configure(background='white')
                time_window.attributes("-topmost", True)
                fnt = 'Times 15'
                txt1 = Text(time_window, width=5, height=1, font=fnt)
                lb1 = Label(time_window, width=3, height=1, text='t1 = ', font=fnt)
                txt2 = Text(time_window, width=5, height=1, font=fnt)
                lb2 = Label(time_window, width=3, height=1, text='t2 = ', font=fnt)


                def nextt():
                    self.t1 = float(txt1.get('1.0', END))
                    self.t2 = float(txt2.get('1.0', END))
                    time_window.destroy()

                bt = Button(time_window, text='Застосувати', activeforeground='blue', fg='blue',
                             command=nextt, font=fnt)

                lb1.grid(row=0, column=1)
                txt1.grid(row=0, column=2)
                lb2.grid(row=1, column=1)
                txt2.grid(row=1, column=2)
                bt.grid(row=2,column=2, columnspan=2)
                time_window.mainloop()

            else:
                self.arrG1 = []
                fig, ax = plt.subplots()
                major_ticks_x = np.arange(-5, 5, 1)
                major_ticks_y = np.arange(-2, 2, 1)
                ax.set_xticks(major_ticks_x)
                ax.set_yticks(major_ticks_y)
                plt.xlabel("просторова змінна Х")
                plt.ylabel("часова змінна t")
                plt.axhline(y=0, color='pink', linewidth=1.0)
                plt.plot(self.arrS01, [0, 0], color='green', marker='o')
                plt.plot(self.subS01, [0, 0], color='blue', marker='*', markersize=7)
                plt.title("Оберіть одну точку, щоб задати крайову область")
                cursor = widg.Cursor(ax,
                                     horizOn=False,
                                     vertOn=True,
                                     color='white',
                                     linewidth=0.1)
                t = []
                def onclick(event):
                    x1, y1 = event.xdata, event.ydata

                    if len(self.arrG1) == 1 and len(t) == 2:
                        plt.title("Точки успішно обрано!")
                        ax.set_facecolor("red")
                        return
                    if len(self.arrG1) == 1:
                        if len(t) < 2:
                            if abs(x1-self.arrG1[0]) <= 0.05:
                                t.append(y1)
                                plt.scatter(self.arrG1[0], y1, color='orange')
                        if len(t) == 2:
                            t.sort()
                            self.t1 = t[0]
                            self.t2 = t[1]
                            plt.plot([self.arrG1[0]]*2, t, color = 'orange', marker = '*', markersize = 7)

                    if abs(y1) <= 0.05 and len(self.arrG1) == 0:
                        if abs(x1 - self.arrS01[0]) <= 0.05:
                            self.arrG1.append(self.arrS01[0])
                            plt.plot(self.arrG1, [0] * len(self.arrG1), color='red', marker='*', markersize=10)
                            plt.axvline(x=self.arrS01[0], color='black', linewidth=1.0)
                            plt.axvline(x=self.arrS01[1], color='gray', linewidth=1.0)
                            plt.title("Оберіть часові обмеження на вертикальній прямій")
                        elif abs(x1 - self.arrS01[1]) <= 0.05:
                            self.arrG1.append(self.arrS01[1])
                            plt.plot(self.arrG1, [0]*len(self.arrG1), color='red', marker='*', markersize=10)
                            plt.axvline(x=self.arrS01[1], color='black', linewidth=1.0)
                            plt.axvline(x=self.arrS01[0], color='gray', linewidth=1.0)
                            plt.title("Оберіть часові обмеження на вертикальній прямій")

                fig.canvas.mpl_connect('button_press_event', onclick)
                plt.ylim([-2, 2])
                plt.xlim([-5, 5])
                plt.show()


        but_G = Button(self.window1, text="7. Уведіть контур крайового спостереження", fg="blue",
                        bg="white", font=GUI.fontEx(), command = Bound,
                        activeforeground='black')
        but_G.place(x=30, y=370)

        def M0():
            if self.process.dimension == 2:
                return
            else:
                self.M0x1 = []
                self.M0y1 = []
                fig, ax = plt.subplots()
                major_ticks_x = np.arange(-5, 5, 1)
                major_ticks_y = np.arange(-2, 2, 1)
                ax.set_xticks(major_ticks_x)
                ax.set_yticks(major_ticks_y)
                plt.xlabel("просторова змінна Х")
                plt.ylabel("часова змінна t")
                plt.axhline(y=0, color='pink',linewidth=1.0)
                plt.plot(self.arrS01, [0,0], color='green', marker='o')
                plt.plot(self.subS01, [0,0], color='blue', marker='*', markersize=7)
                plt.axvline(x=self.arrS01[0], color='black', linewidth=1.0)
                plt.axvline(x=self.arrS01[1], color='black', linewidth=1.0)
                cursor = widg.Cursor(ax,
                                     horizOn=False,
                                     vertOn=True,
                                     color='white',
                                     linewidth=0.1)
                def onclick(event):
                    x1, y1 = event.xdata, event.ydata
                    if self.arrS01[0] < x1 < self.arrS01[1]:
                        if y1 < 0:
                            plt.scatter(x1, y1, color='blue')
                            self.M0x1.append(x1)
                            self.M0y1.append(y1)

                fig.canvas.mpl_connect('button_press_event', onclick)
                plt.ylim([-2, 2])
                plt.xlim([-5, 5])
                plt.title("Оберіть точки для моделювання зовнішнього\n впливу на початковий стан")
                plt.show()


        but_M0 = Button(self.window1, text="8. Уведіть точки моделювання зовнішнього впливу на початковий стан області", fg="blue",
                       bg="white", font=GUI.fontEx(), command = M0,
                       activeforeground='black')
        but_M0.place(x=30, y=420)

        def Mg():
            if self.process.dimension == 2:
                return
            else:
                self.Mgx1 = []
                self.Mgy1 = []
                fig, ax = plt.subplots()
                major_ticks_x = np.arange(-5, 5, 1)
                major_ticks_y = np.arange(-2, 2, 1)
                ax.set_xticks(major_ticks_x)
                ax.set_yticks(major_ticks_y)
                plt.xlabel("просторова змінна Х")
                plt.ylabel("часова змінна t")
                plt.axhline(y=0, color='pink', linewidth=1.0)
                plt.plot(self.arrS01, [0, 0], color='green', marker='o')
                plt.plot(self.subS01, [0, 0], color='blue', marker='*', markersize=7)
                plt.axvline(x=self.arrS01[0], color='black', linewidth=1.0)
                plt.axvline(x=self.arrS01[1], color='black', linewidth=1.0)
                cursor = widg.Cursor(ax,
                                     horizOn=False,
                                     vertOn=True,
                                     color='white',
                                     linewidth=0.1)

                def onclick(event):
                    x1, y1 = event.xdata, event.ydata
                    if x1 < self.arrS01[0] or x1 > self.arrS01[1]:
                        if y1 > 0:
                            plt.scatter(x1, y1, color='lime', marker='*')
                            self.Mgx1.append(x1)
                            self.Mgy1.append(y1)

                fig.canvas.mpl_connect('button_press_event', onclick)
                plt.ylim([-2, 2])
                plt.xlim([-5, 5])
                plt.title("Оберіть точки для моделювання зовнішнього\n впливу на контур області")
                plt.show()


        but_Mg = Button(self.window1, text="9. Уведіть точки моделювання зовнішнього впливу на контур області",
                        fg="blue",
                        bg="white", font=GUI.fontEx(),command = Mg,
                        activeforeground='black')
        but_Mg.place(x=30, y=470)

        but_res = Button(self.window1, text="Отримати результат",
                        fg="blue",
                        bg="white", font='Times 15 bold italic',
                        activeforeground='black', command = self.window1.destroy)
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
              fg="blue", bg="white", font=fontExample).pack(pady=10)
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


        but_exit = Button(add_win, text=" Застосувати ", fg="blue",
                          bg="white", font="Times 10 bold",
                          activeforeground='black', command=lambda: update_txt())
        but_exit.pack(pady=30)
        add_win.mainloop()


gui = GUI()
gui.Window_1()