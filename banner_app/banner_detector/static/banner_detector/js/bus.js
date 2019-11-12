// Bus create AJAX request
$("form#addBus").submit(function() {
    var numberInput = $('input[name="number"]').val().trim();
    if (numberInput) {
        $.ajax({
            url: localStorage.getItem('bus-add-link'),
            data: {
                'number': numberInput,
            },
            dataType: 'json',
            success: function (data) {
                if (data.bus) {
                    appendToBusTable(data.bus);
                }
            }
        });
    } else {
        alert("Все поля должны иметь валидное значение");
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
        if (numberInput) {
            $.ajax({
                url:  localStorage.getItem('bus-update-link'),
                data: {
                    'id': idInput,
                    'number': numberInput,
                },
                dataType: 'json',
                success: function (data) {
                    if (data.bus) {

                    }
                }
            });

        } else {
            alert("Все поля должны иметь валидное значение.");
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
                                <div class="col-md-6">
                                    <div class="form-group">
                                        <div id="bus-${bus.id}">
                                            <input class="form-control" id="form-id" type="hidden" name="formId" value="${ bus.id }">
                                            <div class="busNumber busData" name="number">
                                                <input class="form-control" id="form-number" type="text" value="${bus.number}"name="formNumber"/>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-3">
                                    <button class="btn btn-success form-control" type="submit">Редактировать</button>
                                </div>
                                <div class="col-md-3">
                                    <button class="btn btn-danger form-control" onClick="deleteBus(${bus.pk})">Удалить</button>
                                </div>
                            </div>
                        </form>
                        </div>
    `);
}