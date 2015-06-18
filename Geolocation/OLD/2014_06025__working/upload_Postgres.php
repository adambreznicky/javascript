<?php
//http://www.bostongis.com/postgis_geomfromtext.snippet
//http://postgis.net/docs/ST_GeomFromGeoJSON.html
//http://blog.cnizz.com/2008/03/13/pass-object-array-php-javascript-json/


// Add to Javascript
// xmlhttp.open("POST","coord_post.php",true);
// xmlhttp.send();

$con=pg_connect("host=mypostgres.ceiqkhgminol.us-west-2.rds.amazonaws.com port=5432 dbname=postgres user=adam password=test")
	or die('Could not connect: ' . pg_last_error());
	
// Check connection
// if (sqlsrv_connect_errno())
  // {
  // echo "Failed to connect to SQLServer: " . sqlsrv_connect_error();
  // }
  
$aRequest = file_get_contents('php://input');
$container = json_decode($aRequest);
$counter = 0;
$Psql="INSERT INTO geopoints VALUES ";
$Lsql="INSERT INTO geolines VALUES ";
$Ptrigger = 0;
$Ltrigger = 0;
foreach($container as &$item){
	$splitter = json_decode($item);
	$counter += 1;
	foreach ($splitter as &$value){
		if ($value == NULL){
		$value = "NULL";
		}
	}
	
	//$sql="INSERT INTO geolocation VALUES ('".$splitter[0]."','".$splitter[1]."','".$splitter[2]."','".$splitter[3]."','".$splitter[4]."','".$splitter[5]."','".$splitter[6]."',".$splitter[7].",".$splitter[8].",".$splitter[9].",".$splitter[10].",".$splitter[11].",".$splitter[12].",".$splitter[13].",".$splitter[14].",".$splitter[15].",".$splitter[16].",".$splitter[17].");";
	if($splitter[0]=="POINT"){
			$Ptrigger = 1;
			if($splitter[15]=="NULL"){
			$splitter[15] = "";
			}
			if($splitter[14]=="NULL"){
			$splitter[14] = "";
			}
			if($splitter[13]=="NULL"){
			$splitter[13] = "";
			}
	$Psql .= "('".$splitter[0]."','".$splitter[1]."','".$splitter[2]."','".$splitter[3]."','".$splitter[4]."','".$splitter[5]."',".$splitter[6].",".$splitter[7].",".$splitter[8].",".$splitter[9].",".$splitter[10].",".$splitter[11].",".$splitter[12].",'".$splitter[13]."','".$splitter[14]."','".$splitter[15]."','".$splitter[16]."','".$splitter[17]."',ST_SetSRID(ST_GeomFromGeoJSON('{\"type\":\"Point\",\"coordinates\":".$splitter[18]."}'), 4326)),";
	}
	else{
			$Ltrigger = 1;
			if($splitter[25]=="NULL"){
			$splitter[25] = "";
			}
			if($splitter[24]=="NULL"){
			$splitter[24] = "";
			}
	$Lsql .= "('".$splitter[0]."','".$splitter[1]."','".$splitter[2]."','".$splitter[3]."','".$splitter[4]."','".$splitter[5]."',".$splitter[6].",".$splitter[7].",".$splitter[8].",".$splitter[9].",".$splitter[10].",".$splitter[11].",".$splitter[12].",".$splitter[13].",".$splitter[14].",".$splitter[15].",".$splitter[16].",".$splitter[17].",".$splitter[18].",".$splitter[19].",".$splitter[20].",".$splitter[21].",".$splitter[22].",".$splitter[23].",'".$splitter[24]."','".$splitter[25]."','".$splitter[26]."','".$splitter[27]."',ST_SetSRID(ST_GeomFromGeoJSON('{\"type\":\"LineString\",\"coordinates\":".$splitter[28]."}'), 4326)),";
	}
}

$Psql = rtrim($Psql, ",");
$Psql .= "; ";
$Lsql = rtrim($Lsql, ",");
$Lsql .= "; ";


if ($Ptrigger==1 and $Ltrigger==0){
	$sql= $Psql."UPDATE \"geopoints\" SET \"TXSMS\"=ST_TRANSFORM(\"WGS84\", 3081);";
}
else if($Ptrigger==0 and $Ltrigger==1){
	$sql = $Lsql."UPDATE \"geolines\" SET \"TXSMS\"=ST_TRANSFORM(\"WGS84\", 3081);";
}
else{
$sql = $Psql.$Lsql."UPDATE \"geopoints\" SET \"TXSMS\"=ST_TRANSFORM(\"WGS84\", 3081); UPDATE \"geolines\" SET \"TXSMS\"=ST_TRANSFORM(\"WGS84\", 3081);";
}


if (!pg_query($con,$sql)){
	die('Error: ' . pg_error($con));
}


echo "Upload Complete: ".$counter." records added.";


pg_close($con);
?>