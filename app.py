from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

# Function to run SQL queries
def run_query(query):
    conn = sqlite3.connect('jupyter_sql_tutorial.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

# Main route with query results
@app.route('/')
def index():
    # Run the SQL queries and collect the data
    total_records = run_query("SELECT COUNT(*) AS total_records FROM students")
    inter_dom_counts = run_query("SELECT inter_dom, COUNT(*) AS count_inter_dom FROM students GROUP BY inter_dom")
    phq_stats = run_query("""
        SELECT inter_dom, MIN(todep) AS min_phq, MAX(todep) AS max_phq, 
               ROUND(AVG(todep), 2) AS avg_phq 
        FROM students 
        GROUP BY inter_dom
    """)
    sc_stats = run_query("""
        SELECT inter_dom, MIN(tosc) AS min_sc, MAX(tosc) AS max_sc, 
               ROUND(AVG(tosc), 2) AS avg_sc 
        FROM students 
        GROUP BY inter_dom
    """)
    as_stats = run_query("""
        SELECT inter_dom, MIN(toas) AS min_as, MAX(toas) AS max_as, 
               ROUND(AVG(toas), 2) AS avg_as 
        FROM students 
        GROUP BY inter_dom
    """)
    stay_scores = run_query("""
        SELECT stay, ROUND(AVG(todep), 2) AS average_phq, 
               ROUND(AVG(tosc), 2) AS average_scs, 
               ROUND(AVG(toas), 2) AS average_as 
        FROM students 
        WHERE inter_dom = 'Inter' 
        GROUP BY stay 
        ORDER BY stay DESC
    """)

    # Pass the data to the frontend for rendering in tables
    return render_template('index.html', total_records=total_records, inter_dom_counts=inter_dom_counts, 
                           phq_stats=phq_stats, sc_stats=sc_stats, as_stats=as_stats, stay_scores=stay_scores)

if __name__ == '__main__':
    app.run(debug=True)
