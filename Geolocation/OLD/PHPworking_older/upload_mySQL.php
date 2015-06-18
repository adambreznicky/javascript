<?php

// Add to Javascript
// xmlhttp.open("POST","coord_post.php",true);
// xmlhttp.send();


// Create connection
$con=mysqli_connect("sql306.byethost7.com","b7_13340779","Hendrix9","b7_13340779_geolocation");

// Check connection
if (mysqli_connect_errno())
  {
  echo "Failed to connect to MySQL: " . mysqli_connect_error();
  }


$sql="INSERT INTO geolocation_data (RTE_ID, SPD)
VALUES ('200AA5757', 52.52)";
//('$_POST[firstname]','$_POST[lastname]','$_POST[age]')";
// Replace the above with the name= variable in html


if (!mysqli_query($con,$sql))
  {
  die('Error: ' . mysqli_error($con));
  }
echo "1 record added";

mysqli_close($con);
?>