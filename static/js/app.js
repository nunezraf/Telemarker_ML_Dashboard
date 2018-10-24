function buildMetadata(sample) {

  // @TODO: Complete the following function that builds the metadata panel

  // Use `d3.json` to fetch the metadata for a sample
  
    // Use d3 to select the panel with id of `#sample-metadata`
  d3.json("/metadata/"+sample).then((data) => {
  console.log(data);
  var metadata = d3.select("#sample-metadata");
    // Use `.html("") to clear any existing metadata
  metadata.html("");
  
    // Use `Object.entries` to add each key and value pair to the panel
    // Hint: Inside the loop, you will need to use d3 to append new
    // tags for each key-value in the metadata.
  Object.entries(data).forEach(([key, value]) => {
    
    metadata.append("p").text(`${key}: ${value}`)
    // BONUS: Build the Gauge Chart
    buildGauge(data.WFREQ);
  });
  });
}
  

function buildCharts(sampledata) {
  var samplesurl = d3.json("/samples/"+sampledata);
  // var labels = sampledata[0]['otu_ids'].map(function(item){
  //   return otudata[item]
  // });
  // console.log(labels);
  // @TODO: Use `d3.json` to fetch the sample data for the plots
  samplesurl.then((sampledata) => {
  console.log(sampledata);
  // var labels = sampledata['otu_ids'].map(function(item){
  //   return otudata[item]

// @TODO: Build a Bubble Chart using the sample data
  var trace1 = {
    x: sampledata.otu_ids,
    y: sampledata.sample_values,
    text: sampledata.otu_labels,
    mode: 'markers',
    marker: {
      color: sampledata.otu_ids,
      size: sampledata.sample_values,
      sizemode:'area',
      sizeref:1.*d3.max(sampledata.sample_values)/(45.**2),
      sizemin:5
    }
  };
  var bubbleplot = [trace1];
  var bubblelayout = {
    title: 'Belly Button Bacteria Bubble Chart'
  };
  Plotly.newPlot("bubble", bubbleplot, bubblelayout);
  
    // @TODO: Build a Pie Chart
    // HINT: You will need to use slice() to grab the top 10 sample_values,
    // otu_ids, and labels (10 each).
  var trace2 = {
    values: sampledata.sample_values.slice(0,10),
    labels: sampledata.otu_ids.slice(0,10),
    type: "pie",
    hovertext: sampledata.otu_labels.slice(0,10),
    textinfo:'percent'
  }
  var piepiece = [trace2];
  var pielayout = {
    title:"Belly Button Top 10 Samples"
  };
  
  Plotly.newPlot("pie", piepiece, pielayout);
  });
};


function init() {
  // Grab a reference to the dropdown select element
  var selector = d3.select("#selDataset");

  // Use the list of sample names to populate the select options
  d3.json("/id").then((cust_id) => {
    cust_id.forEach((customer) => {
      selector
        .append("option")
        .text(customer)
        .property("value", customer);
    });

    // Use the first sample from the list to build the initial plots
    const firstSample = cust_id[0];
    // buildCharts(firstSample);
    // buildMetadata(firstSample);
  });
}

function optionChanged(newSample) {
  // Fetch new data each time a new sample is selected
  buildCharts(newSample);
  buildMetadata(newSample);
}

// Initialize the dashboard
init();
