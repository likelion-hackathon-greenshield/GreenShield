document.addEventListener("DOMContentLoaded", function () {
  // graph 요소와 score-percent 요소 가져오기
  var graphElement = document.querySelector(".graph");
  var scorePercentElement = document.querySelector(".score-percent");

  // data-total-score 속성에서 total_score 값 가져오기
  var totalScore = graphElement.dataset.totalScore;
  totalScore = parseFloat(totalScore); // 숫자형으로 변환

  // total_score의 2배 계산
  var scorePercent = totalScore * 2;

  // 그래프의 배경 스타일 설정
  graphElement.style.background = `conic-gradient(#bae3b3 0% ${scorePercent}%, #5a976b ${scorePercent}% 100%)`;

  // 점수 퍼센트 텍스트 설정
  scorePercentElement.textContent = `${scorePercent}%`;
});
