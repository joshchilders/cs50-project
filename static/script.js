function updateSearch() {

    // Get values from range sliders
    let speed = document.getElementById('speed').value;
    let glide = document.getElementById('glide').value;
    let turn = document.getElementById('turn').value;
    let fade = document.getElementById('fade').value;

    // Get all disc cards
    let discs = document.querySelectorAll('#search-result');

    // Update values displayed above range sliders
    updateSpeed(speed);
    updateGlide(glide);
    updateTurn(turn);
    updateFade(fade);

    // Show/hide results based on search
    for (let i = 0; i < discs.length; i++) {
        let disc = discs[i];
        let disc_speed = parseInt(disc.querySelector('#disc-speed').innerHTML);
        let disc_glide = parseInt(disc.querySelector('#disc-glide').innerHTML);
        let disc_turn = parseInt(disc.querySelector('#disc-turn').innerHTML);
        let disc_fade = parseInt(disc.querySelector('#disc-fade').innerHTML);
        if ((speed < 1 || speed == disc_speed) && (glide < 1 || glide == disc_glide) && (turn < -5 || turn == disc_turn) && (fade < 0 || fade == disc_fade)) {
            disc.style.display = 'block';
        }
        else {
            disc.style.display = 'none';
        }
    }
}

function updateSpeed(speed) {

    // Update speed value displayed
    if (speed > 0) {
        document.getElementById('speed-output').value = speed;
    }
    else {
        document.getElementById('speed-output').value = 'Any';
    }
}

function updateGlide(glide) {

    // Update glide value displayed
    if (glide > 0) {
        document.getElementById('glide-output').value = glide;
    }
    else {
        document.getElementById('glide-output').value = "Any";
    }
}

function updateTurn(turn) {

    // Update turn value displayed
    if (turn > -6) {
        document.getElementById('turn-output').value = turn;
    }
    else {
        document.getElementById('turn-output').value = "Any";
    }
}

function updateFade(fade) {

    // Update fade value displayed
    if (fade > -1) {
        document.getElementById('fade-output').value = fade;
    }
    else {
        document.getElementById('fade-output').value = "Any";
    }
}