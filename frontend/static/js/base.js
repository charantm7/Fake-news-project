document.addEventListener("DOMContentLoaded", function () {
  const hamburger = document.getElementById("hamburger");
  const sidebar = document.getElementById("sidebar");

  hamburger.addEventListener("click", function () {
    sidebar.classList.toggle("open");
    event.stopPropagation();
  });
  document.addEventListener("click", function (event) {
    if (!sidebar.contains(event.target) && event.target !== hamburger) {
      sidebar.classList.remove("open");
    }
  });
  window.addEventListener("scroll", function () {
    sidebar.classList.remove("open");
  });
});
// function hamburger(x) {
//   x.classList.toggle("change");
// }

let lastScrollTop = 0;

window.onscroll = function () {
  let currentScroll = window.pageYOffset || document.documentElement.scrollTop;

  if (currentScroll > lastScrollTop) {
    document.getElementById("navbar").style.top = "-94px";
  } else {
    document.getElementById("navbar").style.top = "0";
  }

  lastScrollTop = currentScroll;
};

document.addEventListener("DOMContentLoaded", function () {
  setTimeout(function () {
    // Add fade-out class to all messages after 3 seconds
    const messages = document.querySelectorAll(".message");
    messages.forEach(function (message) {
      message.classList.add("fade-out");
    });
  }, 3000); // 3 seconds delay before starting the fade-out
});
