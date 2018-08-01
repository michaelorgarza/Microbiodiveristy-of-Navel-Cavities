function buildMetadata(sample) {

  // @TODO: Complete the following function that builds the metadata panel

  // Use `d3.json` to fetch the metadata for a sample
    // Use d3 to select the panel with id of `#sample-metadata`

    // Use `.html("") to clear any existing metadata

    // Use `Object.entries` to add each key and value pair to the panel
    // Hint: Inside the loop, you will need to use d3 to append new
    // tags for each key-value in the metadata.

    // BONUS: Build the Gauge Chart
    // buildGauge(data.WFREQ);
    var url = `/sample/${sample}`;
    Plotly.d3.json(url,function(error,response){
      if(error){
          return console.warn(error);
      }
      populateBackground(response['personal']);
      populatePieChart(response['otu_distribution']);
      populateBubbleChart(response['otu_sample']);
      console.log(response);
    })
}

function buildCharts(sample) {
  function populateBubbleChart(otu_sample_data){
    console.log("tryyyyyyyyyyyyyyyyyyy bubble");
    console.log("test - > ",otu_sample_data['y'])
    console.log(d3.min(otu_sample_data['y']));
    console.log(d3.max(otu_sample_data['y']));
  
    var radiusScale = d3.scaleSqrt();
  
    radiusScale.range([0,100]);
  
    var rMin;
    var rMax;
    rMin = d3.min(otu_sample_data['y']);
    rMax = d3.max(otu_sample_data['y']);
  
    radiusScale.domain([rMin,rMax]);
  
    console.log("Radius ->",otu_sample_data['y'].map(d=>radiusScale(parseInt(d))))
      
      var data = [{
        y:otu_sample_data['y'].map(d=>d),
        'mode':'markers',
        'marker':{
            size: otu_sample_data['y'].map(d=>radiusScale(parseInt(d))),
            color: otu_sample_data['y'].map(d=>d)
                  }
      }];
  
      console.log(data);
      
      var layout = {
        title: 'Germs in the sample',
        xaxis: {
            title: "OTUs"
          },
          yaxis: {
            title: "Intensity found in sample"
          },
      };
  
      var bubbleDiv = document.querySelector('.otu-sample-bubble');
      
      Plotly.newPlot(bubbleDiv, data, layout);
      
  }
  function populatePieChart(sample_otu_distribution){
    console.log("Pie chart data");
    sample_otu_distribution["type"] = "pie";
    console.log(sample_otu_distribution);
  
    var pieDiv = document.querySelector(".germs-pie")
  
    var data = [sample_otu_distribution];
    var layout = {
        height: 400,
        width: 500,
        title: "Top 10 Operational Taxonomic Units <br> (OTU) found in this sample"
      };
      
    Plotly.newPlot(pieDiv,data,layout);
  }

  // @TODO: Use `d3.json` to fetch the sample data for the plots

    // @TODO: Build a Bubble Chart using the sample data

    // @TODO: Build a Pie Chart
    // HINT: You will need to use slice() to grab the top 10 sample_values,
    // otu_ids, and labels (10 each).
   
}

function init() {
  // Grab a reference to the dropdown select element
  var selector = d3.select("#selDataset");

  // Use the list of sample names to populate the select options
  d3.json("/names").then((sampleNames) => {
    sampleNames.forEach((sample) => {
      selector
        .append("option")
        .text(sample)
        .property("value", sample);
    });

    // Use the first sample from the list to build the initial plots
    const firstSample = sampleNames[0];
    buildCharts(firstSample);
    buildMetadata(firstSample);
    
  });
}

function optionChanged(newSample) {
  // Fetch new data each time a new sample is selected
  buildCharts(newSample);
  buildMetadata(newSample);

}

// Initialize the dashboard
init();
