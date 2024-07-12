from flask import Flask, request, jsonify, render_template
import pandas as pd

app = Flask(__name__)

@app.route('/') # root, display initial webpage
def index():
    # server-side render
    return render_template('index.html') # render template file

@app.route('/submit', methods=['POST']) # handle POST requests containing JSON data
def submit():
    # request contains information about current http request
    # get.json() parses the body of the request into a dictionary   
    data = request.get_json()
    file_path = 'data.xlsx'

    # attempt to reach existing fle
    try:
        df = pd.read_excel(file_path)
    except FileNotFoundError:
        # initialize new dataframe
        df = pd.DataFrame(columns=['Company', 'Position', 'Location'])
    
    new_row = pd.DataFrame([{
        'Company': data['company'], 
        'Position': data['position'], 
        'Location': data['location']
        }])
    
    df = pd.concat([df, new_row], ignore_index=True) # concatenate new row to df
    df.to_excel(file_path, index=False) # overwrite existing file
    
    return jsonify({'message': 'Excel file updated successfully'}) # notify user

if __name__ == '__main__':
    app.run(debug=True)