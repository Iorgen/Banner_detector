// Bus create AJAX request
$("form#addBus").submit(function() {
    var numberInput = $('input[name="number"]').val().trim();
    var registrationNumberInput = $('input[name="registration_number"]').val().trim();
    if (numberInput) {
        $.ajax({
            url: localStorage.getItem('bus-add-link'),
            data: {
                'number': numberInput,
                'registration_number': registrationNumberInput,
                'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
            },
            dataType: 'json',
            success: function (data) {
                if (data.bus) {
                    appendToBusTable(data.bus);
                }
            }
        });
    } else {
        showAlert("Все поля должны иметь валидное значение");
    }
    $('form#addBus').trigger("reset");
    return false;
});


// Bus update AJAX request
$("form#updateBus").submit(function(event) {
    try{
        var bus = event.target;
        var idInput = $(bus).find('input[name="formId"]').val().trim();
        var numberInput = $(bus).find('input[name="formNumber"]').val().trim();
        var RegistrationNumberInput = $(bus).find('input[name="formRegistrationNumber"]').val().trim();
        if (numberInput && RegistrationNumberInput) {
            $.ajax({
                url:  localStorage.getItem('bus-update-link'),
                data: {
                    'id': idInput,
                    'number': numberInput,
                    'registration_number': RegistrationNumberInput,
                    'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
                },
                dataType: 'json',
                success: function (data) {
                    if (data.bus) {
                        showAlert("Все поля должны иметь валидное значение.");
                    }
                }
            });

        } else {
            showAlert("Все поля должны иметь валидное значение.");
        }
        return false;
    }
    catch (e) {
        console.log(e);
        return false;
    }

});

// Append bus new bus to bus list
function appendToBusTable(bus) {
    $("#busTable:last-child").append(`
<div id="bus-${bus.id}">
<form method="POST" id="updateBus">
                            <div class="row">
                                <div class="col-md-12">
                                    <div class="form-group">
                                        <div>
                                            <input class="form-control" id="form-id" type="hidden" name="formId" value="${ bus.id }">
                                            <div class="busNumber busData input-group" name="number">
                                                <div class="input-group-prepend">
                                                    <span class="input-group-text" id="">
                                                        Маршрут и гос. номер
                                                    </span>
                                                </div>
                                        
                                            <input class="form-control" id="form-number" type="text" value="${bus.number}"name="formNumber"/>
                                            <input class="form-control" id="form-registration-number" type="text" value="${bus.registration_number}"name="formRegistrationNumber"/>
                                            <div class="input-group-append">
                                                 <button class="btn btn-success form-control" type="submit">Редактировать</button>
                                            </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </form>
                        </div>
    `);
}