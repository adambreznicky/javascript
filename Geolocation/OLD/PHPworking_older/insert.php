<?php

// Add to Javascript
// xmlhttp.open("POST","coord_post.php",true);
// xmlhttp.send();


$con=sqlsrv_connect("example.com","peter","abc123","my_db");
// Check connection
if (sqlsrv_connect_errno())
  {
  echo "Failed to connect to SQLServer: " . sqlsrv_connect_error();
  }


$sql="INSERT INTO Persons (FirstName, LastName, Age)
VALUES
// Replace the following with the name= variable in html
('$_POST[firstname]','$_POST[lastname]','$_POST[age]')";

if (!sqlsrv_query($con,$sql))
  {
  die('Error: ' . sqlsrv_error($con));
  }
echo "1 record added";

sqlsrv_close($con);
?>