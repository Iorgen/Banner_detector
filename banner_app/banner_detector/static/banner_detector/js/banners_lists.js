
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
        var bannerTypeId = $(banner).find('input[name="banner_type"]').val().trim();

        if (bannerId && bannerTypeId) {
            $.ajax({
                url: localStorage.getItem('banner-update-link'),
                data: {
                    'id': bannerId,
                    'bannerTypeId': bannerTypeId,
                    'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
                },
                dataType: 'json',
                success: function (data) {
                    if (data.banner) {
                        showAlert("Баннер обновлен ");
                    }
                },
                error: function(error){
                    alert(error);
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
    var tag = 'banner-' +  bannerId;
    var bannerTypeName = $("input[banner-attr=" + tag + "]").val();

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


// the selector will match all input controls of type :checkbox
// and attach a click event handler
$("input:checkbox").on('click', function() {
  // in the handler, 'this' refers to the box clicked on
  var $box = $(this);
  if ($box.is(":checked")) {
    // the name of the box is retrieved using the .attr() method
    // as it is assumed and expected to be immutable
    var group = "input:checkbox[name='" + $box.attr("name") + "']";
    // the checked state of the group/box on the other hand will change
    // and the current value is retrieved using .prop() method
    $(group).prop("checked", false);
    $box.prop("checked", true);
  } else {
    $box.prop("checked", false);
  }
});


$("input[id='set_banner_type_btn']").on('click', function(event) {
    var banner_id = $(this.form).find("input[name='formId']").val()
    $("input[name='intermediate_banner_id']").val(banner_id);
    $('#banner_type_modal_select').modal('show');
});

$("button[id='update_banner_type']").on('click', function(event) {
    var banner_type_id = $("input:checkbox[name='banner_type_id']:checked").val();
    console.log(banner_type_id);
    var banner_id = $("input[name='intermediate_banner_id']").val();
    $("input[banner-attr='banner-" + banner_id + "']").val(banner_type_id);
    $('#banner_type_modal_select').modal('hide');

});

