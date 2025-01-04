const h = document.querySelector('#h');
const b = document.body;

let base = (e) => {
    var x = e.pageX / window.innerWidth - 0.5;
    var y = e.pageY / window.innerHeight - 0.5;
    h.style.transform = `
        perspective(90vw)
        rotateX(${y * 4 + 75}deg)
        rotateZ(${-x * 12 + 45}deg)
        translateZ(-9vw)
    `;
}

b.addEventListener('pointermove', base);

let listening = false;

// Selecciona el elemento de vantilador
const fanGif = document.getElementById("fan_gif");
// Selecciona los elementos de la TV
const tvRight = document.querySelector('.tv__right');
const tvLeft = document.querySelector('.tv__left');

//Envia una solicitud a la ruta /toggle_listen permite alternar el estado de escucha del micrófono
    $("#toggleButton").click(function() {
        //Envia una solicitud POST
        $.post("/toggle_listen", function(data) {
            //Cambia el texto del boton de acuerdo si esta escuchando o no
            listening = data.listening;
            $("#txt").text(listening ? "Escuchando..." : "Talk to Libby");
        });
    });

// Implementacion de la API SpeechSynthesis para la voz de Libby.
    const playVoiceMessage = (message) => {
        const speech = new SpeechSynthesisUtterance(message);
        speech.lang = 'en-US'; // Idioma ingles
        speech.pitch = 1; // Tono de voz
        speech.rate = 1; // Velocidad de voz
        window.speechSynthesis.speak(speech);
    };

function checkLibbyResponse() {
    fetch('/get_respuestaLibby')
        .then(response => response.json())
        .then(data => {
            if (data.respuestaLibby) {
                switch (data.respuestaLibby) {
                    case 'Turn on TV':
                        tvRight.classList.add('encendida');
                        tvLeft.classList.add('encendida');
                        playVoiceMessage('All set! The TV is on, enjoy your show.');
                        break;

                    case 'Turn off TV':
                        tvRight.classList.remove('encendida');
                        tvLeft.classList.remove('encendida');
                        playVoiceMessage('Got it! The TV is now off.');
                        break;

                    case 'Turn on Fan':
                        fanGif.style.backgroundImage = "url('/static/Gif_Fan.gif')";
                        playVoiceMessage('The fan is on! Time to cool down.');
                        break;

                    case 'Turn off Fan':
                        fanGif.style.backgroundImage = "url('/static/Static_Fan.png')";
                        playVoiceMessage('Fan turned off! Hope you\'re feeling comfortable.');
                        break;

                    case 'Comando Invalido':
                        playVoiceMessage('Oops! I don\'t think I understood, How about trying again?');
                        break;

                    default:
                        break;
                }
            }
        })
        .catch(error => console.error('Error:', error))
        .finally(() => {
            // Vuelve a verificar después de un intervalo
            setTimeout(checkLibbyResponse, 1000); // Ajusta el intervalo según sea necesario
        });
}

// Inicia la verificación de la respuesta de Libby
checkLibbyResponse();