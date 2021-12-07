$(window).on("load", function() {
    $(".load-page").fadeOut(1000);
    
    var mode = localStorage.getItem('mode');
    if (mode === "light") {
        document.querySelector('body').classList.add('light');
        document.getElementById('btn-view-mode').innerHTML = '<ion-icon name="moon"></ion-icon>Dark Mode';
    }
    else {
        document.querySelector('body').classList.remove('light');
        document.getElementById('btn-view-mode').innerHTML = '<ion-icon name="sunny"></ion-icon>Light Mode';
    }
});

function changeMode() {  
    let body =  document.querySelector('body');      
    let settingMenu = document.querySelector('.setting-menu');

    body.classList.toggle('light');
    var mode = body.getAttribute('class');
    if (mode === 'light') {
        localStorage.setItem('mode', 'light');
        document.getElementById('btn-view-mode').innerHTML = '<ion-icon name="moon"></ion-icon>Dark Mode';
        settingMenu.classList.remove('show');
    }
    else {
        localStorage.setItem('mode', 'dark');                       
        document.getElementById('btn-view-mode').innerHTML = '<ion-icon name="sunny"></ion-icon>Light Mode';   
        settingMenu.classList.remove('show'); 
    }            
}

let btnSetting = document.querySelector('.btn-setting');
let settingMenu = document.querySelector('.setting-menu');

btnSetting.onclick = function() {
    settingMenu.classList.toggle('show');
} 