$(window).load(function() {

    
    /* initiate magnificPopup
    -----------------------------------------*/
    $('.gallery').magnificPopup({
        delegate: 'a', // child items selector, by clicking on it popup will open
        type: 'image',
        gallery: { enabled: true },
        midClick: true
    });


    /* render picture in canva
    -----------------------------------------*/
    for (var i = 0; i < document.getElementsByTagName("canvas").length; i++) {
        var canvas = document.getElementsByTagName("canvas")[i];
        canvas.width = $('.grid-item').width();
        canvas.height = $('.grid-item').height();
        var ctx = canvas.getContext('2d');
        image = new Image();
        (function(ctx, image) {
            image.onload = function() {
                math_min = Math.min(image.height, image.width)
                if (image.height < image.width) {
                    start = (image.width - math_min) / 2
                    ctx.drawImage(image, start, 0, math_min, math_min,
                        0, 0, canvas.width, canvas.height);
                } else {
                    start = (image.height - math_min) / 2
                    ctx.drawImage(image, 0, start, math_min, math_min,
                        0, 0, canvas.width, canvas.height);
                }
            }
            image.src = document.getElementsByTagName("canvas")[i].parentElement.href;
        })(ctx, image);
    }

});