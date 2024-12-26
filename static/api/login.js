var protocol = window.location.protocol;
//////////////////////////////////////////////////////////////
var hostUrl = protocol + "//" + window.location.host + "/";

$(() => {
    //
    $("#shmdms-login-form").submit(function (e) {
        e.preventDefault();
        loginUser();
    });
    $("#shmdms-login-form").on("keyup", function () {
        // console.log("Hello");
        $("#form-error").html("");
        $("#shmdms-input-email").removeClass("is-invalid");
        $("#shmdms-input-password").removeClass("is-invalid");
    })

    $("#form-error").show();
})

const loginUser = () => {
    const csrftoken = document.querySelector('#shmdms-login-form [name=csrfmiddlewaretoken]').value;
    var email = $("#shmdms-input-email").val();
    var password = $("#shmdms-input-password").val();
    $("#shmdms-btn-login").html("logging in...");
    $("#spinner-container").show();
    $("#form-error").hide();
    
    var settings = {
        "url": hostUrl + "api/en/auth/login/",
        "method": "POST",
        "headers": {
            "Content-Type": "application/json",
            'X-CSRFToken': csrftoken
        },
        'mode': 'same-origin',
        "data": JSON.stringify({
            "username": email,
            "password": password
        }),
    };

    $.ajax(settings).done((response) => {
        $("#spinner-container").hide();
        $("#form-error").show();
        console.log(response);
        if (response.success) {
            $("#shmdms-btn-login").html("Sign In");

            $("#form-error").html("Login success, redirecting please wait...");
            $("#form-error").removeClass("text-danger");
            $("#form-error").addClass("text-success");

            $("#shmdms-input-email").removeClass("is-invalid");
            $("#shmdms-input-password").removeClass("is-invalid");
            ////
            $("#shmdms-login-form").unbind('submit');
            $("#shmdms-login-form").submit();
            $(':input[type="submit"]').prop('disabled', true);
        } else {
            $("#form-error").html(response.message);
            $("#form-error").addClass("text-danger");
            $("#form-error").removeClass("text-success");
            $("#form-error").html(response.message);
            $("#shmdms-input-email").addClass("is-invalid");
            $("#shmdms-input-password").addClass("is-invalid");
            $("#shmdms-btn-login").html("Sign In");
            $(':input[type="submit"]').prop('disabled', false);

        }
    });
}