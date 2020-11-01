# Support Ticketing Web Application
This is the Python Django Web application where users can simply Register and login with their email 
and add a New Support Ticket. Any new ticket raised via the New ticket form will be 
sent to Zoho Desk via API. Also, another page lists all the tickets raised by them.

## 1. Registration / Login page
Basic Email and Password based login. User details like Name, Email, Password will be stored in the Database.

## 2. New Ticket page
A form to capture New ticket input fields like Department, Category, Subject, Description and Priority. Contact Details input fields like Email and Name will be automatically populated from the Web Application Database.
These form details will not be saved in the Web application database, they will be POSTED to Zoho Desk New Ticket API to add a New Ticket. Confirmation of the New Ticket creation will be shown to the user on the page.  

## 3. Manage Tickets page
An interface where users can manage the tickets created by them and Users can see the ticket details like the Subject and Description along with 
the Ticket status and Ticket ID.
The list of tickets in the page will be fetched from the Zoho Desk using the API, as we will not be storing them in the database.
