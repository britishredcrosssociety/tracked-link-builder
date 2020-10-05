let audiences = [];

$(document).ready(function () {
    let url = 'https://sheets.googleapis.com/v4/spreadsheets/1-z7oeONlg8S4y0-bv0DEuYn8TmVUhxkoc895hUPULns/values/Audience?key=AIzaSyD5B9BKiYjXt7AqiDE0Q857IAf12AIApnc';

    $.getJSON(url, function (data) {
        $.each(data.values, function (key, val) {
            if (key >= 0) {
                audiences.push({
                    'name': val[0],
                    'id': val[1]
                });
            }
        });

        $('#socialadaudiencecontainer1').dropdown({
            multipleMode: 'label',
            limitCount: 4,
            input: '<input type="text" maxLength="20" placeholder="Search">',
            data: audiences,
            searchable: true,
        });

        $('#socialadaudiencecontainer2').dropdown({
            multipleMode: 'label',
            limitCount: 4,
            input: '<input type="text" maxLength="20" placeholder="Search">',
            data: audiences,
            searchable: true,
        });

        $('#socialadaudiencecontainer3').dropdown({
            multipleMode: 'label',
            limitCount: 4,
            input: '<input type="text" maxLength="20" placeholder="Search">',
            data: audiences,
            searchable: true,
        });

        $('#socialadaudiencecontainer4').dropdown({
            multipleMode: 'label',
            limitCount: 4,
            input: '<input type="text" maxLength="20" placeholder="Search">',
            data: audiences,
            searchable: true,
        });

        $('#socialadaudiencecontainer5').dropdown({
            multipleMode: 'label',
            limitCount: 4,
            input: '<input type="text" maxLength="20" placeholder="Search">',
            data: audiences,
            searchable: true,
        });
    });
});