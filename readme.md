# Information Retrieval System using Flask and PHPMyAdmin

This is a simple information retrieval system that allows an admin to register new members by collecting their information, including a photo, and stores it in a MySQL database. The system also enables the admin to verify a user's identity by matching their provided photo with the stored photo in the database. The web application is built using Flask as the backend framework and PHPMyAdmin as the MySQL database client.

create a virtual environment both on windows and mac 
python -m venv env
Activate the virtual environment on windows 
env\Scripts\activate
on mac: source env/bin/activate


## Installation

Follow the steps below to set up the information retrieval system on your local machine:

### Step 1: Install Python and Flask

1. Make sure you have Python installed on your system. If not, download the latest version from the official website: https://www.python.org/downloads/

2. Install Flask using pip (Python package manager). Open your terminal/command prompt and run the following command:
   ```
   pip install Flask
   ```

### Step 2: Install MySQL and PHPMyAdmin

1. Install MySQL database on your machine. You can download the installer from the official website: https://dev.mysql.com/downloads/installer/

2. During the installation, make sure to set a root password for MySQL.

3. Install PHPMyAdmin to manage the MySQL database. You can download PHPMyAdmin from: https://www.phpmyadmin.net/downloads/

4. Follow the PHPMyAdmin installation instructions for your web server (e.g., Apache or Nginx).

### Step 3: Clone the Repository

1. Clone this repository to your local machine using git or download the ZIP file and extract it.

   ```
   git clone https://github.com/yourusername/information-retrieval-system.git
   cd information-retrieval-system
   ```

### Step 4: Create the MySQL Database and Table

1. Open PHPMyAdmin in your web browser (usually accessible at http://localhost/phpmyadmin/).

2. Log in using the root username and the password you set during MySQL installation.

3. Create a new database named `information_retrieval_system`.

4. In the newly created database, execute the following SQL query to create the `members` table:

   ```sql
   CREATE TABLE members (
       id INT AUTO_INCREMENT PRIMARY KEY,
       firstname VARCHAR(50),
       lastname VARCHAR(50),
       username VARCHAR(50) UNIQUE,
       address VARCHAR(100),
       gender VARCHAR(10),
       photo LONGBLOB
   );
   ```

### Step 5: Run the Application

1. Open a terminal/command prompt and navigate to the project folder where you cloned or extracted the repository.

2. Run the Flask application using the following command:

   ```
   python app.py
   ```

3. The application should now be running. Open your web browser and go to http://localhost:5000 to access the home page.

## Usage

1. Home Page: The home page welcomes users to the information retrieval system.

2. Login Page for Admin: Navigate to http://localhost:5000/login to access the login page for the admin. The default admin credentials are hardcoded in the Flask app (username: admin, password: password).

3. Register New Member: After logging in as an admin, you can go to http://localhost:5000/register to register a new member. Provide all the required information, including a photo, and submit the form. The member's details will be stored in the MySQL database.

4. Verification: To verify a user's identity, the admin can go to http://localhost:5000/verification. The admin will be prompted to provide the user's photo (either by live capture or by uploading a photo). The provided photo will be compared with the stored photo in the database, and if there's a match, the user's information will be displayed.

## Packages Used

The following Python packages are used in this project:

- Flask: A lightweight web framework for Python to create web applications.
- mysql-connector-python: A MySQL driver for Python to interact with the MySQL database.
- mysqlclient: A MySQL client library for Python, required by Flask MySQL.

You can install these packages using pip as shown in Step 1 of the installation guide.

Please note that this is a basic implementation of an information retrieval system, and it may need additional security and feature enhancements for a production-ready application. Always ensure proper input validation, user authentication, and secure photo storage when developing real-world applications.