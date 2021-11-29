// Part 1 of slider:
//	From: https://gitlab.com/gr0ssmann/otree_slider,
//	Further explanation (older version): https://www.accountingexperiments.com/post/sliders/


var slider_min = 0;
var slider_max = 100;
var slider_step = 1;

var oldval = "";

function showVal1(what) {
    showFloat(document.getElementById("cval1"), what, 0);
    document.getElementById("belief").value = what;

    oldval = what;
}

function show_slider(event) {
    max = parseInt(getComputedStyle(document.getElementById("before")).width.replace("px", ""));
    cur = event.offsetX;


    now = (cur/max)*(slider_max-slider_min) + slider_min;
    now = Math.round(now/slider_step)*slider_step;

    document.getElementById("before").style.display = "none";
    document.getElementById("belief_slider").style.display = "block";
    document.getElementById("show_belief").style.color = "#000";

    showVal1(now);
    document.getElementById("belief_slider").value = now;
}

function showFloat(el, val, dec = 0) {

    if (isNaN(val)) {
        el.innerHTML = "???";
    }
    else {
        el.innerHTML = (parseFloat(val).toFixed(dec) + "%");
    }
}

$(document).ready(function (event) {
    document.getElementById("belief_slider").min = slider_min;
    document.getElementById("belief_slider").max = slider_max;
    document.getElementById("belief_slider").step = slider_step;

    showFloat(document.getElementById("slidermin"), slider_min);
    showFloat(document.getElementById("slidermax"), slider_max);
});