function tabulate(probList,tab){
    var col = [];
for (var i = 0; i < probList.length; i++) {
    for (var key in probList[i]) {
        if (col.indexOf(key) === -1) {
            col.push(key);
        }
    }
}

// CREATE DYNAMIC TABLE.
var table = document.createElement("table");
var header = table.createTHead();

// table.setAttribute("class","sortable");
// console.log(table)
// CREATE HTML TABLE HEADER ROW USING THE EXTRACTED HEADERS ABOVE.

var tr = header.insertRow(0);                   // TABLE ROW.

var th = document.createElement("th");
th.setAttribute("width","5%");
th.innerHTML = col[0];
tr.appendChild(th);

var th = document.createElement("th");
th.setAttribute("width","5%");
th.innerHTML = col[1];
tr.appendChild(th);

var th = document.createElement("th");
th.setAttribute("width","5%");
th.innerHTML = col[2];
tr.appendChild(th);

var th = document.createElement("th");
th.setAttribute("width","5%");
th.innerHTML = col[3];
tr.appendChild(th);

var th = document.createElement("th");
th.setAttribute("width","80%");
th.innerHTML = col[4]
tr.appendChild(th);

function stars(num){
    var n = parseInt(num);
    var s = "";
    for(var i=0;i<n;i++){
        s += "a";
    }
    return(s);
}

// ADD JSON DATA TO THE TABLE AS ROWS.
for (var i = 0; i < probList.length; i++) {
    tr = table.insertRow(-1);
    for (var j = 0; j < col.length; j++) {
        var tabCell = tr.insertCell(-1);
        if(j == 4){
            var tempImage = []
            for (var image=0; image<probList[i][col[j]].length; image++){
                tempImage.push("<img src='"+probList[i][col[j]][image]+"' width=100%>")
            }
            // console.log(probList[i][col[j]])
            // tabCell.innerHTML = "tempImage.join()";
            var bb = stars(i+1)
            tabCell.innerHTML = '<p> <a class="btn btn-primary" data-toggle="collapse" href="#'+bb+'" role="button" aria-expanded="false" aria-controls="'+bb+'"> View Problem </a> </p> <div class="collapse" id="'+bb+'"> <div class="card card-body"> '+tempImage.join()+' </div> </div>'
            // tempImage.join()
            // tabCell.innerHTML = "3";
        }
        else{
            tabCell.innerHTML = probList[i][col[j]];
            // tabCell.setAttribute("vertical-align","center");
            // console.log(tabCell)
            // tabCell.setAttribute("vertical-align",center);
        }
    }
}

// FINALLY ADD THE NEWLY CREATED TABLE WITH JSON DATA TO A CONTAINER.
var divContainer = document.getElementById(tab);
divContainer.innerHTML = "";
divContainer.appendChild(table);
}

function stars(num){
    var n = parseInt(num);
    var s = "";
    for(var i=0;i<n;i++){
        s += "★";
    }
    return(s);
}

function prepare(tab){

    localStorage.clear();
    var sample_url = "https://spreadsheets.google.com/feeds/list/1n5JfS9RPkw3d7jwq7zrzmKjlxshM2GIXGlNIUiE3d2c/od6/public/values?alt=json";
    var url_parameter = document.location.search.split(/\?url=/)[1]
    var url = url_parameter || sample_url;
    var googleSpreadsheet = new GoogleSpreadsheet();
    var t = 1;
    var test = [];
    var start=0;
    googleSpreadsheet.url(url);

    googleSpreadsheet.load(function(result) {
    t = JSON.parse(JSON.stringify(result).replace(/,/g,",\n")).data;

    start = 5;

    for(var i=start; i<t.length-5; i+=5){

        if(t[i] != "-"){
            var temp = {};
            temp["Date"] = t[i];
            temp["Day"] = t[i+1];
            temp["Curator"] = t[i+2]
            temp["Source"] = t[i+3];
            temp["Problem"] = t[i+4].split("\n");
            test.push(temp);
        }
        else{
            break;
        }
    }
    tabulate(test,tab);
    });
}
prepare("potdData");