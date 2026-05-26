// 🔹 SECTION SWITCHING (SPA)
function showSection(sectionId){

    let sections =
    document.querySelectorAll('.content-section');

    sections.forEach(section => {
        section.classList.remove('active');
    });

    document.getElementById(sectionId)
    .classList.add('active');
}

function toggleSidebar(){

    document.querySelector('.sidebar')
    .classList.toggle('active');

}


// 🔹 DARK/LIGHT THEME TOGGLE
function toggleTheme(){

    alert("Theme button working");

    document.body.classList.toggle('dark-mode');

}


// 🔹 LOAD SAVED THEME
window.onload = function () {
    if (localStorage.getItem('theme') === 'dark') {
        document.body.classList.add('dark');
    }
}


// 🔹 OPTIONAL: LOADING SPINNER
function showLoader() {
    let loader = document.getElementById("loader");
    if (loader) loader.style.display = "block";
}

function hideLoader() {
    let loader = document.getElementById("loader");
    if (loader) loader.style.display = "none";
}