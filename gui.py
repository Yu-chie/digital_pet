# Game GUI using Tkinter

# 1. Import necessary libraries (tkinter, DigiPet class)
import tkinter as tk
from digital_pet import DigiPet
from PIL import Image, ImageTk
import time
import tkinter.ttk as ttk

# --- Loading screen function ---
def show_loading_screen():
    loading = tk.Toplevel()
    loading.title("Loading...")
    tk.Label(loading, text="👶 A new baby pet is being born...", font=("Arial", 14)).pack(padx=30, pady=20)
    loading.update()
    loading.after(2000, loading.destroy)  # Show for 2 seconds
    loading.grab_set()
    loading.wait_window()

def show_splash_screen():
    splash = tk.Toplevel()
    splash.title("Welcome to DigiPet!")
    img = Image.open("images/opening.jpg")
    img = img.resize((350, 250))
    photo = ImageTk.PhotoImage(img)
    label = tk.Label(splash, image=photo)
    label.image = photo  # Keep a reference!
    label.pack()
    splash.after(2000, splash.destroy)  # Show for 2 seconds
    splash.grab_set()
    splash.wait_window()

# 4. Set up the main Tkinter window (hidden at first)
root = tk.Tk()
root.title("DigiPet GUI")
root.withdraw()  # Hide main window during splash/loading/name

# 2. Load or create a DigiPet instance
pet = DigiPet.load()
if not pet:
    show_splash_screen()      # <-- Show opening.jpg splash first
    time.sleep(0.2)
    show_loading_screen()     # Then show loading screen
    time.sleep(0.2)
    # Ask for pet name using a simple dialog
    name_prompt = tk.Toplevel()
    name_prompt.title("Name Your Pet")
    tk.Label(name_prompt, text="What do you want to name your pet?").pack(padx=10, pady=10)
    name_var = tk.StringVar()
    entry = tk.Entry(name_prompt, textvariable=name_var)
    entry.pack(padx=10, pady=5)
    entry.focus_set()
    def set_name_and_close():
        name_prompt.destroy()
    tk.Button(name_prompt, text="OK", command=set_name_and_close).pack(pady=10)
    name_prompt.bind('<Return>', lambda event: set_name_and_close())
    name_prompt.grab_set()
    name_prompt.wait_window()
    pet_name = name_var.get() if name_var.get() else "Fluffy"
    pet = DigiPet(pet_name)

root.deiconify()  # Show main window after setup

# 3. Define functions for each button/action:
def update_status():
    """Update the status label with pet's current stats."""
    status_label.config(text=pet.show_status())
    # Update image
    pet_img = Image.open(get_pet_image())
    pet_img = pet_img.resize((120, 120))
    pet_photo = ImageTk.PhotoImage(pet_img)
    img_label.config(image=pet_photo)
    img_label.image = pet_photo
    energy_bar['value'] = pet.energy
    hunger_bar['value'] = pet.hunger
    life_bar['value'] = pet.life
    if pet.life <= 0:
        set_buttons_state("disabled")
        message_label.config(text="💀 Your pet has passed away. Restart the game to try again.")

def set_buttons_state(state):
    feed_btn.config(state=state)
    talk_btn.config(state=state)
    play_btn.config(state=state)
    sleep_btn.config(state=state)
    teach_btn.config(state=state)

def show_action_image(image_path, delay=800):
    set_buttons_state("disabled")
    try:
        action_img = Image.open(image_path)
        action_img = action_img.resize((120, 120))
        action_photo = ImageTk.PhotoImage(action_img)
        img_label.config(image=action_photo)
        img_label.image = action_photo
        root.after(delay, lambda: [update_status(), set_buttons_state("normal")])
    except Exception:
        update_status()
        set_buttons_state("normal")

def do_feed():
    result = pet.feed()
    message_label.config(text=result)
    show_action_image("images/eating_cat.jpg")
    pet.save()

def do_talk():
    result = pet.talk()
    message_label.config(text=result)
    show_action_image("images/talking_cat.jpg")
    pet.save()

def do_play():
    result = pet.play()
    message_label.config(text=result)
    show_action_image("images/playful_cat.jpg")
    pet.save()

def do_sleep():
    result = pet.sleep()
    message_label.config(text=result)
    show_action_image("images/sleep_cat.png")
    pet.save()

def do_teach():
    word = teach_entry.get()
    if word:
        result = pet.teach(word)
        message_label.config(text=result)
        teach_entry.delete(0, tk.END)
        show_action_image("images/proud_cat.jpg")
        teach_entry.focus_set()
        pet.save()

def get_pet_image():
    mood = pet.mood()
    try:
        if mood == "happy":
            return "images/happy_cat.jpg"
        elif mood == "hungry":
            return "images/eating_cat.jpg"
        elif mood == "tired":
            return "images/sleep_cat.png"
        elif mood == "bored":
            return "images/standby_cat.png"
        elif mood == "gone":
            return "images/sad_cat.jpg"
        else:
            return "images/normal_cat.jpg"
    except Exception:
        return "images/normal_cat.jpg"

# Pet image at the top
pet_img = Image.open(get_pet_image())
pet_img = pet_img.resize((120, 120))
pet_photo = ImageTk.PhotoImage(pet_img)
img_label = tk.Label(root, image=pet_photo)
img_label.pack(pady=5)

# 5. Add a frame to hold status and stat bars side by side
status_frame = tk.Frame(root)
status_frame.pack(pady=10)

# Status label on the left
status_label = tk.Label(status_frame, text=pet.show_status(), font=("Consolas", 10), justify="left")
status_label.pack(side=tk.LEFT, padx=10)

# Stat bars on the right, stacked vertically
bars_frame = tk.Frame(status_frame)
bars_frame.pack(side=tk.LEFT, padx=10)

tk.Label(bars_frame, text="Energy").pack(anchor="w")
energy_bar = ttk.Progressbar(bars_frame, length=120, maximum=DigiPet.max_energy)
energy_bar.pack(pady=2)
tk.Label(bars_frame, text="Hunger").pack(anchor="w")
hunger_bar = ttk.Progressbar(bars_frame, length=120, maximum=DigiPet.max_hunger)
hunger_bar.pack(pady=2)
tk.Label(bars_frame, text="Life").pack(anchor="w")
life_bar = ttk.Progressbar(bars_frame, length=120, maximum=DigiPet.max_life)
life_bar.pack(pady=2)

# Message label below status and bars
message_label = tk.Label(root, text="", fg="blue", wraplength=350, justify="left")
message_label.pack(pady=5)

# 6. Add buttons for each action (Feed, Talk, Play, Sleep)
button_frame = tk.Frame(root)
button_frame.pack(pady=5)

feed_btn = tk.Button(button_frame, text="Feed", width=12, command=do_feed)
feed_btn.grid(row=0, column=0, padx=2)

talk_btn = tk.Button(button_frame, text="Talk", width=12, command=do_talk)
talk_btn.grid(row=0, column=1, padx=2)

play_btn = tk.Button(button_frame, text="Play", width=12, command=do_play)
play_btn.grid(row=0, column=2, padx=2)

sleep_btn = tk.Button(button_frame, text="Sleep", width=12, command=do_sleep)
sleep_btn.grid(row=0, column=3, padx=2)

# 7. Add entry and button for teaching a new word
teach_frame = tk.Frame(root)
teach_frame.pack(pady=5)
teach_entry = tk.Entry(teach_frame, width=20)
teach_entry.pack(side=tk.LEFT)
teach_btn = tk.Button(teach_frame, text="Teach Word", command=do_teach)
teach_btn.pack(side=tk.LEFT, padx=5)

# 8. Add a function to save the pet and close the window properly
def on_close():
    pet.save()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_close)

# 9. Start the Tkinter main loop
update_status()  # Initial update
root.mainloop()