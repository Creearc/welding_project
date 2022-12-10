import tkinter as tk

master = tk.Tk()

settings = []

settings.append(["Первые несколько слоев со смещением по Z",
                 "first_layers",
                 tk.IntVar()])
settings[-1][-1].set(5)

settings.append(["Смещение по Z",
                 "first_layers_z",
                 tk.IntVar()])
settings[-1][-1].set(5)

settings.append(["Пропустить точки вначале",
                 "skip_start",
                 tk.IntVar()])
settings[-1][-1].set(5)

settings.append(["Пропустить точки в конце",
                 "skip_end",
                 tk.IntVar()])
settings[-1][-1].set(5)

settings.append(["Скорость после наплавки, до сканирования",
                 "start_speed",
                 tk.IntVar()])
settings[-1][-1].set(50)

settings.append(["Скорость сканирования",
                 "speed",
                 tk.IntVar()])
settings[-1][-1].set(600)

settings.append(["Координата робота X",
                 "robot_x",
                 tk.IntVar()])
settings[-1][-1].set(-309)

settings.append(["Координата датчика X",
                 "sensor_x",
                 tk.IntVar()])
settings[-1][-1].set(-196)

settings.append(["Координата робота Y",
                 "robot_y",
                 tk.IntVar()])
settings[-1][-1].set(-31)

settings.append(["Координата датчика Y",
                 "sensor_y",
                 tk.IntVar()])
settings[-1][-1].set(-39)

settings.append(["Смещение по Z",
                 "sensor_z",
                 tk.IntVar()])
settings[-1][-1].set(0)


def save_data():
    global settings

    with open('config.py', 'w') as f:
        f.write('''settings = dict()\n''')

        for text, key, value in settings:
            f.write('''settings["{}"] = {}\n'''.format(key, value.get()))
          
try:
    
    master.title("Sensor configurator")

    for i, element in enumerate(settings):
        tk.Label(text=element[0]).grid(row=i, column=0)
        tk.Entry(master, textvariable=element[-1]).grid(row=i, column=1)


    tk.Button(master, text="Сохранить настройки", bg="white",
            width=20, height=3, command=save_data).grid(row=i+1, column=0)

    master.mainloop()


except KeyboardInterrupt:
    master.destroy()
