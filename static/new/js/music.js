$(document).ready(function() {

        var audioCtx = new(window.AudioContext || window.webkitAudioContext)();
        var audioElement = document.getElementById('audioElement');
        var audioSrc = audioCtx.createMediaElementSource(audioElement);
        var analyser = audioCtx.createAnalyser();

        var bar_count=  $(window).width() < 768 ? 30 : $(window).width() < 970 ? 50 :100

        // Bind our analyser to the media element source.
        audioSrc.connect(analyser);
        audioSrc.connect(audioCtx.destination);

        //var frequencyData = new Uint8Array(analyser.frequencyBinCount);
        var frequencyData = new Uint8Array(bar_count);

        var svgHeight = $('#animation').height();
        var svgWidth = $('#animation').width();
        var barPadding = '1';


        var svg = d3.select('#animation').append('svg')
            .attr({
                height: svgHeight,
                width: svgWidth
            });

        // Create our initial D3 chart.
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

            // Copy frequency data to frequencyData array.
            analyser.getByteFrequencyData(frequencyData);

            var hueScale = d3.scale.linear()
                .domain([0, bar_count])
                //.range([0, 360]);
                .range([d3.rgb("#43C6AC"), d3.rgb('#F8FFAE')]);


            var height = d3.scale.linear()
                .domain([0, d3.max(frequencyData)])
                .range([0, svgHeight]);

            // Update d3 chart with new data.
            svg.selectAll('rect')
                .data(frequencyData)
                .attr('y', function(d) {
                    return svgHeight - height(d);
                })
                .attr('height', function(d) {
                    return height(d);
                })
                .attr('fill', function(d, i) {
                    return hueScale(i);
                });
        }

        // Run the loop
        renderChart();

    });