// LDX FROG.TIPS
var $FROG = function() {
   var FROG_CTL = '#TIP_FROG',
       HDL_ERROR = function(XHR, HUH) {
         $('#TIP').html('FROG not found. Meditate on FROG. <a href="https://stallman.org/">Ribbit</a>');
         $(FROG_CTL).on('click', TIP_FROG);
       },
       LD_TIP = function(NUM) {
         $(FROG_CTL).off('click');
         $.ajax({
           type: 'GET',
           url: '/api/1/tips/' + NUM,
           success: function(DATA) {
             LD_TIPS({tips: [DATA]});
           },
           error: HDL_ERROR
         });
       },
       LD_TIPS = function(DATA) {
          var HDL_DATA = function(DATA) {
             var TIPS = DATA.tips,
                 SWAP_ID = function(number) {
                   history.replaceState({number: number}, '', '#' + number);
                 },
                 TIP_FROG = function() {
                     var TIP = TIPS.pop();
                     if (TIP !== undefined) {
                        $("#TIP").html('<a href="/#' + TIP.number + '">' + TIP.tip + '</a>');
                        SWAP_ID(TIP.number);
                     } else {
                        LD_TIPS();
                     }
                 };

             TIP_FROG();
             $(FROG_CTL).on('click', TIP_FROG);
          };

          $(FROG_CTL).off('click');

          if (DATA !== undefined) {
            HDL_DATA(DATA);
          } else {
            $.ajax({
              type: 'GET',
              url: '/api/1/tips/',
              success: function(DATA) {
                if (DATA === undefined || (DATA.tips !== undefined && DATA.tips.length === 0)) {
                  // Prevent FROG overflow
                  HDL_ERROR();
                } else {
                  HDL_DATA(DATA);
                }
              },
              error: HDL_ERROR
            });
         }
       },
       LD = function(CRAP) {
         var DATA = CRAP.data;
             NUMBER = document.location.hash || undefined;

         if (NUMBER !== undefined) {
           NUMBER = NUMBER.substr(1);
         }

         if (NUMBER !== undefined) {
           LD_TIP(NUMBER);
         } else {
           LD_TIPS(DATA);
         }
       };
  return LD;
}();
