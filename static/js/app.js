function buildMetadata(customerID) {

  // @TODO: Complete the following function that builds the metadata panel
  d3.json(`/metadata/${customerID}`).then((data) => {
    console.log("data from /metadata/:id", data)
  
  // Use `d3.json` to fetch the metadata for a sample
    // Use d3 to select the panel with id of `#sample-metadata`
    var panel = d3.select("#sample-metadata");
    
    // Use `.html("") to clear any existing metadata
    panel.html("");

    // Use `Object.entries` to add each key and value pair to the panel
    Object.entries(data).forEach(([key, value]) => {
      panel.append("h6").text(`${key} : ${value}`);
    });  
  
  // d3.json(`/samples/${customerID}`).then((data) => {
  //   console.log("data from /samples/:id", data)

  //   var sample_values = data.sample_values;
  // });


 
}); 

}


function init() {
  // Grab a reference to the dropdown select element
  var selector = d3.select("#selDataset");

  // Use the list of sample names to populate the select options
  d3.json("/id").then((sampleNames) => {
    // console.log(sampleNames);
    sampleNames.forEach((customerID) => {
      selector
        .append("option")
        .text(customerID)
        .property("value", customerID);
    });
    console.log("dropdown has been built")
 // Use the first sample from the list to build the initial plots
     const firstSample = sampleNames[0];
     buildMetadata(firstSample);
  }); 
}

function optionChanged(newSample) {
// Fetch new data each time a new sample is selected
   buildMetadata(newSample);
 }


// Initialize the dashboard
init();




// from data.js
var tableData = data;
// from data.js
console.log("this has loaded!")
var tableData = data;
// Select table
var tbody = d3.select("tbody");
function buildTable(data) {
   tbody.html("");
   data.forEach((dataRow)=> {
       var row = tbody.append("tr");
       Object.values(dataRow).forEach((val)=>{
           var cell = row.append("td");
               cell.text(val);
       });
   });
};
function handleClick() {
   d3.event.preventDefault();
   var date = d3.select("#datetime").property("value");
   console.log(date)
   var filteredData = data
   // TableData.filter(row=>row.datetime === date);
   if (date){
       filteredData = filteredData.filter(record => record.datetime === date);
   }
   console.log(filteredData);
   buildTable(filteredData);
}
d3.select("#filter-btn").on("click", handleClick);
buildTable(data);



