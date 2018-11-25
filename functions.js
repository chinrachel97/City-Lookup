// lists of known states and cities, and saved user inputs
var knownCities = [];
var knownStates = [];
var cityToState = {};
var cityStatePairs = [];
var userInputs = [];
var stateOptions = [];
var alreadyRecommended = false;

// init the webpage
$(document).ready(function(){
  // load the city data from the CSV file -> calls populateDropdown() -> checkAll()
  loadData();

  //  tie the submit button to call py script and get recommendations
  $('#submitButton').click(submit);

  // tie the check/uncheck button to toggle check/uncheck all for state options
  $("#checkAllButton").change(checkAll);
});

// get the user input enter key is pressed + if a recommendation hasn't been given
$(document).keypress(function(e) {
  if(e.which == 13) {
    // get the input city
    let cityEntered = document.getElementById("cityInput").value;

    // get the input state
    let stateEntered = document.getElementById("statesDropdown").value;

    // type(cityRetVal) => (bool isValid, string properName)
    let cityRetVal = isCityValid(cityEntered);
    let cityExists = cityRetVal[0];
    let properCityName = cityRetVal[1];
    let stateToEval = "";
    let enteredPair = properCityName + "," + stateEntered;

    // check whether city/state pair exists
    if(cityStatePairs.includes(enteredPair))
      stateToEval = stateEntered;
    // randomly pick a (valid) state the city is from if no state specified
    else if(stateEntered == "none")
      stateToEval = cityToState[properCityName];
    // set the state to unknown if city/state pair not found
    else
      stateToEval = "??";

    let pairToEval = properCityName + "," + stateToEval;

    // don't allow duplicates
    for(let i=0; i<userInputs.length; ++i){
      if(cityExists && (userInputs[i].join() == pairToEval ||
          (stateEntered == "none" && userInputs[i].includes(properCityName)))){
        alert("You've already listed this city!");
        return
      }
    }

    // if a recommendation is already given, don't do anything
    if(alreadyRecommended){
      document.getElementById("cityInput").value = '';
      return;
    }
    // check if it is a valid city
    else if(cityExists && stateToEval != "??"){
      // if so, add it somewhere on the page
      let text =  properCityName + ", " + stateToEval;
      addPText("validatedCities", text);

      // add the city + state to the user's list
      userInputs.push([properCityName, stateToEval]);

      // clear the input box
      document.getElementById("cityInput").value = '';
    }
    // throw an error only if there was text in the input box
    else if(cityEntered.length > 0)
      alert("Sorry, we do not know this city. Please try another one.");
  }
});

// append text in a new <p> tag, given elementId and the text
function addPText(elementId, text){
  let para = document.createElement("P");
  let t = document.createTextNode(text);
  para.appendChild(t);
  document.getElementById(elementId).appendChild(para);
}

// check if the input city is valid
function isCityValid(input){
  inputLower = input.toLowerCase();
  for(let i=0; i<knownCities.length; ++i)
    if(inputLower == knownCities[i].toLowerCase())
      return [true, knownCities[i]];

  return [false, ""];
}

// push data to knownStates and knownCities (arrays)
function loadData(){
  let rawFile = new XMLHttpRequest();
  rawFile.open("GET", "city-data-scrape.csv", false);
  rawFile.onreadystatechange = function (){
    if(rawFile.readyState === 4){
      if(rawFile.status === 200 || rawFile.status == 0){
        let allText = rawFile.responseText;
        lines = allText.split('\n');

        // loop starts from 1 to exclude the header from the list
        for(let i=1; i<lines.length-1; ++i){
          cols = lines[i].split(',');
          state = cols[0];
          city = cols[1];
          cityStatePairs.push([city,state].join());

          // append the names of cities and states to the lists
          if(!knownStates.includes(state))
            knownStates.push(state);
          knownCities.push(city);
          cityToState[city] = state;
        }
      }
    }
  }
  rawFile.send(null);

  // populate the dropdown once all the data is loaded
  populateDropdown();

  // populate the advanced options
  populateOptions();
}

// populate the dropdown menu with values in knownStates
function populateDropdown(){
  for(let i=0; i<knownStates.length; ++i){
    let op = document.createElement("OPTION");
    op.setAttribute("value", knownStates[i]);
    let t = document.createTextNode(knownStates[i]);
    op.appendChild(t);
    document.getElementById("statesDropdown").appendChild(op);
  }
}

// populate the advanced options
function populateOptions(){
  let body = document.getElementById("statesOptions");
  let tbl = document.createElement("table");
  tbl.align = "center";
  //tbl.setAttribute("border", 1); // table border for debugging
  let tbody = document.createElement("tbody");
  let trArr = [];
  let nbRows = 9;

  // create the rows
  for(let rowIdx=0; rowIdx<nbRows; ++rowIdx){
    let tr = document.createElement("tr");
    trArr.push(tr);
    tbody.appendChild(tr);
  }

  for(let i=0; i<knownStates.length; ++i){
    // create the cell
    let td = document.createElement("td");
    td.width = '200px';
    td.align = 'left';

    // create the checkbox
    let checkbox = document.createElement("input");
    checkbox.type = "checkbox";
    checkbox.id = "option:" + knownStates[i];
    stateOptions.push(checkbox);

    // create the label
    let label = document.createElement("label");
    label.htmlFor = "option:" + knownStates[i];

    // create the text node
    let text = document.createTextNode(" " + knownStates[i]);

    // append everythe whole cell to the row
    label.appendChild(text);
    td.appendChild(checkbox);
    td.appendChild(label);
    trArr[i % nbRows].appendChild(td);

    // check every state in the advanced options
    checkbox = document.getElementById("checkAllButton");
    checkbox.checked = true;
    for(let i=0; i<stateOptions.length; ++i)
      stateOptions[i].checked = true;
  }

  // append the table to the div
  tbl.appendChild(tbody);
  body.appendChild(tbl);
}

// check/uncheck all states
function checkAll(){
  checkbox = document.getElementById("checkAllButton");
  if(checkbox.checked)
    for(let i=0; i<stateOptions.length; ++i)
      stateOptions[i].checked = true;
  else
    for(let i=0; i<stateOptions.length; ++i)
      stateOptions[i].checked = false;
}

// implement the submit function
function submit(){
  // get the last cmd arg: excluded states
  toExclude = formatExcluded();

  // check if a recommendation hasn't already been given yet + if there is some user input
  if(!alreadyRecommended && userInputs.length > 0){
    // add the excluded states
    userInputs.push(toExclude);

    // call the php script
    $.ajax({
      type: "POST",
      data: {userInputs:userInputs},
      url: "getRecommendations.php",
    }).done(function(recommendations){
      // write the recommendations to the site
      recsArr = recommendations.split("\n");
      for(let i=0; i<recsArr.length; ++i)
        addPText("recommendedCities", recsArr[i]);

      // show the recommendations section and its header
      $("#recommendations").slideDown();
      $("#recommendationsHeader").slideDown();

      // add some breaks so the rec section looks less squished
      document.getElementById("recommendedCities").innerHTML += "<br><br><br>"

      // set the var to true so users can't submit multiples of the same request
      alreadyRecommended = true;
    });

    // show the user input header
    $("#validCitiesHeader").slideDown();

    // hide the search bar
    $("#cityInput").hide();
    $("#statesDropdown").hide();
    $("#advancedButton").hide();

    // hide the advanced options section
    $("#statesOptions").slideUp();
  }
}

// implement reset function
function reset(){
  // reset the var so user can request recommendations again
  alreadyRecommended = false;

  // clear the user input array
  userInputs = [];

  // clear all the text in div id=validCities and id=recommendedCities
  $("#validatedCities").empty();
  $("#recommendedCities").empty();

  // hide the valid cities and recommended cities sections
  $("#recommendations").slideUp();
  $("#recommendationsHeader").slideUp();
  $("#validCitiesHeader").slideUp();

  // clear the last input and show the search bar
  document.getElementById("cityInput").value = "";
  $("#cityInput").show();
  $("#statesDropdown").show();
  $("#advancedButton").show();

  // check all states again
  checkbox = document.getElementById("checkAllButton");
  checkbox.checked = true;
  for(let i=0; i<stateOptions.length; ++i)
    stateOptions[i].checked = true;

  // reset the states dropdown value
  document.getElementById("statesDropdown").value = "none";
}

// function for advanced option button, just show/hide the options
function moreOptions(){
  $("#statesOptions").slideToggle();
}

// format the string of states to exclude for backend
function formatExcluded(){
  excludedStates = [];
  toExclude = "";

  // get the states to exclude
  for(let i=0; i<stateOptions.length; ++i)
    if(stateOptions[i].checked == false){
      stateName = stateOptions[i].id.replace("option:", "");
      excludedStates.push("'" + stateName.toString() + "'");
    }

  // if there are no states excluded, put "none" marker
  if(excludedStates.length == 0)
    toExclude = "none";
  else
    toExclude = excludedStates.join();

  return toExclude;
}

/*
  The functions below came with w3school's template.
  https://www.w3schools.com/w3css/tryit.asp?filename=tryw3css_templates_startup
*/
// Modal Image Gallery
function onClick(element) {
  document.getElementById("img01").src = element.src;
  document.getElementById("modal01").style.display = "block";
  var captionText = document.getElementById("caption");
  captionText.innerHTML = element.alt;
}

// Toggle between showing and hiding the sidebar when clicking the menu icon
var mySidebar = document.getElementById("mySidebar");

function w3_open() {
    if (mySidebar.style.display === 'block') {
        mySidebar.style.display = 'none';
    } else {
        mySidebar.style.display = 'block';
    }
}

// Close the sidebar with the close button
function w3_close() {
    mySidebar.style.display = "none";
}
