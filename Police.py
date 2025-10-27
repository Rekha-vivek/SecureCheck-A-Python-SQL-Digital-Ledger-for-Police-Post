import streamlit as st
import pandas as pd
import psycopg2
#DATABASE CONNECTION
def creating_connection():
    try:
        conn=psycopg2.connect(
             host="localhost",
             database="securecheck_traffic",
             user="postgres",
             password="123Ugofree6809",
             port="5432"
        )
        return conn
    except Exception as e:
        st.error(f"DATABASE CONNECTION ERROR:{e}")
        return None
    
#FETCHING THE DATA FROM THE DATABASE
def fetching_of_data(query):
    conn=creating_connection()
    if conn:
        try:
            cur=conn.cursor()
            cur.execute(query)
            Result=cur.fetchall()
            columns=[desc[0] for desc in cur.description]
            traffic_df=pd.DataFrame(Result,columns=columns)
                                    
            return traffic_df
        finally:
            conn.close()
    else:
        return pd.DataFrame()
    
#STREAMLITE APP TITLE
st.set_page_config(page_title="DIGITAL POLICE LOGS DASHBOARD",layout="wide")


#                       *********************Page 1-INTRODUCTION************************
st.title("👮**Digital Police Logs Dashboard**")
st.image("police_logo.jpg",use_container_width=True)
st.subheader("📊*Digital platform for managing and analyzing police logs*")
st.markdown("---")
st.header("📝*INTRODUCTION*")
st.markdown("""
### Problem Statement            
Traditional police logbooks are **paper-based**, making them difficult to manage, search, and analyze.  
They often lack real-time accessibility, transparency, and efficiency in operations.

### Objective          
    ✅ To digitize police logs for better record-keeping, transparency, and analytics.
    ✅ To provide an interactive dashboard for monitoring reports and officer activities.
    ✅ To ensure secure, efficient, and scalable data management.
    ✅ Query-powered dashboards for law enforcement
            
### Why Digital Logs?
- Faster access to records 🔎  
- Reduced paperwork 📚  
- Improved accountability ✅  
- Easy tracking of case progress 🚨  
- Data-driven decision making 📈
""")
#                       *********************Page 2-FULL TABLE************************
st.header("🧾 OVERVIEW OF THE POLICE LOGS")
query="SELECT * FROM traffic_stops"
data=fetching_of_data(query)
st.dataframe(data,use_container_width=True)

#                       *********************Page 3-KEY METRICS************************

st.header("📊 KEY METRICS")
col1,col2,col3,col4=st.columns(4)

with col1:
    total_stops=data.shape[0]
    st.metric("Total Police Stops",total_stops)
with col2:
    arrests=data[data['stop_outcome'].str.contains("arrest",case=False,na=False)].shape[0]
    st.metric("Total arrest",arrests)
with col3:
    warnings=data[data['stop_outcome'].str.contains("arrest",case=False,na=False)].shape[0]
    st.metric("Total Warnings",warnings)
with col4:
    drug_related=data[data["drugs_related_stop"]==True].shape[0]
    st.metric("Drugs Related Stop",drug_related)
       
#                       *********************Page 4-ADVANCED INSIGHTS************************

st.header('ADVANCED INSIGHTS')

selected_query=st.selectbox('select a query to run',[
    "Top 10 vehicle number related to drug related stop",
    "Frequently searched vehicle",
    "Driver age group having high arrest rate",
    "Gender distribution of driver stopped in each country",
    "Gender and race combination having highest arrest rate",
    "Time of the day having most traffic stop",
    "Average stop duration for different violation", 
    "Are the stops during the night are more likely to lead to arrests",
    "Violation most associated with search or arrest",
    "Violation most common among young driver (i.e) less than 25",
    "Violation that rarely result in search or arrest",
    "Country reporting the highest rate of drug related stops",
    "Arrest rate by country and violation",
    "Country having most stop with search conducted",
    "Yearly Breakdown of Stops and Arrests by Country ",
    "Driver Violation Trends Based on Age and Race ",
    "Number of stops by year,month,hour of the day",
    "Violations with High Search and Arrest Rates ",
    "Driver Demographics by Country (Age, Gender, and Race)",
    "Top 5 Violations with Highest Arrest Rates"
])

query_map={
    "Top 10 vehicle number related to drug related stop":"""SELECT vehicle_number, COUNT(*) as count FROM traffic_stops WHERE violation ILIKE '%DUI%' GROUP BY vehicle_number ORDER BY count DESC LIMIT 10;""",
    "Frequently searched vehicle":"""select vehicle_number,count(*) as frequent_searched_vehicle from traffic_stops where search_conducted=True group by vehicle_number order by frequent_searched_vehicle desc;""",
    "Driver age group having high arrest rate":"""select driver_age,count(*) as total_stops,
sum(case when is_arrested=True then 1 else 0 end) as total_arrests,
sum(case when is_arrested=True then 1 else 0 end)*100/count(*) as arrest_rate_percentage
from traffic_stops
where driver_age>0
group by driver_age
order by arrest_rate_percentage desc;
""",
    "Gender distribution of driver stopped in each country":"""select country_name,driver_gender,
count(*) as total_stops
from traffic_stops
where driver_gender is not null and country_name is not null
group by driver_gender,country_name
order by country_name,driver_gender;
""",
    "Gender and race combination having highest arrest rate":"""select driver_race,driver_gender,
count(*) as total_stops,
sum(case when search_conducted=True then 1 else 0 end) as total_searches,
sum(case when search_conducted=True then 1 else 0 end)*100/count(*) as search_rate
from traffic_stops
group by driver_gender,driver_race
order by search_rate;
""",
    "Time of the day having most traffic stop":"""select case
when extract(hour from stop_time) between 6 and 11 then 'Morning'
when extract(hour from stop_time) between 12 and 17 then 'Afternoon'
when extract(hour from stop_time) between 18 and 23 then 'Evening' 
else'Night'
end as time_of_day,
count(*) as total_stops
from traffic_stops
where stop_time is not null
group by time_of_day
order by total_stops desc;
""",
    "Average stop duration for different violation": """select violation,
avg
   (case 
         when stop_duration='0-15 Min' then 7.5
         when stop_duration='16=30 Min' then 23
		 when stop_duration='30+ Min' then 45 
		 end)
as avg_stop_duration
from traffic_stops
group by violation
order by avg_stop_duration desc;
""",
    "Are the stops during the night are more likely to lead to arrests":"""select case
         when stop_time between '20:00:00' and '23:59:00' then 'night'
		 when stop_time between '00:00:00' and '06:00:00' then 'night'
		 else 'day'
		 end as time_of_day,
       count(*) as total_stops,
	   sum(case when is_arrested =True then 1 else 0 end) as total_arrests,
	   round(sum(case when is_arrested=True then 1 else 0 end)::decimal/count(*)*100,2) as arrest_rate
from traffic_stops
group by time_of_day
order by arrest_rate desc;
""",
    "Violation most associated with search or arrest":"""SELECT violation,
           COUNT(*) AS total_stops,
           SUM(CASE WHEN search_conducted = TRUE THEN 1 ELSE 0 END) AS total_search,
           ROUND(SUM(CASE WHEN search_conducted = TRUE THEN 1 ELSE 0 END)::decimal / COUNT(*) * 100, 2) AS search_rate,
           SUM(CASE WHEN is_arrested = TRUE THEN 1 ELSE 0 END) AS total_arrest,
           ROUND(SUM(CASE WHEN is_arrested = TRUE THEN 1 ELSE 0 END)::decimal / COUNT(*) * 100, 2) AS arrest_rate
    FROM traffic_stops
    GROUP BY violation
    ORDER BY search_rate DESC, arrest_rate DESC;
""",
    "Violation most common among young driver (i.e) less than 25":"""select violation,driver_age,
    COUNT(*) AS total_stops
FROM traffic_stops
WHERE driver_age < 25
GROUP BY violation,driver_age
ORDER BY total_stops DESC;
""",
    "Violation that rarely result in search or arrest":"""SELECT 
    violation,
    COUNT(*) AS total_stops,
    SUM(CASE WHEN search_conducted = TRUE OR is_arrested = TRUE THEN 1 ELSE 0 END) AS search_or_arrest_count,
    ROUND(
        (SUM(CASE WHEN search_conducted = TRUE OR is_arrested = TRUE THEN 1 ELSE 0 END)::decimal / COUNT(*)) * 100,
        2
    ) AS search_or_arrest_rate
FROM traffic_stops
GROUP BY violation
ORDER BY search_or_arrest_rate;
""",
    "Country reporting the highest rate of drug related stops":"""SELECT 
    country_name,
    COUNT(*) AS total_stops,
    SUM(CASE WHEN drugs_related_stop = TRUE THEN 1 ELSE 0 END) AS drug_stops,
    ROUND(SUM(CASE WHEN drugs_related_stop = TRUE THEN 1 ELSE 0 END)::decimal / COUNT(*) * 100, 2) AS drug_rate_percentage
FROM traffic_stops
GROUP BY country_name
ORDER BY drug_rate_percentage DESC;
""",
    "Arrest rate by country and violation":"""select country_name,violation,
sum(case when is_arrested=True then 1 else 0 end) as total_arrest,
round(sum(case when is_arrested=True then 1 else 0 end)::decimal/count(*)*100,2) as arrest_rate
from traffic_stops
group by country_name,violation
order by arrest_rate desc;
""",
    "Country having most stop with search conducted":"""select country_name,
           sum(case when search_conducted=True then 1 else 0 end) as total_search
           from traffic_stops
           group by country_name
           order by total_search desc;
""",
    "Yearly Breakdown of Stops and Arrests by Country ":"""WITH yearly_data AS (
    SELECT 
        country_name,
        EXTRACT(YEAR FROM stop_date)::int AS year,
        COUNT(*) AS total_stops,
        SUM(CASE WHEN is_arrested = TRUE THEN 1 ELSE 0 END) AS total_arrests
    FROM traffic_stops
    GROUP BY country_name, EXTRACT(YEAR FROM stop_date)
)
SELECT 
    country_name,
    year,
    total_stops,
    total_arrests,
    ROUND((total_arrests::decimal / total_stops) * 100, 2) AS arrest_rate_percentage,

    SUM(total_arrests) OVER (PARTITION BY country_name ORDER BY year) AS cumulative_arrests,

    
    RANK() OVER (PARTITION BY year ORDER BY total_arrests DESC) AS country_rank_by_arrests

FROM yearly_data
ORDER BY country_name, year;
""",
    "Driver Violation Trends Based on Age and Race ":"""WITH age_groups AS (
    SELECT 
        driver_age,
        driver_race,
        violation,
        CASE 
            WHEN driver_age < 25 THEN 'Young (<25)'
            WHEN driver_age BETWEEN 25 AND 40 THEN 'Adult (25-40)'
            WHEN driver_age BETWEEN 41 AND 60 THEN 'Middle Age (41-60)'
            ELSE 'Senior (60+)' 
        END AS age_group
    FROM traffic_stops
    WHERE driver_age > 0
),
counts AS (
    SELECT 
        age_group,
        driver_race,
        violation,
        COUNT(*) AS total_stops
    FROM age_groups
    GROUP BY age_group, driver_race, violation
)
SELECT 
    age_group,
    driver_race,
    violation,
    total_stops,
    ROUND(total_stops * 100.0 / SUM(total_stops) OVER (PARTITION BY age_group, driver_race), 2) AS violation_percentage
FROM counts
ORDER BY age_group, driver_race, violation_percentage DESC;
""",
    "Number of stops by year,month,hour of the day":"""SELECT 
    EXTRACT(YEAR FROM stop_date)::int AS year,
    EXTRACT(MONTH FROM stop_date)::int AS month,
    EXTRACT(HOUR FROM stop_time)::int AS hour,
    COUNT(*) AS total_stops
FROM traffic_stops
GROUP BY year, month, hour
ORDER BY year, month, hour;
""",
    "Violations with High Search and Arrest Rates ":"""SELECT 
    violation,
    COUNT(*) AS total_stops,

    
    SUM(CASE WHEN search_conducted = TRUE THEN 1 ELSE 0 END) AS total_searches,
    ROUND(SUM(CASE WHEN search_conducted = TRUE THEN 1 ELSE 0 END)::decimal / COUNT(*) * 100, 2) AS search_rate,

    
    SUM(CASE WHEN is_arrested = TRUE THEN 1 ELSE 0 END) AS total_arrests,
    ROUND(SUM(CASE WHEN is_arrested = TRUE THEN 1 ELSE 0 END)::decimal / COUNT(*) * 100, 2) AS arrest_rate,

    
    RANK() OVER (ORDER BY SUM(CASE WHEN search_conducted = TRUE THEN 1 ELSE 0 END)::decimal / COUNT(*) DESC) AS rank_by_search_rate,
    RANK() OVER (ORDER BY SUM(CASE WHEN is_arrested = TRUE THEN 1 ELSE 0 END)::decimal / COUNT(*) DESC) AS rank_by_arrest_rate

FROM traffic_stops
GROUP BY violation
ORDER BY search_rate DESC, arrest_rate DESC;
""",
    "Driver Demographics by Country (Age, Gender, and Race)":"""SELECT 
    country_name,
     CASE
        WHEN driver_age BETWEEN 0 AND 17 THEN '0-17'
        WHEN driver_age BETWEEN 18 AND 24 THEN '18-24'
        WHEN driver_age BETWEEN 25 AND 40 THEN '25-40'
        WHEN driver_age BETWEEN 41 AND 60 THEN '41-60'
        ELSE '60+' 
    END AS age_group,
	driver_gender,
    driver_race,
    COUNT(*) AS total_drivers

FROM traffic_stops
WHERE driver_age > 0   
GROUP BY country_name, age_group, driver_gender, driver_race
ORDER BY country_name, age_group, driver_gender, driver_race;
""",
    "Top 5 Violations with Highest Arrest Rates":"""SELECT 
    violation,
    COUNT(*) AS total_stops,
    SUM(CASE WHEN is_arrested = TRUE THEN 1 ELSE 0 END) AS total_arrests,
    ROUND(SUM(CASE WHEN is_arrested = TRUE THEN 1 ELSE 0 END)::decimal / COUNT(*) * 100, 2) AS arrest_rate_percentage
FROM traffic_stops
GROUP BY violation
HAVING COUNT(*) > 0   
ORDER BY arrest_rate_percentage DESC
LIMIT 5;
"""}

if st.button("Run Query"):
    result=fetching_of_data(query_map[selected_query])
    if not result.empty:
        st.write(result)
    else:
        st.warning("No results found for the selected query.")

st.markdown("---")
st.markdown("Built with ❤️ for Law Enforcement by SecureCheck")
st.header("*🔍Smart Traffic Stop Predictor*")

st.header("☄️PREDICT THE OUTCOME AND VIOLATION")

with st.form("new_log_form"):
     stop_date= st.date_input("Stop Date")
     stop_time= st.time_input("Stop Time")
     country_name= st.text_input("Country Name")
     driver_gender=st.selectbox("Driver Gender",['male','female'])
     driver_age=st.number_input("Driver Age",min_value=18,max_value=100,value=27)
     driver_race=st.text_input("Driver Race")
     violation=st.selectbox("VIOLATION",["Seatbelt","Speeding","Signal","DUI","Other"])
     search_conducted=st.selectbox("Was a Search_conducted?",['0','1'])
     search_type=st.text_input("Search Type")
     stop_outcome=st.selectbox("Stop Outcome",["Ticket","Arrest","Warning"])
     stop_duration=st.selectbox("Stop Duration",data['stop_duration'].dropna().unique())
     drugs_related_stop=st.selectbox("DRUG RELATED",["0", "1"])
     vehicle_number=st.text_input('Vehicle Number')
     timestamp=pd.Timestamp.now()

     submit=st.form_submit_button('Predict Stop Outcome & Violation')
if submit:
    filter_data=data[
        (data['driver_gender']==driver_gender)&
        (data['driver_age']==driver_age) &
        (data['search_conducted']==int(search_conducted)) &
        (data['stop_duration']==stop_duration) &
        (data['drugs_related_stop']==int(drugs_related_stop))
    ]

    if not filter_data.empty:
        predicted_outcome=filter_data['stop_outcome'].mode()[0]
        predicted_violations=filter_data['violation'].mode()[0]
    else:
        predicted_outcome='warning'
        predicted_violations='speeding'

    searching="A search was conducted" if int(search_conducted) else "No search was conducted"
    drug_txt="was drugs related" if int(drugs_related_stop) else "was not drug related"
    pronoun="he" if driver_gender=="male" else "she"
        
    st.markdown(f"""
    🔍**Prediction Summary**
                
       ** Predicted Violations:**{predicted_violations}
       ** Predicted Stop_Outcome:**{predicted_outcome}     
     
      🚗 A {driver_age}-year-old {driver_gender} driver was stopped for **{violation}** at **{stop_time.strftime('%I:%M %p')}**.  
      {searching}, and {pronoun} received a **{stop_outcome}**.  
      The stop lasted **{stop_duration}** and {drug_txt}.
      """)

