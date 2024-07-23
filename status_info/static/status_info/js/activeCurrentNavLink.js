function activeCurrentNavLink() {
    const nav_links = document.querySelectorAll("a.navbar_link");
    const currentUrl = window.location;

    for (const nav_link of nav_links) {
        if (nav_link.href == currentUrl) {
            nav_link.classList.add("active");
        }
    }
}

function showSidebar() {
    if (event) {
        event.preventDefault();
    }

    const sidebar = document.querySelector('.sidebar');
    sidebar.style.display = "flex";
}

function hideSidebar() {
    if (event) {
        event.preventDefault();
    }

    const sidebar = document.querySelector('.sidebar');
    sidebar.style.display = "none";
}