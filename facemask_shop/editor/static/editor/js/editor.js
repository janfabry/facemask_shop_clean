$(function() {
    $('#add_to_basket_form').on('submit', function(e) {
        e.preventDefault();

        var orderForm = this;

        uploadFile(EDITOR_UPLOAD_URL, function(response) {
            if (response.success) {
                $('#id_mask-image-id').val(response.mask_id);
                orderForm.submit();
            } else {
                console.error(response);
                alert(response.error || response);
            }
        });
    });
});
