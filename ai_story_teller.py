import asyncio
import edge_tts
import pygame
import os
import time
import speech_recognition as sr
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import threading

# =====================================================
# SETTINGS
# =====================================================

VOICE = "en-US-AriaNeural"
AUDIO_FILE = "voice.mp3"

pygame.init()
pygame.mixer.init()

recognizer = sr.Recognizer()
# =====================================================
# COMPACT RASPBERRY PI TOUCHSCREEN GUI
# =====================================================

root = tk.Tk()
root.title("Rosie AI Story Robot")
root.attributes("-fullscreen", True)
root.configure(bg="#EAF4FF")

# -------------------------------
# HEADER
# -------------------------------

header = tk.Frame(root, bg="#1976D2", height=55)
header.pack(fill="x")

title = tk.Label(
    header,
    text="🤖 Rosie AI Story Robot",
    font=("Arial", 22, "bold"),
    bg="#1976D2",
    fg="white"
)
title.pack(pady=8)

# -------------------------------
# ROBOT
# -------------------------------

robot_label = tk.Label(
    root,
    text="🤖",
    font=("Arial", 55),
    bg="#EAF4FF"
)
robot_label.pack()

status_label = tk.Label(
    root,
    text="Ready",
    font=("Arial", 14, "bold"),
    bg="#EAF4FF",
    fg="green"
)
status_label.pack()

# -------------------------------
# STORY DISPLAY BOX (LARGER)
# -------------------------------

speech_box = tk.Label(
    root,
    text="Select a story and press START",
    font=("Arial", 18),
    bg="white",
    fg="#333333",
    width=48,
    height=6,
    wraplength=720,
    justify="center",
    relief="groove",
    bd=3,
    padx=15,
    pady=15
)
speech_box.pack(pady=8)

# -------------------------------
# STORY TITLE
# -------------------------------

menu_title = tk.Label(
    root,
    text="Choose a Story",
    font=("Arial", 18, "bold"),
    bg="#EAF4FF",
    fg="#1565C0"
)
menu_title.pack()

# -------------------------------
# STORY BUTTONS
# -------------------------------

stories_frame = tk.Frame(root, bg="#EAF4FF")
stories_frame.pack(pady=4)

story1_button = tk.Button(
    stories_frame,
    text="🌳 Rosie Adventure",
    font=("Arial", 14, "bold"),
    bg="#FFE082",
    width=18,
    height=2
)
story1_button.grid(row=0, column=0, padx=5)

story2_button = tk.Button(
    stories_frame,
    text="⭐ The Lost Star",
    font=("Arial", 14, "bold"),
    bg="#90CAF9",
    width=18,
    height=2
)
story2_button.grid(row=0, column=1, padx=5)

story3_button = tk.Button(
    stories_frame,
    text="🌱 The Magic Seed",
    font=("Arial", 14, "bold"),
    bg="#A5D6A7",
    width=18,
    height=2
)
story3_button.grid(row=0, column=2, padx=5)

# -------------------------------
# CHILD RESPONSE
# -------------------------------

child_box = tk.Label(
    root,
    text="Child: ",
    font=("Arial", 14),
    bg="#E8F5E9",
    width=50,
    height=2,
    relief="groove",
    bd=2
)
child_box.pack(pady=6)

# -------------------------------
# PROGRESS BAR
# -------------------------------

progress = ttk.Progressbar(
    root,
    length=500,
    maximum=3
)
progress.pack(pady=4)

# -------------------------------
# CONTROL BUTTONS
# -------------------------------

button_frame = tk.Frame(root, bg="#EAF4FF")
button_frame.pack(pady=10)

start_button = tk.Button(
    button_frame,
    text="▶ START STORY",
    font=("Arial", 18, "bold"),
    bg="#FF9800",
    fg="white",
    width=14,
    height=2
)
start_button.grid(row=0, column=0, padx=10)

exit_button = tk.Button(
    button_frame,
    text="❌ EXIT",
    font=("Arial", 18, "bold"),
    bg="#E53935",
    fg="white",
    width=10,
    height=2,
    command=root.destroy
)
exit_button.grid(row=0, column=1, padx=10)
# =====================================================
# TEXT TO SPEECH
# =====================================================

async def generate_voice(text):

    communicate = edge_tts.Communicate(
        text=text,
        voice=VOICE
    )

    await communicate.save(AUDIO_FILE)


def speak(text):

    print(text)


    # update screen
    root.after(
        0,
        lambda:
        speech_box.config(text=text)
    )


    root.after(
        0,
        lambda:
        status_label.config(
            text="🤖 Robot Speaking"
        )
    )


    robot_label.config(text="😀")


    asyncio.run(
        generate_voice(text)
    )


    pygame.mixer.music.load(AUDIO_FILE)

    pygame.mixer.music.play()


    while pygame.mixer.music.get_busy():

        pygame.time.Clock().tick(10)


    pygame.mixer.music.unload()


    if os.path.exists(AUDIO_FILE):

        os.remove(AUDIO_FILE)


    root.after(
        0,
        lambda:
        status_label.config(
            text="Listening..."
        )
    )

    robot_label.config(text="🙂")

# =====================================================
# MICROPHONE
# =====================================================

def listen():

    root.after(
        0,
        lambda:
        status_label.config(
            text="🎤 Listening"
        )
    )


    robot_label.config(text="🤔")


    with sr.Microphone(device_index=1) as source:


        recognizer.adjust_for_ambient_noise(
            source,
            duration=1
        )


        try:

            audio = recognizer.listen(
                source,
                timeout=8,
                phrase_time_limit=6
            )


            text = recognizer.recognize_google(audio)


            print(text)


            root.after(
                0,
                lambda:
                child_box.config(
                    text="Child: "+text
                )
            )


            return text.lower()



        except:

            return ""

# =====================================================
# INTRODUCTION
# =====================================================

def welcome():

    speak("""
Hello my little friend.

Welcome to the magical story world.

Today we are going to learn
new English words.

Whenever I teach you a new word,

I want you to repeat it after me.

Then I will ask you a simple question.

Are you ready?

Let's begin our adventure.
""")


# =====================================================
# PRONUNCIATION
# =====================================================

def repeat_word(word):

    speak(f"Please repeat after me.")

    speak(word)

    child = listen()

    if word.lower() in child:

        speak("Excellent!")

        speak("You pronounced the word correctly.")

        return True

    else:

        speak("Good try.")

        speak(f"The correct pronunciation is {word}")

        speak("Let's repeat together.")

        speak(word)

        speak(word)

        return False

    # =====================================================
# VOCABULARY LESSON
# =====================================================
def vocabulary(word, pronunciation, meaning, sentence, answer):

    speak("Let's learn a new word.")

    speak(f"Our new word is {word}.")

    speak("Listen carefully to the pronunciation.")

    speak(pronunciation)

    speak(f"The meaning of {word} is.")

    speak(meaning)

    speak("Now listen to an example sentence.")

    speak(sentence)

    repeat_word(word)

    # -----------------------------
    # Voice Quiz
    # -----------------------------

    if word == "Curious":

        question = "What does Curious mean?"

        options = [
            "Wanting to know or learn something",
            "Feeling sleepy",
            "Feeling angry"
        ]

        correct_option = 1

    elif word == "Brave":

        question = "What does Brave mean?"

        options = [
            "Feeling afraid",
            "Showing courage",
            "Feeling hungry"
        ]

        correct_option = 2

    elif word == "Confident":

        question = "What does Confident mean?"

        options = [
            "Believing in yourself",
            "Feeling tired",
            "Feeling sad"
        ]

        correct_option = 1

    elif word == "Shiny":

        question = "What does Shiny mean?"

        options = [
            "Bright and glowing",
            "Very cold",
            "Very noisy"
        ]

        correct_option = 1

    elif word == "Kind":

        question = "What does Kind mean?"

        options = [
            "Being caring and helpful",
            "Being angry",
            "Being sleepy"
        ]

        correct_option = 1

    elif word == "Joyful":

        question = "What does Joyful mean?"

        options = [
            "Feeling very happy",
            "Feeling hungry",
            "Feeling scared"
        ]

        correct_option = 1

    elif word == "Tiny":

        question = "What does Tiny mean?"

        options = [
            "Very small",
            "Very big",
            "Very loud"
        ]

        correct_option = 1

    elif word == "Patient":

        question = "What does Patient mean?"

        options = [
            "Able to wait calmly",
            "Running very fast",
            "Feeling angry"
        ]

        correct_option = 1

    elif word == "Proud":

        question = "What does Proud mean?"

        options = [
            "Feeling happy about an achievement",
            "Feeling sleepy",
            "Feeling afraid"
        ]

        correct_option = 1

    speak(question)

    for i, option in enumerate(options,1):

        speak(f"Option {i}. {option}")

    speak("Please say the option number or the correct answer.")

    response = listen()

    number_map = {
        "1":1,
        "one":1,
        "2":2,
        "two":2,
        "to":2,
        "too":2,
        "3":3,
        "three":3
    }

    correct = False

    if response in number_map:

        if number_map[response] == correct_option:

            correct = True

    elif options[correct_option-1].lower() in response:

        correct = True

    if correct:

        speak("Excellent! That is the correct answer.")

    else:

        speak("Good try.")

        speak("The correct answer is.")

        speak(options[correct_option-1])

    speak("Let's remember this word together.")

    speak(word)

    speak(word)

    speak(word)

    speak("Great job! Let's continue the story.")


# =====================================================
# STORY 1: ROSIE ADVENTURE
# =====================================================

def rosie_intro():

    speak("""
Once upon a time,

there was a little rabbit named Rosie.

Rosie loved exploring the forest.

Every morning,

she walked happily among the trees,

looking at colourful flowers,

beautiful butterflies,

and singing birds.

One bright sunny morning,

Rosie decided to explore

a part of the forest

she had never visited before.
""")


def rosie_middle():

    speak("""
Rosie continued walking.

Soon,

she reached a small wooden bridge.

The river below

was flowing very fast.

Rosie felt a little scared.

She took a deep breath

and carefully crossed the bridge.

On the other side,

she met

a wise old owl.

The owl smiled kindly

and handed Rosie

a magical map.
""")


def rosie_end():

    speak("""
Rosie followed the magical map.

After a long journey,

she discovered

a beautiful garden

filled with colourful flowers.

Many friendly animals

were waiting there.

They clapped

and cheered for Rosie.

Rosie smiled happily.

She had learned

that being curious,

being brave,

and being confident

can help us achieve wonderful things.
""")


def review_rosie():

    speak("""
Let's review

the words we learned today.
""")

    words = [

        ("Curious",
         "Wanting to know or learn something."),

        ("Brave",
         "Showing courage and not being afraid."),

        ("Confident",
         "Believing in yourself.")

    ]

    for word, meaning in words:

        speak(word)

        speak(meaning)

    speak("Now say the words with me.")

    for word, _ in words:

        speak(word)

    speak("Wonderful! You learned three wonderful new words today.")

    speak("Rosie's adventure has finished.")

    speak("See you again for another adventure!")


def story_rosie():

    welcome()

    rosie_intro()

    vocabulary(
        word="Curious",
        pronunciation="Kyoo-ree-us",
        meaning="Wanting to know or learn something new.",
        sentence="Rosie was curious about every flower she saw.",
        answer="wanting to know"
    )

    rosie_middle()

    vocabulary(
        word="Brave",
        pronunciation="Brayv",
        meaning="Showing courage and not being afraid.",
        sentence="Rosie was brave when she crossed the bridge.",
        answer="courage"
    )

    rosie_end()

    vocabulary(
        word="Confident",
        pronunciation="Con-fi-dent",
        meaning="Believing in yourself and your abilities.",
        sentence="Rosie felt confident during her adventure.",
        answer="believing in yourself"
    )

    review_rosie()

    # Reset screen after story finishes
    speech_box.config(text="Touch Start Story")
    status_label.config(text="Ready")
    child_box.config(text="Child: ")
    robot_label.config(text="🙂")

# =====================================================
# STORY 2: THE LOST STAR
# =====================================================

def star_intro():

    speak("""
Once upon a time,

a little girl named Lily

loved watching the stars.

Every night,

she looked at the bright sky

and wondered

what adventures the stars had.

One evening,

a tiny star

fell into a green meadow.

The little star

was glowing softly

and looked frightened.

Lily gently picked up the star

and decided to help it

find its way back home.
""")


def star_middle():

    speak("""
Lily carried the star carefully.

She walked through the meadow,

crossed a small stream,

and climbed a gentle hill.

Along the way,

she helped a rabbit,

a bird,

and a butterfly.

The little star

became brighter

because of Lily's kindness.

Soon they reached

the highest hill

in the valley.
""")


def star_end():

    speak("""
The star looked up

at the night sky.

It began to glow

brighter and brighter.

Suddenly,

it floated gently upward.

Thousands of stars

sparkled across the sky.

The little star

thanked Lily

for helping it.

Lily smiled happily.

She learned

that kindness

and courage

can make the world brighter.
""")


def review_star():

    speak("""
Let's review

the words we learned today.
""")

    words = [

        ("Shiny",
         "Bright and glowing."),

        ("Kind",
         "Being caring and helpful."),

        ("Joyful",
         "Feeling very happy.")

    ]

    for word, meaning in words:

        speak(word)

        speak(meaning)

    speak("Now say the words with me.")

    for word, _ in words:

        speak(word)

    speak("Wonderful! You learned three beautiful new words today.")

    speak("The Lost Star story has finished.")

    speak("See you again for another adventure!")


def story_star():

    welcome()

    star_intro()

    vocabulary(
        word="Shiny",
        pronunciation="Shy-nee",
        meaning="Bright and glowing.",
        sentence="The little star was shiny in the dark sky.",
        answer="bright"
    )

    star_middle()

    vocabulary(
        word="Kind",
        pronunciation="Kynd",
        meaning="Being caring and helpful.",
        sentence="Lily was kind to the lost star.",
        answer="caring"
    )

    star_end()

    vocabulary(
        word="Joyful",
        pronunciation="Joy-ful",
        meaning="Feeling very happy.",
        sentence="Lily felt joyful after helping the star.",
        answer="happy"
    )

    review_star()
    
speech_box.config(text="Touch Start Story")

status_label.config(text="Ready")

child_box.config(text="Child: ")

robot_label.config(text="🙂")
    # =====================================================
# STORY 3: THE MAGIC SEED
# =====================================================

def seed_intro():

    speak("""
Once upon a time,

a little squirrel named Milo

found a magical seed.

The seed was very tiny,

but it sparkled in the sunlight.

An old turtle told Milo,

'Plant this seed with love,

and something wonderful will happen.'

Milo smiled

and planted the seed carefully

in his garden.
""")


def seed_middle():

    speak("""
Every day,

Milo watered the seed.

Sometimes it rained.

Sometimes the weather was hot.

The seed did not grow quickly.

But Milo never gave up.

He waited patiently

and took care of the garden.

One morning,

a small green plant appeared.

Milo was very happy.
""")


def seed_end():

    speak("""
The little plant

grew taller every day.

Soon it became

a giant magical tree.

The tree was filled

with sweet fruits,

colourful flowers,

and singing birds.

All the animals

celebrated together.

Milo smiled proudly.

He learned

that patience

and hard work

bring wonderful rewards.
""")


def review_seed():

    speak("""
Let's review

the words we learned today.
""")

    words = [

        ("Tiny",
         "Very small."),

        ("Patient",
         "Able to wait calmly."),

        ("Proud",
         "Feeling happy about something you achieved.")

    ]

    for word, meaning in words:

        speak(word)

        speak(meaning)

    speak("Now say the words with me.")

    for word, _ in words:

        speak(word)

    speak("Excellent! You learned three wonderful new words today.")

    speak("The Magic Seed story has finished.")

    speak("See you again for another adventure!")


def story_seed():

    welcome()

    seed_intro()

    vocabulary(
        word="Tiny",
        pronunciation="Tie-nee",
        meaning="Very small.",
        sentence="The magical seed was tiny.",
        answer="small"
    )

    seed_middle()

    vocabulary(
        word="Patient",
        pronunciation="Pay-shent",
        meaning="Able to wait calmly.",
        sentence="Milo was patient while the seed grew.",
        answer="wait"
    )

    seed_end()

    vocabulary(
        word="Proud",
        pronunciation="Prowd",
        meaning="Feeling happy about something you achieved.",
        sentence="Milo was proud of the beautiful tree.",
        answer="achievement"
    )

    review_seed()
    review_seed()

speech_box.config(text="Touch Start Story")

status_label.config(text="Ready")

child_box.config(text="Child: ")

robot_label.config(text="🙂")
# =====================================================
# MAIN MENU
# =====================================================
selected_story = None

def select_story(story_name):
    global selected_story
    selected_story = story_name
    speech_box.config(
        text=f"Selected Story:\n\n{story_name}\n\nPress START STORY"
    )
    status_label.config(text="Story Selected")
    robot_label.config(text="😊")

def start_story():

    if selected_story is None:
        speak("Please select a story first.")
        return

    if selected_story == "Rosie Adventure":
        target_story = story_rosie

    elif selected_story == "The Lost Star":
        target_story = story_star

    elif selected_story == "The Magic Seed":
        target_story = story_seed

    threading.Thread(
        target=target_story,
        daemon=True
    ).start()

# =====================================================
# STORY SELECTION BUTTONS
# =====================================================
story1_button.config(
    command=lambda: select_story("Rosie Adventure")
)

story2_button.config(
    command=lambda: select_story("The Lost Star")
)

story3_button.config(
    command=lambda: select_story("The Magic Seed")
)

start_button.config(command=start_story)

# RUN PROGRAM
# =====================================================
# =====================================================
# RUN PROGRAM
# =====================================================
if __name__ == "__main__":
    root.mainloop()