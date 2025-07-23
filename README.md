# Local_food_management_system
A Python/Streamlit web app linking surplus food providers with those in need to reduce waste. Features a data analysis dashboard for insights &amp; full CRUD operations for managing food listings. Uses PostgreSQL for data. Combat food insecurity, promote social good.
Local Food Wastage Management System
Project Overview
This project is a Python-based web application designed to tackle food waste and food insecurity. It creates a platform where individuals and restaurants can list their surplus food, and NGOs or individuals in need can claim it. The system provides valuable insights into food donation trends and facilitates efficient redistribution.

Features
Interactive Dashboard: Visualize key metrics and trends related to food donations, claims, and provider activities.

Food Listing Management (CRUD):

Add Listings: Easily add new surplus food items with details like name, quantity, expiry date, and provider information.

View & Filter Listings: Browse all available food items and filter them by location, food type, or meal type.

Update Listings: Modify details of existing food listings.

Delete Listings: Remove food items from the system.

PostgreSQL Database: Robust backend for storing all food, provider, receiver, and claim data.

Streamlit UI: A user-friendly and responsive web interface for seamless interaction.

Technologies Used
This project leverages a modern stack of technologies to deliver its functionality:

Python 3.8+: The core programming language.

Streamlit: For building the interactive and responsive web application interface.

PostgreSQL: The robust relational database management system used for all data storage.

Pandas: A powerful data manipulation and analysis library for Python.

SQLAlchemy: A comprehensive Python SQL toolkit and Object Relational Mapper (ORM) used for interacting with the PostgreSQL database.

psycopg2: The PostgreSQL adapter for Python, enabling Python to communicate with PostgreSQL.

Requirements
To run this project, you will need the following installed on your system:

Python 3.8 or higher (Anaconda distribution is recommended for easier environment management).

PostgreSQL 10 or higher (e.g., via Postgres.app for macOS, or direct installation for Windows/Linux).

Python Libraries: All required Python libraries are listed in requirements.txt and include:

streamlit

pandas

sqlalchemy

psycopg2-binary (or psycopg2)

python-dateutil (often a dependency of pandas)

pytz (often a dependency of pandas)

numpy (often a dependency of pandas)

Setup Instructions
Follow these steps to get the project running on your local machine.

1. Clone the Repository

First, clone this GitHub repository to your local machine:

git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name # Navigate into your project folder

(Replace your-username/your-repo-name with your actual GitHub repository details)

2. Database Setup (PostgreSQL)

Ensure your PostgreSQL server is installed and running.

Create Database: The database_setup.py script is designed to create a database named food_wastage_db if it doesn't already exist.

Run Database Setup Script:

Open your Terminal.

Navigate to your project directory (if not already there):

cd path/to/your/Food_management_system

Execute the setup script. This script will create all necessary tables (providers, receivers, food_listings, claims) and populate them with initial data from the provided CSV files.

python database_setup.py

Important Note for UniqueViolation Errors: If you encounter UniqueViolation errors when adding new items via the app (e.g., Key (food_id)=(1) already exists), it means the database's auto-increment sequence needs to be reset. Connect to food_wastage_db via psql (e.g., psql -U your_postgres_username -d food_wastage_db) and run the following SQL command:

SELECT setval('food_listings_food_id_seq', (SELECT MAX(food_id) FROM food_listings));

Then type \q to exit psql.

3. Python Environment Setup

It's highly recommended to use a virtual environment to manage Python dependencies, ensuring project isolation.

Create a Virtual Environment:

python -m venv venv

Activate the Virtual Environment:

macOS/Linux:

source venv/bin/activate

Windows:

.\venv\Scripts\activate

Install Dependencies: All required Python libraries are listed in the requirements.txt file.

pip install -r requirements.txt

4. Running the Streamlit Application

Once the database is set up and your Python environment is ready, you can launch the web application.

Start the Application:

Ensure your virtual environment is active (from step 3).

In your Terminal, navigate to your project directory.

Run the Streamlit app:

streamlit run app.py

The application will automatically open in your default web browser (usually http://localhost:8501). Keep the terminal window open as it runs the Streamlit server.

Project Structure
Food_management_system/
├── app.py                      # Main Streamlit web application code
├── database_setup.py           # Script to set up PostgreSQL database and load initial data
├── requirements.txt            # Lists all Python dependencies required for the project
├── README.md                   # This file, providing project overview and setup instructions
├── Food waste management system project.pdf # Original project brief and details
├── providers_data.csv          # Dataset containing information about food providers
├── receivers_data.csv          # Dataset containing information about food receivers
├── food_listings_data.csv      # Dataset detailing available food items
└── claims_data.csv             # Dataset tracking food claims made by receivers
└── [Your_Jupyter_Notebook_Name].ipynb # (Optional) Your Jupyter Notebook for initial data analysis and query testing

Contact
For any questions or feedback, feel free to reach out!

