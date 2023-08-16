document.addEventListener("DOMContentLoaded", function() {
    // Show the footer when scrolling to the bottom of the page
    function showFooter() {
        var scrollY = window.scrollY || window.pageYOffset || document.documentElement.scrollTop;
        var screenHeight = window.innerHeight || document.documentElement.clientHeight;
        var pageHeight = document.documentElement.scrollHeight;

        if (scrollY + screenHeight >= pageHeight) {
            document.body.classList.add("show-footer");
        } else {
            document.body.classList.remove("show-footer");
        }
    }

    // Call the function on page load and scroll
    showFooter();
    window.addEventListener("scroll", showFooter);
});
