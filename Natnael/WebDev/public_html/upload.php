<?php
$servername = "localhost";
$username = "roadqual_admin";
$password = "admin";
$dbname = "roadqual_capstone";

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
} 
echo "Connected successfully";
// enter  data
$sql = "INSERT INTO `data_r_pi`( originalImage, processedImage, iri, gpslat, gpslog, dateRecorded) 
VALUES ('image.jpg','image_p.jpg','3','45654.67','45654.67','2019-02-24')";

if ($conn->query($sql) === TRUE) {
    echo "New record created successfully";
} else {
    echo "Error: " . $sql . "<br>" . $conn->error;
}

$conn->close();




?>