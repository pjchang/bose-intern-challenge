// /***************************** Albums  ******************************/
// // Add album
$(".album_add_btn").on("click", function() {
    var album_name = $("#album_name").val();

    if (album_name != "") {
        $("#loader-container").css('display', 'block')
        $('#main').css('filter', 'brightness(40%)')

        setTimeout(function() {
            $.when($.post("/albums/add", { 'album_name': album_name }).done(function(response) {
                var response = JSON.parse(response);
                if (response.success) {
                    console.log("successfully");
                    location.reload();
                } else {
                    console.log("Error Adding Albums");
                    $('#album_error').text(response.error)
                    // location.reload();
                }
                $("#loader-container").css('display', 'none')
                $('#main').css('filter', 'brightness(100%)')
            }));
        }, 500);
    }
});

// Delete album
$('.album_del_btn').on("click", function() {
    var album_name = $(this).data("albumname");
    console.log(album_name)

    if (album_name != "") {

        $("#loader-container").css('display', 'block')
        $('#main').css('filter', 'brightness(40%)')


        setTimeout(function() {
            $.when($.post("/albums/delete", { 'album_name': album_name }).done(function(response) {

                var response = JSON.parse(response);
                console.log(response);

                if (response.success) {

                    location.reload();
                } else {
                    console.log("Error deleting Albums");
                    location.reload();
                };

                $("#loader-container").css('display', 'none')
                $('#main').css('filter', 'brightness(100%)')
            }));

        }, 500);


    }
});


// Edit Gallery Action
$(document).on("click", '#editGallerybtn', function() {
    var galleryName = $(this).data("name");
    $("#oldGalleryName").val(galleryName);
});


// /***************************** Photos Actions  ******************************/
// Delete Photo Action
$(document).on("click", '.photo_del_btn', function() {

    var albumName = $(this).data("albumname");
    var photoName = $(this).data("photoname");
    var ownerName = $(this).data("ownername");


    if (albumName != "") {
        console.log('i am here')
        $("#loader-container").css('display', 'block')
        $('#main').css('filter', 'brightness(40%)')



        $.when($.post("/album/photos/delete", { 'albumName': albumName, 'photoName': photoName, 'ownerName': ownerName }).done(function(response) {
            var response = JSON.parse(response);

            if (response.success) {
                location.reload();
            } else {
                console.log("Error Deleting Photo");
                location.reload();
            }
        }));


    }
});

$(document).on("click", '.upload_btn', function() {
    $("#loader-container").css('display', 'block')
    $('#main').css('filter', 'brightness(40%)')

});

$(document).on("click", '#popImage', function() {
    var imgSrc = $(this).data("imgsrc");
    $('#imagepreview').attr('src', imgSrc);
    $('#imagemodal').modal('show');
});

$('#popImage').on('click', function() {
    $('.imagepreview').attr('src', $(this).find('img').attr('src'));
    $('#imagemodal').modal('show');
});