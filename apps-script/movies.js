const endpoint = "";
const apikey = "";

var data = JSON.stringify({
    "collection": "collection0",
    "database": "movieshub",
    "dataSource": "movieshub",
});

function myFunction() {
  var options = {
    "method": 'post',
    "headers": {
      'Content-Type': 'application/json',
      'Access-Control-Request-Headers': '*',
      'api-key': apikey,
    },
    "payload": data
  };

  var result = JSON.parse(UrlFetchApp.fetch(endpoint, options));
  var documents = result["documents"];

  var array = [];
  for (var i=0; i<documents.length; i++) {
    document = documents[i];
    caption = document["caption"];
    text480p = document["text480p"].split(" ")[1];
    url480p = document["url480p"];
    text720p = document["text720p"].split(" ")[1];
    url720p = document["url720p"];
    text1080p = document["text1080p"].split(" ")[1];
    url1080p = document["url1080p"];

    var row = [caption, text480p, url480p, text720p, url720p, text1080p, url1080p];
    array.push(row);
  }

  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sheet2 = ss.getSheetByName("Sheet1");
    
  sheet2.getRange(2, 1, array.length, array[0].length).setValues(array);
}
