## EnterSmart: Job Application Data Entry Tool
This web application simplifies the process of tracking job applications by providing a user-friendly interface for entering and viewing job application data. I like to document my job applications, and after 2 years of manual Excel entry, I wanted to optimize my process. I developed this tool to streamline the data entry and tracking process.

### Features
- **Interactive Web Form**: Facilitates the input of company names, job positions, and locations.
- **Application History View**: Displays a list of all submitted job applications with details.
- **Search Functionality**: Allows users to search through their application history.

### Built With
- **Frontend**: HTML, CSS, JavaScript.
- **Backend**: Python with Flask.
- **Data Handling**: 
  - **Pandas**
  - **Excel**

### Prerequisites
You need to have Python installed along with Flask, and Pandas. These can be installed using pip:
```bash
pip install Flask pandas
```

### Running the Application
1. Clone the repository:
   ```bash
   git clone https://github.com/Nifemi-L/EnterSmart.git
   ```
2. Navigate to the project directory:
   ```bash
   cd <project_directory>
   ```
3. Run the application:
   ```bash
   python app.py
   ```
4. Open your web browser and navigate to `http://localhost:5000` to use the application.

### Files
- `index.html`: The entry page where users can input new job applications.
- `application-history.html`: The page where users can view their application history.
- `app.py`: The Flask backend handling data submission and retrieval.

### Screenshots
![Entry Page](Screenshots/Entry%20Page.png)
![Application History Page](Screenshots/Application%20History%20Page.png)

### Future Enhancements
- Enhanced Data Visualization: Integrate charts and graphs to visualize application data.
- Export Functionality: Allow users to export their application history to CSV or Excel files.
- Data manipulation.
- Database storage.
