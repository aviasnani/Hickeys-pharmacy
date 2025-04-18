import { apiPost } from "../common/api.js";

document.addEventListener("DOMContentLoaded", () => {
  const btn = document.getElementById("login-btn");
  btn.addEventListener("click", handleLogin);
});

function handleLogin() {
  var username = document.getElementById("username").value;
  var password = document.getElementById("password").value;
  var data = {
    username: username,
    password: password,
  };
  apiPost("https://hickeys-backend-o3fasm9eb-aviasnanis-projects.vercel.app/admin_login", data)
  .then(response => {
    if (response.error) {
        let error = document.getElementById("error");
        error_message = `Error: ${response.error}`;
        error.innerHTML = error_message;
      }else{
        window.location.href = "/templates/admin/admin_dashboard.html";
      }
    }
  ).catch(function (error) {
    console.log(`Fetch error: ${error}`);
  });
}