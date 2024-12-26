var protocol = window.location.protocol;
///////////////////////////////////////////////////////////
var hostUrl = protocol + "//" + window.location.host + "/";

$(()=>{

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
    
    var memo = $("#memo").val();
    var officeFrom = $("#officeFrom").val();
    var dateReceived = $("#dateReceived").val();
    var contactName = $("#contactName").val();
    var contactNumber = $("#contactNumber").val();

    var settings = {
        "url": hostUrl + "api/en/shmdms/register/received-document/",
        "method": "POST",
        "headers": {
            "Authorization": "Token "+auth_user_token,
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken
        },
        data: JSON.stringify({
            "memo": memo,
            "officeFrom": officeFrom,
            "dateReceived": dateReceived,
            "contactName": contactName,
            "contactNumber": contactNumber
        })
    }

    $.ajax(settings).done((response)=>{
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