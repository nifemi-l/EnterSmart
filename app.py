from flask import Flask, request, jsonify, render_template
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()
    file_path = 'data.xlsx'

    try:
        df = pd.read_excel(file_path)
    except FileNotFoundError:
        df = pd.DataFrame(columns=['Company', 'Position', 'Location'])
    
    new_row = pd.DataFrame([{
        'Company': data['company'], 
        'Position': data['position'], 
        'Location': data['location']
        }])
    
    df = pd.concat([df, new_row], ignore_index=True)
    df.to_excel(file_path, index=False)
    
    return jsonify({'message': 'Excel file updated successfully'})

@app.route('/view-history', methods=['GET'])
def view_application_history(): 
    df = pd.read_excel('data.xlsx', usecols=['Company', 'Position', 'Location', 'Assessment Extended?', 'Interview Extended?', 'Offered?'])
    df['Assessment Extended?'].fillna('N/A', inplace=True)
    df['Interview Extended?'].fillna('N/A', inplace=True)
    df['Offered?'].fillna('N/A', inplace=True)
    print(df)
    data = df.to_dict(orient='records')
    data.reverse()
    return jsonify(data)

@app.route('/application-history.html')
def application_history(): 
    return render_template('application-history.html')

if __name__ == '__main__':
    app.run(debug=True)