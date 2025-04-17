import {apiGet, apiPost, apiDelete, apiPut} from "../common/api.js";

document.addEventListener("DOMContentLoaded", () => {
  const btn = document.getElementById("logout-btn");
  btn.addEventListener("click", logout);

  const btnAddMed = document.getElementById("add-med-btn");
  btnAddMed.addEventListener("click", addMed);

  const searchButton = document.getElementById("search-button");
  searchButton.addEventListener("click", searchMed);

  welcome();
});

document
        .getElementById("show-add-form")
        .addEventListener("click", function () {
          const container = document.getElementById("add-staff-container");
          container.style.display =
            container.style.display === "none" ? "block" : "none";
        });

      function addMed() {
        var name = document.getElementById("name").value;
        var brand = document.getElementById("brand").value;
        var description = document.getElementById("description").value;
        var form = document.getElementById("form").value;
        var dosage = document.getElementById("dosage").value;
        var price = document.getElementById("price").value;
        var data = { name, brand, description, form, dosage, price };

        apiPost("https://hickeys-backend-o3fasm9eb-aviasnanis-projects.vercel.app/add_meds", data)
          .then(response => {
            if (response.error) {
              console.log(`Response status was not 200: ${response.status}`);
            }
            else{
            document.getElementById("name").value = "";
            document.getElementById("brand").value = "";
            document.getElementById("description").value = "";
            document.getElementById("form").value = "";
            document.getElementById("dosage").value = "";
            document.getElementById("price").value = "";
            document.getElementById("add-staff-container").style.display =
              "none";
            welcome();
            console.log("Medicine added successfully");
            }
         
            
          })
          .catch((error) => {
            console.log(`Fetch error: ${error}`);
          });
      }

      function welcome() {
        apiGet("https://hickeys-backend-o3fasm9eb-aviasnanis-projects.vercel.app/staff_dashboard")
          .then(response => {
            if (response.error) {
              console.log(`Response status was not 200: ${response.error}`);
            }else{
              document.getElementById(
                "h1"
              ).innerHTML = `Welcome, ${response.staff_name}!`;
              var tableBody = document.getElementById("table-body");
              tableBody.innerHTML = "";
              response.med.forEach((medicine) => {
                var row = document.createElement("tr");
                row.innerHTML = `
                  <td>${medicine.id}</td>
                  <td>${medicine.name}</td>
                  <td>${medicine.brand}</td>
                  <td>${medicine.description}</td>
                  <td>${medicine.form}</td>
                  <td>${medicine.dosage}</td>
                  <td>${medicine.price}</td>
                  <td><button class="delete-med">Delete</button></td>
                  <td><button class="edit-med">Edit</button></td>
                `;
                row.querySelector(".delete-med").addEventListener("click", () => {
                  deleteMed(medicine.id);
                });
              
                row.querySelector(".edit-med").addEventListener("click", (event) => {
                  editMed(event, medicine); // pass actual object directly
                });
                tableBody.appendChild(row);
              });
            }
            })
            .catch((error) => {
            console.log(`Fetch error: ${error}`);
          });
      }


      function deleteMed(id) {
        apiDelete("https://hickeys-backend-o3fasm9eb-aviasnanis-projects.vercel.app/delete_meds", { id: id })
          .then(response => {
            if (response.error) {
              console.log(`Response status was not 200: ${response.error}`);

            }
            else{
              console.log("Medicine deleted successfully");
              const tableBody = document.getElementById("table-body");
              tableBody.innerHTML = ""; // Clear the table body
              welcome(); // Refresh the dashboard details
            }   
            })
          .catch(function (error) {
            console.log(`Fetch error: ${error}`);
          });
      }
      function searchMed() {
        const searchInput = document.getElementById("search").value;
        const data = { name: searchInput };
        if (!searchInput) {
          alert("Please enter a medicine name to search.");
          return;
        }
        apiPost("https://hickeys-backend-o3fasm9eb-aviasnanis-projects.vercel.app/search_meds", data)
          .then(response => {
            if (response.error) {
              console.log(`Response status was not 200: ${response.error}`);

            }else{
              console.log(data);
              const tableBody = document.getElementById("table-body");
              tableBody.innerHTML = ""; // Clear the table body
              if (response && response.length > 0) {
                response.forEach((medicine) => {
                  var row = document.createElement("tr");
                  row.innerHTML = `
                  <td>${medicine.id}</td>
                  <td>${medicine.name}</td>
                  <td>${medicine.brand}</td>
                  <td>${medicine.description}</td>
                  <td>${medicine.form}</td>
                  <td>${medicine.dosage}</td>
                  <td>${medicine.price}</td>
                `;
                  tableBody.appendChild(row);
                });
              } else {
                const row = document.createElement("tr");
                row.innerHTML = `
                  <td colspan="7">No medicines found</td>
                `;
                tableBody.appendChild(row);
              }}
          })
          .catch(function (error) {
            console.log(`Fetch error: ${error}`);
          });
      }

      function editMed(event, medicine) {
        const row = event.target.closest("tr");
        row.innerHTML = `
          <td>${medicine.id}</td>
          <td><input type="text" id="edited-name-${medicine.id}" value="${
          medicine.name
        }" /></td>
          <td><input type="text" id="edited-brand-${medicine.id}" value="${
          medicine.brand
        }" /></td>
          <td><input type="text" id="edited-description-${
            medicine.id
          }" value="${medicine.description}" /></td>
          <td><input type="text" id="edited-form-${medicine.id}" value="${
          medicine.form
        }" /></td>
          <td><input type="text" id="edited-dosage-${medicine.id}" value="${
          medicine.dosage
        }" /></td>
          <td><input type="number" id="edited-price-${medicine.id}" value="${
          medicine.price
        }" /></td>
          <td><button class="save-button">Save</button></td>
        `;
        row.querySelector(".save-button").addEventListener("click", () => {
          saveMed(medicine);
        }
      );
    }
  
    
      function saveMed(medicine) {
        const id = medicine.id;
        const updated_name = document.getElementById(`edited-name-${id}`).value;
        const updated_brand = document.getElementById(
          `edited-brand-${id}`
        ).value;
        const updated_description = document.getElementById(
          `edited-description-${id}`
        ).value;
        const updated_form = document.getElementById(`edited-form-${id}`).value;
        const updated_dosage = document.getElementById(
          `edited-dosage-${id}`
        ).value;
        const updated_price = document.getElementById(
          `edited-price-${id}`
        ).value;
        const updatedMed = {
          id: id,
          name: updated_name,
          brand: updated_brand,
          description: updated_description,
          form: updated_form,
          dosage: updated_dosage,
          price: updated_price,
        };
        apiPut("https://hickeys-backend-o3fasm9eb-aviasnanis-projects.vercel.app/edit_meds", updatedMed)
          .then(response =>{
            if (response.error) {
              console.log(`Response status was not 200: ${response.error}`);
            }
            else{
              console.log("Medicine updated successfully");
              const tableBody = document.getElementById("table-body");
              tableBody.innerHTML = ""; // Clear the table body
              welcome(); // Refresh the dashboard details
            }
             
            })
          .catch(function (error) {
            console.log(`Fetch error: ${error}`);
          });
      }
      // Logout function
      function logout() {
        apiGet("https://hickeys-backend-o3fasm9eb-aviasnanis-projects.vercel.app/staff_logout")
          .then(response => {
            if (response.error) {
              console.log(`Response status was not 200: ${response.status}`);
            }
          else{
            window.location.href = "/templates/staff/staff_login.html";
            console.log("Logout Successful");
          }
          })
          .catch((error) => {
            console.log(`Fetch error: ${error}`);
          });
      }