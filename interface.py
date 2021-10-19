import database
import tkinter as tk
from tkinter import*
from tkinter import ttk
from tkinter.ttk import Combobox
from PIL import ImageTk, Image



class GUI:
    def __init__(self):
        self.WIN_1()

    def WIN_1(self):
        self.root = Tk()
        self.root.title('Дискретні спостереження для неперервних функцій')
        self.root.geometry('700x500+300+60')
        self.frame1 = Frame(self.root)
        self.frame1.pack(side=TOP)
        self.list_dimensionally = Combobox(self.frame1, values=(1, 2), width=5)
        self.list_process = Combobox(self.root, values=database.db.SelectProcessName(), justify=CENTER)
        text1 = Label(self.frame1, text='Pозмірність просторової області= ',
                      width=30, height=1, font=('Times', 15)).grid(column=0, row=0)
        text2 = Label(self.frame1, text='Pозмірність часової області = 1',
                      width=30, height=1, font=('Times', 13)).grid(column=0, row=1)
        text3 = Label(self.root, text='Оберіть процес:',
                      width=30, font=('Arial,20')).pack(side=TOP, padx=10, pady=10)
        self.button_OK = Button(self.root, text='Застосувати', width=14, height=1, font=('Times', 10),
                                bg='white', fg='black')
        self.button_OK.bind('<Button-1>', self.click_button_OK)







    def click_button_OK(self,event):
        self.WIN_2()
        dim=self.list_dimensionally.get()
        process=self.list_process.get()
        index_process = database.db.SelectProcessName().index(process)
        diff_operator=database.db.SelectDiffOperator(database.db.SelectProcessName()[index_process], dim)

        #print(str(database.db.SelectDiffOperator(database.db.SelectProcessName()[0], dim)[0]))
        #self.dict_process_ph={str(database.db.SelectDiffOperator(database.db.SelectProcessName()[0], dim)[0]) : 'diff_Laplasa.jpg'}
        text3 = Label(self.root, text='формула диф оператора: ', width=50, font=('Times', 14)).pack(side=TOP)
        text4 = Label(self.root, text=diff_operator, width=50, font=('Times', 14)).pack(side=TOP)
        #dict1={'1':"diff_Laplasa.jpg"}
        #fr=Frame(self.root)
        #fr.pack(side=TOP)
        #image1 = ImageTk.PhotoImage(Image.open("diff_Laplasa1.jpg"))
        #panel1=Label(fr, image=image1).pack(side=TOP)
        #text3 = Label(self.root, text=diff_operator,width=30, font=('Times', 14))


    def WIN_2(self):
        def click_button_OK2():
            self.win_3 = Toplevel(win_2)
            self.WIN_3()

        win_2 = Toplevel(self.root)
        win_2.title('Обрати константу')
        win_2.geometry('450x300+100+120')
        text3 = Label(win_2, text='формула диф оператора: ',
                      width=30, font=('Times',12)).grid(column=0,row=0)
        text4 = Label(win_2, text='C= ',
                      width=10, font=('Times', 12)).grid(column=0, row=1)
        c_entry=Entry(win_2, width=10, font=('Times', 12)).grid(column=1, row=1)
        button_OK2 = Button(win_2, text='Застосувати', width=14, height=1, font=('Times', 10),command=click_button_OK2).grid(column=1, row=2)



    def WIN_3(self):
        self.win_3.title('Початкові значення')
        self.win_3.geometry('500x300+750+120')
        frame1 = Frame(self.win_3)
        frame1.pack(side=TOP)
        text1 = Label(frame1, text="Проміжок часу [0,",
                      width=14, font=('Times', 12), justify=LEFT).grid(column=0, row=0)
        time_entry=Entry(frame1,width=3, font=('Times', 12)).grid(column=1, row=0)
        text2 = Label(frame1, text=']',
                      width=1, font=('Times', 12)).grid(column=2, row=0)

    def draw_widgets(self):
        self.list_dimensionally.current(0)
        self.list_dimensionally.grid(column=1, row=0)
        self.list_process.current(0)
        self.list_process.pack(side=TOP,padx=10, pady=0)
        self.button_OK.pack(side=TOP, padx=10, pady=20)
    def show_w(self):
        self.draw_widgets()
        self.root.mainloop()

f=GUI().show_w()




