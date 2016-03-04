// LDX FROG.TIPS
var $FROG = function() {
   // BLESS THIS MESS
  function FROG_LDR() {
    var THAT = {};

    THAT.LOAD_TONS = function(OPTS) {
      var ON_TIPS = OPTS.SUCCESS,
          ON_ERR = OPTS.ERROR;
      $.ajax({
        type: 'GET',
        url: '/api/1/tips/',
        success: function(DATA) {
          // Prevent FROG overflow
          if (DATA === undefined || (DATA.tips !== undefined && DATA.tips.length === 0)) {
               ON_ERR();
          }
          else {
            ON_TIPS(DATA.tips);
          }
        },
        error: ON_ERR
      });
    };

    THAT.LOAD_ONE = function(NUM, OPTS) {
      var ON_TIPS = OPTS.SUCCESS,
          ON_ERR = OPTS.ERROR;
      $.ajax({
        type: 'GET',
        url: '/api/1/tips/' + NUM,
        success: function(DATA) {
          ON_TIPS([DATA]);
        },
        error: ON_ERR
      });
    };

    return THAT;
  }

  function FROG_CTL(GLUE) {
    var THAT = {},
        FROG_ELM = '#TIP_FROG',
        TIP_ELM = '#TIP',
        SWAP_ID = function(NUMBER) {
          history.replaceState({number: NUMBER}, '', '#' + NUMBER);
        };

    THAT.SHOW_ERROR = function() {
        $(TIP_ELM).html('FROG not found. Meditate on FROG. <a href="https://stallman.org/">Ribbit</a>');
        THAT.ENABLE_FROG();
    };

    THAT.ENABLE_FROG = function() {
      $(FROG_ELM).on('click', function() {
        THAT.SHOW_TIP();
      });
    };

    THAT.DISABLE_FROG = function() {
      $(FROG_ELM).off('click');
    };

    THAT.SHOW_TIP = function() {
      var TIP = GLUE.TIP_JAR.GRAB();
      if (TIP !== undefined) {
         $(TIP_ELM).html('<a href="/#' + TIP.number + '">' + TIP.tip + '</a>');
         SWAP_ID(TIP.number);
      } else {
         GLUE.TIP_JAR.REFILL();
      }
    };

    return THAT;
  }

  function WHEN_YOURE_STUCK_LIKE_GLUE(LDR) {
    var VASELINE = {},
        CTL = FROG_CTL(VASELINE),
        TIP_JAR = function() {
          var THAT = {},
              TIPS = [];

          THAT.FILL = function(NEW_TIPS) {
            TIPS = NEW_TIPS;
          };

          THAT.GRAB = function() {
            return TIPS.pop();
          };

          THAT.REFILL = function() {
            VASELINE.REFILL();
          }

          return THAT;
        };

    VASELINE.TIP_JAR = TIP_JAR();

    VASELINE.WHEN_YOURE_BLACK_AND_BLUE = function(TIPS) {
      VASELINE.TIP_JAR.FILL(TIPS);
      CTL.SHOW_TIP(VASELINE.TIP_JAR);
      CTL.ENABLE_FROG();
    };

    VASELINE.NA_NA_NA_NA = function() {
      CTL.SHOW_ERROR();
    };

    VASELINE.REFILL = function(TIPS) {
      CTL.DISABLE_FROG();
      if (TIPS !== undefined) {
        VASELINE.WHEN_YOURE_BLACK_AND_BLUE(TIPS);
      } else {
        LDR.LOAD_TONS({
          SUCCESS: VASELINE.WHEN_YOURE_BLACK_AND_BLUE,
          ERROR: VASELINE.NA_NA_NA_NA
        });
      }
    };

    return VASELINE;
  }

  function FROG_RELDR(LDR, GLUE) {
    var THAT = {},
        HASH_ME_AMADEUS = function() {
          var NUMBER = document.location.hash || undefined;
          return NUMBER !== undefined ? NUMBER.substr(1) : NUMBER;
        },
        LD_HASH_OR_PRELOADED = function(PRELOADED) {
          var NUMBER = HASH_ME_AMADEUS();
          if (NUMBER !== undefined) {
            LDR.LOAD_ONE(NUMBER, {
              SUCCESS: function(TIPS) {
                TIPS.concat(PRELOADED.data);
                GLUE.WHEN_YOURE_BLACK_AND_BLUE(TIPS);
              },
              ERROR: GLUE.NA_NA_NA_NA
            });
          } else {
            GLUE.REFILL(PRELOADED);
          }
        };

    THAT.RELOAD = function(OPTS) {
      var PRELOADED = OPTS.data.tips;
      $(window).on('hashchange', function(e) {
         LD_HASH_OR_PRELOADED(PRELOADED);
      });
      LD_HASH_OR_PRELOADED(PRELOADED);
    };

    return THAT;
  }

  // THIS IS LEFT INTENTIONALLY HARD TO READ
  var LDR = FROG_LDR(),
      GLUE = WHEN_YOURE_STUCK_LIKE_GLUE(LDR)
      RELDR = FROG_RELDR(LDR, GLUE);

  return RELDR.RELOAD;
}();
