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
    else
        Login.classList.remove("hide");
}

checkSession();
