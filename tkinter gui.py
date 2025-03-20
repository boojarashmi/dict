import tkinter as tk
from tkinter import messagebox
from nltk.corpus import wordnet
from gtts import gTTS
import os
import platform

# Function to get word meanings, synonyms, and antonyms
def get_all_meanings_synonyms(word):
    synsets = wordnet.synsets(word)

    if not synsets:
        return ["No meaning found"], [], []
    # Get all meanings (definitions)
    definitions = [synset.definition() for synset in synsets]

    # Get a list of synonyms from all synsets
    synonyms = set()
    antonyms = set()
    for synset in synsets:
        for lemma in synset.lemmas():
            synonyms.add(lemma.name())
            if lemma.antonyms():
                antonyms.add(lemma.antonyms()[0].name())

    return definitions, list(synonyms), list(antonyms)

# Function to fetch word info
def fetch_word_info():
    word = entry_word.get().strip()
    if not word:
        messagebox.showwarning("Input Error", "Please enter a word.")
        return

    definitions, synonyms, antonyms = get_all_meanings_synonyms(word)

    # Display meanings
    text_meanings.delete(1.0, tk.END)
    for idx, definition in enumerate(definitions, 1):
        text_meanings.insert(tk.END, f"{idx}. {definition}\n")

    # Display synonyms
    if synonyms:
        text_synonyms.config(text=', '.join(synonyms))
    else:
        text_synonyms.config(text="No synonyms found.")

    # Display antonyms
    if antonyms:
        text_antonyms.config(text=', '.join(antonyms))
    else:
        text_antonyms.config(text="No antonyms found.")

# Function to pronounce the word
def pronounce_word():
    word = entry_word.get().strip()
    if not word:
        messagebox.showwarning("Input Error", "Please enter a word.")
        return

    try:
        tts = gTTS(text=word, lang='en')
        tts.save(f"{word}.mp3")

        # Platform check for playing audio
        if platform.system() == "Windows":
            os.system(f"start {word}.mp3")
        elif platform.system() == "Darwin":  # macOS
            os.system(f"afplay {word}.mp3")
        else:  # Linux and other Unix systems
            os.system(f"xdg-open {word}.mp3")

    except Exception as e:
        messagebox.showerror("Pronunciation Error", f"Could not pronounce the word: {str(e)}")

# Set up tkinter window
root = tk.Tk()
root.title("Dictionary with Synonyms, Antonyms, and Pronunciation")
root.geometry("600x600")

# Word input
label_word = tk.Label(root, text="Enter Word:", font=("Arial", 14))
label_word.pack(pady=10)
entry_word = tk.Entry(root, font=("Arial", 14))
entry_word.pack(pady=5)

# Buttons
btn_fetch = tk.Button(root, text="Get Meaning", command=fetch_word_info, font=("Arial", 12))
btn_fetch.pack(pady=10)

btn_pronounce = tk.Button(root, text="Pronounce", command=pronounce_word, font=("Arial", 12))
btn_pronounce.pack(pady=5)

# Display area for meanings, synonyms, antonyms
label_meanings = tk.Label(root, text="Meanings:", font=("Arial", 14))
label_meanings.pack(pady=5)

text_meanings = tk.Text(root, height=6, wrap='word', font=("Arial", 12))
text_meanings.pack(pady=5)

label_synonyms = tk.Label(root, text="Synonyms:", font=("Arial", 14))
label_synonyms.pack(pady=5)

text_synonyms = tk.Label(root, text="", wraplength=500, font=("Arial", 12), justify=tk.LEFT)
text_synonyms.pack(pady=5)

label_antonyms = tk.Label(root, text="Antonyms:", font=("Arial", 14))
label_antonyms.pack(pady=5)

text_antonyms = tk.Label(root, text="", wraplength=500, font=("Arial", 12), justify=tk.LEFT)
text_antonyms.pack(pady=5)

# Run the tkinter main loop
root.mainloop()
