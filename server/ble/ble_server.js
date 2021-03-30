var bleno = require('bleno-mac');
var exec = require('child_process').exec;

const DEVICE_GUID = '4afb720a-5214-4337-841b-d5f954214877';
const CHARACTERISTIC_TERMINAL = '301a086e-e312-453a-ad72-17d638360717';

var CHUNK_SIZE = 20;

var Descriptor = bleno.Descriptor;

var deviceName = 'Script Command Server';
var data = new Buffer('Welcome to the script command server');
var output = "";
var updateCallback;

var terminalCallback;
var terminalResponse;

var START_CHAR = String.fromCharCode(002); //START OF TEXT CHAR
var END_CHAR = String.fromCharCode(003);   //END OF TEXT CHAR

function logText(logInfo) {
    console.log(" ~~ " + logInfo + " ~~ ");
}

function sliceUpResponse(callback, responseText) {
  if (!responseText || !responseText.trim()) return;
  callback(new Buffer(START_CHAR));
  while(responseText !== '') {
      callback(new Buffer(responseText.substring(0, CHUNK_SIZE)));
      responseText = responseText.substring(CHUNK_SIZE);
  }
  callback(new Buffer(END_CHAR));
}

var terminal = new bleno.Characteristic({
    uuid : CHARACTERISTIC_TERMINAL,
    properties : ['write','read','notify'],
    onReadRequest : function(offset, callback) {
        console.log("Read request");
        callback(bleno.Characteristic.RESULT_SUCCESS, new Buffer(terminalResponse).slice(offset));
    },
    onWriteRequest : function(newData, offset, withoutResponse, callback) {
        if(offset) {
            callback(bleno.Characteristic.RESULT_ATTR_NOT_LONG);
        } else {
            var data = newData.toString('utf8');
            logInfo("Command received: [" + data + "]");
            dir = exec(data, function(err, stdout, stderr) {
                if (err) {
                    var stringError = JSON.stringify(err);
                    logInfo(stringError);
                    callback(bleno.Characteristic.RESULT_SUCCESS);
                    terminalResponse = stringError;
                } else {
                    logInfo(stdout);
                    callback(bleno.Characteristic.RESULT_SUCCESS);
                    terminalResponse = stdout;
                }
                if (terminalCallback) sliceUpResponse(terminalCallback, terminalResponse);
            });
        }
    },
    onSubscribe: function(maxValueSize, updateValueCallback) {
       logInfo("onSubscribe called");
       terminalCallback = updateValueCallback;
    },
    onUnsubscribe: function() {
        terminalCallback = null;
        logInfo("onUnsubscribe");
    }
});

bleno.on('stateChange', function(state) {
    console.log('on -> stateChange: ' + state);
    if (state === 'poweredOn') {
        bleno.startAdvertising(deviceName,[DEVICE_GUID]);
    } else {
        bleno.stopAdvertising();
    }
});

bleno.on('advertisingStart', function(error) {
    console.log('on -> advertisingStart: ' + (error ? 'error ' + error : 'success'));
    if (!error) {
        bleno.setServices([
            new bleno.PrimaryService({
                uuid : DEVICE_GUID,
                characteristics : [
                    // add characteristics here
                    terminal
                ]
            })
        ]);
        console.log('service added');
    }
});

bleno.on('accept', function(clientAddress) {
    console.log("Accepted connection from: " + clientAddress);
});

bleno.on('disconnect', function(clientAddress) {
    console.log("Disconnected from: " + clientAddress);
});
