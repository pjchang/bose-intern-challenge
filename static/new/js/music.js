$(document).ready(function() {

        /* music controller 
        -----------------------------------------*/
        $('#playing').on('click', function() {

            if ($(this).hasClass("play")) {
                $("#playing").removeClass("play").addClass("pause");
                document.getElementById('audioElement').play();
            } else {
                $("#playing").removeClass("pause").addClass("play");
                document.getElementById('audioElement').pause();
            }

        })
        $('.grid-item').height($('.grid-item').width())
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


        /* d3 animation 
        -----------------------------------------*/
        var audioCtx = new(window.AudioContext || window.webkitAudioContext)();
        var audioElement = document.getElementById('audioElement');
        var audioSrc = audioCtx.createMediaElementSource(audioElement);
        var analyser = audioCtx.createAnalyser();

        var bar_count=  $(window).width() < 768 ? 30 : $(window).width() < 970 ? 50 :100

        // Bind analyser to audio.
        audioSrc.connect(analyser);
        audioSrc.connect(audioCtx.destination);


        var frequencyData = new Uint8Array(bar_count);
        var svgHeight = $('#animation').height();
        var svgWidth = $('#animation').width();
        var barPadding = '1';


        var svg = d3.select('#animation').append('svg')
            .attr({
                height: svgHeight,
                width: svgWidth
            });

       
        svg.selectAll('rect')
            .data(frequencyData)
            .enter()
            .append('rect')
            .attr('x', function(d, i) {
                return i * (svgWidth / frequencyData.length);
            })
            .attr('width', svgWidth / frequencyData.length - barPadding);

        // Continuously loop and update chart with frequency data.
        function renderChart() {
            requestAnimationFrame(renderChart);

            
            analyser.getByteFrequencyData(frequencyData);

            // color panel
            var color_panel = d3.scale.linear()
                .domain([0, bar_count])
                .range([d3.rgb("#43C6AC"), d3.rgb('#F8FFAE')]);


            var height = d3.scale.linear()
                .domain([0, d3.max(frequencyData)])
                .range([0, svgHeight]);

            svg.selectAll('rect')
                .data(frequencyData)
                .attr('y', function(d) {
                    return svgHeight - height(d);
                })
                .attr('height', function(d) {
                    return height(d);
                })
                .attr('fill', function(d, i) {
                    return color_panel(i);
                });
        }

        renderChart();

    });