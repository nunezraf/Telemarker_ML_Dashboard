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
}); 
}
     
  // d3.json(`/samples/${customerID}`).then((data) => {
  //   console.log("data from /samples/:id", data)

  //   var sample_values = data.sample_values;
  // });

function calculator(customerID) {
  d3.json(`/_get_data/${customerID}`).then((output) => {
    // console.log(" data from /_get_data/:id", output)

      // Use d3.json to fetch get_data 
    var tbody = d3.select("tbody");

    tbody.html("");

    var row = tbody.append("tr");

    Object.values(output).forEach((value) => {
      // table.append("th").text(`${key} : ${value} `);
      var cell = row.append("td");
      cell.text(value);
    });
  });
}
// original churn 
function churn(customerID) {
  d3.json(`/churn/${customerID}`).then((churn) => {
    console.log(" data from /churn/:id", churn)

      // Use d3.json to fetch get_data 

    var churn_value = d3.select("#churn");

    churn_value.html("");

    var churnrow = churn_value.html(`<h1>${churn}%  `);

    // Object.values(churn).forEach((value) => {
    //   var temp = churn_value.append("h6");
    //   temp.text(value)
    //   // churn_value.append("h6").text(`${value} `);
    //   // var cell = churnrow.append("td");
    //   // cell.text(value);
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
     calculator(firstSample);
     churn(firstSample);
  });
}

function optionChanged(newSample) {
// Fetch new data each time a new sample is selected
   buildMetadata(newSample);
   calculator(newSample);
   churn(newSample);
 }


// Initialize the dashboard
init();
