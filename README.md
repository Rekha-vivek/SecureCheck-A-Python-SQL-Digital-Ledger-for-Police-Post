# 🚔 SecureCheck — A Python-SQL Digital Ledger for Police Post

### 📖 Overview
**SecureCheck** is a digital record-keeping system built using **Python**, **PostgreSQL**, and **Pandas**.  
It helps police posts maintain daily logs of **traffic stops, arrests, and violations** securely and efficiently.  
Instead of traditional paper registers, SecureCheck provides a **modern SQL-based digital ledger** — making it easier to store, query, and analyze data.

## ⚙️ Features
- 🗃️ Store and retrieve police data (traffic stops, driver details, violations)
- 🔍 Filter and analyze records using SQL queries
- 📊 Generate insights such as:
  - Most common violations  
  - Arrest rate by age group  
  - Average stop duration by violation type  
  - Drug-related stop statistics  
- 🧠 Built using **Python, Pandas, and SQLAlchemy** for smooth data handling
- 🔒 Secure connection with PostgreSQL database

---

## 🧰 Tech Stack
| Component | Technology Used |
|------------|----------------|
| Programming Language | Python |
| Database | PostgreSQL |
| Libraries | psycopg2, SQLAlchemy, Pandas |
| Optional Interface | Streamlit |
| Environment | Jupyter Notebook / Python Script (.py) |

## 📁 Project Structure
SecureCheck-A-Python-SQL-Digital-Ledger-for-Police-Post/
│

├── Police.ipynb       
├── Police.py          
├── README.md         
---

## 🚀 How to Run the Project

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/Rekha-vivek/SecureCheck-A-Python-SQL-Digital-Ledger-for-Police-Post.git
cd SecureCheck-A-Python-SQL-Digital-Ledger-for-Police-Post
```

###2️⃣ Install Dependencies
```
pip install pandas psycopg2 sqlalchemy streamlit
```

### 3️⃣ Configure the Database Connection
```python
conn = psycopg2.connect(
    host="localhost",
    database="securecheck_traffic",
    user="postgres",
    password="your_password",
    port="5432"
)
```
###4️⃣ Run the Code
You can run the project in two ways:
**Jupyter Notebook:**
Open and execute `Police.ipynb`
**Python Script:**
```bash
python Police.py

## 🧡 **PART 5 — SQL Queries Used** 

```markdown

## 🧮 SQL Queries Used

```sql
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
