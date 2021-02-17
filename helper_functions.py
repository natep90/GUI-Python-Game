import tkinter as tk
import pickle
from PIL import Image, ImageTk

# function for creating an empty container frame (in to which the various pages are built)
def create_frame(root):
    container = tk.Frame(root) # create container frame
    container.pack(side="top", fill="both", padx=5, pady=5) # pack container
    container.config(bg="darkblue") # set container background
    container.rowconfigure(0, weight=1) # set first row weight to 1
    container.columnconfigure(0, weight=1) # set first column weight to 1
    return container

# function to create the main title area for a page - container and label text passed in
def create_main_label(container, label_text):
    label = tk.Label(container, text=label_text, fg="white", bg="gray16", relief="ridge", height=4, width=28, font="Roboto 18 bold")
    # create label and add into container using grid method
    label.grid(row=0, column=0, columnspan=4, sticky="nsew", padx=5, pady=5)
    return label

# function to create image in top right of page - container and image file path
def create_side_image(container, image_file):
    img = Image.open("./images/"+image_file) # open image from /images folder
    img = img.resize((167, 178), Image.ANTIALIAS) # set image size/dimensions
    image = ImageTk.PhotoImage(img)
    image_lbl = tk.Label(container, image=image)
    image_lbl.image = image
    image_lbl.grid(row=0, column=4, columnspan=2, padx=5, pady=5, sticky="nsew")

# delete frame (frame deleted when moving to new page)
# will be recreated with updated variables when called again (on button click events)
def delete_frame(frame):
    frame.grid_forget()
    frame.destroy()

# load player and game state from the .bin file selected ('game')
def load_player(game):
    global player
    loaded_game = open(game, "rb") 
    player = pickle.load(loaded_game) 

