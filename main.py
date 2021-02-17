import tkinter as tk
import tkinter.ttk as ttk
from PIL import Image, ImageTk
import glob
import random
import datetime
import time
import pickle
import operator
from story import intro_text
from objects import geography_class, humanities_hallway, history_class, headmasters_office, gym, science_room, music_room
from classes import Player, Consumable, Totem
from helper_functions import create_frame, create_main_label, create_side_image, delete_frame, load_player

# create global player variable to be overwritten in character creation
player = Player('name', 0, geography_class, 'school')

# set variable to adjust colour scheme easily
MAIN_BG_COLOUR = "darkblue"

# create root window, add title, fix size
root = tk.Tk()
root.title("Back to School 2: Electric Boogaloo")
root.config(bg=MAIN_BG_COLOUR)
root.geometry("600x400")
root.resizable(0,0)

def title_page():
    # create container for title page (and pack into root window)
    container = create_frame(root)
    # create main label with text
    create_main_label(container, "BACK TO SCHOOL 2:\n-------------------------------\nELECTRIC BOOGALOO!")
    # create image to be displayed in top right corner
    create_side_image(container, "stationary.jpg")

    # create button to initiate new game - will destroy current page if clicked and navigate to create_character frame
    new_game_button = tk.Button(container, text="NEW GAME", fg="darkgreen", height=4, font="Roboto 12 bold",
        command=lambda: [intro_page(), delete_frame(container)])
    new_game_button.grid(row=1, column=0, columnspan=6, pady=5, padx=5, sticky="nsew")

    # create button to load game(s) - will destroy current page if clicked and navigate to load_game frame
    load_game_button = tk.Button(container, text=f"LOAD GAME", fg="blue", height=4, font="Roboto 12 bold",
                                    command=lambda: [load_game(), delete_frame(container)])
    load_game_button.grid(row=2, column=0, columnspan=6, padx=5, pady=5, sticky="nsew")

    # if there are no saved games (.bin files in the directory), the 'load game' button is disabled
    def disable_button_if_no_saves(button):
        saved_games = glob.glob('*.bin')
        if not saved_games:
            button.config(state="disabled")

    # disable load_game_button if no saves are present
    disable_button_if_no_saves(load_game_button)

def intro_page():
    '''
    explains how the game is to be played
    initiated once the player selects 'new game' on the title_page
    '''
    container = create_frame(root)
    label = tk.Label(container,
    text=intro_text,
    bg="grey16", fg="white", height=45, width=120, font="Roboto 12 bold")
    label.pack()
    next_button = tk.Button(container, text="Continue", fg="darkgreen", width=9, font="Roboto 12 bold", command=lambda: [delete_frame(container), create_character()])
    next_button.place(x=200, y=350)
    back_button = tk.Button(container, text="Back", fg="red", width=9, font="Roboto 12 bold", command=lambda: [delete_frame(container), title_page()])
    back_button.place(x=300, y=350)
    

def load_game():
    global player
    container = create_frame(root)
    create_main_label(container,"Load Game:")
    create_side_image(container, "gym.jpg")

    # get saved games (all .bin files are saved games)
    saved_games = glob.glob('*.bin')

    # create frame to display saved games
    games_frame = tk.Frame(container)
    games_frame.config(bg=MAIN_BG_COLOUR)
    games_frame.grid(row=1, rowspan=4, column=0, columnspan=6, sticky="nsew", padx=5, pady=5)

    # add button for each save - will load game and take player (with saved game state) to main_loop at last location
    for game in saved_games:
        load_game_button = tk.Button(games_frame, text=f"{game.split('.bin')[0]}'s game", height=1, width=12, font="Roboto 12 bold")
        load_game_button["command"] = lambda game=game: [load_player(game), delete_frame(container), main_loop()]
        load_game_button.pack(fill="x", anchor="n")

    return_to_main_menu_button = tk.Button(container, text="Return to Main Menu", height=4, font="Roboto 12 bold", fg="red", command=lambda: [title_page(), delete_frame(container)])
    return_to_main_menu_button.grid(row=6, column=0, columnspan=6, padx=5, pady=5, sticky="nsew")

def create_character():
    container = create_frame(root)
    create_main_label(container, "CREATE YOUR CHARACTER!\n\nCustomisation will affect\nhow the game itself goes!")
    create_side_image(container, "sculpt.jpg")

    # create name entry, label and add via grid method to container
    name_var = tk.StringVar()
    name_label = tk.Label(container, text="Name: ", font="Roboto 11 bold", bg=MAIN_BG_COLOUR, fg="white")
    name_label.grid(row=1, column=0, sticky="E", pady=5)
    name_entry = tk.Entry(container, font=20, width=15, textvariable=name_var, bg="white")
    name_entry.grid(row=1, column=1, sticky="W", pady=5, padx=(0,80))

    # create age spinbox, label and add via grid method to container
    age_label = tk.Label(container, text="Age: ", font="Roboto 11 bold", bg=MAIN_BG_COLOUR, width=3, fg="white")
    age_label.grid(row=1, column=3, pady=5, sticky="E")
    age_var = tk.Spinbox(container, from_=18, to=100, width=3, font="Roboto 11 bold", bg="white")
    age_var.grid(row=1, column=4, sticky="W", pady=5)

    # create school entry, label and add via grid method to container
    school_var = tk.StringVar()
    school_label = tk.Label(container, text="First School: ", font="Roboto 11 bold", bg=MAIN_BG_COLOUR, fg="white", width=12)
    school_label.grid(row=2, column=0, sticky="E", pady=5)
    school_entry = tk.Entry(container, font=20, width=15, textvariable=school_var, bg="white")
    school_entry.grid(row=2, column=1, sticky="W", pady=5, padx=(0,0))

    # create sex radio buttons, label and add via grid method to container
    sex_var = tk.StringVar(value='m')
    sex_label = tk.Label(container, text="Sex: ", font="Arial 11 bold", bg=MAIN_BG_COLOUR, fg="white")
    sex_label.grid(row=2, column=3, pady=5, sticky="E")
    sex_radio_m = tk.Radiobutton(container, text="Male", variable=sex_var, value="m", font="Roboto 11", bg="lightgrey")
    sex_radio_f = tk.Radiobutton(container, text="Female", variable=sex_var, value="f", font="Roboto 11", bg="lightgrey")
    sex_radio_m.grid(row=2, column=4, pady=5, sticky="W")
    sex_radio_f.grid(row=2, column=5, pady=5, sticky="W")

    global player

    # create frame for buttons
    button_frame = tk.Frame(container)
    button_frame.config(bg=MAIN_BG_COLOUR)
    button_frame.grid(row=3, column=0, columnspan=6, sticky="nsew", padx=5, pady=5)

    # overwrites player to create unique player character
    def update_player(name_var, age_var, school_var, sex_var):
        global player
        player.name = name_var.strip().title()
        player.age = int(age_var.strip())
        player.school = school_var.strip().title()
        player.sex = sex_var

    # when play is clicked, the name, sex, school and age entry values are taken and used to update and create new player character
    # starts disabled, only enables when all entries are not empty
    play_button = tk.Button(button_frame, text="Start Game!", height=4, width=18, font="Roboto 12 bold", fg="darkgreen",
                            state="disabled", command=lambda: [update_player(name_var=name_var.get(), age_var=age_var.get(),
                            school_var=school_var.get(), sex_var=sex_var.get()), delete_frame(container), main_loop()])
    play_button.pack(side="left", expand=True, fill="both", padx=5, pady=5)

    # will only enable a button if specified entries are not empty
    def check_if_empty(*args):
        if school_var.get() and name_var.get() and sex_var.get():
            # this block ensures that only an int can be entered as age
            try:
                int(age_var.get())
            except ValueError:
                play_button.config(state="disabled")
            
            play_button.config(state="normal")
        else:
            play_button.config(state="disabled")
        
    # checks entry - and disables/enables based on whether it is empty or not
    school_var.trace("w", check_if_empty)
    name_var.trace("w", check_if_empty)
    sex_var.trace("w", check_if_empty)

    # button to return to main menu
    return_to_main_menu_button = tk.Button(button_frame, text="Return to Main Menu", height=4, fg="red",font="Roboto 12 bold", command=lambda: [title_page(), delete_frame(container)])
    return_to_main_menu_button.pack(side="right", expand=True, fill="both", padx=5, pady=5)

# main in game menu 
def main_loop():
    global player
    # play storyline if player has not visited location before
    if player.location.visited == False:
        storyline()
        # set visited to True so storyline no longer plays if player re enters same location
        player.location.visited = True

    # if player has already visited location, straight to location specific menu    
    else:    
        container = create_frame(root)
        create_main_label(container, f"--- {player.location.name} ---\n\n{player.location.message}" )


        # assign image based on location
        if player.location == geography_class:
            create_side_image(container, "globe.jpg")
        elif player.location == humanities_hallway:
            create_side_image(container, "hallway.jpg")
        elif player.location == history_class:
            create_side_image(container, "old_books.jpg")
        elif player.location == music_room:
            create_side_image(container, "music_room.jpg")
        elif player.location == gym:
            create_side_image(container, "gym.jpg")
        elif player.location == headmasters_office:
            create_side_image(container, "office.jpg")
        elif player.location == science_room:
            create_side_image(container, "lab.jpg")
        else:
            create_side_image(container, "school2.jpg")

        
        
        # create buttons to navigate to connecting rooms
        move_frame = tk.Frame(container)
        move_frame.config(bg=MAIN_BG_COLOUR)
        move_frame.grid(row=1, rowspan=4, column=0, sticky="nsew", padx=5, pady=5)

        move_label = tk.Label(move_frame, text="Move to:", bg=MAIN_BG_COLOUR, font="Roboto 12 bold", fg="white")
        move_label.pack(fill="x", anchor="n", side="top")

        for connection in player.location.connections:
            connection_btn = tk.Button(move_frame, text=connection.name, font="Roboto 12 bold", height=2, width=3)
            connection_btn['command'] = lambda connection=connection: [player.move(connection), delete_frame(container), main_loop()]
            connection_btn.pack(fill="x", anchor="n", pady=2)


        # create buttons to pick up items (and remove item from room once picked up)
        pu_frame = tk.Frame(container)
        pu_frame.config(bg=MAIN_BG_COLOUR)
        pu_frame.grid(row=1, rowspan=4, column=1, sticky="nsew", padx=5, pady=5)

        pick_up_label = tk.Label(pu_frame, text=f"Items:", bg=MAIN_BG_COLOUR, font="Roboto 12 bold", fg="white")
        pick_up_label.pack(fill="x", anchor="n", side="top")

        # add buttons to item frame
        # when button is pressed, item is picked up and the screen is refreshed (so the item is no longer showing)
        for item in player.location.items_to_collect:
            item_btn = tk.Button(pu_frame, text=f"{item.name.title()}", font="Roboto 12 bold", height=2, width=10)
            item_btn["command"] = lambda item=item: [player.pick_up_item(item),
                player.location.items_to_collect.remove(item), delete_frame(container), main_loop()]
            item_btn.pack(fill="x", anchor="n", pady=2)

        # create buttons to quiz with characters
        quiz_frame = tk.Frame(container)
        quiz_frame.config(bg=MAIN_BG_COLOUR)
        quiz_frame.grid(row=1, rowspan=4, column=2, sticky="nsew", padx=5, pady=5)
        quiz_label = tk.Label(quiz_frame, text=f"Quiz:", bg=MAIN_BG_COLOUR, font="Roboto 12 bold", fg="white")
        quiz_label.pack(fill="x", anchor="n", side="top")
        for char in player.location.characters:
            char_btn = tk.Button(quiz_frame, text=char.name, font="Roboto 12 bold", height=2, width=10)
            char_btn['command'] = lambda: [delete_frame(container), quiz()]
            char_btn.pack(fill="x", anchor="n", pady=2)
            if not char.items:
                char_btn.config(state="disabled")

        # creates side menu frame
        side_frame = tk.Frame(container)
        side_frame.config(bg=MAIN_BG_COLOUR)
        side_frame.grid(row=1, rowspan=4, column=4, sticky="nsew", padx=5, pady=5)

        # add buttons to side menu frame
        inventory_btn = tk.Button(side_frame, text="View Inventory", font="Roboto 12 bold", command=lambda: [delete_frame(container), view_inventory()])
        inventory_btn.pack(fill="both", expand=True)
        stats_btn = tk.Button(side_frame, text="Check Stats", font="Roboto 12 bold", command=lambda: [delete_frame(container), check_stats()])
        stats_btn.pack(fill="both", expand=True)
        route_btn = tk.Button(side_frame, text="View Route", font="Roboto 12 bold", command=lambda: [delete_frame(container), view_route()])
        route_btn.pack(fill="both", expand=True)
        save_btn = tk.Button(side_frame, text="Save Game", font="Roboto 12 bold", fg="darkgreen", command=lambda: [save_game()])
        save_btn.pack(fill="both", expand=True)
        return_to_main_menu_button = tk.Button(side_frame, text="Return to Main Menu", font="Roboto 12 bold", fg="purple", command=lambda: [delete_frame(container), title_page()])
        return_to_main_menu_button.pack(fill="both", expand=True)
        exit_btn = tk.Button(side_frame, text="Exit Game", font="Roboto 12 bold", fg="red", command=lambda: [exit_message()])
        exit_btn.pack(fill="both", expand=True)

    # pop up box to confirm whether you want to exit
    def exit_message():
        exit_window = tk.Tk()
        exit_window.title("Caution!")
        label = tk.Label(exit_window, text="Are you sure you want to exit?")
        label.pack(fill="x", side="top", pady=5, padx=5)
        confirm_exit_button = tk.Button(exit_window, text="Yes", command = lambda: [exit_window.destroy(), root.destroy()])
        confirm_exit_button.pack(pady=5, padx=5)
        exit_window.mainloop()

    # pop up box to confirm save game
    def save_game():
        global player
        save_window = tk.Tk()
        save_window.title("Save!")
        label = tk.Label(save_window, text=f"Are you sure you want to save?\n -> ({player.name})")
        label.pack(fill="x", side="top", pady=5, padx=5)
        confirm_button = tk.Button(save_window, text=f"Save Game", command=lambda: [pickle.dump(player, open(f"{player.name.lower()}.bin", "wb")), save_window.destroy()])
        confirm_button.pack(padx=5, pady=5) 
        save_window.mainloop()

# displays storyline if player has not visited a location before
def storyline():
    global player

    container = create_frame(root)
    label = tk.Label(container,
    text=player.location.story,
    bg="grey16", fg="white", height=45, width=120, font="Roboto 12 bold")
    label.pack()
    # takes to main_loop screen for current location
    next_button = tk.Button(container, text="Continue", fg="darkgreen", width=9, font="Roboto 12 bold", command=lambda: [delete_frame(container), main_loop()])
    next_button.place(x=250, y=300) 

# shows route player has travelled
def view_route():
    global player
    container = create_frame(root)
    
    if player.correct_route_direction == True:
        label = tk.Label(container, text=f"From where you started (1)\nto your current location ({len(player.route)})!\n\n", bg="grey16", fg="white", height=45, width=120, font="Roboto 12 bold")
    else:
        label = tk.Label(container, text=f"From your current location (1)\nto where you started ({len(player.route)})!\n\n", bg="grey16", fg="white", height=45, width=120, font="Roboto 12 bold")
    label.pack()
    
    # displays the player route (location by location)
    for i, loc in enumerate(player.route):
        current_text = label.cget("text")
        new_value = current_text + f"{i+1}: {loc}\n"
        label.config(text=new_value)

    # reverse button reverses the route so can see last to first location
    reverse_button = tk.Button(container, text=f"Click to Reverse Order", fg="darkgreen", width=26, font="Roboto 12 bold", command=lambda: [player.reverse_route(), delete_frame(container), view_route()])
    reverse_button.place(x=180, y=300)
    # when player returns to main menu, route_direction is returned to normal (if left in reverse)
    return_to_main_loop_button = tk.Button(container, text=f"Return to {player.location.name}", fg="red", width=26, font="Roboto 12 bold", command=lambda: [player.ensure_correct_route_direction(), delete_frame(container), main_loop()])
    return_to_main_loop_button.place(x=180, y=350)


# frame to view player inventory
def view_inventory():
    global player
    container = create_frame(root)
    create_main_label(container, f"--- {player.name}'s Backpack ---\n\nHealth: {player.health}/{player.max_health}")
    create_side_image(container, "backpack.jpg")

    # creates frame and label to display consumables
    food_frame = tk.Frame(container)
    food_frame.config(bg=MAIN_BG_COLOUR)
    food_frame.grid(row=1, rowspan=3, column=0, sticky="nsew", padx=5, pady=5)
    food_label = tk.Label(food_frame, text=f"Consumables:", bg=MAIN_BG_COLOUR, font="Roboto 12 bold", fg="white")
    food_label.pack(fill="x", anchor="n", side="top")
 

    # create buttons to interact correctly with inventory items - inventory items are in alphabetical order
    inv = sorted(player.items, key=operator.attrgetter('name'))
    for item in inv:
        btn = tk.Button(food_frame, text=f"{item.name.title()} (+{item.value})", font="Roboto 12 bold", width=4)
        # removes item from inventory, adds item.value to player.health and refreshes the inventory screen (this removes the consumed item)
        btn["command"] = lambda item=item: [player.items.remove(item), consume(item), delete_frame(container), view_inventory()]
        btn.pack(fill="x")

    # will consume item when button for that consumable is pressed - adds value of item to player health (maxes out at max health)
    def consume(item):
        global player
        player.health += item.value
        if player.health > player.max_health:
            player.health = player.max_health

    # create totem frame and label in which to display totems
    totem_frame = tk.Frame(container)
    totem_frame.config(bg=MAIN_BG_COLOUR)
    totem_frame.grid(row=1, rowspan=3, column=1, sticky="nsew", padx=5, pady=5)
    totem_label = tk.Label(totem_frame, text=f"Totems:", bg=MAIN_BG_COLOUR, font="Roboto 12 bold", fg="white")
    totem_label.pack(fill="x", anchor="n", side="top")

    # create buttons for each totem - need to add functionality here -> equip or inspect etc
    for item in player.totems:
        btn = tk.Button(totem_frame, text=item.name.title(), command=None, font="Roboto 12 bold", width=4)
        btn.pack(fill="x")       

    # return to current location (main loop)
    return_to_main_loop_button = tk.Button(container, text=f"Return to {player.location.name}", font="Roboto 12 bold", fg="darkgreen", height=2, width=22, command=lambda: [delete_frame(container), main_loop()])
    return_to_main_loop_button.grid(row=7, column=1, padx=5, pady=5, sticky="s")
    
# quiz frame - specific to character in the current location
# will be unavailable if quiz has already been won
def quiz():
    global player
    # set the only character in the room as the 'quizmaster'
    quizmaster = player.location.characters[0]
    container = create_frame(root)
    create_main_label(container, f"--- Quiz with {quizmaster.name}! ---")
    create_side_image(container, "backpack.jpg")

    # choose question randomly from characters questions dictionary
    random_num = random.randint(0, len(quizmaster.questions) - 1)
    random_q = quizmaster.questions[random_num]
    # question is asked (and the corresponding answer(s) are returned)
    for q, a in random_q.items():
        q_label = tk.Label(container, text=f"{quizmaster.name.title()}: {q}", bg=MAIN_BG_COLOUR, font="Roboto 12 bold", fg="white")
        q_label.grid(row=1, column=0, columnspan=6, padx=5, pady=5, sticky="nsew")
        # upon return, a is compared to user_input to determine whether right/wrong
    
    # creates answer field and submit button
    answer = tk.StringVar()
    answer_entry = tk.Entry(container, font=20, width=15, textvariable=answer)
    answer_entry.grid(row=2, column=0, columnspan=3, sticky="nsew", pady=5, padx=5)
    # when submit_button is pressed, answer_entry is compared with correct answer(s)
    submit_button = tk.Button(container, text=f"Submit answer", command=lambda: check_answer(), font="Roboto 12 bold", fg="darkgreen")
    submit_button.grid(row=2, column=4, padx=5, pady=5) 

    # check if the player has answered correctly
    def check_answer():
        # if answer is correct, display message and collect totem
        if answer.get().lower() in a:
            a_label = tk.Label(container, text=f"Correct!\nYou win the {quizmaster.items[0].name} from {quizmaster.name}!", bg="darkgreen", fg="white", font="Roboto 12 bold")
            a_label.grid(row=3, column=0, columnspan=6, padx=5, pady=5, sticky="nsew")
            totem = quizmaster.items.pop()
            player.pick_up_item(totem)
            # button is disabled as quiz is already complete
            submit_button.config(state="disabled")
            # checks if the player now has all totems - if so, game is won and you_win screen displayed
            if len(player.totems) == Totem.totem_count:
                delete_frame(container)
                you_win()
        # if answer is incorrect, take damage, display message and check that player is still alive
        else:
            player.health -= (quizmaster.damage)
            a_label = tk.Label(container, text=f"Incorrect!\n{quizmaster.name} hits you with {quizmaster.weapon}.\n{quizmaster.damage} damage!\nYou now have {player.health}/{player.max_health} health remaining!", bg="darkred", fg="white", font="Roboto 12 bold")
            a_label.grid(row=3, column=0, columnspan=6, padx=5, pady=5, sticky="nsew")
            check_player_health(container)


    # return to current location (main loop)
    return_to_main_loop_button = tk.Button(container, text=f"Return to {player.location.name}", font="Roboto 12 bold", command=lambda: [delete_frame(container), main_loop()])
    return_to_main_loop_button.grid(padx=5, pady=5, row=6, column=2)

# displays player stats - name, age, sex, health, location, school and totems collected    
def check_stats():
    global player
    container = create_frame(root)
    label = tk.Label(container,
    text=f"Name: {player.name}\n\nAge: {player.age}\n\nSex: {player.sex.title()}\n\nHealth: {player.health}/{player.max_health}\n\nLocation: {player.location.name}, {player.school.title()}\n\nTotems: {len(player.totems)}/{Totem.totem_count}",
    bg="grey16", fg="white", height=45, width=120, font="Roboto 12 bold")
    label.pack()
    return_to_main_loop_button = tk.Button(container, text=f"Back to {player.location.name}", fg="red", width=24, font="Roboto 12 bold", command=lambda: [delete_frame(container), main_loop()])
    return_to_main_loop_button.place(x=185, y=330) 

    # image of player shown depends on sex chosen by user
    if player.sex == "m":
        img = Image.open("./images/man.jpg")
    else:
        img = Image.open("./images/woman.jpg") 
    img = img.resize((167, 178), Image.ANTIALIAS)
    image = ImageTk.PhotoImage(img)
    image_lbl = tk.Label(container, image=image)
    image_lbl.image = image
    image_lbl.place(x=10, y=10)

# function to check player health - used in the quiz screen when player gets a question wrong and takes damage
def check_player_health(container):
    global player
    if player.health <= 0:
        delete_frame(container)
        you_died() # sends to you_died screen - then to main menu

# frame will automatically show when player health drops to 0 (or below)
def you_died():
    global player
    time.sleep(1)
    container = create_frame(root)
    create_main_label(container, f"{player.name} is dead. Long live {player.name}!")
    create_side_image(container, "skull.jpg")
    return_to_main_menu_button = tk.Button(container, text="Return to Main Menu", height=4, fg="red",font="Roboto 12 bold", command=lambda: [title_page(), delete_frame(container)])
    return_to_main_menu_button.grid(padx=5, pady=5)

# frame will automatically show when player wins game (all totems are collected)
def you_win():
    global player
    time.sleep(1)
    container = create_frame(root)
    create_main_label(container, f"Congratulations {player.name}!\nYou have escaped from {player.school}!\nYou win!")
    create_side_image(container, "winner.jpg") # trophy image
    return_to_main_menu_button = tk.Button(container, text="Return to Main Menu", height=4, fg="green",font="Roboto 12 bold", command=lambda: [title_page(), delete_frame(container)])
    return_to_main_menu_button.grid(padx=5, pady=5)

# sets the inital page as title_page
title_page()

# starts game window
root.mainloop()