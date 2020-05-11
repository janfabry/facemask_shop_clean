$(function() {
    $('#add_to_basket_form').on('submit', function(e) {
        e.preventDefault();
        var facemaskCanvas = document.getElementById('application-canvas');
        var orderForm = this;
        facemaskCanvas.toBlob(function(blob) {
            var formData = new FormData();
            formData.append('full_image', blob, 'full_image.jpg');
            $.ajax({
                url: EDITOR_UPLOAD_URL,
                type: "POST",
                data: formData,
                processData: false,
                contentType: false,
            }).done(function(response){
                if (response.success) {
                    $('#id_mask-image-id').val(response.mask_id);
                    orderForm.submit();
                } else {
                    console.error(response);
                    alert(response.error || response);
                }
            }).fail(function (response) {
                console.error(response);
                alert(response.error || response);
            });
        });
    });
});
