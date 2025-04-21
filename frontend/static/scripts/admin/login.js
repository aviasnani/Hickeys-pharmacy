import { apiPost } from "../common/api.js";
import{API_BASE_URL} from "../common/utils.js";

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
  console.log(data);
  apiPost(`${API_BASE_URL}/admin_login`, data)
  .then(response => {
    if (response.error) {
        let error = document.getElementById("error");
        let error_message = `Error: ${response.error}`;
        error.innerHTML = error_message;
      }else{
        window.location.href = "/templates/admin/admin_dashboard.html";
      }
    }
  ).catch(function (error) {
    console.log(`Fetch error: ${error}`);
    console.log("Error: " + error);
  });
}