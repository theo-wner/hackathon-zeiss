"""
Author: Steven
Description:
    - This is a test file for GUI testing
    - It contains an adapted version of this tutorial: https://stackoverflow.com/questions/19838972/how-to-update-an-image-on-a-canvas
    - Instead of using a button to change the image, the image changes automatically every 10ms
    - Later on, this will be used to display the camera feed with the detected keypoints from YOLO
"""

from tkinter import *
import customtkinter

class MainWindow():
    def __init__(self, main):
        # canvas for image
        self.canvas = Canvas(main, width=60, height=60)
        self.canvas.grid(row=0, column=0)
        
        # images
        self.my_images = []
        self.my_images.append(PhotoImage(file="ball1.gif"))
        self.my_images.append(PhotoImage(file="ball2.gif"))
        self.my_images.append(PhotoImage(file="ball3.gif"))
        self.my_image_number = 0
        
        # set first image on canvas
        self.image_on_canvas = self.canvas.create_image(0, 0, anchor='nw', image=self.my_images[self.my_image_number])
        
        # button to change image
        self.button = customtkinter.CTkButton(main, text="Change", command=self.onButton)
        self.button.grid(row=1, column=0)

    def onButton(self):
        # next image
        self.my_image_number += 1

        # return to first image
        if self.my_image_number == len(self.my_images):
            self.my_image_number = 0

        # change image
        self.canvas.itemconfig(self.image_on_canvas, image=self.my_images[self.my_image_number])


    def draw(self, new_image):
        while True:
            self.onButton()
            self.canvas.update()
            self.canvas.after(100)

#-----------------------------------------------------------------------------------------------

customtkinter.set_appearance_mode('dark')
customtkinter.set_default_color_theme('green')

root = customtkinter.CTk()
window = MainWindow(root)
window.draw()
# root.mainloop()