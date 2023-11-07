function toggleSettings() {
    var settingsMenu = document.getElementById('settings-menu');
    if (settingsMenu.style.display === 'block') {
        settingsMenu.style.display = 'none';
    } else {
        settingsMenu.style.display = 'block';
    }
}

document.addEventListener("DOMContentLoaded", function () {
    const tabButtons = document.querySelectorAll(".tab-button");
    const tabContents = document.querySelectorAll(".tab-content");

    tabButtons.forEach((button) => {
        button.addEventListener("click", function () {
            tabButtons.forEach((btn) => btn.classList.remove("active"));
            tabContents.forEach((content) => (content.style.display = "none"));

            const tabId = this.id.replace("tab", "");
            const contentId = `content${tabId}`;
            document.getElementById(contentId).style.display = "block";
            this.classList.add("active");
        });
    });

    // Initially, show the first tab
    // tabButtons[0].click();

    
    
});


