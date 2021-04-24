# Parks
Wikiloc 
GeFLTrailLinks.py finds links to to trails in the state of Florida for various activities by scrolling though search page results and writes the links to a CSV file.
The links are used in the trail-scraper program to extract trail data.  This program requires a Wikiloc account username and password.

trail_scraper.py originally written by Roi Weinberger & Sagiv Yaari -- Nov 2019 - ITC data science project, was modified to read trail links obtained from GetFLtrailsLinks.py 
and extract trail data.

MapMyFitness
MMFParks.py is a modification of a previous program written for the AppCompare project which uses MMF API's "close_to_location" option to extract trail data in a radius about 
the centroid of all FL State Parks.
Input requires a CSV file with the lat/lon/buffer of areas of interest (in this case State Parks found in State_Park_Coordinates.csv) and a MapMyFitness API key and secret. 

AllTrails
Searches AllTrails for trails in Florida State Parks then subsequently extracts the trail data and writes results to a CSV file.
