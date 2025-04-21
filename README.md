# Hickeys Pharmacy Inventory Management System

This web application is designed to allow admins to manage staff and inventory for a pharmacy, while staff can manage medicine inventory. The system includes two separate panels: one for admin and another for staff, with different functionalities for each role. It is built using Flask for the backend and HTML and JavaScript for the frontend.

## Features

Pharmacy Handling Inventory and Managing Users
• Admin Panel:
• Admins can manage users (staff), including creating, reading, updating, and deleting staff members.
• Admins have full control over the system’s functionality, ensuring that staff users are appropriately managed.
• Staff Panel:
• Staff members can manage the pharmacy’s inventory, including adding, updating, and deleting medicines.
• Staff can view the current medicine inventory and make necessary changes to it.

## Panels

Admin Panel
• CRUD Operations on Staff: Admins can perform CRUD operations to manage the staff.
• Manage Users: Admins can create, edit, and delete staff user accounts.

## Staff Panel

• Inventory Management: Staff can add, update, or delete medicines in the inventory, keeping track of names, and other details related to each medicine.
• View Inventory: Staff can view the list of medicines available and their details.

## Technologies Used

• Backend:
• Python
• Flask (Web Framework)
• Flask-SQLAlchemy (Database management)
• Flask-Login (User authentication)
• Frontend:
• HTML (Structure)
• CSS (Styling)
• JavaScript (API calls and frontend logic using Fetch API)
• Database: SQL
• SQLite (for local development)
• Version Control:
• Git (for version control)

## How to Run:

1. Clone the repository:
   `git clone https://github.com/aviasnani/Hickeys-pharmacy.git`

2. Install dependencies:
   `pip install -r requirements.txt`

3. Configure your database connection (for AWS RDS or SQLite) in the config.py file.
4. Run the flask application
   `python3 main.py`
5. The app should now be running locally on http://localhost:5000/.

## References:

1. OpenAI: for assisting in code snippets such as API helpers (apiPost, apiDelete, apiPut, apiGet) in frontend/static/scripts/common/api.js and resolving any bugs and errors.
2. Amazon Q Developer: Resolving errors and bugs.
3. W3Schools: For helpful tutorials and references regarding HTML, CSS, and JavaScript. https://www.w3schools.com
4. Fetch APIs (Julian Nash): https://www.youtube.com/watch?v=QKcVjdLEX_s&t=165s
5. Flask CRUD Operations (Parwiz Forogh): https://www.youtube.com/watch?v=XTpLbBJTOM4&t=3306s
