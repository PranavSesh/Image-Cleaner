from ctypes import windll
from PIL import Image
import customtkinter as ctk
import tkinter as tk

from PIL.JpegPresets import presets


class Cleaner:
    FONT_TYPE = "Helvetica"
    MAX_ERROR = 10

    def __init__(self):
        self.root = tk.Tk()
        windll.shcore.SetProcessDpiAwareness(1)
        screen_x, screen_y = 1200, 950
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
        self.compare_operator: None | str = None
        self.error: int = 0

        self.slider_vars = {
            "target": [ctk.IntVar() for _ in range(4)],
            "replace": [ctk.IntVar() for _ in range(3)]
        }
        self.comparisons: list[str] = ["<", ">", "="]

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

        filepath_var = ctk.StringVar(value="sample.png")
        filepath_entry = ctk.CTkEntry(file_path_entry_frame,
                                      width=529, height=40,
                                      corner_radius=10,
                                      bg_color="transparent",
                                      fg_color="#5e6063",
                                      text_color="white",
                                      textvariable=filepath_var,
                                      font=(Cleaner.FONT_TYPE, 18))
        filepath_entry.pack(padx=10, pady=10, fill=tk.X)

        slider_page = ctk.CTkFrame(container,
                                   fg_color="grey")
        slider_page.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        presets_page = ctk.CTkFrame(container,
                                    fg_color="light grey")
        presets_page.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        ctk.CTkLabel(slider_page,
                     fg_color="transparent",
                     width=80, height=50,
                     font=(Cleaner.FONT_TYPE, 20),
                     text_color="white",
                     anchor="w",
                     text="Target Color").pack(fill=tk.X, padx=20)

        colors: list[str] = ["red", "green", "blue", "black"]
        for i in range(4):
            slider_frame = ctk.CTkFrame(slider_page,
                                        width=100,
                                        height=50,
                                        corner_radius=0,
                                        bg_color="transparent",
                                        fg_color="transparent")
            slider_frame.pack(fill=tk.X)

            if i == 3:
                ctk.CTkLabel(slider_frame,
                             width=100,
                             height=30,
                             text_color="white",
                             text="Error",
                             anchor="w",
                             font=(self.FONT_TYPE, 20)).pack(fill=tk.X, padx=20)

            ctk.CTkSlider(slider_frame,
                          width=200, height=30,
                          bg_color="transparent",
                          fg_color="white",
                          from_=0,
                          to=255 if i < 3 else self.MAX_ERROR,
                          number_of_steps=255,
                          progress_color=colors[i],
                          corner_radius=0,
                          variable=self.slider_vars["target"][i]).pack(padx=20, side=tk.LEFT, fill=tk.X, expand=True)

            ctk.CTkEntry(slider_frame,
                         width=60, height=20,
                         corner_radius=10,
                         bg_color="transparent",
                         fg_color="#5e6063",
                         text_color="white",
                         textvariable=self.slider_vars["target"][i],
                         font=(Cleaner.FONT_TYPE, 18)).pack(padx=10, pady=10, side=tk.RIGHT)

        comparison_button_frame = ctk.CTkFrame(slider_page,
                                               width=100,
                                               height=80,
                                               corner_radius=0,
                                               fg_color="transparent")
        comparison_button_frame.pack(fill=tk.X)

        for i in range(3):
            ctk.CTkButton(comparison_button_frame,
                          text=self.comparisons[i],
                          font=(Cleaner.FONT_TYPE, 30),
                          fg_color="transparent",
                          corner_radius=0,
                          border_width=0,
                          command=lambda j=i: self.set_compare_state(self.comparisons[j])).pack(fill=tk.X,
                                                                                            pady=10,
                                                                                            side=tk.LEFT,
                                                                                            expand=True)

        ctk.CTkLabel(slider_page,
                     fg_color="transparent",
                     width=80, height=50,
                     font=(Cleaner.FONT_TYPE, 20),
                     text_color="white",
                     anchor="w",
                     text="Replace Color").pack(fill=tk.X, padx=20)

        for i in range(3):
            slider_frame = ctk.CTkFrame(slider_page,
                                        width=100,
                                        height=50,
                                        corner_radius=0,
                                        bg_color="transparent",
                                        fg_color="transparent")
            slider_frame.pack(fill=tk.X)

            ctk.CTkSlider(slider_frame,
                          width=200, height=30,
                          bg_color="transparent",
                          fg_color="white",
                          from_=0,
                          to=255,
                          number_of_steps=255,
                          progress_color=colors[i],
                          corner_radius=0,
                          variable=self.slider_vars["replace"][i]).pack(padx=20, side=tk.LEFT, fill=tk.X, expand=True)

            ctk.CTkEntry(slider_frame,
                         width=60, height=20,
                         corner_radius=10,
                         bg_color="transparent",
                         fg_color="#5e6063",
                         text_color="white",
                         textvariable=self.slider_vars["replace"][i],
                         font=(Cleaner.FONT_TYPE, 18)).pack(padx=10, pady=10, side=tk.RIGHT)

        ctk.CTkButton(presets_page,
                      text="Clean",
                      command=self.clean).pack()

        # # image = ctk.CTkImage(light_image=Image.open(self.filepath_entry.get()),
        # #                      dark_image=Image.open(self.filepath_entry.get()),
        # #                      size=(200, 200))
        # #
        # # ctk.CTkLabel(self.root, text="", image=image).pack()
        #
        # self.slider_frame_holder = ctk.CTkFrame(self.root,
        #                                         width=900,
        #                                         height=800,
        #                                         fg_color="transparent")
        # self.slider_frame_holder.pack()
        #

        #
        # for i in range(7):
        #     slider_frame = ctk.CTkFrame(self.slider_frame_holder,
        #                                 width=800,
        #                                 height=200,
        #                                 corner_radius=0,
        #                                 bg_color="transparent")
        #     slider_frame.grid(column=0 if i < 4 else 1, row=i % 4)
        #
        #     if ((i % 3 == 0) if i < 4 else (i % 7 == 0)) and i > 0:
        #         ctk.CTkLabel(slider_frame,
        #                      width=200,
        #                      height=30,
        #                      text_color="white",
        #                      text="Error",
        #                      font=(self.FONT_TYPE, 20)).pack()
        #
        #     progress_color = ""
        #     if i == 0 or i == 4:
        #         progress_color = "red"
        #     elif i == 1 or i == 5:
        #         progress_color = "green"
        #     elif i == 2 or i == 6:
        #         progress_color = "blue"
        #
        #     ctk.CTkSlider(slider_frame,
        #                  width=300, height=30,
        #                  bg_color="transparent",
        #                   fg_color="white",
        #                   from_=0,
        #                   to=255 if ((i != 3) if i < 4 else (i != 7)) else self.MAX_ERROR,
        #                   number_of_steps=255,
        #                   progress_color=progress_color,
        #                  corner_radius=0,
        #                  variable=self.slider_vars["target" if i < 4 else "replace"][i % 4]).pack(padx=10, side=tk.LEFT)
        #
        #     ctk.CTkEntry(slider_frame,
        #                    width=60, height=20,
        #                    corner_radius=10,
        #                    bg_color="transparent",
        #                    fg_color="#5e6063",
        #                    text_color="white",
        #                    textvariable=self.slider_vars["target" if i < 4 else "replace"][i % 4],
        #                    font=(Cleaner.FONT_TYPE, 18)).pack(padx=10, pady=10, side=tk.RIGHT)
        #
        # ctk.CTkButton(self.root,
        #               text="Clean",
        #               font=(Cleaner.FONT_TYPE, 25),
        #               width=100, height=50,
        #               command=self.clean).pack()

    def set_compare_state(self, operator: str):
        print("Test:", operator)
        self.compare_operator = operator

    def compare_func(self, num1: int, num2: int):
        pass

    def clean(self):
        self.img = None
        self.rgba = None
        self.image_datas = None
        self.post_data = []

        self.target_color = (
            self.slider_vars["target"][0].get(),
            self.slider_vars["target"][1].get(),
            self.slider_vars["target"][2].get(),
            255)

        self.replace_color = (
            self.slider_vars["replace"][0].get(),
            self.slider_vars["replace"][1].get(),
            self.slider_vars["replace"][2].get(),
            255
        )

        print(self.target_color, "Error:", self.slider_vars["target"][3].get(), self.replace_color)
        print(self.compare_operator)
        # try:
        #     filepath_str = self.filepath_entry.get().strip()
        #     self.img = Image.open(filepath_str)
        # except OSError:
        #     print("Invalid file path")
        #     return
        #
        # self.rgba = self.img.convert('RGBA')
        # self.image_datas = self.rgba.getdata()
        #
        # self.error = 10
        # for pixel in self.image_datas:
        #     # if (abs(pixel[0] - self.target_color[0]) < self.error and
        #     #     abs(pixel[1] - self.target_color[1]) < self.error and
        #     #     abs(pixel[2] - self.target_color[2]) < self.error
        #             # and pixel[3] == self.target_color[3]
        #     # ):
        #     if (pixel[3] > 0
        #      ):
        #         self.post_data.append(self.replace_color)
        #     else:
        #         self.post_data.append(pixel)
        #
        #
        # self.rgba.putdata(self.post_data)
        # split_path = self.filepath_entry.get().split(".")
        # image_name = split_path[-2]
        # self.rgba.save(f'./{image_name}_cleaned.png', 'PNG')
        # print("Cleaned image outputted")


if __name__ == '__main__':
    app = Cleaner()
    app.root.mainloop()
