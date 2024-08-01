document.addEventListener("DOMContentLoaded", function () {
  const currentPath = window.location.pathname;
  const navLinks = document.querySelectorAll(".nav-list a");
  const pageGroups = {
    "환경 호르몬 노출 평가": [
      "/test/",
      "/result/",
      "/detail-result/",
      "/analysis/",
      "/detail-analysis/",
    ],
    "맞춤형 플래너": ["/list/"],
    커뮤니티: [
      "/community/",
      "/community_create/",
      "/community_delete/",
      "/community_detail/",
      "/community_update/",
    ],
    "추천 상품": ["/market/"],
    "전문가 상담/예약": [
      "/expert/",
      "/reserve/",
      "/reserve_ok/",
      "/reserve_complete/",
    ],
  };

  navLinks.forEach((link) => {
    if (link.getAttribute("href") === currentPath) {
      link.classList.add("selected");
    } else {
      link.classList.remove("selected");
    }
  });
});
