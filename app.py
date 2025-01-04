from flask import Flask, render_template, request, jsonify
import speech_recognition as sr
import threading
import libby
import time

app = Flask(__name__)

recognizer = sr.Recognizer()
is_listening = False
transcripcion = ""
respuestaLibby = ""
last_response = ""

# Obtener la lista de micrófonos y mostrarla al usuario
print("Dispositivos de audio disponibles:")
mic_list = sr.Microphone.list_microphone_names()

for index, name in enumerate(mic_list):
    print(f"Idx {index}: {name}")

# Solicitar al usuario que elija el micrófono
mic_idx = int(input("Introduce el índice del micrófono que deseas usar: "))

############################################################
# FUNCION LISTEN - SPEECH TO TEXT + LIBBY IMPLEMENTATION
############################################################

def listen():
    #Acceso variables globales
    global transcripcion
    global respuestaLibby

    #Seleccion del microfono deseado y asignacion a variable source
    with sr.Microphone(device_index=mic_idx) as source:

        #Mientras este activa la escucha, se realizara la transcripcion de voz a texto en ingles
        while is_listening:
            try:

                #Filtrar ruido del ambiente
                recognizer.adjust_for_ambient_noise(source, duration=0.2)
                #Comienza la escucha a traves del microfono seleccionado
                audio = recognizer.listen(source)
                # Using google to recognize audio
                transcripcion = recognizer.recognize_google(audio, language="en-US")
                #Imprime en pantalla la transcripcion
                print(transcripcion)
                # IMPLMENTACION DE LIBBY -> ¡¡INTERPRETE DE INSTRUCCIONES!!
                ## Se almacena la respuesta del I.I. acerca de la accion a realizar
                respuestaLibby = libby.main(transcripcion)

            except sr.UnknownValueError:
                transcripcion = "Could not understand audio"
            except sr.RequestError as e:
                transcripcion = f"Could not request results; {e}"

@app.route('/')
def index():
    return render_template('index.html', respuestaLibby = respuestaLibby)

# la ruta /toggle_listen permite alternar el estado de escucha del micrófono. 
# Al recibir una solicitud POST... 
@app.route('/toggle_listen', methods=['POST'])
def toggle_listen():
# invierte el estado de is_listening, 
    global is_listening
    is_listening = not is_listening

# inicia el proceso de escucha en un hilo separado si está activado
    if is_listening:
        thread = threading.Thread(target=listen)
        thread.start()

# y devuelve el estado actualizado al cliente para que la interfaz pueda reflejar el cambio.
    return jsonify({'listening': is_listening})

# la ruta /get_respuestaLibby permite devolver la respuesta del I.I. en formato JSON
@app.route('/get_respuestaLibby', methods=['GET'])
def get_respuestaLibby():
    global last_response
    start_time = time.time()
    timeout = 20  # Timeout de 30 segundos

    while time.time() - start_time < timeout:
        if respuestaLibby != last_response:
            last_response = respuestaLibby
            return jsonify({'respuestaLibby': respuestaLibby})
        time.sleep(0.5)  # Espera 1 segundo antes de volver a verificar

    if respuestaLibby == "Comando Invalido":
        return jsonify({'respuestaLibby': "Comando Invalido"})
    return jsonify({'respuestaLibby': None})  # Devuelve None si no hay respuesta después de 30 segundos.

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)