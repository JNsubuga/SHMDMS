var protocol = window.location.protocol
var hostUrl = protocol + "//" + window.location.host + "/"

$(() => {
    receivedDocuments();
})

const receivedDocuments = () => {
    $('#spinner-container').show();
    var auth_user_token = $('#auth-user-token').val();
    var auth_user_id = $('#auth-user-id').val();

    $.ajax({
        "url": hostUrl + "api/en/shmdms/received-documents/",
        "method": "GET",
        "headers": {
            "Authorization": "Token " + auth_user_token
        },
        onerror: (error) => {
            $("#spinner-container").hide();
            console.log(error.responseText);
        }
    }).done((response)=>{
        // console.log(response)
        $('#spinner-container').hide();
        var allReceivedDocuments = [];
        for(let i = 0; i < response.length; i++) {
            var receivedDocument = response[i];
            var dateFormat = new Date(receivedDocument.dateReceived)
            // if(auth_user_id == receivedDocument.submitted_by.id || receivedDocument.submitted_by.pk == 1){
                // var Actions = '<button type="button" onclick="receivedDocumentForm(' + receivedDocument.id + ')" class="btn btn-default btn-sm"><i class="fa fa-edit"></i> Edit</button> <button type="button" onclick="deleteDirective(' + receivedDocument.id + ')" type="button" class="btn btn-danger btn-sm"><i class="fa fa-trash"></i> Delete</button>'
                var Actions = '<button type="button" onclick="receivedDocumentForm(' + receivedDocument.id + ')" class="btn btn-default btn-sm"><i class="fa fa-edit"></i> Edit</button>'
            // } else {
                // var Actions = ''
            // }
            allReceivedDocuments.push({
                memo: receivedDocument.memo,
                officeFrom: receivedDocument.officeFrom,
                dateReceived: dateFormat.toLocaleDateString("en-GB"),
                contact: receivedDocument.contactNumber +"/"+ receivedDocument.contactName,
                Actions: Actions
            })
        }

        const dataSet = allReceivedDocuments.map(({memo, officeFrom, dateReceived, contact, Actions}) => [memo, officeFrom, dateReceived, contact, Actions])
        
        $("#received-document-data-table").DataTable({
            data: dataSet,
            responsive: true,
            lengthChange: false,
            autoWidth: false,
            bDestroy: true,
            buttons: ["copy", "csv", "excel", "pdf", "print", "colvis"],
            columns: [
                {title: "Memo/Brief", width:"40%"},
                {title: "Letter From/To"},
                {title: "Date Received"},
                {title: "Contact"},
                {title: "Action(s)", className:"dt-center"},

            ]
        })
        .buttons()
        .container()
        .appendTo('#received-document-data-table_wrapper .col-md-6:eq(0)')
    })
} 

const resetForm = (() => {
    $("#memo").val("");
    $("#officeFromTo").val("");
    $("#dateReceived").val("");
    $("#contactNumber").val("");
    $("#contactName").val("");
});

const receivedDocumentForm = ((receiveddocumentid = null) => {
    $("#modal-xl").modal('show');
    $('#form-alert').hide();
    var auth_user_token = $("#auth-user-token").val();
    const csrftoken = document.querySelector('#received-document-form [name=csrfmiddlewaretoken]').value;
    if (receiveddocumentid != null) {
        $("#spinner-container-init-edit").show();
        $("#selected-received-document-id").val(receiveddocumentid);
        $(".modal-title").html("Edit Record");
        $("#save-btn").html("Save Changes");
        $("#is-disabod").html('<input class="custom-control-input" type="checkbox" id="is-disabled"><label for="is-disabled" class="custom-control-label">Disabled</label>');

        $.ajax({
            "url": hostUrl + "api/en/shmdms/received-document/" + receiveddocumentid,
            "method": "GET",
            "headers": {
                "Authorization": "Token " + auth_user_token
            },
            onerror: (error) => {
                $("#spinner-container-init-edit").hide();
                console.log(error.responseText);
            }
        }).done((response) => {
            $("#spinner-container-init-edit").hide();
            // console.log(response);
            $("#memo").val(response.memo);
            $("#officeFromTo").val(response.officeFrom);
            $("#dateReceived").val(response.dateReceived);
            $("#contactNumber").val(response.contactNumber);
            $("#contactName").val(response.contactName);
            $("#is-disabled").val(response.is_disabled).prop('checked', response.is_disabled);
        });

    } else {
        resetForm();
        var receiveddocumentid = "null";
        $("#selected-received-document-id").val(receiveddocumentid);
        $(".modal-title").html("Register Received Document");
        $("#save-btn").html("Submit");
        $("#is-disabod").html('');
    }
});

const saveData = (() => {
    const csrftoken = document.querySelector('#received-document-form [name=csrfmiddlewaretoken]').value;
    var auth_user_token = $("#auth-user-token").val();
    var receiveddocumentid = $("#selected-received-document-id").val();
    $("#spinner-container").show();
    
    var data = JSON.stringify({
        "memo": $("#memo").val(),
        "officeFrom": $("#officeFromTo").val(),
        "dateReceived": $("#dateReceived").val(),
        "contactName": $("#contactName").val(),
        "contactNumber": $("#contactNumber").val(),
        "is_disabled": $("#is-disabled").is(":checked")
    })

    if(receiveddocumentid != "null"){
        $.ajax({
            "url": hostUrl + "api/en/shmdms/update/receiveddocument/" + receiveddocumentid,
            "method": "PUT",
            "headers": {
                "Authorization": "Token " + auth_user_token,
                "X-CSRFToken": csrftoken,
                "Content-Type": "application/json"
            }, onerror: (error) => {
                $("#spinner-container").hide();
                console.log(error,responseText);
            },
            "data": data
        }).done((response) => {
            if(response.status) {
                $('#form-alert').show();
                $("#form-alert").html('<div class="alert alert-success alert-dismissible"><button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button><h5><i class="icon fas fa-check"></i> Success!</h5>' + response.message + '</div>');
                setTimeout(() => {
                  $("#modal-xl").modal('hide');
                }, 2000);
              } else {
                $("#form-alert").html('<div class="alert alert-danger alert-dismissible"><button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button><h5><i class="icon fa fa-times"></i> Error!</h5>' + response.message + '</div>');
            }
            receivedDocuments();
        });
    }
    else{
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
            //console.log(response);
            if (response.status) {
                $('#form-alert').show();
                $("#form-alert").html('<div class="alert alert-success alert-dismissible"><button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button><h5><i class="icon fas fa-check"></i> Success!</h5>' + response.message + '</div>');
                setTimeout(() => {
                  $("#modal-xl").modal('hide');
                }, 2000);
              } else {
                $("#form-alert").html('<div class="alert alert-danger alert-dismissible"><button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button><h5><i class="icon fa fa-times"></i> Error!</h5>' + response.message + '</div>');
            }
            // console.log(response);
            receivedDocuments();
        })
    }
})