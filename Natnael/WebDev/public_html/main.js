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
        'data': 
        {
            "features": [
              {
                "type": "Feature",
                "properties": {
                
                  "level": 1,
                  "name": "Bird Exhibit",
                  "height": 500,
                  "base_height": 0,
                  "color": "red"
                },
                "geometry": {
                    "coordinates":  [
                        [
                          [
                            -104.61800398736341,
                            50.44716596077606
                          ],
                          [
                            -104.61800398736341,
                            50.44707031253935
                          ],
                          [
                            -104.61722078233106,
                            50.447060064502516
                          ],
                          [
                            -104.617210053495,
                            50.44716596077606
                          ],
                          [
                            -104.61800398736341,
                            50.44716596077606
                          ]
                        ]
                      ],
                      "type": "Polygon"
                },
                "id": "06e8fa0b3f851e3ae0e1da5fc17e111e"
              },
              {
                "type": "Feature",
                "properties": {
                
                  "level": 1,
                  "name": "Bird Exhibit",
                  "height": 300,
                  "base_height": 0,
                  "color": "blue"
                },
                "geometry": {
                    "coordinates": [
                        [
                          [
                            -104.617210053495,
                            50.44716596077606
                          ],
                          [
                            -104.61723151116712,
                            50.447060064502516
                          ],
                          [
                            -104.61615862756116,
                            50.447049816463476
                          ],
                          [
                            -104.61615862756116,
                            50.44716596077606
                          ],
                          [
                            -104.617210053495,
                            50.44716596077606
                          ]
                        ]
                      ],
                      "type": "Polygon"
                },
                "id": "06e8fa0b3f851e3ae0e1da5fc17e111w"
              }
            ],
            "type": "FeatureCollection"
          }

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
            new mapboxgl.Popup()
            .setLngLat(e.lngLat)
            .setHTML(e.lngLat)
            .addTo(map);
            });
    map.addLayer({
    'id': 'lines',
    'type': 'line',
    'source': {
    'type': 'geojson',
    'data': {
        "type": "FeatureCollection",
        "features": [
          {
            "type": "Feature",
            "geometry": {
              "type": "LineString",
              "coordinates": [
                [
                  -104.61821106816069,
                  50.47148367980349
                ],
                [
                  -104.61821106816069,
                  50.450775139153386
                ]
              ]
            },
            "properties": {
                "line-width" :5,
                "color":json
            }
          }
        ]
      }
    },
    'paint': {
        'line-width': 3,
        // Use a get expression (https://docs.mapbox.com/mapbox-gl-js/style-spec/#expressions-get)
        // to set the line-color to a feature property value.
        'line-color': ['get', 'color']
        }
    });
    });