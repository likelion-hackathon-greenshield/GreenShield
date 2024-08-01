document.addEventListener("DOMContentLoaded", function () {
  const itemsSets = [
    document.querySelectorAll(".main_middle_1_items_1, .main_middle_1_items_2, .main_middle_1_items_3, .main_middle_1_items_4"),
    document.querySelectorAll(".main_middle_1_items_5, .main_middle_1_items_6, .main_middle_1_items_7, .main_middle_1_items_8"),
    document.querySelectorAll(".main_middle_1_items_9, .main_middle_1_items_10, .main_middle_1_items_11, .main_middle_1_items_12"),
  ];
  let currentSetIndex = 0;

  function showSet(setIndex) {
    itemsSets.forEach((set, index) => {
      set.forEach((item) => {
        item.style.display = index === setIndex ? "flex" : "none";
      });
    });
  }

  function showNextSet() {
    currentSetIndex = (currentSetIndex + 1) % itemsSets.length;
    showSet(currentSetIndex);
  }

  showSet(currentSetIndex); // 초기 세트 표시
  setInterval(showNextSet, 3000); // 3초마다 세트 변경
});
