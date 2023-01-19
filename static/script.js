window.onload = function() {
    updateSearch();
}

function updateSearch() {

    // Get values from range sliders
    let speed = document.getElementById('speed').value;
    let glide = document.getElementById('glide').value;
    let turn = document.getElementById('turn').value;
    let fade = document.getElementById('fade').value;

    // Update values displayed above range sliders
    updateSpeed(speed);
    updateGlide(glide);
    updateTurn(turn);
    updateFade(fade);

    // Get all disc cards
    let discs = document.querySelectorAll('#search-result');

    // Clear current search results
    for (let i = 0; i < discs.length; i++) {
        discs[i].style.display = 'none';
    }

    // Show results based on search
    let count = 0;
    for (let i = 0; i < discs.length; i++) {
        let disc = discs[i];
        let disc_speed = parseInt(disc.querySelector('#disc-speed').innerHTML);
        let disc_glide = parseInt(disc.querySelector('#disc-glide').innerHTML);
        let disc_turn = parseInt(disc.querySelector('#disc-turn').innerHTML);
        let disc_fade = parseInt(disc.querySelector('#disc-fade').innerHTML);
        if ((speed < 1 || speed == disc_speed) && (glide < 1 || glide == disc_glide) && (turn < -5 || turn == disc_turn) && (fade < 0 || fade == disc_fade)) {
            if (count < 6) {
                fadeIn(disc);
                count++;
            }
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

function updateItemList() {
    let plastic = document.getElementById('plastic').value;
    let run = document.getElementById('run').value;
    let items = document.querySelectorAll('#item');

    for (let i = 0; i < items.length; i++) {
        let item = items[i];
        let item_plastic = item.querySelector('#item-plastic').innerHTML;
        let item_run = item.querySelector('#item-run').innerHTML;

        if ((item_plastic == plastic || plastic == 'All Plastics') && (item_run == run || run == 'All Runs')) {
            item.style.display = 'block';
        }
        else {
            item.style.display = 'none';
        }
    }
}

function updateRunOptions(runs) {
    let plastic = document.getElementById('plastic').value;
    let select = document.getElementById('run');

    if (plastic != 'All Plastics') {
        // Remove all current options
        while (select.options.length > 0) {
            select.remove(0);
        }
        let newOption = new Option('All Runs', 'All Runs');
        select.add(newOption, undefined);

        // Add new appropriate options
        for (i = 0; i < runs[plastic].length; i++) {
            let newOption = new Option(runs[plastic][i], runs[plastic][i]);
            select.add(newOption, undefined);
        }
    }
    else {
        // Remove all options other than 'All Runs'
        while (select.options.length > 0) {
            select.remove(0);
        }
        let newOption = new Option('All Runs', 'All Runs');
        select.add(newOption, undefined);
    }
}

function fadeIn(element) {
    let opacity = 0.1;  // initial opacity
    element.style.opacity = opacity;
    element.style.display = 'block';
    let timer = setInterval(function () {
        if (opacity >= 1){
            clearInterval(timer);
        }
        element.style.opacity = opacity;
        element.style.filter = 'alpha(opacity=' + opacity * 100 + ")";
        opacity += opacity * 0.1;
    }, 10);
}
