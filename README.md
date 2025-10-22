🚔 SecureCheck — A Python-SQL Digital Ledger for Police Post
📖 Overview

SecureCheck is a digital record-keeping system built using Python, PostgreSQL, and Pandas.
It helps police posts maintain daily logs of traffic stops, arrests, and violations securely and efficiently.
Instead of traditional paper registers, SecureCheck provides a modern SQL-based digital ledger — making it easier to store, query, and analyze data.

⚙️ Features

🗃️ Store and retrieve police data (traffic stops, driver details, violations)

🔍 Filter and analyze records using SQL queries

📊 Generate insights such as:

Most common violations

Arrest rate by age group

Average stop duration by violation type

Drug-related stop statistics

🧠 Built using Python, Pandas, and SQLAlchemy for smooth data handling

🔒 Secure connection with PostgreSQL database

🧰 Tech Stack
Component	Technology Used
Programming Language	Python
Database	PostgreSQL
Libraries	psycopg2, SQLAlchemy, Pandas
Optional Interface	Streamlit
Environment	Jupyter Notebook / Python Script (.py)
📁 Project Structure
SecureCheck-A-Python-SQL-Digital-Ledger-for-Police-Post/
│
├── Police.ipynb       # Jupyter Notebook for data analysis and queries
├── Police.py          # Python script for database connection and functions
├── README.md          # Project documentation
└── requirements.txt   # (optional) Required Python packages

🚀 How to Run the Project
1️⃣ Clone the Repository
git clone https://github.com/Rekha-vivek/SecureCheck-A-Python-SQL-Digital-Ledger-for-Police-Post.git
cd SecureCheck-A-Python-SQL-Digital-Ledger-for-Police-Post

2️⃣ Install Dependencies
pip install pandas psycopg2 sqlalchemy streamlit

3️⃣ Configure the Database Connection

Update your connection details inside Police.py:

conn = psycopg2.connect(
    host="localhost",
    database="securecheck_traffic",
    user="postgres",
    password="your_password",
    port="5432"
)

4️⃣ Run the Code

You can run the project in two ways:

Jupyter Notebook:
Open and execute Police.ipynb

Python Script:

python Police.py

🧮 SQL Queries Used
-- 1. Count total number of traffic stops
SELECT COUNT(*) FROM traffic_stops;

-- 2. Highest arrest rate by driver age
SELECT driver_age,
       ROUND(SUM(CASE WHEN is_arrested=TRUE THEN 1 ELSE 0 END)::DECIMAL / COUNT(*) * 100, 2) AS arrest_rate
FROM traffic_stops
WHERE driver_age > 0
GROUP BY driver_age
ORDER BY arrest_rate DESC;

-- 3. Average stop duration by violation
SELECT violation,
       AVG(CASE 
             WHEN stop_duration='0-15 Min' THEN 7.5
             WHEN stop_duration='16-30 Min' THEN 23
             WHEN stop_duration='30+ Min' THEN 45 
           END) AS avg_stop_duration
FROM traffic_stops
GROUP BY violation
ORDER BY avg_stop_duration DESC;

-- 4. Top vehicles involved in drug-related stops
SELECT vehicle_number, COUNT(*) AS count
FROM traffic_stops
WHERE drugs_related_stop = TRUE
GROUP BY vehicle_number
ORDER BY count DESC
LIMIT 10;

-- 5. Most common violations
SELECT violation, COUNT(*) AS total_violations
FROM traffic_stops
GROUP BY violation
ORDER BY total_violations DESC
LIMIT 5;

-- 6. Total arrests by country
SELECT country_name, COUNT(*) AS total_arrests
FROM traffic_stops
WHERE is_arrested = TRUE
GROUP BY country_name
ORDER BY total_arrests DESC;

🧩 Key Python Functions
Function	Purpose
creating_connection()	Connects Python to the PostgreSQL database
fetching_of_data(query)	Executes SQL queries and returns results as a Pandas DataFrame
pd.read_sql(query, con=engine)	Reads SQL queries directly into Pandas
create_engine()	Creates an SQLAlchemy connection engine for smoother integration
📊 Example Outputs
driver_age	total_stops	total_arrests	arrest_rate
30	52	22	42.31%
25	45	10	22.22%
19	10	3	30.00%
violation	avg_stop_duration
DUI	45.00
Speeding	23.00
No Seatbelt	7.50
🌟 Future Enhancements

Add Streamlit dashboard for visual reports 📊

Add login authentication for police users 🔐

Enable data export to CSV or Excel 📁

Integrate with AWS or Azure for remote access ☁️

👩‍💻 Author

Rekha Vivek
