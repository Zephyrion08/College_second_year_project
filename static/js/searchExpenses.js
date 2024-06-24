const searchField = document.querySelector("#searchField");

const tableOutput = document.querySelector(".table-output");
const appTable = document.querySelector(".app-table");
const paginationContainer = document.querySelector(".pagination-container");
const noResults = document.querySelector(".no-results");
const tbody = document.querySelector(".table-body");

// Initially hide the table output and no results message
tableOutput.style.display = "none";
noResults.style.display = "none";

// Event listener for keyup event on search input field
searchField.addEventListener("keyup", (e) => {
  const searchValue = e.target.value;

  // If search value is not empty
  if (searchValue.trim().length > 0) {
    paginationContainer.style.display = "none";
    tbody.innerHTML = ""; // Clear previous search results

    // Fetch data from the server using POST method
    fetch("/search-expenses", {
      body: JSON.stringify({ searchText: searchValue }),
      method: "POST",
    })
      .then((res) => res.json())
      .then((data) => {
        console.log("data", data);

        // Hide main table and show search results
        appTable.style.display = "none";
        tableOutput.style.display = "block";

        // If no results found, display the no results message
        if (data.length === 0) {
          noResults.style.display = "block";
          tableOutput.style.display = "none";
        } else {
          noResults.style.display = "none";
          // Populate table body with search results
          data.forEach((item) => {
            tbody.innerHTML += `
              <tr>
                <td>${item.amount}</td>
                <td>${item.category}</td>
                <td>${item.description}</td>
                <td>${item.date}</td>
              </tr>`;
          });
        }
      })
      .catch((error) => {
        console.error("Error fetching search results:", error);
        // Handle errors or show appropriate messages to the user
      });
  } else {
    // If search value is empty, show main table and pagination
    tableOutput.style.display = "none";
    appTable.style.display = "block";
    paginationContainer.style.display = "block";
  }
});
