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
//echo "Connected successfully";
$gpslong = $_POST['gpslong'];
$gpslat = $_POST['gpslat'];




$getIDsql = "SELECT id,iri,gpslong,gpslat, AVG(iri) AS iri FROM `data_r_pi`
WHERE ABS(gpslong - (".$gpslong.")) < 0.0003
GROUP BY gpslong ORDER BY `id` ASC LIMIT 1";
$getID_result = $conn->query($getIDsql);
$ID = $getID_result->fetch_assoc();
$currentID = $ID["id"];
// echo $ID["id"];
$bound = 100;
$upperBound = $currentID +$bound;
$lowerBound = $currentID -$bound;

$sql = "SELECT id,iri,gpslong,gpslat, AVG(iri) AS iri FROM `data_r_pi`
WHERE id>".$lowerBound." AND id<".$upperBound."
GROUP BY gpslong ORDER BY `id` ASC LIMIT 200";


$result = $conn->query($sql);
$nu = $result->num_rows;
$count = 0;
$iri_data = array(200);
if ($result->num_rows > 0) {
    // output data of each row
    while($row = $result->fetch_assoc()) {
        
        $iri_data[$count] = $row["iri"];
        //echo "<br> id: ". $row["id"]. " - iri: ". $row["iri"]. "- gpslong: " . $row["gpslat"] ."- gpslat: ". $row["gpslong"] . "<br>";
        $count ++;
    }
} else {
    echo "0 results";
}

echo json_encode($iri_data);
?>