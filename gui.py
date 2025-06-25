# Game GUI using Tkinter

# 1. Import necessary libraries (tkinter, DigiPet class)
import tkinter as tk
from digital_pet import DigiPet
from PIL import Image, ImageTk

# 2. Load or create a DigiPet instance
pet = DigiPet.load()
if not pet:
    pet_name = input("What do you want to name your pet?: ")
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
    result = pet.feed()
    message_label.config(text=result)
    update_status()

def do_talk():
    result = pet.talk()
    message_label.config(text=result)
    update_status()

def do_play():
    result = pet.play()
    message_label.config(text=result)
    update_status()

def do_sleep():
    result = pet.sleep()
    message_label.config(text=result)
    update_status()

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
        return "happy_cat.jpg"
    elif mood == "hungry":
        return "eating_cat.jpg"
    elif mood == "tired":
        return "sleep_cat.jpg"
    elif mood == "bored":
        return "standby_cat.jpg"
    elif mood == "gone":
        return "sad_cat.jpg"
    else:
        return "normal_cat.jpg"

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