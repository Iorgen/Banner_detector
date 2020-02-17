
function resize_img(input_id){
    var resize_width = 600;
    var item = document.querySelector(input_id).files[0];
    var reader = new FileReader();
    reader.readAsDataURL(item);
    reader.name = item.name;
    reader.size = item.size;
    reader.onload = function(event) {
        var img = new Image();
        img.src = event.target.result;
        img.name = event.target.name;
        img.size = event.target.size;
        img.onload = function(el) {
            var elem = document.createElement('canvas');
            var scaleFactor = resize_width / el.target.width;
            elem.width = resize_width;
            elem.height = el.target.height * scaleFactor;
            var ctx = elem.getContext('2d');
            ctx.drawImage(el.target, 0, 0, elem.width, elem.height);
            var srcEncoded = ctx.canvas.toDataURL(el.target, 'image/jpeg', 0);
            document.querySelector('#profile-img-tag').src = srcEncoded;
            $('#billboard_form').submit()
        }
    }
}

$(document).ready(function() {
    $('#id_bus').select2();
    document.getElementById("id_image").addEventListener("change", function (event) {
        resize_img('#id_image');
    });
    $( "#billboard_form" ).submit(function( event ) {
        showModal();
        event.preventDefault();
        var resizedImage = document.getElementById('profile-img-tag');
        var block = resizedImage.src.split(";");
        var contentType = block[0].split(":")[1];
        var realData = block[1].split(",")[1];
        var blob = b64toBlob(realData, contentType);
        var formData = new FormData(document.getElementById('billboard_form'));
        formData.delete('image');
        formData.append("image", blob,'someimage.png');
        send_stand_form_data(formData);
        return true;
    });
});




function send_stand_form_data(formData){
    $.ajax({
        url: '',
        data: formData,
        processData: false,
        contentType: false,
        type: 'POST',
        success: function(data){
            hideModal();
            if (data['recognize']){
                showAlert('Стенд успешно отправлен на распознавание');
            }else{
                showAlert('Заполните форму');
            }
            console.log(data['recognize']);
        },
        error: function (error) {
            showAlert('Произошла ошибка' + error);
        }
    });
}









