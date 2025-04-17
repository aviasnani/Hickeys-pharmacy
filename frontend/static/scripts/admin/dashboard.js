import {apiGet, apiPost, apiDelete, apiPut} from "../common/api.js";

document.addEventListener("DOMContentLoaded", () => {
  const btn = document.getElementById("logout-btn");
  btn.addEventListener("click", logout);

  const btnAddMed = document.getElementById("add-staff-btn");
  btnAddMed.addEventListener("click", addStaff);

  const searchButton = document.getElementById("search-btn");
  searchButton.addEventListener("click", searchStaff);

  dashboardDetails();
});

function dashboardDetails() {
  apiGet("https://hickeys-pharmacy-ejpk67g7i-aviasnanis-projects.vercel.app/admin_dashboard")
    .then(response => {
      if (response.error) {
        console.log(`Response status was not 200: ${response.error}`);
      }
      else {
        var staff_people = response.staff;  
        var admin = response.admin_name;   
        var h1 = document.getElementById("h1");
        h1.innerHTML = `Welcome ${admin}`;
        const tableBody = document.getElementById("table-body");
        staff_people.forEach((staff) => {
          const row = document.createElement("tr");
          row.innerHTML = `
            <td>${staff.id}</td>
            <td>${staff.fname}</td>
            <td>${staff.lname}</td>
            <td>${staff.age}</td>
            <td>${staff.phone}</td>
            <td>${staff.dob}</td>
            <td>${staff.username}</td>
            <td><button class='delete-btn'>Delete</button></td>
            <td><button class='update-btn'>Update</button></td>
          `;
          row.querySelector(".delete-btn").addEventListener("click", () => {
            deleteStaff(staff.id);
          });
        
          row.querySelector(".update-btn").addEventListener("click", (event) => {
            updateStaff(event, staff); // pass actual object directly
          });
          tableBody.appendChild(row);
          tableBody.appendChild(row);

        });
      }
    })
    .catch(function (error) {
      console.log(`Fetch error: ${error}`);
    });
}

document
  .getElementById("show-add-form")
  .addEventListener("click", function () {
    const container = document.getElementById("add-staff-container");
    if (container.style.display === "none") {
      container.style.display = "block";
    } else {
      container.style.display = "none";
    }
  });

function addStaff() {
  const fname = document.getElementById("fname").value;
  const lname = document.getElementById("lname").value;
  const age = document.getElementById("age").value;
  const phone = document.getElementById("phone").value;
  const dob = document.getElementById("dob").value;
  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;
  const confirm_password =
    document.getElementById("confirm_password").value;

  const data = {
    fname: fname,
    lname: lname,
    age: age,
    phone: phone,
    dob: dob,
    username: username,
    password: password,
    confirm_password: confirm_password,
  };
  if (data.password !== data.confirm_password) {
    alert("Passwords do not match");
    return;
  }
  apiPost("https://hickeys-pharmacy-ejpk67g7i-aviasnanis-projects.vercel.app/add_staff",data)
    .then(response => {
      if (response.error) {
          console.log(response.error); 
        }else{
          const tableBody = document.getElementById("table-body");
          document.getElementById("add-staff-container").style.display =
            "none";
          tableBody.innerHTML = ""; 
          dashboardDetails(); 
        }
      }
    )
    .catch(function (error) {
      console.log(`Fetch error: ${error}`);
    });
}
function searchStaff() {
  const searchInput = document.getElementById("search").value;
  if (!searchInput) {
    alert("Please enter a medicine name to search.");
    return;
  }

  const data = { fname: searchInput };  // Define the data object

  apiPost("https://hickeys-pharmacy-ejpk67g7i-aviasnanis-projects.vercel.app/search_staff", data)
    .then(response => {
      if (response.error) {
        console.log(`Response status was not 200: ${response.error}`);
      }
      else {
        const tableBody = document.getElementById("table-body");
        tableBody.innerHTML = ""; // Clear the table body
        if (response && response.length > 0) {
          response.forEach((staff) => { 
            const row = document.createElement("tr");
            row.innerHTML = `
              <td>${staff.id}</td>
              <td>${staff.fname}</td>
              <td>${staff.lname}</td>
              <td>${staff.age}</td>
              <td>${staff.phone}</td>
              <td>${staff.dob}</td>
              <td>${staff.username}</td>
            `;
            tableBody.appendChild(row);
          });
        } else {
          const row = document.createElement("tr");
          row.innerHTML = `
            <td colspan="7">No Staff found with the name ${searchInput}</td>
          `;
          tableBody.appendChild(row);
        }
      }
    })
    .catch(function (error) {
      console.log(`Fetch error: ${error}`);
    });
}
function updateStaff(event, staff) {
  const row = event.target.closest("tr");
  row.innerHTML = `
    <td>${staff.id}</td>
    <td><input type="text" id="edited-fname-${staff.id}" value="${
    staff.fname
  }" /></td>
    <td><input type="text" id="edited-lname-${staff.id}" value="${
    staff.lname
  }" /></td>
    <td><input type="text" id="edited-age-${staff.id}" value="${
    staff.age
  }" /></td>
    <td><input type="text" id="edited-phone-${staff.id}" value="${
    staff.phone
  }" /></td>
    <td><input type="text" id="edited-dob-${staff.id}" value="${
    staff.dob
  }" /></td>
    <td><input type="text" id="edited-username-${staff.id}" value="${
    staff.username
  }" /></td>
    <td><button class='save-btn'>Save</button></td>
  `;
  row.querySelector(".save-btn").addEventListener("click", () => {
    saveStaff(staff);
  });
}

function saveStaff(staff) {
  const id = staff.id;
  const updated_fname = document.getElementById(
    `edited-fname-${id}`
  ).value;
  const updated_lname = document.getElementById(
    `edited-lname-${id}`
  ).value;
  const updated_age = document.getElementById(`edited-age-${id}`).value;
  const updated_phone = document.getElementById(
    `edited-phone-${id}`
  ).value;
  const updated_dob = document.getElementById(`edited-dob-${id}`).value;
  const updated_username = document.getElementById(
    `edited-username-${id}`
  ).value;
  const updatedStaff = {
    id: id,
    fname: updated_fname,
    lname: updated_lname,
    age: updated_age,
    phone: updated_phone,
    dob: updated_dob,
    username: updated_username,
  };
  apiPut("https://hickeys-pharmacy-ejpk67g7i-aviasnanis-projects.vercel.app/update_staff", updatedStaff)
    .then(response => {
      if (response.error) {
        console.log(`Response status was not 200: ${response.error}`);
      }
     else{
      console.log(response);
      const tableBody = document.getElementById("table-body");
      tableBody.innerHTML = ""; // Clear the table body
      dashboardDetails(); // Refresh the dashboard details
     }
       
      })
    .catch(function (error) {
      console.log(`Fetch error: ${error}`);
    });
}

function deleteStaff(id) {
  apiDelete("https://hickeys-pharmacy-ejpk67g7i-aviasnanis-projects.vercel.app/delete_staff", { id: id })
    .then(response => {
      if (response.error) {
        console.log(`Response status was not 200: ${response.error}`);
      }
      else{
        console.log(response);
        const tableBody = document.getElementById("table-body");
        tableBody.innerHTML = ""; // Clear the table body
        dashboardDetails(); // Refresh the dashboard details
      }
      })
    .catch(function (error) {
      console.log(`Fetch error: ${error}`);
    });
}


function logout() {
  apiGet(`https://hickeys-pharmacy-ejpk67g7i-aviasnanis-projects.vercel.app/admin_logout`)
    .then(response =>  {
      // response from the server
      if (response.error) {
        console.log(`Response status was not 200: ${response.error}`);
      }
    else{
      window.location.href = "/templates/admin/admin_login.html"; // redirecting to the staff dashboard
      console.log("Logout Successful"); // consoling it to see the data
    }

       
      })
    .catch(function (error) {
      console.log(`Fetch error: ${error}`);
    });
}