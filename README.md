# covidmetrics

###An Overview of the COVIDMetrics Dashboard Platform for Schools

https://il.covidmetrics.bsmartin.info/

The COVIDMetrics Dashboard Platform (CMDP) is a simple tool designed to provide school districts and schools with a way to manage and share information related to their COVID operation and preparedness with their staff, faculty, administration, and the general public.  

The tool is broken down into 5 key areas of information, each presented with snapshots related to the districts defined thresholds and status.  The snapshots themselves are meant to be simple to understand and interpret, but they are also not meant to be rules for policy or execution.  Instead, they are meant to be informational in nature to help guide administrative decision making.

###Snapshot Areas

+ Regional Geographic Status - This section represents the state of disease through positivity testing rates, incidence rates, and other metrics as defined by the Illinois Department of Public Health and county health departments.  Districts can choose to include individual metrics in their snapshot status as well as define appropriate threshold and duration values for the metrics as they choose to or as directed by prevailing authorities/guidance.  All of the data presented is loaded directly from the prevailing authority without manual modification or adjustment.
+ Facility PPE Inventories - This section presents information on the types and quantities of PPE being maintained at each facility in the district.  Tools allow district wide purchasing and facilities management to update inventories at all facilities in the district.  Other tools allow individual facility administrators to also update the inventories for their schools.  Consumption trends over 7 and 14 day periods are used to predictively indicate whether the district or facilities are at risk of running out of supplies of PPE materials.
+ Facility Space - This section presents information on the number of student desks in each type of room in the facilities that are available for students as well as the demand/need for those desks by facility.  Tools allow the district administration and individual facility administrators to update enrollment numbers and assign demand for desks to the types of rooms available.  
+ Facility Staffing - This section presents information on the number and type of human resources necessary to operate the district facilities.  Tools in this section allow district and facility administrators to update the number of each type of resource that is required to support the facility operation as well as report on the number of each of those resources that are actually available.  The frequency of update for this data is dependent on district or facility administrators to update as the data changes.
+ Transportation - This section presents information on the number and type of bus routes/groups and the availability and demand for seats within those bus routes/groups.  Tools in this section allow district and facility administrators the ability to update and assign demand to different bus groups.

###Setup

In order to setup a district, a district administrator user must first signup for the site and indicate which district they are signing up for.  To signup, visit https://il.covidmetrics.bsmartin.info/signup

Once they have signed up, the superintendent for the district will need to send an email to ilcovidmetrics@bsmartin.info with the district name and the email address of the user who signed up to have them assigned as the district administrator.

After a district administrator has been assigned, other users may signup at the same form and the district administrator will be able to assign those individuals roles/permissions/facilities.

###Future Enhancements

+ Graphs/visualizations - I will be adding some visualizations to provide trending and context on various metrics in the snapshots
+ Integrations - I will be adding the ability for districts to call API endpoints through integrations with other existing staffing, inventory, or district management platforms.  However, the work of actually integrating would be up to the district to pursue independently.
+ Embedding - I will be providing the ability for districts to embed the snapshots in their own web presence platforms if capable/desired.
+ Additional Metrics - I will support adding additional metrics as much as possible based on effort and demand.

###Support

This is a best effort project done in my spare time, you get the picture.

###Source Code

The source code is freely available for use and modification. 
