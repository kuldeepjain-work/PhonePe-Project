document.addEventListener('DOMContentLoaded', function() {
    const buttonsContainer = document.getElementById('buttons-container');
    const fileContentDiv = document.getElementById('file-content');
    const dialog = document.querySelector("dialog");
    const closeButton = document.querySelector("dialog button");
    const para = document.querySelector(".dialog-text");
    const usernameDisplay = document.getElementById('username-display');
    const logoutButton = document.getElementById('logout-button');

    closeButton.addEventListener("click", () => {
        dialog.close();
    });

    const loggedInUser = localStorage.getItem('loggedInUser');
    if (!loggedInUser) {
        console.error('No logged-in user found in storage.');
        buttonsContainer.textContent = "No user is logged in.";
        return;
    }
    fetch(`/list_text_files?user=${encodeURIComponent(loggedInUser)}`)
        .then(response => response.json())
        .then(data => {
            const files = data.files || [];
            buttonsContainer.innerHTML = '';
            files.forEach(file => {
                const button = document.createElement('button');
                const date = new Date(file.time * 1000);
                const formattedTime = date.toLocaleString();
                const testSummary = file.summary || "No summary available";
                button.innerHTML = `TEST FILE LOGGED IN AT:<br>${formattedTime}<br><br>TEST CASE SUMMARY:<br>${testSummary}`;
                button.onclick = function() {
                    dialog.showModal();
                    fetchFileContent(loggedInUser, file.name);
                };
                button.style.borderRadius = "15px";
                button.style.backgroundColor = "white";
                button.style.padding = "10px 20px";
                button.style.marginBottom = "10px";
                button.style.border = "1px solid #ccc"
                buttonsContainer.appendChild(button);
            });
            if (files.length === 0) {
                buttonsContainer.textContent = "No files available for this user.";
            }
        })
        .catch(error => {
            console.error('Error listing files:', error);
            buttonsContainer.textContent = "Failed to list files.";
        });

    function escapeHtml(text) {
        var map = {
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            '"': '&quot;',
            "'": '&#039;'
        };
        return text.replace(/[&<>"']/g, function(m) { return map[m]; });
    }

    function fetchFileContent(user, fileName) {
        fetch(`/get_text_file_content?user=${encodeURIComponent(user)}&file_name=${encodeURIComponent(fileName)}`)
            .then(response => response.json())
            .then(data => {
                const safeContent = escapeHtml(data.content);
                para.innerHTML = '<pre>' + safeContent + '</pre>';
            })
            .catch(error => {
                console.error('Error fetching file content:', error);
                fileContentDiv.textContent = "Failed to fetch file content.";
            });
    }

    fetch('/get_minion_data')
        .then(response => response.json())
        .then(data => displayMinionInfo(data.output))
        .catch(error => {
            console.error('Error fetching minion data:', error);
            document.getElementById('minion-states').innerText = "Failed to fetch minion data.";
        });

    function displayMinionInfo(minionData) {
        const container = document.getElementById('minion-states');
        const lines = minionData.split('\n');

        let currentMinion = document.createElement('div');
        currentMinion.classList.add('minion');

        lines.forEach(line => {
            if (line.includes("Fetching system information for:")) {
                if (currentMinion.hasChildNodes()) {
                    container.appendChild(currentMinion);
                    currentMinion = document.createElement('div');
                    currentMinion.classList.add('minion');
                }
                const title = document.createElement('h2');
                title.textContent = line;
                currentMinion.appendChild(title);
            } else if (line.includes("==========================================")) {
                const divider = document.createElement('hr');
                currentMinion.appendChild(divider);
            } else {
                const detail = document.createElement('p');
                detail.textContent = line;
                currentMinion.appendChild(detail);
            }
        });

        if (currentMinion.hasChildNodes()) {
            container.appendChild(currentMinion);
        }
    }
});
