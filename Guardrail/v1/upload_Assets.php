<?php
//http://www.bostongis.com/postgis_geomfromtext.snippet
//http://postgis.net/docs/ST_GeomFromGeoJSON.html
//http://blog.cnizz.com/2008/03/13/pass-object-array-php-javascript-json/


// Add to Javascript
// xmlhttp.open("POST","coord_post.php",true);
// xmlhttp.send();

$con=pg_connect("host=stevie.heliohost.org port=5432 dbname=smudge_assets user=smudge_adam password=05M-w}J$.;F[")
	or die('Could not connect: ' . pg_last_error());
	
// Check connection
// if (sqlsrv_connect_errno())
  // {
  // echo "Failed to connect to SQLServer: " . sqlsrv_connect_error();
  // }
  
$aRequest = file_get_contents('php://input');
$container = json_decode($aRequest);
$counter = 0;
$Psql="INSERT INTO \"Guardrails\" VALUES ";
foreach($container as &$item){
	$splitter = json_decode($item);
	$counter += 1;
	foreach ($splitter as &$value){
		if ($value == NULL){
		$value = "NULL";
		}
        }
	$Psql .= "('".$splitter[0]."','".$splitter[1]."','".$splitter[2]."','".$splitter[3]."','".$splitter[4]."','".$splitter[5]."',".$splitter[6].",".$splitter[7].",".$splitter[8].",".$splitter[9].",".$splitter[10].",".$splitter[11]."),";
}

$Psql = rtrim($Psql, ",");
$Psql .= "; ";


if (!pg_query($con,$Psql)){
	die($Psql);
}


echo "Upload Complete: ".$counter." records added.";


pg_close($con);
?>