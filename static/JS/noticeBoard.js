//세션가져와서 로그인되어있는지 확인하는 코드 작성
async function getNoticeBoardData() {
    //로그인 하지 않을 경우 보이는 화면
let main = document.querySelector(".noticeBoard_main");

let zeroNoticeBoard = main.querySelector(".zeroNoticeBoard");
let viewNoticeBoard = main.querySelector(".viewNoticeBoard");

const response = await fetch('/getNoticeBoardData', {
    method: 'GET',
    credentials: 'include'
});

const data = await response.json();    

if (data.status === "success") {
    zeroNoticeBoard.classList.add("hide");

    const container = viewNoticeBoard;
    data.Contents.forEach(post => {
      const div = document.createElement("div");
      div.classList.add("noticeBoard_Item");
      div.innerHTML = `
        <h3>${post.title}</h3>
        <p>${post.content}</p>
        <small>작성자: ${post.author} | ${post.created_at}</small>
      `;
      container.appendChild(div);
    });
  } else {
    viewNoticeBoard.classList.add("hide");
    console.error("불러오기 실패:", data.message);
  }

    
}

getNoticeBoardData();