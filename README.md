# 🤖 AI-Powered Text-to-SQL Generator

An AI-powered Text-to-SQL application that converts natural language questions into SQL queries using Google's Gemini Large Language Model (LLM). The application executes the generated SQL queries on an SQLite database and displays the results through an interactive Streamlit web interface.

The goal of this project is to simplify database interactions by allowing users to retrieve information using plain English instead of writing SQL queries manually.

## 🚀 Features

- **Natural Language to SQL:** Convert English questions into SQL queries.
- **Google Gemini Integration:** Use a Large Language Model to understand user questions and generate SQL.
- **Prompt Engineering:** Provide database schema and examples to guide SQL generation.
- **Automated Query Execution:** Execute generated SQL queries against an SQLite database.
- **Interactive Web Interface:** Enter questions and view results through Streamlit.
- **SQL Query Preview:** Display the generated SQL query before or alongside the results.
- **Tabular Results:** Present database output in a structured table.
- **Error Handling:** Display errors encountered during query generation or execution.

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core application logic |
| Streamlit | Interactive web interface |
| Google Gemini API | Natural language understanding and SQL generation |
| NLP | Processing natural language questions |
| LLMs | Understanding user intent and generating SQL |
| SQLite | Database storage and query execution |
| SQL | Retrieving and analyzing database records |
| python-dotenv | Loading environment variables securely |

## 🏗️ Architecture

```text
User
  |
  v
Streamlit Web Interface
  |
  v
Natural Language Question
  |
  v
Prompt Engineering + Gemini LLM
  |
  v
Generated SQL Query
  |
  v
SQLite Database (student.db)
  |
  v
Query Execution
  |
  v
Database Results
  |
  v
Streamlit Results Table
```

## ⚙️ How It Works

1. The user enters a question in plain English.
2. The application combines the question with a prompt containing the database schema and example queries.
3. Google Gemini processes the question and generates an SQL query.
4. The application retrieves the generated SQL query.
5. Python's SQLite interface executes the query against `student.db`.
6. The database returns the matching records.
7. Streamlit displays the generated SQL and query results.

## 💡 Example

### User Input

```text
Show all students who scored more than 90 marks.
```

### Generated SQL Query

```sql
SELECT *
FROM STUDENT
WHERE MARKS > 90;
```

### Example Database Output

| NAME | CLASS | MARKS |
|---|---|---:|
| James Miller | 10th Grade | 95 |
| Sophia Wilson | 10th Grade | 93 |

*The table above is illustrative. Actual results depend on the records stored in your database.*

## 🗃️ Database Schema

The application uses an SQLite database named `student.db` containing a table named `STUDENT`.

| Column | Description |
|---|---|
| NAME | Student's name |
| CLASS | Student's class or grade |
| AGE | Student's age |
| GENDER | Student's gender |
| ADDRESS | Student's address |
| SECTION | Student's section |
| MARKS | Student's marks |

## 📂 Project Structure

```text
TextToSQL/
│
├── app.py              # Main Streamlit application
├── student.db          # SQLite database
├── .env                # API key configuration
├── .gitignore          # Files excluded from Git
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation
```

## 📋 Prerequisites

- Python 3.9 or a compatible supported version
- A Google Gemini API key
- pip package manager
- An SQLite database containing the required `STUDENT` table

## 🔧 Installation and Setup

### 1. Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd TextToSQL
```

Replace `YOUR_GITHUB_REPOSITORY_URL` with your actual repository URL.

### 2. Create a Virtual Environment

**macOS / Linux**

```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows**

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

If `requirements.txt` is not available yet, install the packages with:

```bash
pip install streamlit python-dotenv google-generativeai
```

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```env
GOOGLE_API_KEY=your_google_gemini_api_key
```

Replace the placeholder with your API key. Never commit the `.env` file or expose your API key publicly.

### 5. Prepare the Database

Ensure `student.db` exists and contains the `STUDENT` table with the columns described above.

### 6. Run the Application

```bash
streamlit run app.py
```

The terminal will provide a local URL, usually:

```text
http://localhost:8501
```

Open it in your browser to start using the application.

## 🧪 Example Questions to Try

Try entering questions such as:

- How many students are in the database?
- Show all female students.
- Find students who scored more than 90 marks.
- What is the average marks of all students?
- Who scored the highest marks?
- Show students older than 15 years.
- Display students from a specific class.
- Find students whose marks are above the overall average.
- Group students by class and calculate their average marks.

The generated SQL depends on the question, the configured model, and the database schema.

## 🔐 Security Considerations

- Store API keys in environment variables.
- Never upload `.env` files or credentials to GitHub.
- Validate generated SQL before execution.
- Restrict query execution to permitted read-only operations when appropriate.
- Use parameterized queries when handling user-supplied values in application-written SQL.
- Consider a read-only database connection and query limits when running against sensitive or production data.

**Important:** LLM-generated SQL may be incorrect or unsafe. This project should not execute unrestricted AI-generated SQL against a production database without suitable validation and access controls.

## 🎯 Learning Outcomes

Through this project, I explored:

- Integrating an LLM into a Python application.
- Converting natural language into SQL using prompt engineering.
- Working with Google Gemini API.
- Connecting Python applications to SQLite databases.
- Executing SQL queries and processing database results.
- Building interactive applications with Streamlit.
- Managing API credentials using environment variables.
- Handling application and database errors.

## 🔮 Future Improvements

- Add support for PostgreSQL and MySQL.
- Implement SQL query validation and read-only execution.
- Display query execution time and result summaries.
- Add downloadable CSV reports.
- Support more complex queries, joins, aggregations, and subqueries.
- Add database schema discovery and multi-table query generation.
- Improve the interface with query history and suggested questions.
- Deploy the application to a cloud hosting platform.

## 👨‍💻 Author

**Faizan**

AI Developer | Generative AI | LLM Applications | Full-Stack Development

- GitHub: [faizankhan005](https://github.com/faizankhan005)
- LinkedIn: [faizan05](https://www.linkedin.com/in/faizan05/)

## 📄 License

This project can be distributed under the MIT License if you choose to include one. Add a `LICENSE` file to the repository before claiming that the project is officially MIT-licensed.
