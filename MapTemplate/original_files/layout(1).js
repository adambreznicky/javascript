 dojo.require("esri.widgets");
 dojo.require("esri.arcgis.utils");


 var map;
 var timeSlider;
 var timeProperties = null;
 var configOptions;

 function initMap(options) {
     configOptions = options;




     //read the legend header text from the localized strings file 
////     dojo.byId('legendHeader').innerHTML = configOptions.i18n.tools.legend.label;

     if (configOptions.bingMapsKey) {
         configOptions.bingmapskey = configOptions.bingMapsKey;
     }


     var itemInfo = configOptions.itemInfo || configOptions.webmap;
     var mapDeferred = esri.arcgis.utils.createMap(configOptions.itemInfo, "map", {
         mapOptions: {
             slider: true,
             sliderStyle: 'small',
             nav: false,
             showAttribution: true,
             wrapAround180: true
         },
         ignorePopups: false,
         bingMapsKey: configOptions.bingmapskey
     });

     mapDeferred.addCallback(function(response) {
         document.title = configOptions.title || response.itemInfo.item.title;
////         dojo.byId("subtitle").innerHTML = configOptions.subtitle || response.itemInfo.item.snippet || "";
		 var t = configOptions.title || response.itemInfo.item.title;

		 dojo.byId("title").innerHTML = "<table style='width:100%; height:100%;'><tr><th id='HeaderDist' align='center' style='width:33%;'></th><th align='center' style='width:33%;'>" 
										+ t + "</th><th id='HeaderCnty' align='center' style='width:33%;'></th></tr></table>"; 

         map = response.map;

         //get any time properties that are set on the map
         if (response.itemInfo.itemData.widgets && response.itemInfo.itemData.widgets.timeSlider) {
             timeProperties = response.itemInfo.itemData.widgets.timeSlider.properties;
         }
         if (map.loaded) {
             initUI(response);
         } else {
             dojo.connect(map, "onLoad", function() {
                 initUI(response);
             });
         }
         //resize the map when the browser resizes
         dojo.connect(dijit.byId('map'), 'resize', map, map.resize);

		/*Handler to updated the District and County name*/
		dojo.connect(map, "onExtentChange", GetLocation);
     });

     mapDeferred.addErrback(function(error) {
         alert(configOptions.i18n.viewer.errors.createMap + " : " + error.message);
     });
 }



 function initUI(response) {

 	/*Sets InitialExtent to the County Boundaries layers.*/
//	InitialExtent = new esri.geometry.Extent
//    ({
//        "xmin": -10885793.51321316,
//        "xmax": -10878455.558497792,
//        "ymin": 3539171.421167662,
//        "ymax": 3547531.7211363413,
//        "spatialReference": { "wkid": 3857 }
//    });
//	map.setExtent(InitialExtent);
	 
	 GetLocation();

	/*Displays current date*/
	var monthNames = [ "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December" ];

	var d = new Date();
    var curr_date = d.getDate();
    var curr_month = monthNames[d.getMonth()];
    var curr_year = d.getFullYear();
	document.getElementById("DateLabel").innerHTML = curr_month + " " + curr_date + ", " + curr_year;

     //add chrome theme for popup
     dojo.addClass(map.infoWindow.domNode, "chrome");
     //add the scalebar 
     var scalebar = new esri.dijit.Scalebar({
		id: "testdiv",
         map: map,
         scalebarUnit: configOptions.i18n.viewer.main.scaleBarUnits //metric or english
     }, ScalebarTD);

	var tw = document.getElementById("FooterTable").rows[0].cells[1].offsetWidth;
	var tw1 = document.getElementById("ha").offsetWidth;
	var tw2 = document.getElementById("ScalebarTD").offsetWidth;
	//alert(tw + " || " + tw1 + " || " + tw2)
	document.getElementById("ScalebarTD").style.left = Math.round(tw / 4) + "px";

     //create the legend - exclude basemaps and any note layers
////     var layerInfo = esri.arcgis.utils.getLegendLayers(response);
////     if (layerInfo.length > 0) {
////         var legendDijit = new esri.dijit.Legend({
////             map: map,
////             layerInfos: layerInfo
////         }, "legendDiv");
////         legendDijit.startup();
////     } else {
////         dojo.byId('legendDiv').innerHTML = configOptions.i18n.tools.legend.layerMessage;
////     }

     //check to see if the web map has any time properties

////     if (timeProperties) {

////         var startTime = timeProperties.startTime;
////         var endTime = timeProperties.endTime;
////         var fullTimeExtent = new esri.TimeExtent(new Date(startTime), new Date(endTime));

////         map.setTimeExtent(fullTimeExtent);
////         //create the slider
////         timeSlider = new esri.dijit.TimeSlider({
////             style: "width: 100%;"
////         }, dojo.byId("timeSliderDiv"));

////         map.setTimeSlider(timeSlider);
////         //Set time slider properties 
////         timeSlider.setThumbCount(timeProperties.thumbCount);
////         timeSlider.setThumbMovingRate(timeProperties.thumbMovingRate);
////         //define the number of stops
////         if (timeProperties.numberOfStops) {
////             timeSlider.createTimeStopsByCount(fullTimeExtent, timeProperties.numberOfStops);
////         } else {
////             timeSlider.createTimeStopsByTimeInterval(fullTimeExtent, timeProperties.timeStopInterval.interval, timeProperties.timeStopInterval.units);
////         }
////         //set the thumb index values if the count = 2
////         if (timeSlider.thumbCount == 2) {
////             timeSlider.setThumbIndexes([0, 1]);
////         }


////         dojo.connect(timeSlider, 'onTimeExtentChange', updateTimeSliderTitle);

////         timeSlider.startup();
////     }
 }
////function updateTimeSliderTitle(timeExtent) {
////    var slider = this;
////    var start = null,
////        end = null;

////    if (!timeExtent) {
////        // startup
////        if (slider.thumbCount == 2) {
////            start = slider.timeStops[0];
////            end = slider.timeStops[1];
////        } else {
////            start = slider.timeStops[0];
////        }
////    } else {
////        start = timeExtent.startTime;
////        if ((timeExtent.endTime.getTime() - timeExtent.startTime.getTime()) > 0) {
////            end = timeExtent.endTime;
////        }
////    }

////    var startDatePattern = null;
////    var endDatePattern = null;
////    var startTimePattern = null;
////    var endTimePattern = null;
////    if (end && start.getFullYear() == end.getFullYear()) {
////        if (start.getMonth() == end.getMonth()) {
////            if (start.getDate() == end.getDate()) {
////                if (start.getHours() == end.getHours()) {
////                    if (start.getMinutes() == end.getMinutes()) {
////                        if (start.getSeconds() == end.getSeconds()) {
////                            // same second
////                            startDatePattern = configOptions.i18n.tools.time.datePattern;
////                            startTimePattern = configOptions.i18n.tools.time.millisecondTimePattern;
////                            endTimePattern = configOptions.i18n.tools.time.millisecondTimePattern;
////                        } else { // same minute
////                            startDatePattern = configOptions.i18n.tools.time.datePattern;
////                            startTimePattern = configOptions.i18n.tools.time.secondTimePattern;
////                            endTimePattern = configOptions.i18n.tools.time.secondTimePattern;
////                        }
////                    } else { // same hour
////                        startDatePattern = configOptions.i18n.tools.time.datePattern;
////                        startTimePattern = configOptions.i18n.tools.time.minuteTimePattern;
////                        endTimePattern = configOptions.i18n.tools.time.minuteTimePattern;
////                    }
////                } else { // same day
////                    startDatePattern = configOptions.i18n.tools.time.datePattern;
////                    startTimePattern = configOptions.i18n.tools.time.hourTimePattern;
////                    endTimePattern = configOptions.i18n.tools.time.hourTimePattern;
////                }
////            } else { // same month
////                if (end.getDate() - start.getDate() < 2) {
////                    // less than 2 days
////                    startDatePattern = configOptions.i18n.tools.time.datePattern;
////                    startTimePattern = configOptions.i18n.tools.time.hourTimePattern;
////                    endDatePattern = configOptions.i18n.tools.time.datePattern;
////                    endTimePattern = configOptions.i18n.tools.time.hourTimePattern;
////                } else {
////                    startDatePattern = configOptions.i18n.tools.time.datePattern;
////                    endDatePattern = configOptions.i18n.tools.time.datePattern;
////                }
////            }
////        } else { // same year
////            startDatePattern = configOptions.i18n.tools.time.datePattern;
////            endDatePattern = configOptions.i18n.tools.time.datePattern;
////        }
////    } else if (end && end.getFullYear() - start.getFullYear() > 2) {
////        startDatePattern = configOptions.i18n.tools.time.yearPattern;
////        endDatePattern = configOptions.i18n.tools.time.yearPattern;
////    } else {
////        startDatePattern = configOptions.i18n.tools.time.datePattern;
////        endDatePattern = configOptions.i18n.tools.time.datePattern;
////    }

////    var startTime = dojo.date.locale.format(start, {
////        datePattern: startDatePattern,
////        timePattern: startTimePattern,
////        selector: (startDatePattern && startTimePattern) ? null : (startDatePattern ? "date" : "time")
////    });
////    var endTime = null;
////    if (end) {
////        endTime = dojo.date.locale.format(end, {
////            datePattern: endDatePattern,
////            timePattern: endTimePattern,
////            selector: (endDatePattern && endTimePattern) ? null : (endDatePattern ? "date" : "time")
////        });
////    }

////    var info;
////    if (end) {
////        info = dojo.string.substitute(configOptions.i18n.tools.time.timeRange, {
////            start_time: startTime,
////            end_time: endTime
////        });
////    } else {
////        info = "" + startTime;
////    }
////    dojo.byId("timeSliderLabel").innerHTML = info;

////}

 function formatDate(date, datePattern) {
     return dojo.date.locale.format(date, {
         selector: 'date',
         datePattern: datePattern
     });
 }


 /*Gets the District and County*/
 function GetLocation()
 {
	var Location_QueryTask = new esri.tasks.QueryTask("https://maps.dot.state.tx.us/ArcGIS/rest/services/Boundaries_Simple/MapServer/1");
    var Location_Query = new esri.tasks.Query();
    Location_Query.returnGeometry = false;
    Location_Query.outFields = ["CNTY_NM", "DIST_NBR"];

    Location_Query.geometry = map.extent.getCenter();

	Location_Query.where = "1=1";
    Location_QueryTask.execute(Location_Query, Location_Success, Location_Failed)
 }

 function Location_Success(e)
 {
	var DistNm;
	switch (e.features[0].attributes.DIST_NBR)
	{
		case 1:
			DistNm = "Paris";
			break;
		case 2: 
			DistNm = "Fort Worth";
			break;
		case 3:
			DistNm = "Wichita Falls";
			break;
		case 4: 
			DistNm = "Amarillo";
			break;
		case 5: 
			DistNm = "Lubbock";
			break;
		case 6: 
			DistNm = "Odessa";
			break;
		case 7: 
			DistNm = "San Angelo";
			break;
		case 8: 
			DistNm = "Abilene";
			break;
		case 9: 
			DistNm = "Waco";
			break;
		case 10: 
			DistNm = "Tyler";
			break;
		case 11: 
			DistNm = "Lufkin";
			break;
		case 12: 
			DistNm = "Houston";
			break;
		case 13: 
			DistNm = "Yoakum";
			break;
		case 14: 
			DistNm = "Austin";
			break;
		case 15:
			DistNm = "San Antonio";
			break;
		case 16:
			DistNm = "Corpus Christi";
			break;
		case 17:
			DistNm = "Bryan";
			break;
		case 18:
			DistNm = "Dallas";
			break;
		case 19:
			DistNm = "Atlanta";
			break;
		case 20:
			DistNm = "Beaumont";
			break;
		case 21:
			DistNm = "Pharr";
			break;
		case 22: 
			DistNm = "Laredo";
			break;
		case 23:
			DistNm = "Brownwood";
			break;
		case 24:
			DistNm = "El Paso";
			break;
		case 25:
			DistNm = "Childress";
			break;
	}

	document.getElementById("HeaderDist").innerHTML = DistNm + " District";
	document.getElementById("HeaderCnty").innerHTML = e.features[0].attributes.CNTY_NM + " County";
 }


 function Location_Failed(e)
 {
	document.getElementById("HeaderDist").innerHTML = "";
	document.getElementById("HeaderCnty").innerHTML = "";
	alert("Please keep the center of map within the bounds of Texas.");
	return;
 }