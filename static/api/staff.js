
var protocol = window.location.protocol;
//////////////////////////////////////////////////////////////
var hostUrl = protocol + "//" + window.location.host + "/";

$(function () {
    initStaff();
    ////
});

function initStaff() {
    const csrftoken = document.querySelector('#global-auth-form [name=csrfmiddlewaretoken]').value;
    //document.querySelector("#spinner-container").style.display = "block";
    $("#spinner-container").show();
    var auth_user_token = $("#auth-user-token").val();
    var settings = {
        "url": hostUrl + "api/en/staff/",
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
        var allstaff = [];
        for (var i = 0; i < response.length; i++) {
            var staff = response[i];
            allstaff.push({
                StaffName: staff.first_name + " " + staff.middle_name + " " + staff.last_name,
                Address: staff.address,
                Birthdate: staff.birth_date,
                District: staff.district.district_name,
                Actions: '<button type="button" onclick="staffForm(' + staff.id + ')" class="btn btn-default btn-sm"><i class="fa fa-edit"></i> Edit</button> <button type="button" onclick="deleteStaff(' + staff.id + ')" type="button" class="btn btn-danger btn-sm"><i class="fa fa-trash"></i> Delete</button>'
            })
        }

        const dataSet = allstaff.map(({ StaffName, Address, Birthdate, District, Actions }) => [StaffName, Address, Birthdate, District, Actions])
        //console.log(dataSet);

        $("#staff-data-table")
            .DataTable({
                data: dataSet,
                responsive: true,
                lengthChange: false,
                autoWidth: false,
                buttons: ["copy", "csv", "excel", "pdf", "print", "colvis"],
                columns: [
                    { title: 'Staff Name' },
                    { title: 'Address' },
                    { title: 'Birth Date' },
                    { title: 'District' },
                    { title: 'Action(s)' },
                ],
            })
            .buttons()
            .container()
            .appendTo("#staff-data-table_wrapper .col-md-6:eq(0)");
    });
}

// function initStaffEditModal(staffid=null) {
function staffForm(staffid = null) {
    if (staffid != null) {
        $("#modal-xl").modal('show');
        var auth_user_token = $("#auth-user-token").val();
        const csrftoken = document.querySelector('#staff-form [name=csrfmiddlewaretoken]').value;
        $("#spinner-container-init-edit").show();

        $("#selected-staff-id").val(staffid);

        ////////////////
        var settings = {
            "url": hostUrl + "api/en/staff/" + staffid + "/",
            "method": "GET",
            "headers": {
                "Authorization": "Token " + auth_user_token,
            },
        };

        $.ajax(settings).done(function (response) {
            // console.log(response.gender_id.initials)
            $("#spinner-container-init-edit").hide();
            $("#first-name").val(response.first_name);
            $("#middle-name").val(response.middle_name);
            $("#last-name").val(response.last_name);
            $("#nin-no").val(response.nin_no);
            $("#staff-category-id").val(response.staff_category.id);
            $("#country-id").val(response.nationality.id);
            $("#region-id").val(response.region.id);
            $("#district-id").val(response.district.id);
            $("#sub-county-id").val(response.sub_county.id);
            $("#salary-scale-id").val(response.salary_scale.id);
            $("#teaching-load").val(response.teaching_load);
            $("#registration-no").val(response.registration_no);
            $("#phone-no").val(response.phoneno);
            $("#birth-date").val(response.birth_date);
            $("#appointment-minute-number").val(response.appointment_minute_number);
            $("#computer-no").val(response.computer_number);
            if (response.gender_id.initials == "F") {
                $("#radio-F").prop('checked', true);
            }
            if (response.gender_id.initials == "M") {
                $("#radio-M").prop('checked', true);
            }
            $("#is-verified").val(response.is_verified).prop('checked', response.is_verified);
            $("#is-genuine").val(response.is_genuine).prop('checked', response.is_genuine);
            $("#is-disabled").val(response.is_disabled).prop('checked', response.is_disabled);

            // console.log(response);
        });
    }
    else {
        $("#modal-xl").modal('show');
        var auth_user_token = $("#auth-user-token").val();
        const csrftoken = document.querySelector('#staff-form [name=csrfmiddlewaretoken]').value;
        $("#spinner-container-init-edit").show();
    }
}

function saveStaff() {

    alert("Edit user: " + userid);
    //initStaff();
}



function deleteStaff(userid) {
    alert("delete user: " + userid);
    //initStaff();
}