import tkinter as tk
from tkinter import colorchooser
from tkinter import filedialog
import csv

DATA_TO_CHANGE = dict()

############################
#Insert here a palette path#
PALETTE_PATH = ''
############################


import tkinter as tk

class ButtonCatia(tk.Button):
    def __init__(self, master, type: str, text: str, command, width=7):
        super().__init__(master=master)
        self.type = type
        self.text = text
        self.command = command
        self.width = width
        self.apply_styles()
        self.bind("<Enter>", self._set_button_color_hover)
        self.bind("<Leave>", self._set_button_color_normal)

    def apply_styles(self): 
        self.configure(text = self.text)
        self.configure(relief=tk.RIDGE)
        self.configure(borderwidth=0.5)
        self.configure(font=("Roboto", 10))
        self.configure(width=self.width)
        self.configure(command=self.command)

        if self.type == 'blue':
            self.configure(activebackground = '#005686')
            self.configure(bg="#42A2DA")
            self.configure(activeforeground='#FFFFFF')
            self.configure(fg='#FFFFFF')
            self.configure(font=("Roboto", 10, "bold"))
        


    def _set_button_color_hover(self, event):
        if self.type == 'blue':
            event.widget.config(bg="#368EC4")

    def _set_button_color_normal(self, event):
        if self.type == 'blue':
            event.widget.config(bg="#42A2DA")


class CheckbuttonCatia(tk.Checkbutton):
    def __init__(self, master, text: str, state=False):
        super().__init__(master=master)
        self.text = text
        self.bind("<ButtonRelease-1>", self._set_checkbox_color)
        self.state = state
        self.configure(variable=self.state)
        self.configure(text=self.text)

    def _set_checkbox_color(self, event):
        if self.state:
            event.widget.config(selectcolor="#FFFFFF")
            self.state = False
        else:
            event.widget.config(selectcolor="#42A2DA")
            self.state = True

class PaletteCollorSelector:
        def __init__(self, root):
            self.root = root
            screen_width = root.winfo_screenwidth()
            screen_height = root.winfo_screenheight()
            center_x = int(screen_width/2 - 250)
            center_y = int(screen_height/2 - 150)
            root.geometry(f"+{center_x}+{center_y}")
            root.resizable(0, 0)

            self.root.title("Palette Color Selector")
            root.font=("Roboto", 10)
            self._create_widgets()


class PaletteCollorSelector:
        def __init__(self, root, palette_fields, data_dict, file_path):
            self.root = root
            self.file_path = file_path
            self.palette_fields = palette_fields
            self.data_dict = data_dict
            screen_width = root.winfo_screenwidth()
            center_x = int(screen_width/2 - 250)
            self.root.geometry(f"+{center_x}+{50}")
            self.root.resizable(0, 0)

            self.root.title("Palette Color Selector")
            # photo = tk.PhotoImage(file = sources.compas_icon)
            # self.root.iconphoto(False, photo)
            self.root.font=("Roboto", 10)
            self._create_widgets()

        def _create_widgets(self):
            self.file_label = tk.Label(self.root, text='Choose a palette field')
            self.file_label.grid(row=0, column=0, padx=10, pady=5, sticky=tk.EW)

            self.chosen_field = tk.StringVar(self.root)
            self.attribute_list = tk.Listbox(self.root, listvariable=self.chosen_field, activestyle='none',  highlightcolor='#B4B6BA', selectbackground='#42A2DA', height=20, width=35, relief='groove', border=0.5)
            [self.attribute_list.insert(tk.END, i) for i in self.palette_fields]
            self.attribute_list.grid(row=1, column=0, rowspan=100, padx=10, pady=10, sticky=tk.N+tk.S)
            self.attribute_list.select_set(0) #This only sets focus on the first item.
            self.attribute_list.bind("<<ListboxSelect>>", func=self._draw_palette)
            self.attribute_list.select_set(0) #This only sets focus on the first item.

            self.color_frame = tk.Frame(self.root)
            self.color_frame.grid(row=1, column=1, rowspan=100, columnspan=2, padx=10, pady=10, sticky=tk.N+tk.S)            
            self.start_palette_label = tk.Label(self.color_frame, text="Choose a field to explore palette")
            self.start_palette_label.grid(row=1, column=1, columnspan=2, padx=10, pady=10, sticky=tk.N)


            ok_button = ButtonCatia(self.root, type='blue', text="OK", command=self._write_new_pallete)
            ok_button.grid(row=102, column=1, padx=0, pady=10)

            cancel_button = ButtonCatia(self.root, type='gray', text="Cancel", command=self.root.destroy)
            cancel_button.grid(row=102, column=2, padx=10, pady=10)

        def _write_new_pallete(self):
            new_csv = []
            with open(self.file_path, 'r') as outf:
                reader = csv.reader(outf)
                for line in reader:
                    new_csv.append(line)


            with open(self.file_path, 'w', newline='') as outf:
                writer = csv.writer(outf)
                for i, line in enumerate(new_csv):
                    if i in DATA_TO_CHANGE.keys():
                        writer.writerow(line[:3] + DATA_TO_CHANGE[i])
                    else:
                        writer.writerow(line)
            self.root.destroy()
        
        def _draw_palette(self, event):
            # print(self.data_dict)
            self.color_frame.destroy()
            field_name = self.attribute_list.get(self.attribute_list.curselection()[0])
            self.color_frame = tk.Frame(self.root)
            self.color_frame.grid(row=1, column=1, rowspan=100, columnspan=2, padx=10, pady=10, sticky=tk.N+tk.S) 
            # pixel = tk.PhotoImage(width=70, height=10)
            color_list = self.data_dict[field_name][:-1] if self.data_dict[field_name][-1][1] == '' else self.data_dict[field_name]
            is_numeric = self.data_dict[field_name][-1][1] == ''
            for i, value in enumerate(color_list):
                # print(value)
                color = value[1] if value[2] not in DATA_TO_CHANGE.keys() else DATA_TO_CHANGE[value[2]][0]
                text_label = f'{value[0]} -> {self.data_dict[field_name][i+1][0]}' if is_numeric else value[0]
                tk.Label(self.color_frame, text=text_label, font=("Roboto", 8)).grid(row=i+1, column=1, padx=10, pady=1)
                tk.Button(self.color_frame, name=f'color_button_{i}', command=lambda values=[i, value, field_name, self.data_dict[field_name][-1]]: self.get_color(values), bg=color, width=10, relief='flat', border=0).grid(row=i+1, column=2, padx=10, pady=1, sticky=tk.N)

        def get_color(self, values):
            color = colorchooser.askcolor()[1]
            tk.Button.nametowidget(self.color_frame, name=f'color_button_{values[0]}').config(bg=color)
            DATA_TO_CHANGE[values[1][2]] = [color]
            # print(DATA_TO_CHANGE)


class PaletteFileSelector:
    def __init__(self, root):
        self.root = root
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        center_x = int(screen_width/2 - 250)
        center_y = int(screen_height/2 - 150)
        root.geometry(f"+{center_x}+{center_y}")
        root.resizable(0, 0)

        self.root.title("Palette File Selector")
        root.font=("Roboto", 10)
        # print(type(temp_file_path))
        self._create_widgets()

    def _create_widgets(self):
        self.file_label = tk.Entry(self.root, width=40)
        self.file_label.grid(row=0, column=0, columnspan=5, padx=10, pady=5, sticky=tk.EW)
        file_button = ButtonCatia(self.root, type='gray', text="Select File", command=self._open_file_dialog, width=12)
        file_button.grid(row=0, column=5, columnspan=2, padx=10, pady=5, sticky=tk.EW)

        # self.remember_checkbox = CheckbuttonCatia(self.root, text="Remember palette file")
        # self.remember_checkbox.grid(row=1, column=0, columnspan=4, sticky='W', padx=5, pady=15)

        ok_button = ButtonCatia(self.root, type='blue', text="OK", command=self._show_ok_window)
        ok_button.grid(row=2, column=5, padx=0, pady=10)
        cancel_button = ButtonCatia(self.root, type='gray', text="Cancel", command=self.root.destroy)
        cancel_button.grid(row=2, column=6, padx=10, pady=10)
        if PALETTE_PATH != '':
            self.file_path = PALETTE_PATH
            self._show_ok_window()

    def _open_file_dialog(self):
        # file_path = filedialog.askopenfilename(initialdir="C:\\Users\\DMH5\\AppData\\Local\\DassaultSystemes\\CATTemp", defaultextension=".csv", filetypes=[("Palette files", "*.csv")])
        self.file_path = filedialog.askopenfilename(defaultextension=".csv", filetypes=[("Palette files", "*.csv")])
        self.file_label.delete(0, len(self.file_label.get()))
        self.file_label.insert(0, self.file_path)

    def _show_ok_window(self):
        with open (self.file_path, 'r') as file:
            csvreader = csv.reader(file)
            next(csvreader, None)
            temp_list = []
            data_dict = dict()
            for i, row in enumerate(csvreader):
                if row[1] != '' and len(temp_list) == 0:
                    temp_list.append([row[2], row[3], i+1])
                    data_dict[row[1]] = temp_list
                elif row[1] == '':
                    temp_list.append([row[2], row[3], i+1])
                else:
                    temp_list = []
                    temp_list.append([row[2], row[3], i+1])
                    data_dict[row[1]] = temp_list
        palette_fields = list(data_dict.keys())
        DATA_TO_CHANGE = dict()
        # if self.remember_checkbox.getboolean(self.remember_checkbox.state):
        #     with open (os.path.join(os.path.dirname(self.file_path), "temp_bool_palette_script.txt"), "w") as temp_file:
        #         writer = csv.writer(temp_file)
        #         writer.writerow([self.file_path])

        self.root.destroy()

        root = tk.Tk()
        app = PaletteCollorSelector(root, palette_fields, data_dict, self.file_path)
        root.mainloop()

root = tk.Tk()
app = PaletteFileSelector(root)

root.mainloop()
