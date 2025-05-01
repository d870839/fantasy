function fetchStats() {
    fetch('/fetch')
        .then(res => res.json())
        .then(data => {
            const list = document.getElementById('teamList');
            list.innerHTML = '';
            data.forEach(team => {
                const li = document.createElement('li');
                li.textContent = team.name;
                list.appendChild(li);
            });
        });
}
