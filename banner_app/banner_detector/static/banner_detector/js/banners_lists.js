
// Delete banner function
function deleteBanner(id) {
    let action = confirm("Уверены что хотите удалить баннер? ");
    if (action != false) {
        $.ajax({
            url: localStorage.getItem('banner-delete-link'),
            data: {
                'id': id,
            },
            dataType: 'json',
            success: function (data) {
                if (data.deleted) {
                    $("#BannerList #Banner-" + id).remove();
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
                },
                dataType: 'json',
                success: function (data) {
                    if (data.banner) {
                        alert('update success');
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

// Set banner as base banner function
function setAsBase(bannerId) {
    $.ajax({
        url: localStorage.getItem('banner-set-as-base-link'),
        data: {
            'id': bannerId,
        },
        dataType: 'json',
        success: function (data) {
            if (data.created) {
                alert('установлен как базовый');
            }
        }
    });

}