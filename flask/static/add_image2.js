// Function to handle image upload for card 2
function readURLCard2(input) {
  if (input.files && input.files[0]) {
    var reader = new FileReader();
    reader.onload = function(e) {
      $('.image-upload-wrap-card2').hide();
      $('.file-upload-image-card2').attr('src', e.target.result);
      $('.file-upload-content-card2').show();
      $('.image-title-card2').html(input.files[0].name);
    };

    reader.readAsDataURL(input.files[0]);

  } else {
    removeUploadCard2();
  }
}

// Function to remove image upload for card 2
function removeUploadCard2() {
  $('.file-upload-input-card2').replaceWith($('.file-upload-input-card2').clone());
  $('.file-upload-content-card2').hide();
  $('.image-upload-wrap-card2').show();
}

$(document).ready(function() {
  // Image upload for card 1
  $('.image-upload-wrap').bind('dragover', function() {
    $('.image-upload-wrap').addClass('image-dropping');
  });

  $('.image-upload-wrap').bind('dragleave', function() {
    $('.image-upload-wrap').removeClass('image-dropping');
  });

  // Image upload for card 2
  $('.image-upload-wrap-card2').bind('dragover', function() {
    $('.image-upload-wrap-card2').addClass('image-dropping');
  });

  $('.image-upload-wrap-card2').bind('dragleave', function() {
    $('.image-upload-wrap-card2').removeClass('image-dropping');
  });
});
