$('.glyphicon-list-alt').click(function () {
    let idNumber = $(this).attr('id').substring(13);

    $.ajax({
        url: 'employee_message/' + idNumber,
        dataType: "html",
        method: "GET",
        timeout: 10000,

        success: function (content) {
            const messageFromEmployee = JSON.parse(content);

            function dialog() {
                let myDialog = $("#emp_message_dialog");
                myDialog.dialog({

                    autoOpen: true,
                    modal: true,
                    minHeight: 500,
                    minWidth: 800,

                    show: {
                        effect: "blind",
                        duration: 300
                    },
                    hide: {
                        effect: "explode",
                        duration: 300
                    },

                    buttons: {
                        Ok: function () {
                            $(this).dialog("close");
                        }
                    }
                });

                myDialog.text(messageFromEmployee);
                myDialog.css('font-size', 16);
            }

            dialog();
        }
    }).fail(() => {
        alert('Unexpected problem with showing the message');
    });
    return false;

});