var protocol = window.location.protocol;
///////////////////////////////////////////////////////////
var hostUrl = protocol + "//" + window.location.host + "/";

$(()=>{
    $("#is-disabod").html('<input class="custom-control-input" type="checkbox" id="is-disabled"><label for="is-disabled" class="custom-control-label">Disabled</label>');
})


const resetFrom = (() => {
    $("#memo").val("");
    $("#leterFrom").val("");
    $("#receivedAt").val("");
    $("#contactNumber").val("");
    $("#contactName").val("");
});

const saveData = (() => {
    const csrftoken = document.querySelector('#received-document-form [name=csrfmiddlewaretoken]').value;
    var auth_user_token = $("#auth-user-token").val();
    
    var data = JSON.stringify({
        "memo": $("#memo").val(),
        "officeFrom": $("#officeFrom").val(),
        "dateReceived": $("#dateReceived").val(),
        "contactName": $("#contactName").val(),
        "contactNumber": $("#contactNumber").val(),
        "is_disabled": $("#is-disabled").is(":checked")
    })

    $.ajax({
        "url": hostUrl + "api/en/shmdms/register/received-document/",
        "method": "POST",
        "headers": {
            "Authorization": "Token "+auth_user_token,
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken
        },
        data: data
    }).done((response)=>{
        // $('#spinner-container').hide();
        // $('#save-btn').prop('disabled', false);
        // if(response.success){
        //     $('#from-error').html('')
        // }
        // window.location.href = hostUrl + 'users/';
            if (response.success) {
                setTimeout(() => {
                    window.location.href = hostUrl + 'received-documents/';
                }, 5000);
            }
            console.log(response);
    })
})