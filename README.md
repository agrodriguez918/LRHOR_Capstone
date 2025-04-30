# LRHOR_Capstone
Florida Polytechnic's LRH OR Capstone Team Project

Lakeland Regional Health has asked us to create them a functioning dashboard that works in real-time within their Operating Rooms throughout the hospital. It must account real-time information including operation information and cleanup/transition. The aim is to have it a 30-minute turnaround time for 80%+ of their weekly cases. It must function properly with current implemented applications used. This Github repository contains our solution to this problem. The branch schema for the repository as well as their deliverables are included below. 


# Branch Schema : 

Cerner - interface information/guide, all code required for FHIR interface  <br>
*includes test script

Dashboard - dashboard information/guide, stores finalized iteration of Tableau workbook  <br>
*includes test dummy database 

# How to Run the Sever (local):
<br>
I recommend having a static ip for the database and you can host on a secure port to provide more security. <br>
Also FLASK is setup in the code, switch to FHIR of course would provide more security options and follow hospital data standards. <br>
<br>
Step 1: Download files. <br>
<br>
Step 2: Open the index.html and change the Ip address (line 43)  "fetch("http://<IP-OF-HOST>:5000/metrics")" change the Ip to the Ip of the system that will run the sever (Hint when you run system_monitor.py it shows the Ip its running on). <br>
<br>
Step 3: Now open up two CMD (Command Propmts) In the first one run the command "python system_monitor.py" this will start the WDC (Web data collecter needed for Tableau). <br>
<br>
Step 4: In the other CMD use the command "python3 -m http.server 8000" this will allow us to connect through the internet. WARANING this will run it on port 80 which is open, using other ports or hospital only ports can make this secure. (Still recommend switching to FHIR). <br>
<br>
Step 5: In Tableau Go to: Data -> New Data Source -> To a Server -> Web Data Connector. Then add in the url to connect to the WDC "http://<IP-OF-HOST>:8000/index.html" <br>
<br>
Step 6: Once its all connected it should populate the tables.Also I recommend refreshing the data on the dashboard as we had crashes when doing it in the table view. <br>
<br>
