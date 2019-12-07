
// Delete banner function
function deleteBanner(id) {
    let action = confirm("Уверены что хотите удалить баннер? ");
    if (action != false) {
        $.ajax({
            url: localStorage.getItem('banner-delete-link'),
            data: {
                'id': id,
                'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
            },
            dataType: 'json',
            success: function (data) {
                if (data.deleted) {
                    $("#BannerList #Banner-" + id).remove();
                    showAlert("Баннер удален");
                }
            }
        });
    }
}

// Update banner function
$("form#updateBanner").submit(function(event) {
    try {
        var banner = event.target;
        var bannerId = $(banner).find('input[name="formId"]').val().trim();
        var bannerTypeName = $(banner).find('input[name="banner_type"]').val().trim();

        if (bannerId && bannerTypeName) {
            $.ajax({
                url: localStorage.getItem('banner-update-link'),
                data: {
                    'id': bannerId,
                    'banner_type_name': bannerTypeName,
                    'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
                },
                dataType: 'json',
                success: function (data) {
                    if (data.banner) {
                        showAlert("Баннер обновлен ");
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

// Set banner as base banner function
function setAsBase(bannerId) {
    var bannerTypeName = $("input[base-attr='banner-358']").val();

    $.ajax({
        url: localStorage.getItem('banner-set-as-base-link'),
        data: {
            'id': bannerId,
            'banner_type': bannerTypeName,
            'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
        },
        dataType: 'json',
        success: function (data) {
            var message = '';

            if (data.banner_type_created) {
                message = message + 'Создан новый тип баннера! ';
            } else {
                message = message + 'Тип баннера установлен! ';
            }

            if (data.base_banner_created) {
                message = message + 'Баннер установлен как базовый';
            } else {
                message = message + 'Такой базовый баннер уже существует';
            }
            showAlert(message);
        }
    });

}