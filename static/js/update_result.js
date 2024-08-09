<script>
    function selectMatch(matchId, hostTeam, guestTeam) {
        document.getElementById('selectedMatchId').value = matchId;
        document.getElementById('scoreForm').style.display = 'block';
        // Additional logic to prefill scores based on selected match can be added here
    }

    function addResultRow() {
        var table = document.getElementById('resultTable').getElementsByTagName('tbody')[0];
        var rowCount = table.rows.length;
        var row = table.insertRow(rowCount);

        // Create cells
        var cell1 = row.insertCell(0);
        var cell2 = row.insertCell(1);
        var cell3 = row.insertCell(2);
        var cell4 = row.insertCell(3);

        // Add player dropdown
        cell1.innerHTML = `
            <select name="player_id_${rowCount}" class="form-control">
                {% for player in players %}
                <option value="{{ player.id }}">{{ player.name }}</option>
                {% endfor %}
            </select>
        `;

        // Add score type dropdown
        cell2.innerHTML = `
            <select name="score_type_${rowCount}" class="form-control">
                <option value="goal">Bàn Thắng</option>
                <option value="penalty">Penalty</option>
            </select>
        `;

        // Add score time input
        cell3.innerHTML = `<input type="number" name="score_time_${rowCount}" class="form-control" required>`;

        // Add remove button
        cell4.innerHTML = `<button type="button" class="btn btn-danger" onclick="removeResultRow(this)">Xóa</button>`;
    }

    function removeResultRow(button) {
        var row = button.closest('tr');
        row.parentNode.removeChild(row);
    }

    document.getElementById('searchInput').addEventListener('input', function() {
        var input = this.value.toLowerCase();
        var rows = document.querySelectorAll('#matchesTable tbody tr');
        rows.forEach(function(row) {
            var text = row.textContent.toLowerCase();
            if (text.includes(input)) {
                row.style.display = '';
            } else {
                row.style.display = 'none';
            }
        });
    });
</script>