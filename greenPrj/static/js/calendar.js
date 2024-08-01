// calendar.js
// reserve.html
document.addEventListener("DOMContentLoaded", function () {
  const calendarBody = document.getElementById("calendar-body");
  const monthTitle = document.getElementById("month-title");
  let currentDate = new Date();
  let selectedDateElement = null; // 선택된 날짜의 td 요소

  function updateCalendar(date) {
    calendarBody.innerHTML = ""; // 기존 달력 내용 삭제
    const year = date.getFullYear();
    const month = date.getMonth();
    const firstDay = new Date(year, month, 1).getDay();
    const lastDate = new Date(year, month + 1, 0).getDate();

    // 월 제목 업데이트
    monthTitle.textContent = date.toLocaleDateString("ko-KR", {
      year: "numeric",
      month: "long",
    });

    // 첫 번째 주 빈 공간 채우기
    let row = document.createElement("tr");
    for (let i = 0; i < firstDay; i++) {
      let cell = document.createElement("td");
      row.appendChild(cell);
    }

    // 날짜 채우기
    for (let day = 1; day <= lastDate; day++) {
      if (row.children.length === 7) {
        calendarBody.appendChild(row);
        row = document.createElement("tr");
      }
      let cell = document.createElement("td");
      cell.textContent = day;

      // 날짜 클릭 이벤트 추가
      cell.addEventListener("click", () => {
        // 이전에 선택된 날짜의 스타일 초기화
        if (selectedDateElement) {
          selectedDateElement.style.backgroundColor = "";
        }
        // 선택된 날짜 스타일 적용
        cell.style.backgroundColor = "#BAE3B3";
        selectedDateElement = cell;

        // input date 값 업데이트
        document.getElementById("date").value = `${year}-${String(
          month + 1
        ).padStart(2, "0")}-${String(day).padStart(2, "0")}`;
      });

      row.appendChild(cell);
    }
    calendarBody.appendChild(row);
  }

  document.getElementById("prev-month").addEventListener("click", () => {
    currentDate.setMonth(currentDate.getMonth() - 1);
    updateCalendar(currentDate);
  });

  document.getElementById("next-month").addEventListener("click", () => {
    currentDate.setMonth(currentDate.getMonth() + 1);
    updateCalendar(currentDate);
  });

  // 초기 달력 로드
  updateCalendar(currentDate);

  // 상담 시간 예약 버튼
  // 상담 시간 예약 버튼
  // 상담 시간 예약 버튼
  const timeButtons = document.querySelectorAll(".time");
  let selectedTimeButton = null; // 선택된 시간 버튼

  // 시간 버튼 클릭 이벤트 추가
  timeButtons.forEach((button) => {
    button.addEventListener("click", function () {
      // 이전에 선택된 버튼의 스타일 초기화
      if (selectedTimeButton) {
        // selectedTimeButton.classList.remove("selected");
        selectedTimeButton.style.backgroundColor = "";
      }
      // 선택된 버튼 스타일 적용
      //   this.classList.add("selected");
      //   selectedTimeButton = this;
      this.style.backgroundColor = "#BAE3B3";
      selectedTimeButton = this;

      // input hidden 필드 값 업데이트
      document.getElementById("time").value = this.getAttribute("data-time");
    });
  });
});
