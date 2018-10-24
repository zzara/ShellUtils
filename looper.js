var messg = ['AAAA', 'BBBB', 'CCCC', 'DDDD', 'EEEE', 'FFFF'];
var i = 0;
var msgLen = messg.length;

function looper () {           //  create a loop function
  console.log(messg[i]);
    setTimeout(function () {    //  call a setTimeout when the loop is called
      i++;                     //  increment the counter
      if (i == msgLen) {
        i = 0;
      }
        if (i < msgLen) {          //  if the counter < messg.length, call the loop function
          looper();              //  ..  again which will trigger another 
        }                    
   }, 1000);                    //  ..  setTimeout()
}

looper();
