let items = [];

$(document).ready(function () {
    let url = 'https://sheets.googleapis.com/v4/spreadsheets/1-z7oeONlg8S4y0-bv0DEuYn8TmVUhxkoc895hUPULns/values/Campaigns?key=AIzaSyD5B9BKiYjXt7AqiDE0Q857IAf12AIApnc';

    $.getJSON(url, function (data) {
        $.each(data.values, function (key, val) {
            if (key >= 0) {
                items.push({
                    'name': val[0],
                    'id': val[1]
                });
            }
        });

        $('#campaignselect').dropdown({
            readOnly: true,
            input: '<input type="text" maxLength="20" placeholder="Search">',
            data: items,
            searchable: true,
        });
    });
});