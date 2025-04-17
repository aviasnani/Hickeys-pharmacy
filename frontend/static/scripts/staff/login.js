import {apiPost} from "../common/api.js";

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
  apiPost(`https://hickeys-pharmacy-ejpk67g7i-aviasnanis-projects.vercel.app/staff_login`, data)
    .then(response => {
      if (response.error) {
        console.log(`Response status was not 200: ${response.status}`);
        let responded = document.getElementById("backend-res");
        responded.innerHTML = "Error: " + response.error;
      }else{
        window.location.href = "/templates/staff/staff_dashboard.html"
      }
})
    .catch(function (error) {
      console.log(`Fetch error: ${error}`);
    });
}