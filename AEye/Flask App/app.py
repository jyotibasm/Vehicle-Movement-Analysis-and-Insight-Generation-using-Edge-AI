from flask import Flask, render_template
import pandas as pd 
 
# Read the Excel file
df = pd.read_excel('./Database/updates.xlsx', sheet_name='Sheet1') 

item = df.to_dict(orient='records')
data = item [0]


# Drop rows with NaN values in the 'License Plate' column
df = df.dropna(subset=['Unauthorized'])

# Find the length of a specific column (e.g., 'License Plate')
column_length = len(df['Unauthorized'])

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('Vehicle Movement Patterns.html',data=data)

@app.route('/Vehicle Matching')
def Vehicle_Matching():
    return render_template('Vehicle Matching.html',data=item,column_length=column_length)

@app.route('/Parking Occupancy')
def Parking_Occupancy():
    return render_template('Parking Occupancy.html',data=data)

@app.route('/Vehicle Movement Patterns')
def Vehicle_Movement_Patterns():
    return render_template('Vehicle Movement Patterns.html',data=data)


if __name__ == '__main__':
    app.run(debug=True)
