const date = new Date();
document.querySelector('.year').innerHTML = date.getFullYear();

// add following for login register
setTimeout(() => {
    $('#message').fadeOut("slow");
}, 3000);

