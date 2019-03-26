$(document).ready(function(){
    $(".img_button").click(function(){
        var point = turf.point([-90.548630, 14.616599]);
        var buffered = turf.buffer(point, 500, {units: 'miles'});
        
        console.log(buffered);
        map.addLayer(buffered);
        if (this.innerHTML == 'Processed Image')
        {
            this.style.backgroundColor = "red";
            this.innerHTML = 'Original Image';
        }
       else if(this.innerHTML == 'Original Image')
       {
           this.style.backgroundColor = "#4CAF50";
           this.innerHTML = 'Processed Image';
       }
       
       var dataArray = [0.34, 0.12, 0.75,1,0.1,0.58,0.453,0.235, 0.19, 0.3,0.20,0.1];
       var lableArray = ["Red", "Blue", "Yellow", "Green", "Purple", "Orange","Red", "Blue", "Yellow", "Green", "Purple", "Orange"];
       myFunction(dataArray,lableArray);




    });
  });
  var json = "blue";

  map.on('load', function() {
    map.addLayer({
        'id': 'room-extrusion',
        'type': 'fill-extrusion',
        'source': {
        // GeoJSON Data source used in vector tiles, documented at
        // https://gist.github.com/ryanbaumann/a7d970386ce59d11c16278b90dde094d
        'type': 'geojson',
        'data': 'http://roadquality.ca/GEOjson/albert2.json'
        },
        'paint': {
        // See the Mapbox Style Specification for details on data expressions.
        // https://docs.mapbox.com/mapbox-gl-js/style-spec/#expressions
         
        // Get the fill-extrusion-color from the source 'color' property.
        'fill-extrusion-color': ['get', 'color'],
         
        // Get fill-extrusion-height from the source 'height' property.
        'fill-extrusion-height': ['get', 'height'],
         
        // Get fill-extrusion-base from the source 'base_height' property.
        'fill-extrusion-base': ['get', 'base_height'],
         
        
        }
        });
    map.on('click', 'room-extrusion', function (e) {
            var t = e.lngLat;
            var x = t.toString();
            var clean = x.replace('LngLat(','');
            var coordinates = (clean.replace(')','')).split(",");
            var gpslong = coordinates[0].trim();
            var gpslat = coordinates[1].trim();
            var label = new Array(200);
            var size = 200;
            var label = new Array(200);
            var count = -100;
            
            for (var i = 0;i<size;i++)
             {                  
                 label[i] = count.toString();
                 count ++;
                 
            }
            $.post("graph.php",
            {
                gpslong: gpslong ,
                gpslat: gpslat
            },
            function(data, status){
            var custom_dataArray = JSON.parse(data);
                               /* alert(label); */
            $("canvas#myChart").remove();
             $("div.graph").append('<canvas class = "iriGraph" id="myChart" ></canvas>');
              
                myFunction(custom_dataArray,label);
                //alert("Data: " + data + "\nStatus: " + status);
                
            });
            




                /* new mapboxgl.Popup()
                .setLngLat(e.lngLat)
                .setHTML(e.lngLat)
                .addTo(map);*/
                }); 
        });
var dataArray = [0.34, 0.12, 0.75,1,0.1,0.58,0.453,0.235, 0.19, 0.3,0.20,1];
var lableArray = ["Red", "Blue", "Yellow", "Green", "Purple", "0","Red", "Blue", "Yellow", "Green", "Purple", "Orange"];

function myFunction(dataArray_p,lableArray_p) {

    var ctx = document.getElementById("myChart").getContext('2d');
var myChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: lableArray_p,
        datasets: [{
            label: '# of Votes',
            data: dataArray_p,
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(153, 102, 255, 0.2)',
                'rgba(255, 159, 64, 0.2)'
            ],
            borderColor: [
                'rgba(255,99,132,1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)'
            ],
            borderWidth: 1
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero:true
                }
            }]
        }
    }
});
  }
var ctx = document.getElementById("myChart").getContext('2d');
var myChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: lableArray,
        datasets: [{
            label: '# of Votes',
            data: dataArray,
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(153, 102, 255, 0.2)',
                'rgba(255, 159, 64, 0.2)'
            ],
            borderColor: [
                'rgba(255,99,132,1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)'
            ],
            borderWidth: 1
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero:true
                }
            }]
        }
    }
});