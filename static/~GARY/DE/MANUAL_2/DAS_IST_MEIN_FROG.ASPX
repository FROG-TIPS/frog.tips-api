<head>
  <script src="/js/frog.js"></script>
  <script type='text/javascript' src='http://www.midijs.net/lib/midi.js'></script>
  <script>
    MIDIjs.play("bluedanube.mid");

    (function() {
      var id = '#TIPS',
          auf_fehler = function(eigenschaften) { /* nichts tun */ };

      $.ajax({
        type: 'GET',
        url: '/api/1/tips/de',
        success: function(daten) {
          if (daten === undefined || (daten.tips !== undefined && daten.tips.length === 0)) {
            auf_fehler();
          }
          else {
            var element = $(id);
            while (daten.tips) {
              element.html('<li>' + daten.tips.pop().tip + '</li>');
            }
          }
        },
        error: auf_fehler,
      });
    })();
  </script>
</head>
</script>
<center>
  <img src="deutschland.gif" />
  <h1>Willkommen in die FROG Tips!</h1>
  <a href="#" onClick="MIDIjs.stop();">Stop MIDI Playback</a>
  <ol style="text-align: center; list-style-position:inside;" id="TIPS">
  </ol>
  <img src="frog.gif" />
</center>
