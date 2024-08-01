document.addEventListener("DOMContentLoaded", () => {
  // completionData는 HTML에서 직접 선언된 전역 변수입니다.
  if (completionData) {
    // 모든 <ul class="bar1"> 내의 <li> 요소를 선택
    const barElements = document.querySelectorAll("ul.bar1 li");

    // 오늘의 요일을 구합니다 (0: 일요일, 1: 월요일, ..., 6: 토요일)
    const today = new Date().getDay();

    // completionData 객체의 day와 count에 접근
    let index = 0;
    for (const day in completionData) {
      if (completionData.hasOwnProperty(day)) {
        const count = completionData[day];
        if (barElements[index]) {
          if (count === 0) {
            // count가 0인 경우
            barElements[index].style.height = "100px";
            barElements[index].style.backgroundColor = "#e0e0e0"; // 예를 들어 연한 회색으로 설정
          } else if (index < today) {
            // 오늘 이전의 요일
            barElements[index].style.height = count * 20 + "px";
            barElements[index].style.backgroundColor = "#5a976b";
          } else if (index === today) {
            // 오늘
            barElements[index].style.height = count * 20 + "px";
            barElements[index].style.backgroundColor = "#bae3b3";
          }
          // 오늘 이후 요일은 스타일 변경 없음
        }
        index++;
      }
    }
  }
});
