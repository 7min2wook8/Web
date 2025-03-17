//세션가져와서 로그인되어있는지 확인하는 코드 작성
async function checkSession() {
    const response = await fetch('/dashboard', {
        method: 'GET',
        credentials: 'include'  // 세션 유지!
    });

    const data = await response.json();
    console.log(data);
    
    if (data.status == "success") {
        return true;
    }
    else
        return false;
    }


window.onload = () =>{

    let notLogin = document.querySelector(".notLogin");
    let onLogin = document.querySelector(".onLogin");
    console.log("login 버튼들 찾아용");
    console.log(notLogin);
    console.log(onLogin);
    //로그인 정보 확인 후 오른쪽 상단 버튼 숨김 보임 표시
    if (checkSession()) {

        notLogin.classList.add("hide");
        onLogin.classList.remove("hide");
        
    }
    else{
        onLogin.classList.add("hide");
        notLogin.classList.remove("hide");
        
    }
}

document.addEventListener("DOMContentLoaded", () =>{

   


});
