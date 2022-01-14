// JS for slider.
// Inspired by: https://codepen.io/JavRok/pen/pgJagr


// Defining variables
var range = document.getElementById("belief");
var minusButton = document.querySelector(".control-minus");
var plusButton = document.querySelector(".control-plus");
var steps = 100;

var output = document.getElementById("show_belief");
var touched = 0;

var minus_button_clicks = 0;
var plus_button_clicks = 0;

console.log("minus button clicks: ", minus_button_clicks);
console.log("plus button clicks: ", plus_button_clicks);

// All browsers but IE
range.addEventListener("input", function(evt) {
  current_value ();
}, false);
// IE10
range.addEventListener("change", function(evt) {
  current_value ();
}, false);

// Updating values
function current_value () {
  output.innerHTML = range.value;
  range.className = "slider";
  touched = 1;
}

// Plus and minus buttons
minusButton.addEventListener("click", function() {
  range.stepDown();
  current_value ();

  minus_button_clicks += 1;
  document.getElementById("minus_button_clicks").value = minus_button_clicks;
  console.log("minus button clicks: ", minus_button_clicks);

}, false);


plusButton.addEventListener("click", function() {
  range.stepUp();
  current_value ();

  plus_button_clicks += 1;
  document.getElementById("plus_button_clicks").value = plus_button_clicks;
  console.log("plus button clicks: ", plus_button_clicks);

}, false);



// on form submission, check that all elements have been moved
function checkTouched() {
    if (touched === 1 ) {
          form.submit();
    }
    else {
        event.preventDefault();
        window.scrollTo(0, 0);
        document.getElementById('alert').style.display="block";
    }
}
