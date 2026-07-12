(function () {
  var STORAGE_KEY = "homely_lang";
  var DEFAULT_LANG = "en";
  var html = document.documentElement;

  function applyLang(lang) {
    html.setAttribute("data-lang", lang);
    document.querySelectorAll("[data-set-lang]").forEach(function (btn) {
      btn.classList.toggle("active", btn.getAttribute("data-set-lang") === lang);
    });
    try { localStorage.setItem(STORAGE_KEY, lang); } catch (e) {}
  }

  function initLang() {
    var saved = DEFAULT_LANG;
    try {
      saved = localStorage.getItem(STORAGE_KEY) || DEFAULT_LANG;
    } catch (e) {}
    applyLang(saved);
  }

  document.addEventListener("DOMContentLoaded", function () {
    initLang();
    document.querySelectorAll("[data-set-lang]").forEach(function (btn) {
      btn.addEventListener("click", function () {
        applyLang(btn.getAttribute("data-set-lang"));
      });
    });

    var toggle = document.querySelector(".nav-toggle");
    var nav = document.querySelector(".main-nav");
    if (toggle && nav) {
      toggle.addEventListener("click", function () {
        nav.classList.toggle("open");
      });
    }
  });
})();
