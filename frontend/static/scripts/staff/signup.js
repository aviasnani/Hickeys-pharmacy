import {apiPost} from "../common/api.js";

document.addEventListener("DOMContentLoaded", () => {
  const btn = document.getElementById("signup-btn");
  btn.addEventListener("click", handleSignup);
});

function handleSignup() {
  var fname = document.getElementById("fname").value;
  var lname = document.getElementById("lname").value;
  var age = document.getElementById("age").value;
  var phone_number = document.getElementById("phone_number").value;
  var dob = document.getElementById("dob").value;
  var username = document.getElementById("username").value;
  var password = document.getElementById("password").value;
  var confirm_password =
    document.getElementById("confirm_password").value;
  var data = {
    first_name: fname,
    last_name: lname,
    age: age,
    phone_number: phone_number,
    date_of_birth: dob,
    username: username,
    password: password,
    confirm_password: confirm_password,
  };
  apiPost(`https://hickeys-backend-c66t793lq-aviasnanis-projects.vercel.app/staff_signup`, data)
    .then(response => {
      if (response.error) {
          let responded = document.getElementById("backend-res");
          const data_string = `Error: ${response.error}`;
          responded.innerHTML = data_string;
           
        }else{
          window.location.href = "/templates/staff/staff_login.html"
        }
      })
    .catch(function (error) {
      console.log(`Fetch error: ${error}`);
    });
}