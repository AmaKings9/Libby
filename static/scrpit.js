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

    function updateRespuestaLibby() {
        //realiza peticion get a la ruta establecida de donde obtiene un objeto json
        // con la respuesta del interprete.
        $.get("/get_respuestaLibby", function(data) {
            // Compara la respuesta
            switch (data.respuestaLibby){
                case 'Turn on TV':
                    tvRight.classList.add('encendida');
                    tvLeft.classList.add('encendida');
                    break;

                case 'Turn off TV':
                    tvRight.classList.remove('encendida');
                    tvLeft.classList.remove('encendida');
                    break;

                case 'Turn on Fan':
                    fanGif.style.backgroundImage = "url('/static/Gif_Fan.gif')";
                    break;

                case 'Turn off Fan':
                    fanGif.style.backgroundImage = "url('/static/Static_Fan.png')";
                    break;

                case 'Comando Invalido':
                    console.log('Comand invalid');
                    break;

                default:
            }
        });
    }

    // Llama a updateTranscription cada segundo para actualizar la transcripción en la página
    setInterval(updateRespuestaLibby, 1000);