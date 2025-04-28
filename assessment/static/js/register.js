const loginText2 = document.querySelector(".title-text2 .login2");
const loginForm2 = document.querySelector("form.login2");
loginForm2.style.marginLeft = "-50%";
loginText2.style.marginLeft = "-50%";
function toggleTab2(tab) {
  const loginText2 = document.querySelector(".title-text2 .login2");
  const loginForm2 = document.querySelector("form.login2");
  const loginTab2 = document.getElementById('login2-tab2');
  const registerTab2 = document.getElementById('register-tab2');
  const sliderTab2 = document.querySelector('.slider-tab2');
  
  if (tab === 'login2') {
    // Update text colors
    loginTab2.style.color = '#fff'; // Turn "Login" text white
    registerTab2.style.color = '#000'; // Turn "Register" text black
    sliderTab2.style.left = '0';
    loginForm2.style.marginLeft = "0";
    loginText2.style.marginLeft = "0";
    // Move slider tab to "Login"
    
  } else if (tab === 'register2') {
    // Update text colors
    loginTab2.style.color = '#000'; // Turn "Login" text black
    registerTab2.style.color = '#fff'; // Turn "Register" text white
    sliderTab2.style.left = '50%';
    loginForm2.style.marginLeft = "-50%";
    loginText2.style.marginLeft = "-50%";
    // Move slider tab to "Register"
    
  }
}