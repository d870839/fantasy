function fetchStats() {
    fetch('/fetch')
        .then(res => res.json())
        .then(data => {
            const list = document.getElementById('teamList');
            list.innerHTML = '';
            data.forEach(team => {
                const li = document.createElement('li');
                li.textContent = team.name + ' (Owner: ' + team.owner + ')';
                list.appendChild(li);
            });
        })
        .catch(err => {
            console.error("Error:", err);
            document.getElementById('teamList').innerHTML = '<li>Failed to load teams.</li>';
        });
}

