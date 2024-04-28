import tkinter
import tkinter.messagebox
from tkinter import Tk, font 
import customtkinter
from PIL import Image

customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("Team PhotoLab")
        self.geometry(f"{1920}x{1080}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)  # Allow column 1 to expand horizontally
        self.grid_columnconfigure((2, 3), weight=0)  # Columns 0, 2, and 3 remain fixed
        self.grid_rowconfigure((0, 1, 2, 3), weight=1)  # All rows expand vertically

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="PoseFit Trainer", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.radiobutton_frame = customtkinter.CTkFrame(self)
        self.radiobutton_frame.grid(row=1, column=0, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.radio_var = tkinter.IntVar(value=0)
        self.label_radio_group = customtkinter.CTkLabel(master=self.radiobutton_frame, text="Your Workout:")
        self.label_radio_group.grid(row=2, column=0, columnspan=1, padx=10, pady=10, sticky="")
        self.sidebar_button_1 = customtkinter.CTkRadioButton(master=self.radiobutton_frame, variable=self.radio_var, value=0, text="Squat", command=self.sidebar_button_event_squat)
        self.sidebar_button_1.grid(row=3, column=0, pady=10, padx=20, sticky="n")
        self.sidebar_button_2 = customtkinter.CTkRadioButton(master=self.radiobutton_frame, variable=self.radio_var, value=1, text="Pullup", command=self.sidebar_button_event)
        self.sidebar_button_2.grid(row=4, column=0, pady=10, padx=20, sticky="n")
        self.sidebar_button_3 = customtkinter.CTkRadioButton(master=self.radiobutton_frame, variable=self.radio_var, value=2, text="Pushup", command=self.sidebar_button_event)
        self.sidebar_button_3.grid(row=5, column=0, pady=10, padx=20, sticky="n")

        # create slider for joint angle
        self.slider_progressbar_frame = customtkinter.CTkFrame(self)
        self.slider_progressbar_frame.grid(row=2, column=0, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.slider_progressbar_frame.grid_columnconfigure(0, weight=1)
        self.slider_progressbar_frame.grid_rowconfigure(2, weight=1)
        self.slider_1 = customtkinter.CTkSlider(self.slider_progressbar_frame, from_=0, to=180, number_of_steps=180)
        self.slider_1.grid(row=1, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")
        self.slider_label = customtkinter.CTkLabel(self.slider_progressbar_frame, text=f"Joint Angle: {self.slider_1.get():.0f} degree", anchor="w")
        self.slider_label.grid(row=0, column=0, padx=20, pady=(10, 0))

        # create settings frame with widgets
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=6, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=7, column=0, padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=8, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=9, column=0, padx=20, pady=(10, 20))

        # Create CTkImage
        self.my_image = customtkinter.CTkImage(light_image=Image.open("test.jpg"),
                                          dark_image=Image.open("test.jpg"), size=(1280, 720))
        self.my_image_label = customtkinter.CTkLabel(self, image=self.my_image, text="")
        self.my_image_label.grid(row=0, rowspan=6, column=1, padx=(20, 0), pady=(20, 0), sticky="n")

        # create textbox
        self.textbox = customtkinter.CTkTextbox(self, width=250, height=30)
        self.textbox.grid(row=3, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")

        # set default values
        self.appearance_mode_optionemenu.set("Dark")
        self.scaling_optionemenu.set("100%")

    def open_input_dialog_event(self):
        dialog = customtkinter.CTkInputDialog(text="Type in a number:", title="CTkInputDialog")
        print("CTkInputDialog:", dialog.get_input())

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def sidebar_button_event(self):
        self.my_image.configure(light_image=Image.open("test_image_1.jpg"))
        self.my_image.configure(dark_image=Image.open("test_image_1.jpg"))

    def sidebar_button_event_squat(self):
        self.textbox.insert("0.0", "You're squatting right now, we will watch over your form!\n")
        self.my_image.configure(light_image=Image.open("test_image.jpg"))
        self.my_image.configure(dark_image=Image.open("test_image.jpg"))

    def change_image(self, image):
        self.my_image.configure(light_image=image)
        self.my_image.configure(dark_image=image)


if __name__ == "__main__":
    app = App()
    while True:
        app.update()
    
    # app.mainloop()