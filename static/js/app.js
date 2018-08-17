function namesCollector(){
  var selector = document.getElementById('selDataset');
  var url = "/names";
  Plotly.d3.json(url, function(error, successHandle) {
      if (error) return console.warn(error);
      var data = successHandle;
      data.map(function(sample){
          var option = document.createElement('option')
          option.text = sample
          option.value = sample
          selector.appendChild(option)
      });
  });
};
namesCollector();

function optionChanged(sample){
  genPie(sample);
  genBubble(sample);
  genMeta(sample);
};


function genPie(sample) {
  var url = `/samples/${sample}`
  Plotly.d3.json(url,function(error,successHandle){
      if (error) return console.log(error);
      var labels = []
      var values = []
      var hovers = []
      for(i=0; i<10; i++){
          var label = successHandle[0].otu_ids[i];
          labels.push(label);
          var value = successHandle[1].sample_values[i];
          values.push(value);
          var hover = successHandle[2][label - 1];
          hovers.push(hover);
      };
      var trace = {values: values,labels: labels,type: "pie",text: hovers,hoverinfo: "label+text+value+percent",textinfo: "percent"};
      var data = [trace]
      var layout = {
          margin: {l: 10,r: 10,b: 10,t: 10,pad: 4}
      }   
      Plotly.newPlot("pie", data, layout)
  });
};

function genBubble(sample) {
  var url = `/samples/${sample}`
  Plotly.d3.json(url,function(error,successHandle){
      if (error) return console.log(error);
      var otuIDs = successHandle[0].otu_ids;
      var sampleInfo = successHandle[1].sample_values
      var otuInfo = [];
      for(i=0; i<otuIDs.length; i++) {
          otuInfo.push(successHandle[2][otuIDs[i] - 1]);
      };
      var trace = {
          x: otuIDs,
          y: sampleInfo,
          mode: 'markers',
          type: 'scatter',
          marker: {size: sampleInfo,color: otuIDs,colorscale: "Rainbow"},
          text: otuInfo,
        };
      var data = [trace]
      Plotly.newPlot("bubble", data)
  });
};
function genMeta(sample){
  var url = `/metadata/${sample}`
  Plotly.d3.json(url,function(error,successHandle){
      if (error) return console.log(error);
      console.log(successHandle);
      var data = successHandle[0];
      console.log(data)
      var metaList = document.getElementById('sampleMetadata');
      metaList.innerHTML = '';
      var metaElements = [["Sample","SAMPLEID"],["Ethnicity","ETHNICITY"],["Gender","GENDER"],["Age","AGE"],
          ["Weekly Wash Frequency","WFREQ"],["Country","COUNTRY012"]];
      console.log(metaList)
      for(i=0; i<metaElements.length; i++){
          var elementList = document.createElement('li');
          elementList.innerHTML = `${metaElements[i][0]}: ${data[metaElements[i][1]]}`;
          metaList.appendChild(elementList);
      };
  });
};

optionChanged("BB_940"); 










