// Bus create AJAX request
$("form#addBannerType").submit(function() {
    var nameInput = $('input[name="name"]').val().trim();
    if (nameInput) {
        $.ajax({
            url: localStorage.getItem('banner-type-add-link'),
            data: {
                'name': nameInput,
            },
            dataType: 'json',
            success: function (data) {
                if (data.banner_type) {
                    appendToBannerTypeTable(data.banner_type);
                }
            }
        });
    } else {
        alert("Все поля должны иметь валидное значение");
    }
    $('form#addBannerType').trigger("reset");
    return false;
});

// Bus update AJAX request
$("form#updateBannertType").submit(function(event) {
    try{
        var bus = event.target;
        var idInput = $(bus).find('input[name="formId"]').val().trim();
        var nameInput = $(bus).find('input[name="formName"]').val().trim();
        if (nameInput) {
            $.ajax({
                url:  localStorage.getItem('banner-type-update-link'),
                data: {
                    'id': idInput,
                    'name': nameInput,
                },
                dataType: 'json',
                success: function (data) {
                    if (data.banner_type) {
                        alert('update_success')
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
function appendToBannerTypeTable(bannerType) {
    $("#bannerTypeTable:last-child").append(`
                 <div id="bannerType-${bannerType.id}">
                            <form method="POST" id="updateBannerType" >
                                <div class="row">
                                    <div class="col-md-6">
                                        <div class="form-group">
                                            <div >
                                                <input class="form-control" id="form-id" type="hidden" name="formId" value="${bannerType.id }">
                                                <div class="bannerTypeName BannerTypeData" name="name">
                                                    <input class="form-control" id="form-name" type="text" value="${bannerType.name}"name="formName"/>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="col-md-3">
                                        <button class="btn btn-success form-control" type="submit">Редактировать</button>
                                    </div>
                                </div>
                            </form>
                        </div>
    `);
}