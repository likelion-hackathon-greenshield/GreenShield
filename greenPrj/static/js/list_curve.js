document.addEventListener("DOMContentLoaded", function () {
  // 현재 날짜 가져오기
  const today = new Date();
  const currentMonth = today.getMonth(); // 0 (January) ~ 11 (December)

  // 월 이름 배열
  const monthNames = [
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec",
  ];

  // 최근 4개월 계산
  const recentMonths = [];
  for (let i = 3; i >= 0; i--) {
    const monthIndex = (currentMonth - i + 12) % 12;
    recentMonths.push(monthNames[monthIndex]);
  }

  // bar2-x-axis 요소 업데이트
  const xAxisElements = document.querySelectorAll(".bar2-x-axis li");
  xAxisElements.forEach((element, index) => {
    element.textContent = recentMonths[index];
    if (index === 3) {
      // 가장 최근 달인 경우 스타일 추가
      element.style.color = "#5a976b";
    }
  });

  // 곡선 그래프
  // 곡선 그래프
  // 곡선 그래프

  // JSON 데이터 가져오기
  const dataElement = document.getElementById("data");
  console.log("Raw JSON data:", dataElement.textContent);
  const data = JSON.parse(dataElement.textContent);

  // 최근 4개월의 데이터 가져오기
  const counts = recentMonths.map((month) => data[month] || 0);

  // y값 계산
  const yValues = counts.map((count) => 100 - count * 2);

  // SVG path의 d 속성 값 생성
  const d = `
    M 15 ${yValues[0]}
    C 45 ${yValues[0]} 75 ${yValues[1]} 105 ${yValues[1]}
    C 135 ${yValues[1]} 165 ${yValues[2]} 195 ${yValues[2]}
    C 225 ${yValues[2]} 255 ${yValues[3]} 285 ${yValues[3]}
  `;

  // path 요소 업데이트
  const pathElement = document.querySelector(".bar2-line path");
  pathElement.setAttribute("d", d);
});
