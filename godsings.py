from flask import Flask, render_template
from pytunegen.tunegen import TuneGen
import random
import time
import requests
import os

def generateMusic(seed=0):
    godsaid = "I'm down"
    try:
        response = requests.get('https://godsays.xyz')
        if response.status_code == 200:
            godsaid = str(response.content, 'utf-8')
            if seed == 0:
                for word in godsaid.split(" "):
                    for char in word:
                        seed += ord(char)
    except:
        print("god is down")

    tunegen = TuneGen(seed=seed, music_length=20)
    music = tunegen.generate()
    note_pitches = []
    note_durations = []
    for bar in music:
        for note in bar.notes:
            note_pitches.append(note.pitch)
            note_durations.append(note.duration)
    sensible_music = []
    for i in range(len(note_pitches)):
        sensible_music.append([note_pitches[i], note_durations[i] * (60/tunegen.bpm_current)])
    return godsaid, sensible_music, seed

app = Flask(__name__, template_folder='templates')
app.debug = True
app._static_folder = os.path.abspath("templates/static/")

@app.route('/', methods=['GET'])
def index():
    words, song, seed = generateMusic()
    return render_template('layouts/index.html',
                           words=words,
                           song=song,
                           seed=seed)

@app.route('/<seed>', methods=['GET'])
def custom_seed(seed):
    try:
        seed = int(seed)
    except:
        pass
    words, song, seed = generateMusic(seed=seed)
    return render_template('layouts/index.html',
                           words=words,
                           song=song,
                           seed=seed)
