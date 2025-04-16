//세션가져와서 로그인되어있는지 확인하는 코드 작성
async function checkSession() {
        //로그인 하지 않을 경우 보이는 화면
    let Login = document.querySelector(".Login");

    //로그인 되었을 경우 보이는 화면
    let logout = document.querySelector(".logout");

    logout.classList.add("hide");
    Login.classList.add("hide");   


    const response = await fetch('/dashboard', {
        method: 'GET',
        credentials: 'include'  // 세션 유지!
    });

    const data = await response.json();    

    if(data.status == "success"){
        logout.classList.remove("hide");
    }
    else{
        Login.classList.remove("hide");
    }
        
}

checkSession();

document.getElementById("logoutbtn").addEventListener("click", async() => {

    try {
      
        const response = await fetch('/logout', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json',
          },            
        });
  
        const data = await response.json();
        console.log(data.status)
        if (data.status == "success") {
          
          window.location.href = data.redirect;  // 페이지 이동
        }else
        {
          alert("data.status값 못받음");
          window.location.href = "/welcom"
        }
      } catch (error) {
        console.error('Error:', error);
      }


});