<?php
$servername = "localhost";
$username = "roadqual_admin";
$password = "admin";
$dbname = "roadqual_capstone";

//set the filename
$filename = 'GEOjson/albert.json';
//open or create the file
$handle = fopen($filename,'w+');



// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
} 
echo "Connected successfully";


$count = 0;
$current = array(0.0,0.0 ,0.0 ,0.0);
$temp1 = array(0.0,0.0 ,0.0 ,0.0);
$center = array(0.0,0.0 ,0.0 ,0.0);
$sidePoint_1 = array(0.0,0.0);
$sidePoint_2 = array(0.0,0.0); 
$sidePoint_3 = array(0.0,0.0);
$sidePoint_4 = array(0.0,0.0); 
function degToRad ($x) {
  return $x * (pi() / 180);
}
 function radToDeg ($x) {
  return (180 * $x) / pi();
}

  function getBoundingBox($centerPoint, $distance) {
    $MIN_LAT;$MAX_LAT; $MIN_LON; $MAX_LON; $R; $radDist; $degLat; $degLon; $radLat; $radLon; $minLat; $maxLat; $minLon; $maxLon; $deltaLon;
  
  if ($distance < 0) {
    echo "Illegal arguments";
  }
// coordinate limits
$MIN_LAT = degToRad(-90);
$MAX_LAT = degToRad(90);
$MIN_LON = degToRad(-180);
$MAX_LON = degToRad(180);

  // Earth's radius (km)
  $R = 6378.1;
  // angular distance in radians on a great circle
  $radDist = $distance / $R;
  // center point coordinates (deg)
  $degLat = $centerPoint[0];
  $degLon = $centerPoint[1];
  // center point coordinates (rad)
  $radLat = degToRad($degLat);
  $radLon = degToRad($degLon);
  // minimum and maximum latitudes for given distance
  $minLat = $radLat - $radDist;
  $maxLat = $radLat + $radDist;
  // minimum and maximum longitudes for given distance
  $minLon =  0;
  $maxLon =  0;

  // define deltaLon to help determine min and max longitudes
  $deltaLon = asin(sin($radDist) / cos($radLat));
  if ($minLat > $MIN_LAT && $maxLat < $MAX_LAT) {
    $minLon = $radLon - $deltaLon;
    $maxLon = $radLon + $deltaLon;
    if ($minLon < $MIN_LON) {
      $minLon = $minLon + 2 * M_PI;
    }
    if ($maxLon > $MAX_LON) {
      $maxLon = $maxLon - 2 * M_PI;
    }
  }
  // a pole is within the given distance
  else {
    $minLat = max($minLat, $MIN_LAT);
    $maxLat = min($maxLat, $MAX_LAT);
    $minLon = $MIN_LON;
    $maxLon = $MAX_LON;
  }
  $finalGPS = [radToDeg($minLon),radToDeg($maxLat),
               radToDeg($minLon),radToDeg($minLat),   
               radToDeg($maxLon),radToDeg($minLat),
               radToDeg($maxLon),radToDeg($maxLat),
               radToDeg($minLon),radToDeg($maxLat)];
  return $finalGPS;
  
}

$sidePoint_custom = getBoundingBox( $temp1,0.009);
echo "sidePoint_1 Custom Function: ".$sidePoint_custom[0].", ".strval($sidePoint_custom[1])."<br>";
echo "sidePoint_2 Custom Function: ".$sidePoint_custom[2].", ".strval($sidePoint_custom[3])."<br>";
echo "sidePoint_3 Custom Function: ".$sidePoint_custom[4].", ".strval($sidePoint_custom[5])."<br>";
echo "sidePoint_4 Custom Function: ".$sidePoint_custom[6].", ".strval($sidePoint_custom[7])."<br>";
echo "sidePoint_4 Custom Function_loop: ".$sidePoint_custom[8].", ".strval($sidePoint_custom[9])."<br>";
fwrite($handle,"  {
           \"features\": [");
//echo "<br> id: ". $row["id"]. " - iri: ". $row["iri"]. "- gpslong: " . $row["gpslong"] ."- gpslat: ". $row["gpslat"] . "<br>";
$sql = "SELECT id,iri,gpslong,gpslat, AVG(iri) AS iri FROM `data_r_pi` GROUP BY gpslong ORDER BY `id` ASC ";
$result = $conn->query($sql);

if ($result->num_rows > 0) {
    // output data of each row
    while($row = $result->fetch_assoc()) {
      $current[0] = $row["gpslat"];
      $current[1] = $row["gpslong"];
      $current[2] = $row["iri"];
      $current[3] = $row["id"];
      $sidePoint_custom = getBoundingBox( $current,0.009);
      $height =0;
      $color ="";
      if ($current[2]>0 && $current[2]<1.5)
      {
        $height =300;
        $color ="blue";
      }
      else if($current[2]>1.5 && $current[2]<3)
      {
        $height =400;
        $color ="royalblue";
      }
      else if($current[2]>3 && $current[2]<4.5)
      {
        $height =500;
        $color ="cyan";
      }
      else if($current[2]>4.5 && $current[2]<6)
      {
        $height =600;
        $color ="lime";
      }
      else if($current[2]>6 && $current[2]<7.5)
      {
        $height =700;
        $color ="yellow";
      }
      else if($current[2]>7.5)
      {
        $height =800;
        $color ="red";
      }
      fwrite($handle,"
      {
        \"type\": \"Feature\",
        \"properties\": {
        
          \"level\": 1,
          \"name\": \"Bird Exhibit\",
          \"height\":" .$height.",
          \"base_height\": 0,
          \"color\": \"".$color."\"
        },
        \"geometry\": {
            \"coordinates\": [
                [
                  ["
                  .$sidePoint_custom[0].","
                  .$sidePoint_custom[1].
                  "],
                  ["
                  .$sidePoint_custom[2].","
                  .$sidePoint_custom[3].
                  "],
                  ["
                  .$sidePoint_custom[4].","
                  .$sidePoint_custom[5].
                  "],
                  ["
                  .$sidePoint_custom[6].","
                  .$sidePoint_custom[7].
                  "],
                  ["
                  .$sidePoint_custom[8].","
                  .$sidePoint_custom[9].
                  "]
                ]
              ],
              \"type\": \"Polygon\"
        },
        \"id\": \"06e8fa0b3f851e3ae0e1da5fc17e111w\"
  },
  ");
      echo "<br> id: ". $row["id"]. " - iri: ". $row["iri"]. "- gpslong: " . $row["gpslat"] ."- gpslat: ". $row["gpslong"] . "<br>";

    }
} else {
    echo "0 results";
}
fwrite($handle,"  ],
              \"type\": \"FeatureCollection\"
      }");
















fwrite($handle,"\n");

//close the file
fclose($handle);
$conn->close();




?>