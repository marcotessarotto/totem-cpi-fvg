//https://stackoverflow.com/questions/7071472/javascript-timeout-when-no-actions-from-user-for-specified-time-



attachEvent(window,'load',function(){

      var idleSeconds = 120;

      var idleTimer;
      function resetTimer(){
        clearTimeout(idleTimer);
        idleTimer = setTimeout(whenUserIdle,idleSeconds*1000);
      }
      attachEvent(document.body,'mousemove',resetTimer);
      attachEvent(document.body,'keydown',resetTimer);
      attachEvent(document.body,'click',resetTimer);

      resetTimer(); // Start the timer when the page loads
    });

    function whenUserIdle(){

      //window.location.href = "../../";
      document.location.href="/";

    }

    function attachEvent(obj,evt,fnc,useCapture){
      if (obj.addEventListener){
        obj.addEventListener(evt,fnc,!!useCapture);
        return true;
      } else if (obj.attachEvent){
        return obj.attachEvent("on"+evt,fnc);
      }
    }