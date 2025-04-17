Pharmacy Inventory Management System

This web application is designed to allow admins to manage staff and inventory for a pharmacy, while staff can manage medicine inventory. The system includes two separate panels: one for admin and another for staff, with different functionalities for each role. It is built using Flask for the backend and HTML and JavaScript for the frontend.

Features

Pharmacy Handling Inventory and Managing Users
• Admin Panel:
• Admins can manage users (staff), including creating, reading, updating, and deleting staff members.
• Admins have full control over the system’s functionality, ensuring that staff users are appropriately managed.
• Staff Panel:
• Staff members can manage the pharmacy’s inventory, including adding, updating, and deleting medicines.
• Staff can view the current medicine inventory and make necessary changes to it.

Panels

Admin Panel
• CRUD Operations on Staff: Admins can perform CRUD operations to manage the staff, ensuring that each staff member has the appropriate permissions.
• Manage Users: Admins can create, edit, and delete staff user accounts.
• View Inventory: Admins can also access the inventory, although their role is more focused on managing staff.

Staff Panel
• Inventory Management: Staff can add, update, or delete medicines in the inventory, keeping track of quantities, names, and other details related to each medicine.
• View Inventory: Staff can view the list of medicines available and their details.

Technologies Used
• Backend:
• Python
• Flask (Web Framework)
• Flask-SQLAlchemy (Database management)
• Flask-Login (User authentication)
• SQLite (Local development database, can be swapped with AWS RDS for production)
• Frontend:
• HTML (Structure)
• CSS (Styling)
• JavaScript (API calls and frontend logic using Fetch API)
• Database:
• AWS RDS (for production)
• SQLite (for local development)
• Version Control:
• Git (for version control)

How to Run 1. Clone the repository:
`git clone <repository_url>`

2. Install dependencies:
   `pip install -r requirements.txt`

3. Configure your database connection (for AWS RDS or SQLite) in the config.py file.
4. Run the flask application
   `python3 main.py`
5. The app should now be running locally on http://localhost:5000/.

## Attributions:

1. OpenAI: for assisting in code snippets
2. Amazon Q Developer: For the insight and integration of AWS RDS into the backend as well as resolving errors and bugs.
3. W3Schools: For helpful tutorials and references regarding HTML, CSS, and JavaScript.
4. Fetch APIs (Julian Nash): https://www.youtube.com/watch?v=QKcVjdLEX_s&t=165s
5. Flask CRUD Operations (Parwiz Forogh): https://www.youtube.com/watch?v=XTpLbBJTOM4&t=3306s
6. 3schools: https://www.w3schools.com
