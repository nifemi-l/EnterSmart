from flask import Flask, request, jsonify, render_template
import pandas as pd
import shutil

app = Flask(__name__)

# constants
DATA = 'data'
XLSX = '.xlsx'
BACKUP = '_backup'

@app.route('/')
def index():
    """Render landing page."""
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    """Submit given data to excel."""
    data = request.get_json()
    file_path = DATA + XLSX

    # backup file before modifying
    try:
        shutil.copyfile(file_path, DATA + BACKUP + XLSX)
    except FileNotFoundError:
        pass # file dne
    
    try:
        df = pd.read_excel(file_path)
    except FileNotFoundError:
        df = pd.DataFrame(columns=['Company', 'Position', 'Location'])
    
    new_row = pd.DataFrame([{
        'Company': data['company'], 
        'Position': data['position'], 
        'Location': data['location']
        }])
    
    # update df
    df = pd.concat([df, new_row], ignore_index=True)

    # save with context manager
    with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
    
    return jsonify({'message': 'Excel file updated successfully'})

@app.route('/view-history', methods=['GET'])
def view_application_history():
    """Generate application history data."""
    df = pd.read_excel('data.xlsx', usecols=['Company', 'Position', 'Location', 'Assessment Extended?', 'Interview Extended?', 'Offered?'])
    df['Assessment Extended?'].fillna('N/A', inplace=True)
    df['Interview Extended?'].fillna('N/A', inplace=True)
    df['Offered?'].fillna('N/A', inplace=True)

    data = df.to_dict(orient='records')
    data.reverse()

    return jsonify(data)

@app.route('/application-history')
def application_history(): 
    """Render history-viewing template."""
    return render_template('application-history.html')

@app.route('/delete', methods=['POST'])
def delete():
    """Handle deletion based on given identifiers."""
    data = request.get_json()
    file_path = 'data.xlsx'

    # backup file before modifying
    try:
        shutil.copyfile(file_path, DATA + BACKUP + XLSX)
    except FileNotFoundError:
        return jsonify({'message': 'File not found'}), 404

    # read the excel file
    try:    
        df = pd.read_excel(file_path)
    except FileNotFoundError: 
        return jsonify({'message': 'File not found'}), 404

    # filter out matching row
    df = df[~(
        (df['Company'] == data['company']) &
        (df['Position'] == data['position']) &
        (df['Location'] == data['location'])
    )]

    # save with context manager
    with pd.ExcelWriter(file_path, engine='openpyxl') as writer: 
        df.to_excel(writer, index=False)
    
    return jsonify({'message': 'Entry deleted successfully'})

@app.route('/update', methods=['POST'])
def update():
    """Receive new & old data to identify and modify record."""
    # get info from request
    data = request.get_json()
    file_path = 'data.xlsx'

    # read the excel file
    try:
        df = pd.read_excel(file_path)
    except FileNotFoundError:
        return jsonify({'message': 'File not found'}), 404

    # find the row to update
    mask = (
        (df['Company'] == data['oldCompany']) &
        (df['Position'] == data['oldPosition']) &
        (df['Location'] == data['oldLocation'])
    )

    # update matched rows
    df.loc[mask, ['Company', 'Position', 'Location', 'Assessment Extended?', 'Interview Extended?', 'Offered?']] = [
        data['newCompany'], data['newPosition'], data['newLocation'], 
        data['newAssessment'], data['newInterview'], data['newOffered']
    ]

    # backup file before modifying
    try:
        shutil.copyfile(file_path, DATA + BACKUP + XLSX)
    except FileNotFoundError:
        return jsonify({'message': 'File not found'}), 404
    
    # save file
    df.to_excel(file_path, index=False)

    return jsonify({'message': 'Entry updated successfully'})

if __name__ == '__main__':
    app.run(debug=True)