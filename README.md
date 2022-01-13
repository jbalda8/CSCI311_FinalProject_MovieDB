# **** Watch videos for Demo ****

# Objective
The objective of this project was to implement an application which required communication between a front-end application (Python) and a back-end DBMS (PL/SQL). In this project, I implemented a Movie Rental System (MRS) using c1_MMcreate database. The MRS contains a catalog of movies that can be managed, viewed, and rented out.  The MRS also contains a catalog of members and their payment options that can be managed and viewed.

# Component Details: 
The Movie Rental System (MRS) has three main components a) the movie catalog management 
component; b) member catalog management component; c) movie catalog viewing and renting 
component; 
 
Movie Catalog Management Component 
The movie catalog management component should avail an admin user with the following 
functionalities: 
1. Ability to view, add, update, and delete movie from the catalog.  
2. Ability to login to the system as admin role. The system would just have a predefined set 
of username and password which allow them to login as an admin. 
Member Catalog Management Component 
The member catalog management component should avail an admin user with the following 
functionalities: 
1. Ability to view, add, update, and delete member from the catalog. Ability to update 
members’ payment information. 
2. Send members notice for overdue movies.  
3. Ability to login to the system as admin role. The system would just have a predefined set 
of user name and password which allow them to login as an admin. 
 
Movie Catalog Viewing and Renting Component 
The movie catalog viewing and renting component allows to members only to perform the 
following: 
1. Search and view for movie. Searching capabilities could be limit to the title (or other 
fields) of the movie. 
2. Rent new movies. 
3. Return movies. 
 
Implementation Details 
Command line Menu: 
Main Menu: 
1) Admin 
2) Member 
3) Exit 
 
 
User could select an option from this list. If user select 1, it should display Admin Menu with the 
following options: 
 
Admin Menu: 
1) Add new movie (including movie type) 
2) Add new member (including payment option) 
3) Search and update movie 
4) Search and delete movie 
5) Search and update member 
6) Search and delete member 
Implements these options for admin personnel. 
 
In main menu, if user select 2 from the Main Menu it should display member menu. Member 
menu should contain the following options: 
Member Menu: 
1) Search movie 
2) Rent movie (this should fire a trigger automatically to update the inventory) 
3) Return movie (this should fire a trigger automatically to update the inventory) 
Your application should also fire a trigger automatically to notify user if there is any overdue.
