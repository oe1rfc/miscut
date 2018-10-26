

$(window).ready(function(){
   $('#video-canvas').height($('#video-canvas').width() * .562);
});
$(window).resize(function(){
   $('#video-canvas').height($('#video-canvas').width() * .562);
});


var cutter;
var player;

cutter = new Vue({
    el: '#cutter-container',
    data: {
        active_segment: null,
        segments: null,
        files: null
    },
    watch: {
        segments: function (newval, oldval) {
            if(oldval == null) {
                for (var i = 0, total = newval.length; i < total; ++i) {
                    if (newval[i].videofile.type == 'footage') {
                        cutter.active_segment = newval[i];
                        break;
                    }
                }
            }
        },
        active_segment: function (newval, oldval) {
            this.mediaplayerUpdate(newval, oldval==null);
        },
    },
    methods: {
        setSegmentStart: function(event) {
            if(this.active_segment) {
                var end = this.active_segment.start + this.active_segment.length;
                if (player.media.currentTime < end) {
                    this.active_segment.start = player.media.currentTime;
                    this.active_segment.length = end - this.active_segment.start;
                    this.mediaplayerUpdate(this.active_segment);
                }
            }
        },
        setSegmentStop: function(event) {
            if(this.active_segment && player.media.currentTime > this.active_segment.start) {
                this.active_segment.length = player.media.currentTime - this.active_segment.start;
                this.mediaplayerUpdate(this.active_segment);
            }
        },
        mediaplayerUpdate: function(segment, updatesrc = false) {
            player.options.markers = [segment.start, (segment.start + segment.length)];
            player.setmarkers(player.controls);
            if (updatesrc) {
                player.setSrc(segment.videofile.url);
                player.setCurrentTime(segment.start);
                player.load();
            }
        }
    }
})

function initPlayer() {

$('#mediaplayer').mediaelementplayer({
//    pluginPath: "{{ url_for('static', filename='lib/mediaelement-plugins/dist/') }}",
    features: ['playpause', 'current', 'progress', 'duration', 'skipback', 'jumpforward', 'tracks', 'speed', 'volume', 'markers'],
    alwaysShowControls: true,
    markerColor: '#E00000',
    markers: [0, 0],
    markerWidth: 2,
    speeds: ['10.0', '5.00', '2.50', '1.00', '0.50'],
    autoplay: false,
    controls: true,
    success: function(mediaElement, originalNode, instance) {
        player = instance;
    },
    markerCallback: function(media, time) {
        player.pause();
    }
});

console.log(cutter, player);
}




window.onloadNO = function(){
    var videoContext = new VideoContext(document.getElementById("video-canvas"));

    var videoNode1 = videoContext.video("{{ url_for('static', filename='assets/demo/162.ts.proxy.mp4') }}", 0, 4, {volume:0.2, loop:true});
    videoNode1.startAt(0);
    videoNode1.stopAt(6);
    
    var videoNode2 = videoContext.video("{{ url_for('static', filename='assets/demo/pw17-162.mp4.proxy.mp4') }}", 120, 4, {volume:0.2, loop:true});
    videoNode2.startAt(3);
    videoNode2.stopAt(11);

    var crossFade = videoContext.transition(VideoContext.DEFINITIONS.CROSSFADE);

    videoNode1.connect(crossFade);
    videoNode2.connect(crossFade);

    crossFade.connect(videoContext.destination);
    crossFade.transition(3,6,0.0,1.0);

    document.getElementById("play-button").onclick = videoContext.play.bind(videoContext);
    document.getElementById("pause-button").onclick = videoContext.pause.bind(videoContext);

    InitVisualisations(videoContext, "visualisation-canvas");
}

function InitVisualisations(videoCtx, visualisationCanvasID){
    var visualisationCanvas = document.getElementById(visualisationCanvasID);

    function render () {
        //VideoCompositor.renderPlaylist(playlist, visualisationCanvas, videoCompositor.currentTime);
        VideoContext.visualiseVideoContextTimeline(videoCtx, visualisationCanvas, videoCtx.currentTime);
        requestAnimationFrame(render);
    }
    requestAnimationFrame(render);

    visualisationCanvas.addEventListener("mousedown", function(evt){
        var x;
        if (evt.x!== undefined){
            x = evt.x - visualisationCanvas.offsetLeft;
        }else{
            x = evt.clientX + document.body.scrollLeft + document.documentElement.scrollLeft;
        }
        var secondsPerPixel = videoCtx.duration / visualisationCanvas.width;
        if(secondsPerPixel*x !== Infinity) videoCtx.currentTime = secondsPerPixel*x;
    }, false);
}
