import tkinter as tk
from tkinter import*
from tkinter import ttk
from tkinter.ttk import Combobox

class GUI:
    def __init__(self):
        self.root = Tk()
        self.root.title('Дискретні спостереження для неперервних функцій')
        self.root.geometry('700x500+300+60')
        self.frame1 = Frame(self.root)
        self.frame1.pack(side=TOP)
        self.list_dimensionally = Combobox(self.frame1, values=(1, 2),width=5)
        self.list_process=Combobox(self.root, values=('гіперболічний','параболічний'),justify=CENTER)
        text1 = Label(self.frame1, text='Pозмірність просторової області= ',
                        width=30, height=1, font=('Times',15)).grid(column=0,row=0)
        text2 = Label(self.frame1, text='Pозмірність часової області = 1',
                        width=30, height=1,font=('Times',13)).grid(column=0, row=1)
        text3 = Label(self.root, text='Оберіть процес:',
                       width=30, font=('Arial,20')).pack(side=TOP, padx=10, pady=10)
        self.button_OK = Button(self.root, text='Застосувати', width=14, height=1, font=('Times', 10), bg='white', fg='black',)
        self.button_OK.bind('<Button-1>', self.click_button_OK)

    def click_button_OK(self,event):
        win_2=Toplevel(self.root)




    def draw_widgets(self):
        self.list_dimensionally.current(0)
        self.list_dimensionally.grid(column=1, row=0)
        self.list_process.pack(side=TOP,padx=10, pady=0)
        self.button_OK.pack(side=TOP, padx=10, pady=80)
    def show_w(self):
        self.root.mainloop()

f=GUI()
f.draw_widgets()
f.show_w()



