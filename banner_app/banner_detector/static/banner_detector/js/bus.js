function initSearchTable(){
    $('#bus-dt').DataTable({
        "searching": true, // false to disable search (or any other option)
        "language": {
            "url": "//cdn.datatables.net/plug-ins/9dcbecd42ad/i18n/Russian.json"
        },
        "ordering": true // false to disable sorting (or any other option)

    });
    $('.dataTables_length').addClass('bs-select');
}

$(document).ready(function () {
    initSearchTable();
});

// Bus create AJAX request
$("form#addBus").submit(function() {
    var numberInput = $('input[name="number"]').val().trim();
    var registrationNumberInput = $('input[name="registration_number"]').val().trim();
    var standTypeId = $('select[name="stand_type"] option:selected').val().trim();
    if (numberInput) {
        $.ajax({
            url: localStorage.getItem('bus-add-link'),
            data: {
                'number': numberInput,
                'standTypeId': standTypeId,
                'registration_number': registrationNumberInput,
                'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
            },
            dataType: 'json',
            success: function (data) {
                if (data.bus) {
                    appendToBusTable(data.bus);
                    showAlert("Автобус успешно создан");
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
    var table = $('#bus-dt').DataTable();
    var rowNode = table.row.add([
        bus.stand.stand_name,
        bus.number,
        bus.registration_number
    ]).draw().node();

    $(rowNode)
    .css( 'color', 'red' )
    .animate( { color: 'black' } );
}