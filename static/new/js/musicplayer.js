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
     $("#playing").removeClass("pause").addClass("play");
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