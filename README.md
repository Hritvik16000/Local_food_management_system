# Local Food Wastage Management System

## 📌 Project Overview

Food wastage is a serious issue globally, with excess food being discarded while many people face food insecurity. This project aims to build a **Local Food Wastage Management System** using **Python, SQL, and Streamlit** to:

* Connect restaurants and individuals with surplus food to NGOs and individuals in need.
* Enable real-time CRUD operations on food listings and claims.
* Visualize food wastage trends for informed distribution.

## 🚀 Features

✅ **Streamlit App:**

* Displays outputs of 15+ SQL analytical queries.
* Filters by city, provider, food type, and meal type.
* Displays provider and receiver contact details.
* Supports adding, updating, deleting, and reading food listings and claims.

✅ **SQL-Powered Analysis:**

* Trends in food donations and claims.
* Analysis of provider contributions and receiver demands.
* Insights on wastage patterns for better planning.

✅ **Clean, user-friendly interface** for efficient food redistribution.

## 🗂️ Project Structure

```
📁 local-food-wastage-management/
 ├── food_wastage_streamlit_app.py        # Streamlit application
 ├── food_wastage_queries.sql             # 15+ SQL queries
 ├── food_wastage_eda.ipynb               # (Optional) EDA notebook
 ├── requirements.txt                     # Python dependencies
 ├── project_report.pdf                   # Project report with screenshots
 └── README.md                            # This file
```

## 🛠️ Tech Stack

* **Python** (data handling, CRUD, analysis)
* **SQL (PostgreSQL)** for structured data storage and analysis
* **Streamlit** for interactive application
* **Pandas, SQLAlchemy** for data operations

## 📊 Datasets Used

* `providers_data.csv`
* `receivers_data.csv`
* `food_listings_data.csv`
* `claims_data.csv`

## 📈 Analytical Questions Covered

1. Number of food providers and receivers in each city.
2. Top contributing provider types.
3. Contact details of providers by city.
4. Receivers with the highest claims.
5. Total food quantity available.
6. City with highest food listings.
7. Most common food types.
8. Claims per food item.
9. Provider with highest successful claims.
10. Percentage distribution of claim statuses.
11. Average quantity claimed per receiver.
12. Most claimed meal type.
13. Total food donated per provider.
    ... and more.

## 💻 How to Run the Project

1️⃣ **Clone the Repository:**

```bash
git clone <repository_link>
cd local-food-wastage-management
```

2️⃣ **Set up the Database:**

* Create a PostgreSQL database named `food_wastage_db`.
* Import CSV data into respective tables (`providers`, `receivers`, `food_listings`, `claims`).

3️⃣ **Install Dependencies:**

```bash
pip install -r requirements.txt
```

4️⃣ **Run the Streamlit App:**

```bash
streamlit run food_wastage_streamlit_app.py
```

## ✅ Project Evaluation Checklist

* [x] Clean and stored data in SQL database.
* [x] 15+ SQL queries executed with outputs.
* [x] CRUD operations implemented.
* [x] Streamlit app fully functional.
* [x] Visualizations and filters working.
* [x] Project report with screenshots ready.

## 📬 Submission Guidelines

* Upload the project to **GitHub**.
* Share the **GitHub repository link** on ZenClass.
* Book a **Live Evaluation Slot** if required using [this form](https://forms.gle/1m2Gsro41fLtZurRA).
* Ensure you are prepared to demonstrate CRUD, query execution, and explain your architecture during evaluation.

## 🙌 Acknowledgements

This project is created for the **Food Wastage Capstone** under the **Data Science & AIML program**, aiming to apply SQL, Python, and Streamlit skills for social good.

---

If you find this project useful, consider ⭐ starring the repository and sharing your learnings!

---

For any queries, contact:
Hritvik.sajo@gmail.com
