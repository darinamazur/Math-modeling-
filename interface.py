from tkinter import *
from tkinter import ttk, messagebox
from tkinter.messagebox import showinfo
from PIL import ImageTk, Image
import matplotlib.pyplot as plt
import matplotlib.widgets as widg
import numpy as np
import math
import database
import process
import core


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
        self.Mgx1 = []#точки для зовнишнього впливу на область контуру - иксы
        self.Mgy1 = []#точки для зовнишнього впливу на область контуру - игреки
        self.t1 = 0#точка для ограничения подконтура по времени нижняя
        self.t2 = 0#точка для ограничения подконтура по времени верхняя
        #for dim 2
        self.flag = None
        self.arrS0x2 = []#иксы точек контура
        self.arrS0y2 = []#игреки точек контура
        self.rectangle = []#если область прямоугольник - одна точка - в массиве координаты икс и игрек
        self.subrectangle = []#подобласть прямоугольника - тоже прямоугольник
        self.subx2 = []#иксы точек подконтура
        self.suby2 = []#игреки точек подконтура
        self.lines_eq = []#нужно чтобы попадать точно на линии при вводе подобласти
        self.contour_x = []#точки подконтура - иксы
        self.contour_y = []#точки подконтура - игреки
        self.M0x2 = []#точки для зовнишнього впливу на початковий стан - иксы
        self.M0y2 = []#точки для зовнишнього впливу на початковий стан - игреки
        self.M0z2 = []#точки для зовнишнього впливу на початковий стан - зэт

        self.Mgx2 = []#точки для зовнишнього впливу на область контуру - иксы
        self.Mgy2 = []#точки для зовнишнього впливу на область контуру - игреки
        self.Mgz2 = []#точки для зовнишнього впливу на область контуру - зэт


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
                    major_ticks_x = np.arange(-5, 5, 1)
                    major_ticks_y = np.arange(-2, 2, 1)
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
                    but_rec.configure(bg="white")
                    self.flag = 1

                def change_rec():
                    but_rec.configure(bg="skyblue")
                    but_poly.configure(bg="white")
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
                time_window.geometry("400x100")
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

                lb1.grid(row=0, column=1, columnspan=2)
                txt1.grid(row=0, column=3, columnspan=2)
                lb2.grid(row=1, column=1, columnspan=2)
                txt2.grid(row=1, column=3, columnspan=2)
                bt.grid(row=2,column=2, columnspan=3)
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
                self.M0x2 = []
                self.M0y2 = []
                self.M0z2 = []
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
                    x1, y1 = event.xdata, event.ydata
                    plt.scatter(x1, y1, color='purple', marker='*')
                    self.M0x2.append(x1)
                    self.M0y2.append(y1)


                fig.canvas.mpl_connect('button_press_event', onclick)
                if self.flag == 1:
                    plt.ylim([-2, 2])
                    plt.xlim([-5, 5])
                else:
                    plt.ylim([-1, 4])
                    plt.xlim([-1, 10])
                plt.title("Оберіть точки моделювання зовнішньоговпливу \nна початковий стан (проекції на вісь OZ) усередині області")
                plt.show()

                z_window = Tk()
                n = len(self.M0x2)
                self.M0z2 = [0] * n
                k = 1
                if n > 10:
                    k = int(n / 10 + 1)
                h = n + 1
                if n <= 10:
                    h = n + 1
                else:
                    h = 11
                z_window.geometry(f"{400 * k}x{50 * h + 5}")
                z_window.resizable(width=False, height=False)
                z_window.title(f'Оберіть ординати введених точок (> 0)')
                z_window.configure(background='white')
                z_window.attributes("-topmost", True)
                fnt = 'Times 15'
                scales = []
                lbls = []
                for i in range(0, n):
                    scales.append(Scale(z_window, from_=-50, to=-0.1, orient='horizontal', resolution=0.1,
                                        activebackground='deepskyblue', bd=2, background='white', font=GUI.fontEx(),
                                        length=250, highlightcolor='pink', fg='blue', troughcolor='floralwhite'))

                    lbls.append(Label(z_window, width=10, height=1, text=f'M0[{i}]_z =', font=fnt))

                def nextt():
                    z_window.destroy()

                bt = Button(z_window, text='Застосувати', activeforeground='blue', fg='blue',
                            command=nextt, font=fnt)

                def callbackFuncScale(event):
                    for i in range(0, n):
                        self.M0z2[i] = scales[i].get()

                for i in range(0, n):
                    scales[i].bind("<ButtonRelease-1>", callbackFuncScale)

                for i in range(0, n):
                    lbls[i].grid(row=i - 10*(i//10), column=3 + 10*(i//10), columnspan=3)
                    scales[i].grid(row=i - 10*(i//10), column=7 + 10*(i//10), columnspan=3)

                bt.grid(row=n + 1, column=2, columnspan=3)
                z_window.mainloop()

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
                self.Mgx2 = []
                self.Mgy2 = []
                self.Mgz2 = []
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
                    x1, y1 = event.xdata, event.ydata
                    plt.scatter(x1, y1, color='lime', marker='*')
                    self.Mgx2.append(x1)
                    self.Mgy2.append(y1)

                fig.canvas.mpl_connect('button_press_event', onclick)
                if self.flag == 1:
                    plt.ylim([-2, 2])
                    plt.xlim([-5, 5])
                else:
                    plt.ylim([-1, 4])
                    plt.xlim([-1, 10])
                plt.title(
                    "Оберіть точки моделювання зовнішньоговпливу \nна контур області (проекції на вісь OZ) поза областю")
                plt.show()

                z_window = Tk()
                n = len(self.Mgx2)
                self.Mgz2 = [0] * n
                k = 1
                if n > 10 :
                    k = int(n/10 + 1)
                h = n + 1
                if n <= 10:
                    h = n + 1
                else: h = 11
                z_window.geometry(f"{400*k}x{50*h+5}")
                z_window.resizable(width=False, height=False)
                z_window.title(f'Оберіть ординати введених точок (> 0)')
                z_window.configure(background='white')
                z_window.attributes("-topmost", True)
                fnt = 'Times 15'
                scales = []
                lbls = []
                for i in range(0, n):
                    scales.append(Scale(z_window, from_=0.1, to=self.process.T, orient='horizontal', resolution=0.1,
                                        activebackground='deepskyblue', bd=2, background='white', font=GUI.fontEx(),
                                        length=250, highlightcolor='pink', fg='blue', troughcolor='floralwhite'))

                    lbls.append(Label(z_window, width=10, height=1, text=f'Mg[{i}]_z =', font=fnt))

                def nextt():
                    z_window.destroy()

                bt = Button(z_window, text='Застосувати', activeforeground='blue', fg='blue',
                            command=nextt, font=fnt)

                def callbackFuncScale(event):
                    for i in range(0, n):
                        self.Mgz2[i] = scales[i].get()

                for i in range(0, n):
                    scales[i].bind("<ButtonRelease-1>", callbackFuncScale)

                for i in range(0, n):
                    lbls[i].grid(row=i - 10 * (i // 10), column=3 + 10 * (i // 10), columnspan=3)
                    scales[i].grid(row=i - 10 * (i // 10), column=7 + 10 * (i // 10), columnspan=3)

                bt.grid(row=n + 1, column=2, columnspan=3)
                z_window.mainloop()

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
                        activeforeground='black', command = self.calculate)
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

    def calculate(self):
        if self.process.dimension == 2:
            S_0 = []
            obs_area_0 = []
            obs_area_g = []
            t_a = 0
            t_b = 0
            m_0_points = []
            m_g_points = []

            if len(self.rectangle) != 0:
                x_rect = self.rectangle[0]
                y_rect = self.rectangle[0]
                S_0 = [[0, 0], [0, y_rect], [x_rect, y_rect], [x_rect, 0]]
                x_subrect = self.subrectangle[0]
                y_subrect = self.subrectangle[1]
                obs_area_0 = [[0, 0], [0, y_subrect], [x_subrect, y_subrect], [x_subrect, 0]]
            else:
                for i in range(0, len(self.arrS0x2)):
                    S_0.append([self.arrS0x2[i], self.arrS0y2[i]])
                for i in range(0, len(self.subx2)):
                    obs_area_0.append([self.subx2[i], self.suby2[i]])
            for i in range(0, len(self.contour_x)):
                obs_area_g.append([self.contour_x[i], self.contour_y[i]])
            t_a = self.t1
            t_b = self.t2

            for i in range(0, len(self.M0x2)):
                m_0_points.append([self.M0x2[i], self.M0y2[i], self.M0z2[i]])
            for i in range(0, len(self.Mgx2)):
                m_g_points.append([self.Mgx2[i], self.Mgy2[i], self.Mgz2[i]])

            c = core.core()
            c.set_T(self.process.T)
            c.set_S_0(S_0)
            if self.process.func == "x+y+t":
                func_tmp = lambda x, y, t: x + y + t
                c.set_observation_function(func_tmp)
            elif self.process.func == "t*(sin(x)+cos(y))":
                func_tmp = lambda x, y, t: t * (np.sin(x) + np.cos(y))
                c.set_observation_function(func_tmp)
            elif self.process.func == "0.001*cos(x)*cos(y)*cos(t)":
                func_tmp = lambda x, y, t: 0.001 * np.cos(x) * np.cos(y) * np.cos(t)
                c.set_observation_function(func_tmp)
            else:
                func_tmp = lambda x, y, t: 0
                c.set_observation_function(func_tmp)

            if self.process.green == "1/(2*pi)*ln(1/r)":
                func_tmp = lambda x, y, t: 1 / (2 * math.pi) * math.log(1 / math.sqrt(x ** 2 + y ** 2))
                c.set_green_function(func_tmp)
            elif self.process.green == "H(t-r/c)/(2*pi*c*sqrt(c^2*t^2-r^2))":
                cons = self.process.const
                func_tmp = lambda x, y, t: np.heaviside(t - math.sqrt(x ** 2 + y ** 2) / cons, 1) / (
                            2 * math.pi * cons * math.sqrt(cons ** 2 * t ** 2 - (x ** 2 + y ** 2) ** 2))
                c.set_green_function(func_tmp)
            else:
                func_tmp = lambda x, y, t: 0
                c.set_green_function(func_tmp)

            c.push_observation_area([obs_area_0, [0.0, 0.0]])
            c.push_observation_area([obs_area_g, [t_a, t_b]])
            c.set_m0_size(len(m_0_points))
            for i in range(0, len(m_0_points)):
                c.push_modeling_point(m_0_points[i])
            for i in range(0, len(m_g_points)):
                c.push_modeling_point(m_g_points[i])

            c.solve()
            c.print_py_plot(0)
            c.print_py_plot(t_a)
            c.print_py_plot((t_a + t_b) * 0.5)
            c.print_py_plot(t_b)
        else:
            c = core.core()
            c.set_dimension(1)
            c.set_arrS01(self.arrS01)
            c.set_arrG1(self.arrG1)
            c.set_subS01(self.subS01)
            print(self.M0x1, self.M0y1)
            c.set_M0(self.M0x1, self.M0y1)
            print(self.Mgx1, self.Mgy1)
            c.set_Mg(self.Mgx1, self.Mgy1)
            c.set_t_dim_1(self.t1, self.t2)
            c.set_T(self.process.T)

            if self.process.func == "x+t":
                func_tmp = lambda x, t: x + t
                c.set_observation_function_dim1(func_tmp)
            elif self.process.func == "sin(x*t)":
                func_tmp = lambda x, t: np.sin(x*t)
                c.set_observation_function_dim1(func_tmp)
            elif self.process.func == "0.001*x":
                func_tmp = lambda x, t: 0.001*x
                c.set_observation_function_dim1(func_tmp)
            elif self.process.func == "0.001*sin(x)":
                func_tmp = lambda x, t: 0.001 * np.sin(x)
                c.set_observation_function_dim1(func_tmp)
            elif self.process.func == "0.001*sin(x)*sin(t)":
                func_tmp = lambda x, t: 0.001 * np.sin(x) * np.sin(t)
                c.set_observation_function_dim1(func_tmp)
            else:
                func_tmp = lambda x, t: x + t
                c.set_observation_function_dim1(func_tmp)

            if self.process.green == "-r/2":
                func_tmp = lambda x, t: - 0.5 * abs(x)
                c.set_green_function_dim1(func_tmp)
            elif self.process.green == "H(t-r/c)/(2*c)":
                cons = self.process.const
                func_tmp = lambda x, t: np.heaviside(t - abs(x) / cons, 0) / (2 * cons)
                c.set_green_function_dim1(func_tmp)
            elif self.process.green == "H(t)/(4*pi*k*t)^(-1/2)*exp((x^2)/4*k*t)":
                cons = self.process.const
                func_tmp = lambda x, t: np.heaviside(t, 0) / (4 * math.pi * cons * t) ** (-0.5) * np.exp((x ** 2) / (4 * cons * t))
                c.set_green_function_dim1(func_tmp)
            else:
                func_tmp = lambda x, t: 0
                c.set_green_function_dim1(func_tmp)

            c.solve_dim1()
            c.print_py_plot_dim1()

gui = GUI()
gui.Window_1()





