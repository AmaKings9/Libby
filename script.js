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


let gifActivo = false;
let tvStatus = false;

function runLibby(){
    // Apagar - encender ventilador...
    const fanGif = document.getElementById("fan_gif");

    if (gifActivo){
        fanGif.style.backgroundImage = "url('static/Static_Fan.png')";

    } else {
        fanGif.style.backgroundImage = "url('static/Gif_Fan.gif')";
    }
    gifActivo = !gifActivo;

    // Apagar - encender TV...

    const tvRight = document.querySelector('.tv__right');
    const tvLeft = document.querySelector('.tv__left');

    tvRight.classList.toggle('encendida');
    tvLeft.classList.toggle('encendida');

    tvStatus = !tvStatus;
}