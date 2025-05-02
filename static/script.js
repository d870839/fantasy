function fetchStats() {
    fetch('/fetch')
        .then(res => {
            if (!res.ok) {
                throw new Error("Failed to fetch ESPN data");
            }
            return res.json();
        })
        .then(data => {
            const list = document.getElementById('teamList');
            list.innerHTML = '';

            if (data.error) {
                list.innerHTML = `<li>Error: ${data.error} (${data.status_code})</li>`;
                return;
            }

            data.teams.forEach(team => {
                const li = document.createElement('li');
                li.textContent = team.location + ' ' + team.nickname;
                list.appendChild(li);
            });
        })
        .catch(err => {
            document.getElementById('teamList').innerHTML = `<li>${err.message}</li>`;
            console.error(err);
        });
}

