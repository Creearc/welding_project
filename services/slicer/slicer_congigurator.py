import tkinter as tk

master = tk.Tk()

settings = []

settings.append(["Пропустить точки вначале",
                 "skip_start",
                 tk.IntVar()])
settings.append(["Пропустить точки вконце"] = tk.IntVar()

settings.append(["Скорость после наплавки, до сканирования"] = tk.IntVar()
settings.append(["Скорость сканирования"] = tk.IntVar()

settings.append(["sensor_x"] = tk.IntVar()
settings.append(["sensor_y"] = tk.IntVar()
settings.append(["sensor_z"] = tk.IntVar()


def save_data():
    global settings

    with open('config.py', 'w') as f:
        f.write('''settings = dict()\n''')

        for key, element in settings.items():
            f.write('''settings["{}"] = {}\n'''.format(key, element.get()))


try:
    
    master.title("Sensor configurator")


    tk.Button(master, text="Сохранить настройки", bg="white",
            width=20, height=3, command=save_data).grid(row=5, column=0)

    master.mainloop()


except KeyboardInterrupt:
    master.destroy()
