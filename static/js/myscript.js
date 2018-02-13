// /***************************** Albums  ******************************/
// // Add album
$(".album_add_btn").on("click", function() {
    var album_name = $("#album_name").val();

    if (album_name != "") {
        $("#loading_spin").html('<img src="/static/images/loader.gif">');

        setTimeout(function() {
            $.when($.post("/albums/add", { 'album_name': album_name }).done(function(response) {
                var response = JSON.parse(response);
                if (response.success) {
                    location.reload();
                } else {
                    console.log("Error Adding Albums");
                    location.reload();
                }
                $("#loading_spin").html('');
            }));
        }, 1000);
    }
});

// Delete album
$('.album_del_btn').on("click", function() {
    var album_name = $(this).data("albumname");
    console.log(album_name)

    if (album_name != "") {

        $("#loading_spin").html('<img src="/static/images/loader.gif">');

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
                $("#loading_spin").html('');
            }));

        }, 1000);


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

        $.when($.post("/album/photos/delete", { 'albumName': albumName, 'photoName': photoName,'ownerName':ownerName }).done(function(response) {
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


$(document).on("click", '#popImage', function() {
    var imgSrc = $(this).data("imgsrc");
    $('#imagepreview').attr('src', imgSrc);
    $('#imagemodal').modal('show');
});

$('#popImage').on('click', function() {
    $('.imagepreview').attr('src', $(this).find('img').attr('src'));
    $('#imagemodal').modal('show');
});