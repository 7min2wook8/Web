const signUpButton = document.getElementById('signUp');
const signInButton = document.getElementById('signIn');
const container = document.getElementById('container');


signUpButton.addEventListener('click', () => {
    //alert("회원가입1");
  container.classList.add("right-panel-active");
});

signInButton.addEventListener('click', () => {
   // alert("회원가입2");
  container.classList.remove("right-panel-active");
});
