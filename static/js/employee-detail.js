$('.glyphicon-list-alt').click(function () {
    let idNumber = $(this).attr('id').substring(13);

    // console.log('idNumber = ' + idNumber);

    $.ajax({
        url: 'employee_message/' + idNumber,
        dataType: "html",
        method: "GET",
        timeout: 10000,

        success: function (content) {
            let messageFromEmployee = JSON.parse(content);
            dialog();

            function dialog() {
                // console.log('before dialog open');

                let myDialog = $("#dialog");
                myDialog.dialog({
                    autoOpen: true,

                    show: {
                        // minHeight: 500,
                        // minWidth: 800,
                        effect: "blind",
                        text: "test",
                        duration: 300
                    },
                    hide: {
                        effect: "explode",
                        duration: 300
                    }
                });
                myDialog.text(messageFromEmployee);
            }
        }
    }).fail(() => {
        alert('Unexpected problem with showing the message');
    });
    return false;
});

