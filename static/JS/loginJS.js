//profile.html 적용되는 JS

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


//회원가입 스크립트

document.getElementById("registerbtn").onclick = async function sendRegister(){
  const inputName = document.getElementById('inputName').value;
  const inputEmail = document.getElementById('inputEmail').value;
  const inputPw = document.getElementById('inputPw').value;
    
  try {
    
    const response = await fetch('/register', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json',
      },
      body: JSON.stringify({ inputName: inputName, inputEmail:inputEmail, inputPw: inputPw }),
    });

    const data = await response.json();
    
    if (data.status == "success") {
      
      window.location.href = data.redirect;  // 페이지 이동
    }else
    {
      alert("data.status값 못받음");
    }
  } catch (error) {
    console.error('Error:', error);
  }

return false;  // 폼 새로고침 방지
}


//async function sendLogin(){
document.getElementById('loginbtn').onclick = async function sendLogin(){
  
  const inputEmail = document.getElementById('loginEmail').value;
  const inputPw = document.getElementById('loginPw').value;
  
  try {
    /*response 변수에는 fetch 요청의 최종 결과 객체가 저장되지만, 
    이 객체는 .json() 메서드를 호출하기 전의 Response 객체 상태입니다. 
    따라서, response에는 JSON 파싱된 데이터가 아니라 Response 객체 자체가 저장됩니다.*/
    const response = await fetch('/login', {
        method: 'POST',
        headers: {
        'Content-Type': 'application/json'
        },
        credentials: 'include',  // 세션 유지 (Flask의 session 사용 시 필수!)
        body: JSON.stringify({ inputEmail: inputEmail, inputPw: inputPw }),
    });

    const contentType = response.headers.get("content-type");
    if (!contentType || !contentType.includes("application/json")) {
          throw new Error("서버 응답이 JSON이 아닙니다.");
    }
    
    if (!response.ok) {
    console.error(`❌ 서버 오류: ${response.status}`);
    return;
    }
    else{
      const data = await response.json();
      console.log("📌 응답 JSON 데이터:", data);

      if (data.status == "success") {
        
      window.location.href = data.redirect;  // 페이지 이동

      }else if (data.status == "fail") {
        //로그인 정보 X
        alert(data.message)
        location.reload(true);
      }

    }
} catch (error) {
    console.error('Error:', error);
    alert(error);
}

  // 폼 새로고침 방지
  return false;
}

