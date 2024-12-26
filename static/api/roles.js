
var protocol = window.location.protocol;
//////////////////////////////////////////////////////////////
var hostUrl = protocol + "//" + window.location.host + "/";

$(function () {
    initRoles();
    //Bootstrap Duallistbox
    $('#permissions-list').bootstrapDualListbox({
        nonSelectedListLabel: 'All permissions',
        selectedListLabel: 'Chosen user permissions',
        preserveSelectionOnMove: 'moved',
        selectorMinimalHeight: 100,
        moveOnSelect: false,
        nonSelectedFilter: ''
    });
    // getDefaultPermissions(role_id, selectpermissions);

    ////
});

function initRoles() {
    //document.querySelector("#spinner-container").style.display = "block";
    $("#spinner-container").show();
    var auth_user_token = $("#auth-user-token").val();
    var settings = {
        "url": hostUrl + "api/en/security/groups/",
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
        var allRoles = [];
        for (var i = 0; i < response.length; i++) {
            var role = response[i];
            allRoles.push({
                GroupName: role.group_name,
                Actions: role.code_name == "admin" ? "" : '<button type="button" onclick="UserRoleForm(' + role.group_id + ')" class="btn btn-default btn-sm"><i class="fa fa-edit"></i> Edit</button> <button type="button" onclick="deleteUserRole(' + role.group_id + ')" type="button" class="btn btn-danger btn-sm"><i class="fa fa-trash"></i> Delete</button>'
            })
        }
        const dataSet = allRoles.map(({ GroupName, Actions }) => [GroupName, Actions])
        //console.log(dataSet);
        $("#roles-data-table").DataTable({
            data: dataSet,
            responsive: true,
            lengthChange: false,
            autoWidth: false,
            bDestroy: true,
            buttons: ["copy", "csv", "excel", "pdf", "print", "colvis"],
            columns: [
                { title: 'Role Name' },
                { title: 'Action(s)' },
            ],
            columnDefs: [
                {
                    targets: [0],
                    className: 'dt-left'
                },
                {
                    targets: [1],
                    className: 'dt-right'
                },
            ],
        })
            .buttons()
            .container()
            .appendTo("#roles-data-table_wrapper .col-md-6:eq(0)")
        // .ajax.reload();
    });
}


// Call formData
const UserRoleForm = (roleid = null) => {
    // console.log(roleid);

    $("#modal-lg").modal('show');
    var auth_user_token = $("#auth-user-token").val();
    const csrftoken = document.querySelector('#role-form [name=csrfmiddlewaretoken]').value;


    if (roleid != null) {
        $("#spinner-container-init-edit").show();
        getDefaultPermissions(roleid)
        $("#selected-role-id").val(roleid);
        $(".modal-title").html("Edit Role");
        $("#save-btn").html("Save Changes");
        $("#is-disabod").html('<input class="custom-control-input" type="checkbox" id="is-disabled"><label for="is-disabled" class="custom-control-label">Disabled</label>');
        ////////////////
        var settings = {
            "url": hostUrl + "api/en/security/groups/" + roleid + "/",
            "method": "GET",
            "headers": {
                "Authorization": "Token " + auth_user_token
            },
            error: function (error) {
                $("#spinner-container-init-edit").hide();

            }
        };
        $.ajax(settings).done((response) => {
            $("#spinner-container-init-edit").hide();
            $("#selected-role-id").val(response.group_id);
            $("#role-name").val(response.group_name);
            $("#is-disabled").val(response.is_disabled).prop('checked', response.is_disabled);
            // console.log(response);
        });
        // console.log(reviewid)
    } else {
        var roleid = "null";
        $("#selected-role-id").val(roleid);
        $("#role-name").val("");
        $(".modal-title").html("New role");
        $("#save-btn").html("Submit");
        $("#is-disabod").html('')
        $('#permissions-list').val([]);
        $('#permissions-list').bootstrapDualListbox('refresh', true);
        // console.log(reviewid)
    }
}


// Save FormData
const saveData = () => {
    var auth_user_token = $("#auth-user-token").val();
    const csrftoken = document.querySelector('#role-form [name=csrfmiddlewaretoken]').value;
    var roleid = $("#selected-role-id").val();
    $("#spinner-container").show();
    var role_name = $("#role-name").val();

    if (roleid != 'null') {
        var is_disabled = $("#is-disabled").prop('checked');
        var isDisabled = is_disabled ? 'true' : 'false';
        var settings = {
            "url": hostUrl + "api/en/security/groups/" + roleid + "/update/?group_name=" + role_name + "&is_disabled=" + isDisabled,
            "method": "GET",
            "headers": {
                "Authorization": "Token " + auth_user_token
            },
            error: function (error) {
                $("#spinner-container").hide();
                $("#modal-lg").modal('hide');
                try {
                    var jerror = error.responseJSON;
                    toastr.error(jerror.message);
                } catch (e) {

                }
            }
        };

        $.ajax(settings).done(function (response) {
            // $("#spinner-container").hide();
            $("#modal-lg").modal('hide');
            // Re-initialize the roles
            initRoles();
            if (response.success) {
                addDefaultPermissionsToGroup(response.group.group_id);
            } else {
                toastr.error(response.message);
            }
            console.log(response);
        });
    } else {
        var settings = {
            "url": hostUrl + "api/en/security/groups/create/?group_name=" + role_name,
            "method": "GET",
            "headers": {
                "Authorization": "Token " + auth_user_token
            },
            error: function (error) {
                $("#spinner-container").hide();
                $("#modal-lg").modal('hide');
                try {
                    var jerror = error.responseJSON;
                    toastr.error(jerror.message);
                } catch (e) {

                }
            }
        };

        $.ajax(settings).done(function (response) {
            initRoles();
            $("#modal-lg").modal('hide');
            if (response.success) {
                addDefaultPermissionsToGroup(response.group.group_id);
            } else {
                toastr.error(response.message);
            }
            // console.log(response);
        });
        // Re-initialize the roles

    }
}



function deleteUserRole(userid) {

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

function addDefaultPermissionsToGroup(groupid) {
    var auth_user_token = $("#auth-user-token").val();
    var permissions_list = $('#permissions-list').val();
    var new_permission_list = permissions_list.map((e) => parseInt(e));
    const csrftoken = document.querySelector('#role-form [name=csrfmiddlewaretoken]').value;
    if (new_permission_list.length > 0) {
        var settings = {
            "url": hostUrl + "api/en/security/user/group/" + groupid + "/permissions/default/batch/create/",
            "method": "POST",
            "headers": {
                "Authorization": "Token " + auth_user_token,
                "Content-Type": "application/json",
                'X-CSRFToken': csrftoken
            },
            "data": JSON.stringify(new_permission_list),
        };

        $.ajax(settings).done(function (response) {
            console.log(response);
        });
    }
}