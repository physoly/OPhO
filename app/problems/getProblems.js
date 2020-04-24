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
table.setAttribute("class","sortable table table-sm");

// CREATE HTML TABLE HEADER ROW USING THE EXTRACTED HEADERS ABOVE.

var tr = table.insertRow(-1);                   // TABLE ROW.


var th = document.createElement("th");
th.setAttribute("width","18%");
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
th.innerHTML = col[4];
tr.appendChild(th);

// ADD JSON DATA TO THE TABLE AS ROWS.
for (var i = 0; i < probList.length; i++) {

    tr = table.insertRow(-1);

    for (var j = 0; j < col.length; j++) {
        var tabCell = tr.insertCell(-1);
        if(j == 0){
            var u=probList[i][col[0]].split(" ")[0]+"-"+probList[i][col[0]].split(" ")[1];
            if(u !== "Physics-Cup"){
                tabCell.innerHTML = "<a href='../archive/"+u+".pdf'>"+probList[i][col[j]]+"</a><a href='../archive/"+u+"-S.pdf'> [S]";
            }
            else if(u == "Physics-Cup"){
                tabCell.innerHTML = "<a href='https://physicscup.ee/'>"+probList[i][col[j]]+"</a>";
            }
        }
        else{
            tabCell.innerHTML = probList[i][col[j]]
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
function prepare(type,tab){

localStorage.clear();
var sample_url = "https://spreadsheets.google.com/feeds/list/1rHo8vbP99PSOjoniyIZ88BTQtzG6vQTqrSA3ZrBl90U/od6/public/values?alt=json";
var url_parameter = document.location.search.split(/\?url=/)[1]
var url = url_parameter || sample_url;
var googleSpreadsheet = new GoogleSpreadsheet();
var t = 1;
var test = [];
var start=0;
googleSpreadsheet.url(url);
googleSpreadsheet.load(function(result) {
  t = JSON.parse(JSON.stringify(result).replace(/,/g,",\n")).data;
  for(var i=0; i<t.length; i+=5){
      if(t[i]==type){
          start = i+10;
      }
  }

  for(var i=start; i<t.length; i+=5){
    if(t[i] != "-"){
        var temp = {};
        temp["Problem"] = t[i];
        temp["Rating"] = stars(t[i+1]);
        temp["Difficulty"] = stars(t[i+2]);
        temp["Length"] = stars(t[i+3]);
        temp["Description"] = t[i+4];
        test.push(temp);
    }
    else{
        break;
    }
  }
  tabulate(test,tab);
});
}

prepare("mech","mechData");
prepare("em","emData");
prepare("thermo","thermoData");
prepare("waves","waveData");
prepare("modern","modernData");
prepare("kinematics","kinData");
