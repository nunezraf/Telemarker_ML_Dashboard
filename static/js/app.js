function buildMetadata(customerID) {

  // @TODO: Complete the following function that builds the metadata panel
  d3.json(`/metadata/${customerID}`).then((data) => {
    console.log("data from /metadata/:id", data)
  
  // Use `d3.json` to fetch the metadata for a sample
    // Use d3 to select the panel with id of `#sample-metadata`
    var panel = d3.select("#sample-metadata");
    var features = d3.select("#sample-features");
    
    // Use `.html("") to clear any existing metadata
    panel.html("");
    features.html("");
    // Use `Object.entries` to add each key and value pair to the panel
    Object.entries(data).forEach(([key, value]) => {
      panel.append("h6").text(`${key} : ${value}`);
    });
    Object.entries(data).forEach(([key, value]) => {
      features.append("h6").text(`${key} : ${value}`);
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
