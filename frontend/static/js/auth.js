document.addEventListener("DOMContentLoaded", function () {
  const login = document.getElementById("login");
  const signup = document.getElementById("signup");
  const loginSection = document.getElementById("login-form");
  const signupSection = document.getElementById("signup-form");

  login.onclick = () => {
    loginSection.classList.add("open");
    signupSection.classList.remove("open");
  };

  signup.onclick = () => {
    signupSection.classList.add("open");
    loginSection.classList.remove("open");
  };
});

document.addEventListener("DOMContentLoaded", () => {
  const queryParams = new URLSearchParams(window.location.search);
  const action = queryParams.get("action");
  const loginSection = document.getElementById("login-form");
  const signupSection = document.getElementById("signup-form");

  if (action === "signup") {
    signupSection.classList.add("open");
  } else if (action === "login") {
    loginSection.classList.add("open");
  }
});

function togglePassword(fieldId) {
  var passwordField = document.getElementById(fieldId);
  var hideIcon = document.getElementById("hide-" + fieldId);
  var showIcon = document.getElementById("show-" + fieldId);

  if (passwordField.type === "password") {
    passwordField.type = "text";
    hideIcon.style.display = "none";
    showIcon.style.display = "block";
  } else {
    passwordField.type = "password";
    hideIcon.style.display = "block";
    showIcon.style.display = "none";
  }
}
