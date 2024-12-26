var protocol = window.location.protocol;
//////////////////////////////////////////////////////////////
var hostUrl = protocol + "//" + window.location.host + "/";

$(() => {
    //Bootstrap Duallistbox
    $('#permissions-list').bootstrapDualListbox({
        nonSelectedListLabel: 'Available user permissions',
        selectedListLabel: 'Chosen user permissions',
        preserveSelectionOnMove: 'moved',
        selectorMinimalHeight: 100,
        moveOnSelect: false,
        nonSelectedFilter: ''
    });
    ////////////////////////////////////////
    $("#role-id").on('change', function () {
        var role_id = parseInt($("#role-id").val());
        if (role_id) {
            getDefaultPermissions(role_id);
        }

    })
    ///////////////////////////////////////

})
initUserPermissions();

function resetForm() {
    $("#user-name").val("");
    $("#first-name").val("");
    $("#last-name").val("");
    $("#phoneno").val("");
    $("#birth-date").val("");
    $("#gender").val("");
    $("#email").val("");
    $("#address").val("");
    $("#new-password").val("");
    $("#confirm-password").val("");
    $("#role-id").val("");
    $("#auth-user-token").val("");
    $("#bio").val("");
    $('#permissions-list').val([]);
    $('#permissions-list').bootstrapDualListbox('refresh', true);
}

function saveData() {
    const csrftoken = document.querySelector('#user-form [name=csrfmiddlewaretoken]').value;
    //////////////////////////////////////////////////
    var selected_user_token = $("#selected-user-token").val();
    var user_name = $("#user-name").val();
    var first_name = $("#first-name").val();
    var last_name = $("#last-name").val();
    var phoneno = $("#phoneno").val();
    var birth_date = $("#birth-date").val();
    var gender = parseInt($("#gender").val());
    var email = $("#email").val();
    var address = $("#address").val();
    var new_password = $("#new-password").val();
    var confirm_password = $("#confirm-password").val();
    var role_id = parseInt($("#role-id").val());
    var bio = $("#bio").val();
    //////////////////////////////////////////////
    var is_staff = $("#is_staff").prop("checked");
    var is_superuser = $("#is_superuser").prop("checked");
    var is_active = $("#is_active").prop("checked");
    ////////////////////////////////////////////////
    $("#form-error").html("Updating account...");
    $("#spinner-container").show();
    $("#save-btn").prop("disabled", true);
    document.querySelector(".spinner-container").style.display = "block";
    //////////////////////////////////////////////////


    var settings = {
        "url": hostUrl + "api/en/auth/user/update/",
        "method": "POST",
        "headers": {
            "Authorization": "Token " + selected_user_token,
            "Content-Type": "application/json",
            'X-CSRFToken': csrftoken
        },
        "data": JSON.stringify({
            "username": user_name,
            "email": email,
            "is_superuser": is_superuser,
            "security_group_id": role_id,
            "first_name": first_name,
            "last_name": last_name,
            "new_password": new_password,
            "confirm_password": confirm_password,
            "is_editable": "",
            "is_deletable": "",
            "gender": gender,
            "phoneno": phoneno,
            "bio": bio,
            "address": address,
            "birth_date": birth_date,
            "photo": "",
            "is_staff": is_staff,
            "is_active": is_active,
        }),
    };
    $.ajax(settings).done(function (response) {

        $("#save-btn").prop("disabled", false);
        if (response.success) {
            addPermissionToUser(selected_user_token);
        } else {
            $("#spinner-container").hide();
            document.querySelector(".spinner-container").style.display = "none";
            $("#form-error").html('<div class="alert alert-danger alert-dismissible"><button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button><h5><i class="icon fa fa-times"></i> Error!</h5>' + response.message + '</div>');
        }
        console.log(response);
    });

}


function getDefaultPermissions(groupid) {
    var auth_user_token = $("#auth-user-token").val();
    var settings = {
        "url": hostUrl + "api/en/security/user/group/" + groupid + "/default/permissions/",
        "method": "GET",
        "headers": {
            "Authorization": "Token " + auth_user_token
        },
    };
    $.ajax(settings).done(function (response) {
        if (response.success) {
            // console.log(response);
            var new_permission_list = response.permissions.map((e) => String(e.permission_id).toString());
            $('#permissions-list').val(new_permission_list);
            $('#permissions-list').bootstrapDualListbox('refresh', true);

        }
    });
}

function addPermissionToUser(usertoken) {
    const csrftoken = document.querySelector('#user-form [name=csrfmiddlewaretoken]').value;
    var permissions_list = $('#permissions-list').val();
    var new_permission_list = permissions_list.map((e) => parseInt(e))
    if (new_permission_list.length > 0) {
        var settings = {
            "url": hostUrl + "api/en/security/user/permissions/batch/add/",
            "method": "POST",
            "headers": {
                "Authorization": "Token " + usertoken,
                "Content-Type": "application/json",
                'X-CSRFToken': csrftoken
            },
            "data": JSON.stringify(new_permission_list)
        };

        $.ajax(settings).done(function (response) {
            $("#spinner-container").hide();
            document.querySelector(".spinner-container").style.display = "none";
            if (response.success) {
                $("#form-error").html('<div class="alert alert-success alert-dismissible"><button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button><h5><i class="icon fas fa-check"></i> Success!</h5>User updated successfully, Redirecting in 2 seconds....</div>');
                setTimeout(() => {
                    window.location.href = hostUrl + 'users/';
                }, 2000);

            } else {
                $("#form-error").html('<div class="alert alert-danger alert-dismissible"><button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button><h5><i class="icon fa fa-times"></i> Error!</h5>' + response.message + '</div>');
            }
            console.log(response);
        });
    }
}

function initUserPermissions() {
    var selected_user_token = $("#selected-user-token").val();
    var settings = {
        "url": hostUrl + "api/en/security/user/permissions/?all=false",
        "method": "GET",
        "headers": {
            "Authorization": "Token " + selected_user_token
        },
    };
    $.ajax(settings).done(function (response) {
        var permissions = [];
        if (response.success) {
            var mpermissions = response.permissions;
            for (var x = 0; x < mpermissions.length; x++) {
                var permission = mpermissions[x].permission;
                permissions.push(permission.permission_id);
            }
            var new_permission_list = permissions.map((e) => String(e).toString());
            $('#permissions-list').val(new_permission_list);
            $('#permissions-list').bootstrapDualListbox('refresh', true);
        }


    });

}

