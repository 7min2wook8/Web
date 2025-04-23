
async function getNoticeBoardData() {
  console.log("호출")
let main = document.querySelector(".noticeBoard_main");

let zeroNoticeBoard = main.querySelector(".zeroNoticeBoard");
let viewNoticeBoard = main.querySelector(".viewNoticeBoard");

const response = await fetch('/getNoticeBoardData', {
    method: 'GET',
    credentials: 'include'
});

const data = await response.json();    

if (data.status == "success") {
  if (!data || !Array.isArray(data.contents) || data.contents.length === 0){
    console.log("데이터가 잘못됨")
    return;
  }
    
    zeroNoticeBoard.classList.add("hide");

    const container = viewNoticeBoard;
    data.contents.forEach(con => {
      const div = document.createElement("div");
      div.classList.add("noticeBoard_Item");
      
          // yyyy-mm-dd 형식으로 출력
      //const formattedDate = date.toISOString().split("T")[0];
      const createdAt = new Date(con.created_at);
      const now = new Date();
      const isSameDate =
      createdAt.getFullYear() === now.getFullYear() &&
      createdAt.getMonth() === now.getMonth() &&
      createdAt.getDate() === now.getDate();

      let formattedDate = "";
      if (isSameDate) {
          // 오늘이면 시:분:초
          const hours = String(createdAt.getHours()).padStart(2, '0');
          const minutes = String(createdAt.getMinutes()).padStart(2, '0');
          const seconds = String(createdAt.getSeconds()).padStart(2, '0');
          formattedDate = `${hours}:${minutes}:${seconds}`;
      } else {
          // 오늘이 아니면 년-월-일
          const year = createdAt.getFullYear();
          const month = String(createdAt.getMonth() + 1).padStart(2, '0');
          const day = String(createdAt.getDate()).padStart(2, '0');
          formattedDate = `${year}-${month}-${day}`;
      }


  

      div.innerHTML += `
      <div class="holseHead">${con.holseHead}</div>
      <a href="/post/${con.Content_SERIAL_id2}" class="item_title"><div>${con.Title}</div></a>
      <a href="#" class="item_writer"><div>${con.Email} </div></a>
      <div class="item_writeDate">${formattedDate}</div>
      <div class="item_viewCount">${con.viewCount}</div>
      <div class="item_greatCount">${con.greatCount}</div>
      `;


      container.appendChild(div);
    });
  } else {
    viewNoticeBoard.classList.add("hide");
    console.error("불러오기 실패:", data.message);
  }

    
}


getNoticeBoardData();

