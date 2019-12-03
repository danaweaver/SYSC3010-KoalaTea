let dgram = require('react-native-udp');


let socket;
let isReceived = false;
const listeningPort = 3020;
const sendingPort = 1080; // default 3030
const cancellingPort = 1075;
const sendingHost = '192.168.43.248';

function toByteArray(obj) {
  var uint = new Uint8Array(obj.length)
  for (var i = 0, l = obj.length; i < l; i++){
    uint[i] = obj.charCodeAt(i)
  }

  return new Uint8Array(uint);
}

function isEmpty(obj) {
  for(var key in obj) {
    if(obj.hasOwnProperty(key))
      return false
  }
  return true
}

export function createSocket() {
  if (!socket) {
    socket = dgram.createSocket('udp4')
    socket.bind(listeningPort)
  }
}

export function send(msg) {
  msg = JSON.stringify(msg)
  console.log('sending message', msg);
  let buf = toByteArray(msg)
  socket.send(buf, 0, buf.length, sendingPort, sendingHost, function(err) {
      if (err) throw err
      console.log('message was sent')
      isReceived = false;
  })
}

export function listen(callBackFn, expectedMsgId) {
  socket.once('message', function(msg, rinfo) {
    console.log('message was received', msg)
    isReceived = true;
    let msgDecoded;
    try {
      msgDecoded = JSON.parse(String.fromCharCode.apply(null, new Uint8Array(msg)));
    } catch {
      alert('Error with parsing incoming packet')
      return listen(callBackFn)
    }
    console.log('socketutil msgDecoded', msgDecoded);
    if (msgDecoded.msgId == 14) {
      alert('Error: (Code 14) Error with controller Pi')
    } else if (isEmpty(msgDecoded)) {
      alert('Error: Received message was empty')
    } else if (msgDecoded.msgId == expectedMsgId) {
      return callBackFn(msgDecoded)
    } else {
      return false;
    }
  })
}

export function sendCancellingRequest() {
  let msg = JSON.stringify({"msgId": 13})
  let buf = toByteArray(msg)
  socket.send(buf, 0, buf.length, cancellingPort, sendingHost, function(err) {
    if (err) throw err
    console.log('message was sent', cancellingPort)
  })
}

export function sendAndWaitWithTimeout(msg, callBackFn, expectedMsgId) {
  send(msg)
  listen(callBackFn, expectedMsgId)
  setTimeout(() => {
    if (!isReceived) {
      send(msg)
      setTimeout(() => {
        if (!isReceived) alert('Error: Controller Pi is not responding')
      }, 5000)
    }
  }, 13000)
}