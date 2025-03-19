//세션가져와서 로그인되어있는지 확인하는 코드 작성
async function checkSession() {
    const response = await fetch('/dashboard', {
        method: 'GET',
        credentials: 'include'  // 세션 유지!
    });

    const data = await response.json();    
    
    return data.status === "success"; //자료형과 값이 일치하면 true
}

document.addEventListener("DOMContentLoaded", async () =>{

   //로그인 하지 않을 경우 보이는 화면
   let notLogin = document.querySelector(".notLogin");

   //로그인 되었을 경우 보이는 화면
   let onLogin = document.querySelector(".onLogin");
   onLogin.classList.add("hide");
   notLogin.classList.add("hide");   
    
   //로그인 정보 확인 후 오른쪽 상단 버튼 숨김 보임 표시 
    if (await checkSession()) {
            
            onLogin.classList.remove("hide");
    }
    else{
            
            notLogin.classList.remove("hide");
        
    }
});
