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


$sql = "SELECT * FROM data_r_pi" ;
$result = $conn->query($sql);

    while($rows=mysqli_fetch_assoc($result))
{

   $image = $rows['gpslog'];    
    print $image;



}

$conn->close();

?>