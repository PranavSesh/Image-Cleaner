from ctypes import windll
from PIL import Image
import customtkinter as ctk
import tkinter as tk
from database import *

class Cleaner:
    FONT_TYPE = "Helvetica"
    MAX_ERROR = 10

    def __init__(self):
        self.root = tk.Tk()
        windll.shcore.SetProcessDpiAwareness(1)
        screen_x, screen_y = 1200, 1000
        self.root.geometry(f'{screen_x}x{screen_y}')
        self.root.configure(bg="#474747")
        self.root.minsize(screen_x, screen_y)
        self.root.maxsize(screen_x, screen_y)
        self.root.title('Image Cleaners')

        self.img: Image = None
        self.rgba: Image = None
        self.image_datas = None
        self.post_data = []

        self.target_color: tuple[int] = (0, 0, 0, 0)
        self.replace_color: tuple[int] = (0, 0, 0, 0)
        self.compare_operator = ctk.StringVar()
        self.compare_operator.set("=")
        self.error: int = 0

        self.slider_vars = {
            "target": [ctk.IntVar() for _ in range(4)],
            "replace": [ctk.IntVar() for _ in range(4)]
        }

        container = ctk.CTkFrame(self.root,
                                 bg_color="transparent",
                                 fg_color="transparent")
        container.pack(fill=tk.BOTH, expand=True)

        file_path_entry_frame = ctk.CTkFrame(container,
                                             width=510, height=300,
                                             bg_color="#90959e",
                                             corner_radius=0)
        file_path_entry_frame.pack()

        ctk.CTkLabel(file_path_entry_frame,
                     text="Image File Path",
                     width=50, height=40,
                     text_color="white",
                     anchor="w",
                     font=(Cleaner.FONT_TYPE, 30)).pack(padx=20, pady=10, side=tk.LEFT)

        self.filepath_var = ctk.StringVar(value="sample.png")
        filepath_entry = ctk.CTkEntry(file_path_entry_frame,
                                      width=529, height=40,
                                      corner_radius=10,
                                      bg_color="transparent",
                                      fg_color="#5e6063",
                                      text_color="white",
                                      textvariable=self.filepath_var,
                                      font=(Cleaner.FONT_TYPE, 18))
        filepath_entry.pack(padx=10, pady=10, fill=tk.X)

        slider_page = ctk.CTkFrame(container,
                                   fg_color="#44464a")
        slider_page.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        presets_page = ctk.CTkFrame(container,
                                    fg_color="#44464a")
        presets_page.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        ctk.CTkLabel(slider_page,
                     fg_color="transparent",
                     width=80, height=50,
                     font=(Cleaner.FONT_TYPE, 20),
                     text_color="white",
                     anchor="w",
                     text="Target Color").pack(fill=tk.X, padx=20)

        # target color inputs
        colors: list[str] = ["red", "green", "blue", "black"]
        for i in range(4):
            slider_frame = ctk.CTkFrame(slider_page,
                                        width=100,
                                        height=50,
                                        corner_radius=0,
                                        bg_color="transparent",
                                        fg_color="transparent")
            slider_frame.pack(fill=tk.X)

            ctk.CTkLabel(slider_frame,
                         text=colors[i][0].upper() + ':' if i < 3 else "   ",
                         font=(Cleaner.FONT_TYPE, 18)).pack(side=tk.LEFT, padx=10)

            if i == 3:
                ctk.CTkLabel(slider_frame,
                             width=100,
                             height=30,
                             text_color="white",
                             text="Error",
                             anchor="w",
                             font=(self.FONT_TYPE, 20)).pack(fill=tk.X, padx=20)

            ctk.CTkSlider(slider_frame,
                          width=400, height=30,
                          bg_color="transparent",
                          fg_color="white",
                          from_=0,
                          to=255 if i < 3 else self.MAX_ERROR,
                          number_of_steps=255,
                          progress_color=colors[i],
                          corner_radius=0,
                          variable=self.slider_vars["target"][i]).pack(padx=10, side=tk.LEFT, fill=tk.X)

            ctk.CTkEntry(slider_frame,
                         width=50, height=20,
                         corner_radius=10,
                         bg_color="transparent",
                         fg_color="#5e6063",
                         text_color="white",
                         textvariable=self.slider_vars["target"][i],
                         font=(Cleaner.FONT_TYPE, 18)).pack(padx=10, pady=10, side=tk.LEFT)

        # frame to hold all button inputs
        comparison_button_frame = ctk.CTkFrame(slider_page,
                                               width=100,
                                               height=80,
                                               corner_radius=0,
                                               fg_color="transparent")
        comparison_button_frame.pack(fill=tk.X, pady=10)

        # comparison button select
        comparisons: list[str] = ["<", ">", "="]
        for i in range(3):
            ctk.CTkButton(comparison_button_frame,
                          width=130,
                          text=comparisons[i],
                          font=(Cleaner.FONT_TYPE, 30),
                          fg_color="transparent",
                          corner_radius=0,
                          border_width=0,
                          hover_color='#333436',
                          command=lambda j=i: self.set_compare_state(comparisons[j])).pack(fill=tk.X,
                                                                                            pady=10,
                                                                                            side=tk.LEFT)
        # shows current comparison button
        ctk.CTkEntry(comparison_button_frame,
                     textvariable=self.compare_operator,
                     state=ctk.DISABLED,
                     border_width=0,
                     width=30,
                     font=(Cleaner.FONT_TYPE, 25)).pack(pady=10, padx=40, fill=tk.BOTH, side=tk.RIGHT)

        # header for replace color
        ctk.CTkLabel(slider_page,
                     fg_color="transparent",
                     width=80, height=50,
                     font=(Cleaner.FONT_TYPE, 20),
                     text_color="white",
                     anchor="w",
                     text="Replace Color").pack(fill=tk.X, padx=20)

        # replace color inputs
        for i in range(4):
            slider_frame = ctk.CTkFrame(slider_page,
                                        width=100,
                                        height=50,
                                        corner_radius=0,
                                        bg_color="transparent",
                                        fg_color="transparent")
            slider_frame.pack(fill=tk.X)

            ctk.CTkLabel(slider_frame,
                         text=(colors[i] if i < 3 else "A")[0].upper() + ':',
                         font=(Cleaner.FONT_TYPE, 18)).pack(side=tk.LEFT, padx=10)

            ctk.CTkSlider(slider_frame,
                          width=400, height=30,
                          bg_color="transparent",
                          fg_color="white",
                          from_=0,
                          to=255,
                          number_of_steps=255,
                          progress_color=colors[i],
                          corner_radius=0,
                          variable=self.slider_vars["replace"][i]).pack(padx=10, side=tk.LEFT, fill=tk.X)

            ctk.CTkEntry(slider_frame,
                         width=60, height=20,
                         corner_radius=10,
                         bg_color="transparent",
                         fg_color="#5e6063",
                         text_color="white",
                         textvariable=self.slider_vars["replace"][i],
                         font=(Cleaner.FONT_TYPE, 18)).pack(padx=10, pady=10, side=tk.LEFT)

        self.presets: list[Preset] = []
        self.presets_frame = ctk.CTkScrollableFrame(presets_page)
        self.presets_frame.pack(fill=tk.BOTH, expand=True)

        # clean button
        ctk.CTkButton(presets_page,
                      width=300,
                      text="Clean",
                      command=self.clean).pack(side=tk.BOTTOM)

        ctk.CTkButton(presets_page,
                      width=300,
                      text="Add Preset",
                      command=self.add_preset).pack(side=tk.BOTTOM)

    def set_compare_state(self, operator: str):
        self.compare_operator.set(operator)

    def compare_func(self, num1: int | float, num2: int) -> bool:
        match self.compare_operator.get():
            case "<":
                return num1 < num2
            case ">":
                return num1 > num2
            case "=":
                return abs(num1 - num2) < self.slider_vars["target"][3].get()
            case _:
                return False

    def add_preset(self):
        target_color = (
            self.slider_vars["target"][0].get(),
            self.slider_vars["target"][1].get(),
            self.slider_vars["target"][2].get())

        replace_color = (
            self.slider_vars["replace"][0].get(),
            self.slider_vars["replace"][1].get(),
            self.slider_vars["replace"][2].get(),
            self.slider_vars["replace"][3].get())

        operator_val = self.compare_operator.get()

        # create preset
        preset = Preset(target_color, replace_color, operator_val)
        add_preset_to_database(preset)

        # get id of preset as set it
        preset.id = get_row_id_from_record(preset)

        preset_back = ctk.CTkFrame(self.presets_frame,
                                   bg_color="white")
        preset_back.pack(fill=tk.X)

        preset.preset_frame = preset_back

        preset.select_button = ctk.CTkButton(preset_back,
                                             text=f"Target: {target_color} E: {self.slider_vars["target"][3].get()}\n"
                                                        f"Replace: {replace_color}\n"
                                                        f"Operator: {operator_val}",
                                             width=220)
        preset.select_button.pack(fill=tk.X, side=tk.LEFT)

        preset.remove_button = ctk.CTkButton(preset_back,
                                             text="-",
                                             width=20,
                                             command=lambda: self.remove_preset(preset))
        preset.remove_button.pack(side=tk.LEFT, fill=tk.Y)

        self.presets.append(preset)

    def remove_preset(self, preset):

        def filter_preset(p):
            if p.id == rowid:
                p.preset_frame.destroy()
            return p.id != rowid

        rowid = get_row_id_from_record(preset)
        delete_preset(rowid)
        self.presets = [preset for preset in filter(filter_preset, self.presets)]

    def clean(self):
        self.img = None
        self.rgba = None
        self.image_datas = None
        self.post_data = []

        self.target_color = (
            self.slider_vars["target"][0].get(),
            self.slider_vars["target"][1].get(),
            self.slider_vars["target"][2].get())

        self.replace_color = (
            self.slider_vars["replace"][0].get(),
            self.slider_vars["replace"][1].get(),
            self.slider_vars["replace"][2].get(),
            self.slider_vars["replace"][3].get())

        try:
            filepath_str = self.filepath_var.get().strip()
            self.img = Image.open(filepath_str)
        except OSError:
            print("Invalid file path")
            return

        self.rgba = self.img.convert('RGBA')
        self.image_datas = self.rgba.getdata()

        for pixel in self.image_datas:
            if self.compare_func(pixel[0], self.slider_vars["target"][0].get()) and \
                    self.compare_func(pixel[1], self.slider_vars["target"][1].get()) and \
                    self.compare_func(pixel[2], self.slider_vars["target"][2].get()):
                self.post_data.append(self.replace_color)
            else:
                self.post_data.append(pixel)

        self.rgba.putdata(self.post_data)
        split_path = self.filepath_var.get().split(".")
        self.rgba.save(f'./{split_path[-2]}_cleaned.png', 'PNG')
        print("Cleaned image outputted")


if __name__ == '__main__':
    app = Cleaner()
    app.root.mainloop()
    sql_connection.close()