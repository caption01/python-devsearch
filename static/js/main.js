let searchForm = document.getElementById("searchForm");
let pageLinks = document.getElementsByClassName("page-link");

if (searchForm) {
    for (let i = 0; pageLinks.length > i; i++) {
        pageLinks[i].addEventListener("click", function (e) {
            e.preventDefault();
            let page = this.dataset.page;

            searchForm.innerHTML += `
            <input
                name="page"
                hidden
                value=${page}
            />
            `;

            searchForm.submit();
        });
    }
}