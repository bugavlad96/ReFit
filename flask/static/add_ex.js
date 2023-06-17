function readURL(input) {
  if (input.files && input.files[0]) {
    var reader = new FileReader();
    var $fileUpload = $(input).closest('.file-upload');

    reader.onload = function(e) {
      $fileUpload.find('.image-upload-wrap').hide();
      $fileUpload.find('.file-upload-image').attr('src', e.target.result);
      $fileUpload.find('.file-upload-content').show();
      $fileUpload.find('.image-title').html(input.files[0].name);
    };

    reader.readAsDataURL(input.files[0]);
  } else {
    removeUpload(input);
  }
}

function removeUpload(input) {
  var $fileUpload = $(input).closest('.file-upload');

  $fileUpload.find('.file-upload-input').replaceWith($fileUpload.find('.file-upload-input').clone());
  $fileUpload.find('.file-upload-content').hide();
  $fileUpload.find('.image-upload-wrap').show();
}

$(document).ready(function() {
  $('.image-upload-wrap').bind('dragover', function() {
    $(this).addClass('image-dropping');
  });

  $('.image-upload-wrap').bind('dragleave', function() {
    $(this).removeClass('image-dropping');
  });
});
