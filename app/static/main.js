console.log("JavaScriptが読み込まれました.");

const btn = document.getElementById("scroll-top-button");

if (btn) {
  btn.addEventListener("click", function () {
    window.scrollTo({
      top: 0,
      behavior: "smooth",
    });
  });
}
