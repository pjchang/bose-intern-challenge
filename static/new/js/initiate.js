/* animation for header and logo */
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

/* event listener */
$('#shareModal').on('hidden.bs.modal', function() {
    $('#link_copy_indicator').css('opacity', '0')
})
$('#share_link').val(window.location.toString());
$("#share_link").click(function() {
    this.select();
    document.execCommand('copy');
    $('#link_copy_indicator').css('opacity', '1')
});

// Remove preloader (https://ihatetomatoes.net/create-custom-preloading-screen/)
$('body').addClass('loaded');

// input current year.
$(".tm-copyright-year").text(new Date().getFullYear());

/* music controller */
$('#playing').on('click', function() {

    if ($(this).hasClass("play")) {
        $("#playing").removeClass("play").addClass("pause");
        document.getElementById('audioElement').play();
    } else {
        $("#playing").removeClass("pause").addClass("play");
        document.getElementById('audioElement').pause();
    }

})


 var track = [];
 var current_track = 0;
 $('.track').each(function() {
     track.push($(this).attr('data-location'));
 });

 /*  load from button */
 $('.prevSong').click(function() { update_song(0); });

 $('.nextSong').click(function() { update_song(1); });

 /*  load from playlist */
 $('.track').click(function() {
     load_track = $(this).attr('data-location');
     change_track(load_track);
 });


 function change_track(sourceUrl) {
     var audio = $("#audioElement");
     audio.attr("src", sourceUrl);
     audio[0].pause();
     audio[0].load(); //suspends and restores all audio element
     audio[0].oncanplaythrough = audio[0].play();
     audio[0].addEventListener('ended', function() {update_song(1);});
     $("#playing").removeClass("play").addClass("pause");
     src = sourceUrl.split('/');
     $('#song_name').text(src[src.length - 1])
 };

 function update_song(type) {
     if (type == 0) {
         current_track = current_track == 0 ? 0 : current_track - 1;
         change_track(track[current_track]);
     } else {
         current_track = current_track == (track.length - 1) ? (track.length - 1) : current_track + 1;
         change_track(track[current_track]);
     }

 }
 change_track(track[0])