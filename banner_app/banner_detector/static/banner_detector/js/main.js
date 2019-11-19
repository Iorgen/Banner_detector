// $("#success-alert").hide();
function showAlert(alert_message) {
    $("#success-alert #alert_text").text(alert_message);
    $("#success-alert").fadeTo(2000, 500).slideUp(500, function() {
        $("#success-alert").slideUp(500);
    });
}

function showModal(){
    $('.modal').modal('show');
}

function hideModal(){
    $('.modal').modal('hide');
}
