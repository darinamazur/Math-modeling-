import tkinter as tk

brands = ["Bugatti","VW","Opel","Porsche"]
models = [["Veyron","Chiron"],
          ["Golf","Passat","Polo","Caddy"],
          ["Insignia","Corsa","Astra"],
          ["Taycan","Cayenne","911"]]

root = tk.Tk()
canvas = tk.Canvas(root, height=500, width= 500, bg="white")
canvas.pack()

tkvar = tk.StringVar(root)
tkvar.set('Choose')

tkvar2 = tk.StringVar(root)
tkvar2.set('Model')

popupMenu1 = tk.OptionMenu(canvas, tkvar, *brands)
popupMenu1.pack()


popupMenu2 = tk.OptionMenu(canvas, tkvar2, [])
popupMenu2.pack()

def change_dropdown(*args):

    print("Chosen brand " + tkvar.get())
    for i in range(len(brands)):
        if tkvar.get() == brands[i]:
            popupMenu2["menu"].delete(0, "end")
            for item in models[i]:
                   popupMenu2['menu'].add_command(label=item, command=tk._setit(tkvar2, item))


tkvar.trace('w', change_dropdown)
root.mainloop()