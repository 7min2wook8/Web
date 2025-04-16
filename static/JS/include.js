//header와 footer를 호출하고 그 안에 script를 실행함

async function loadComponent(id, url) {
  const element = document.getElementById(id);
  if (element) {
    const response = await fetch(url);
    const html = await response.text();

    // 임시 DOM에 파싱
    const tempDiv = document.createElement("div");
    tempDiv.innerHTML = html;

    // script 태그 분리
    const scripts = tempDiv.querySelectorAll("script");
    scripts.forEach(script => script.remove()); // 일단 제거

    // HTML만 삽입
    element.innerHTML = tempDiv.innerHTML;

    // script 수동 실행
    scripts.forEach(oldScript => {
      const newScript = document.createElement("script");
      if (oldScript.src) {
        newScript.src = oldScript.src;
      } else {
        newScript.textContent = oldScript.textContent;
      }
      document.body.appendChild(newScript);
    });
  }
}

// 실행
document.addEventListener("DOMContentLoaded", () => {
  loadComponent("header", "/static/header.html");
  loadComponent("footer", "/static/footer.html");

});