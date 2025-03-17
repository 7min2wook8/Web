// 공통 요소 삽입 함수
async function loadComponent(id, url) {
    const element = document.getElementById(id);
    if (element) {
        const response = await fetch(url);
        const html = await response.text();
        element.innerHTML = html;
    }
}

//위 함수 실행
// 페이지 로드 시 실행
document.addEventListener("DOMContentLoaded", () => {
    loadComponent("header", "../static/header.html");
    loadComponent("footer", "../static/footer.html");

});