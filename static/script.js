$(document).ready(function() {
    $("#tableForm").submit(function(event) {
        event.preventDefault();

        // Zbieranie danych z tabeli
        const tableData = [];
        $("table tbody tr").each(function() {
            const row = [];
            $(this).find("input, select").each(function() {
                row.push($(this).val());
            });
            tableData.push(row);
        });

        // Wysyłanie danych do serwera
        $.ajax({
            url: "/update",
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify(tableData),
            success: function(response) {
                alert("Table data saved successfully!");
                console.log(response.data);
            },
            error: function() {
                alert("An error occurred while saving the table data.");
            }
        });
    });
});
