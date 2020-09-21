/* dropdown fun https://www.w3schools.com/howto/howto_js_dropdown.asp*/
function dropdown(id) {
    document.getElementById(id).classList.toggle("show");
    console.log(dropdownId)
  }
  
// Close the dropdown menu if the user clicks outside of it
window.onclick = function(event) {
    if (!event.target.matches('.dropbtn')) {
        var dropdowns = document.getElementsByClassName("dropdown-content");
        var i;
        for (i = 0; i < dropdowns.length; i++) {
            var openDropdown = dropdowns[i];
            if (openDropdown.classList.contains('show')) {
                openDropdown.classList.remove('show');
            }
        }
    }
}

/* switcher */

function switcher(type) {
    if (document.getElementById('equation').classList.contains('show')) {
        document.getElementById('equation').classList.remove('show');
    }
    if (document.getElementById('multiple_choice').classList.contains('show')) {
        document.getElementById('multiple_choice').classList.remove('show');
    }
    document.getElementById(type).classList.toggle('show');
    document.getElementById(type).value.setAttribute('value', type);
}