function toggleTab(tab) {
    const loginText = document.querySelector(".title-text .login");
    const loginForm = document.querySelector("form.login");
    const loginTab = document.getElementById('login-tab');
    const registerTab = document.getElementById('register-tab');
    const sliderTab = document.querySelector('.slider-tab');

    if (tab === 'register') {
      // Update text colors
      loginTab.style.color = '#000'; // Turn "Login" text black
      registerTab.style.color = '#fff'; // Turn "Register" text white

      // Move slider tab to "Register"
      sliderTab.style.left = '50%';
      loginForm.style.marginLeft = "-50%";
      loginText.style.marginLeft = "-50%";
    } else {
      // Update text colors
      loginTab.style.color = '#fff'; // Turn "Login" text white
      registerTab.style.color = '#000'; // Turn "Register" text black

      // Move slider tab to "Login"
      sliderTab.style.left = '0';
      loginForm.style.marginLeft = "0";
      loginText.style.marginLeft = "0";
    }
  }