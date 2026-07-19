document.addEventListener("DOMContentLoaded", function () {
  /* ---------------- Loader ---------------- */
  var loader = document.getElementById("loader");
  if (loader) {
    var hideLoader = function () {
      loader.classList.add("loaded");
      setTimeout(function () {
        loader.style.display = "none";
      }, 450);
    };
    if (document.readyState === "complete") {
      setTimeout(hideLoader, 200);
    } else {
      window.addEventListener("load", function () {
        setTimeout(hideLoader, 200);
      });
    }
    /* Safety fallback in case the load event never fires */
    setTimeout(hideLoader, 2500);
  }

  /* ---------------- Back to top button ---------------- */
  var topBtn = document.getElementById("topBtn");
  if (topBtn) {
    var toggleTopBtn = function () {
      if (window.scrollY > 320) {
        topBtn.classList.add("show");
      } else {
        topBtn.classList.remove("show");
      }
    };
    window.addEventListener("scroll", toggleTopBtn, { passive: true });
    toggleTopBtn();
    topBtn.addEventListener("click", function () {
      window.scrollTo({ top: 0, behavior: "smooth" });
    });
  }

  /* ---------------- Navbar shadow on scroll ---------------- */
  var navbar = document.querySelector(".custom-navbar");
  if (navbar) {
    var toggleNavbarState = function () {
      if (window.scrollY > 12) {
        navbar.classList.add("is-scrolled");
      } else {
        navbar.classList.remove("is-scrolled");
      }
    };
    window.addEventListener("scroll", toggleNavbarState, { passive: true });
    toggleNavbarState();
  }

  /* ---------------- Auto-dismiss toast notifications ---------------- */
  var toasts = document.querySelectorAll(".toast.show");
  toasts.forEach(function (toast, index) {
    setTimeout(function () {
      toast.style.transition = "opacity .4s ease, transform .4s ease";
      toast.style.opacity = "0";
      toast.style.transform = "translateX(20px)";
      setTimeout(function () {
        toast.remove();
      }, 450);
    }, 4200 + index * 300);
  });
});
