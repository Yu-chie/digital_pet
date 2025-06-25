# Game GUI using Tkinter

# 1. Import necessary libraries (tkinter, DigiPet class)
import tkinter as tk
from digital_pet import DigiPet
from PIL import Image, ImageTk
import time

# --- Loading screen function ---
def show_loading_screen():
    loading = tk.Tk()
    loading.title("Loading...")
    tk.Label(loading, text="👶 A new baby pet is being born...", font=("Arial", 14)).pack(padx=30, pady=20)
    loading.update()
    loading.after(2000, loading.destroy)  # Show for 2 seconds
    loading.mainloop()

def show_splash_screen():
    splash = tk.Tk()
    splash.title("Welcome to DigiPet!")
    img = Image.open("images/opening.jpg")
    img = img.resize((350, 250))
    photo = ImageTk.PhotoImage(img)
    label = tk.Label(splash, image=photo)
    label.image = photo  # Keep a reference!
    label.pack()
    splash.after(2000, splash.destroy)  # Show for 2 seconds
    splash.mainloop()

# 2. Load or create a DigiPet instance
pet = DigiPet.load()
if not pet:
    show_splash_screen()      # <-- Show opening.jpg splash first
    show_loading_screen()     # Then show loading screen
    # Ask for pet name using a simple dialog
    name_prompt = tk.Tk()
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
    name_prompt.mainloop()
    pet_name = name_var.get() if name_var.get() else "Fluffy"
    pet = DigiPet(pet_name)
    
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

def do_feed():
    show_action_image("images/eating_cat.jpg")
    result = pet.feed()
    message_label.config(text=result)
    # update_status() will be called by show_action_image after delay

def do_talk():
    result = pet.talk()
    message_label.config(text=result)
    update_status()
    show_action_image("images/talking_cat.jpg")  # Show talking image

def do_play():
    result = pet.play()
    message_label.config(text=result)
    update_status()
    show_action_image("images/playing_cat.jpg")  # Show playing image

def do_sleep():
    result = pet.sleep()
    message_label.config(text=result)
    update_status()
    show_action_image("images/sleep_cat.jpg")  # Show sleeping image

def do_teach():
    word = teach_entry.get()
    if word:
        result = pet.teach(word)
        message_label.config(text=result)
        teach_entry.delete(0, tk.END)
        update_status()

def get_pet_image():
    mood = pet.mood()
    if mood == "happy":
        return "images/happy_cat.jpg"
    elif mood == "hungry":
        return "images/eating_cat.jpg"
    elif mood == "tired":
        return "images/sleep_cat.jpg"
    elif mood == "bored":
        return "images/standby_cat.jpg"
    elif mood == "gone":
        return "images/sad_cat.jpg"
    else:
        return "images/normal_cat.jpg"

def show_action_image(image_path, delay=800):
    """Show an action image for a short time, then revert to mood image."""
    action_img = Image.open(image_path)
    action_img = action_img.resize((120, 120))
    action_photo = ImageTk.PhotoImage(action_img)
    img_label.config(image=action_photo)
    img_label.image = action_photo
    root.after(delay, update_status)  # revert to mood image after delay (ms)

# 4. Set up the main Tkinter window
root = tk.Tk()
root.title("DigiPet GUI")

# 5. Add labels for status and messages
status_label = tk.Label(root, text=pet.show_status(), font=("Consolas", 10), justify="left")
status_label.pack(pady=10)

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

pet_img = Image.open(get_pet_image())
pet_img = pet_img.resize((120, 120))
pet_photo = ImageTk.PhotoImage(pet_img)
img_label = tk.Label(root, image=pet_photo)
img_label.pack(pady=5)

# 8. Add a function to save the pet and close the window properly
def on_close():
    pet.save()
    root.destroy()
    
# 9. Start the Tkinter main loop
root.mainloop()