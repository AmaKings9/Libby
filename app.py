from flask import Flask, render_template, request, jsonify
import speech_recognition as sr
import threading

app = Flask(__name__)

recognizer = sr.Recognizer()
is_listening = False
transcription = ""

def listen():
    global transcription
    with sr.Microphone() as source:
        while is_listening:
            try:
                audio = recognizer.listen(source, timeout=5)
                transcription = recognizer.recognize_google(audio, language="en-US")
            except sr.UnknownValueError:
                transcription = "Could not understand audio"
            except sr.RequestError as e:
                transcription = f"Could not request results; {e}"

@app.route('/')
def index():
    return render_template('index.html', transcription=transcription)

@app.route('/toggle_listen', methods=['POST'])
def toggle_listen():
    global is_listening
    is_listening = not is_listening

    if is_listening:
        thread = threading.Thread(target=listen)
        thread.start()

    return jsonify({'listening': is_listening})

if __name__ == '__main__':
    app.run(debug=True)
