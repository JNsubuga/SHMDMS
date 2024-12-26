
var protocol = window.location.protocol;
//////////////////////////////////////////////////////////////
var hostUrl = protocol + "//" + window.location.host + "/";

$(function () {
    initUsers();
    ////
});

function initUsers() {
    $("#spinner-container").show();
    var auth_user_token = $("#auth-user-token").val();

    var settings = {
        "url": hostUrl + "api/en/auth/users/",
        "method": "GET",
        "headers": {
            "Authorization": "Token " + auth_user_token
        },
        onerror: function (error) {
            $("#spinner-container").hide();
            console.log(error.responseText);
        }
    };
    $.ajax(settings).done(function (response) {
        // document.querySelector("#spinner-container").style.display = "none";
        $("#spinner-container").hide();
        // console.log(response);
        var allUsers = [];
        for (var i = 0; i < response.length; i++) {
            var user = response[i];
            allUsers.push({
                UserName: user.username,
                FirstName: user.first_name,
                LastName: user.last_name,
                Email: user.email,
                Role: user.group.group_name,
                Gender: user.profile.gender != null ? user.profile.gender.gender_name : "",
                PhoneNumber: user.profile.phoneno != null ? user.profile.phoneno : "",
                BirthDate: user.profile.birth_date != null ? user.profile.birth_date : "",
                Address: user.profile.address != null ? user.profile.address : "",
                SuperUser: user.is_superuser ? 'Yes' : 'No',
                Staff: user.is_staff ? 'Yes' : 'No',
                Active: user.is_active ? 'Yes' : 'No',
                Actions: user.is_superuser ? "" : '<a href="' + hostUrl + 'user/' + user.id + '/update/" class="btn btn-default btn-sm"><i class="fa fa-edit"></i> Edit</a> <button type="button" onclick="deleteUser(' + user.id + ')" type="button" class="btn btn-danger btn-sm"><i class="fa fa-trash"></i> Delete</button>'
            })
        }

        const dataSet = allUsers.map(({ UserName, FirstName, LastName, Email, Role, Gender, PhoneNumber, BirthDate, Address, SuperUser, Staff, Active, Actions }) => [UserName, FirstName, LastName, Email, Role, Gender, PhoneNumber, BirthDate, Address, SuperUser, Staff, Active, Actions])
        //console.log(dataSet);
        $("#user-data-table")
            .DataTable({
                data: dataSet,
                responsive: true,
                lengthChange: false,
                autoWidth: false,
                buttons: ["copy", "csv", "excel", "pdf", "print", "colvis"],
                columns: [
                    { title: 'User Name' },
                    { title: 'First Name' },
                    { title: 'Last Name' },
                    { title: 'Email' },
                    { title: 'Role' },
                    { title: 'Gender' },
                    { title: 'Phone Number' },
                    { title: 'Birth Date' },
                    { title: 'Address' },
                    { title: 'SuperUser' },
                    { title: 'Staff' },
                    { title: 'Active' },
                    { title: 'Action(s)' },
                ],
            })
            .buttons()
            .container()
            .appendTo("#user-data-table_wrapper .col-md-6:eq(0)");
    });

}


function deleteUser(userid) {
    alert("user " + userid + " deleted successfully");
    const csrftoken = document.querySelector('#global-auth-form [name=csrfmiddlewaretoken]').value;
    var auth_user_token = $("#auth-user-token").val();

    $.ajax({
        "url": `${hostUrl}api/en/auth/user/${userid}/`,
        "method": "GET",
        "headers": {
            "Authorization": `Token ${auth_user_token}`
        },
    }).done((toUpdate) => {
        console.log(toUpdate.id);
        $.ajax({
            "url": `${hostUrl}api/en/auth/user/${toUpdate.id}/update/`,
            "method": "POST",
            "headers": {
                "Authorization": `Token ${auth_user_token}`,
                "X-CSRFToken": csrftoken,
                "Content-Type": "application/json"
            },
            "data": JSON.stringify({
                "username": null,
                "first_name": null,
                "email": null,
                "last_name": null,
                "is_staff": null,
                "is_superuser": null,
                "is_active": false,
                "gender": null,
                "phoneno": null,
                "address": null,
                "birth_date": null,
                "photo": null,
                "security_group_id": null,
                "is_editable": null,
                "is_deletable": null
            })
        }).done((deleted) => {
            console.log(deleted)
        })
    });

}