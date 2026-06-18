const searchBar = document.getElementById("search");
const results = document.getElementById("results");
const form = document.querySelector("form");

document.body.addEventListener("htmx:load", () => {
    const tags = document.querySelectorAll(".tags");
    
    tags.forEach((tag) => {
        tag.addEventListener("click", () => {
            searchBar.value = tag.innerText;
            results.innerHTML = "";
            form.submit();
        });
    });
});
