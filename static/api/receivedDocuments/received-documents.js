var protocol = window.location.protocol
var hostUrl = protocol + "//" + window.location.host + "/"

$(() => {
    receivedDocument();
})

const receivedDocument = () => {
    const csrftoken = document.querySelector('#global-auth-from [name=csrfmiddlewaretoken]').value;
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
            if(auth_user_id == receivedDocument.submitted_by.id){
                var Actions = '<button type="button" onclick="directiveForm(' + receivedDocument.id + ')" class="btn btn-default btn-sm"><i class="fa fa-edit"></i> Edit</button> <button type="button" onclick="deleteDirective(' + receivedDocument.id + ')" type="button" class="btn btn-danger btn-sm"><i class="fa fa-trash"></i> Delete</button>'
            } else {
                var Actions = ''
            }
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
            resnponse: true,
            lengthChange: false,
            autoWidth: false,
            bDestroy: true,
            button: ["copy", "csv", "excel", "pdf", "print", "colvis"],
            columns: [
                {title: "Memo/Breif"},
                {title: "Letter From/Office"},
                {title: "Received At"},
                {title: "Contact"}
            ]
        })
        .buttons()
        .container()
        .appendTo('#received-document-data-table_wrapper .col-md-6:eq(0)')
    })
} 