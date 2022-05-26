# ICT239
ICT239 Full Stack Web Development (Jan 2022)

## Staycay Folder
[ TMA ]

Simple booking web application for guests to view packages offered by various hotels
- landing page: **Login** page
- if user is not registered, there's a **Register** page

- upon Login, user is redirected to **Packages** page
    - each package has a **Book** button for user to book the package they are interested in

- if user is Admin:
    - Admin has access to the **Dashboard** page that shows a trend chart of bookings and total cost of all hotels across a date range
    - Admin has access to **Upload** page that allows the upload of csv files to link to database (MongoDB)

## staycation Folder
[ ECA ]

(extension of TMA)

User logged in is Admin:
- Admin has access to **Dashboard** page
    - upon clicking the **Dashboard** page, Admin is redirected to **Total Income** page which shows the same trend chart of the total income of hotels across a date range
    - Admin is able to dive further to view total cost **Due Per Hotel** and **Due Per User**, where Admin selects a hotel/user to view:
        - **Due Per User**: selects a user to view total bookings made across various hotels
        - **Due Per Hotel**: selects a hotel to view total bookings made by various users
