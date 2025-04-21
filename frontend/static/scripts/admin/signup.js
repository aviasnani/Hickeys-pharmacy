import {apiPost} from "../common/api.js"

document.addEventListener("DOMContentLoaded", () => {
  const btn = document.getElementById("signup-btn");
  btn.addEventListener("click", handleSignup);
});

function handleSignup() {
  var first_name = document.getElementById("first_name").value;
  var last_name = document.getElementById("last_name").value;
  var email = document.getElementById("email").value;
  var username = document.getElementById("username").value;
  var password = document.getElementById("password").value;
  var confirm_password =
    document.getElementById("confirm_password").value;
  var data = {
    first_name: first_name,
    last_name: last_name,
    email: email,
    username: username,
    password: password,
    confirm_password: confirm_password,
  };
  apiPost("http://127.0.0.1:5000/admin_signup", data)
    .then(response => {
      if (response.error) {
          let errors_div = document.getElementById("error-div");
          var data_string = `Error: ${response.error}`;
          errors_div.innerHTML = data_string;
          console.log(`Response status was not 200: ${response.error}`);
      }else{
        window.location.href = "/templates/admin/admin_login.html";
      }
      })
    .catch(function (error) {
      console.log(`Fetch error: ${error}`);
    });
}