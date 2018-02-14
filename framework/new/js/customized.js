function resizeHeaderOnScroll() {
    const distanceY = window.pageYOffset || document.documentElement.scrollTop,
        shrinkOn = 200,
        headerEl = document.getElementById('js-header');

    if (distanceY > shrinkOn) {
        headerEl.classList.add("smaller");
    } else {
        headerEl.classList.remove("smaller");
    }
}

window.addEventListener('scroll', resizeHeaderOnScroll);

$(window).load(function() {

    /*share link and photo delete listener*/
    $('#shareModal').on('hidden.bs.modal', function() {
        $('#link_copy_indicator').css('opacity', '0')
    })

    $('#share_link').val(window.location.toString());
    $("#share_link").click(function() {
        this.select();
        document.execCommand('copy');
        $('#link_copy_indicator').css('opacity', '1')
    });

    /* magnificPopup pop up initiate
    -----------------------------------------*/
    $('.gallery').magnificPopup({
        delegate: 'a', // child items selector, by clicking on it popup will open
        type: 'image',
        gallery: { enabled: true },
        midClick: true
    });


    /* render picture in canva
    -----------------------------------------*/
    $('.grid-item').height($('.grid-item').width())
    for (var i = 0; i < document.getElementsByTagName("canvas").length; i++) {
        var canvas = document.getElementsByTagName("canvas")[i];
        canvas.width = $('.grid-item').width();
        canvas.height = $('.grid-item').height();
        //var ctx = document.getElementsByTagName("canvas")[i].getContext('2d'),
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

    // Remove preloader (https://ihatetomatoes.net/create-custom-preloading-screen/)
    $('body').addClass('loaded');

    // Write current year in copyright text.
    $(".tm-copyright-year").text(new Date().getFullYear());

    $('#playing').on('click', function() {

        if ($(this).hasClass("play")) {
            $("#playing").removeClass("play").addClass("pause");
            document.getElementById('audioElement').play();
        } else {
            $("#playing").removeClass("pause").addClass("play");
            document.getElementById('audioElement').pause();
        }

    })



});