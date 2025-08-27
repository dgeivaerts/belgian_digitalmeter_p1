import pandas as pd
import psycopg2


try:
    conn = psycopg2.connect(
        database="postgres",
        user="postgres",
        password="example",
        host="localhost",
        port="5432"
    )

    # Read the data into a pandas DataFrame
    df = pd.read_sql_query('SELECT ts, value  FROM public."1-0:1.7.0" ', conn)
    data_dict = df.to_dict(orient='list')

except (Exception, psycopg2.DatabaseError) as error:
    print(error)
finally:
    if conn:
        conn.close()
        print("Database connection closed.")



# Convert the DataFrame to a dictionary for Chart.js


from flask import Flask, jsonify, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('chart.html')

@app.route('/data')
def data():
    return jsonify(data_dict)

if __name__ == '__main__':
    app.run(debug=True)