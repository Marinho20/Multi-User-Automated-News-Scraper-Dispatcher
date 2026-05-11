# Multi-User-Automated-News-Scraper-Dispatcher
A robust, multi-user automated news monitoring and delivery system.

Universal News Sentinel is a Python-based backend application designed to monitor news sources (currently BBC News), filter headlines based on individual user interests (keywords), and deliver personalized summaries directly to their email.

The system uses a relational database to manage users and track notification history, ensuring that each user receives only fresh, relevant content.

#Key Features

->Multi-User Scalability: Manages individual profiles, keywords, and history for multiple users.

->Intelligent Filtering: Real-time headline scanning matched against custom user-defined keywords.

->Duplicate Prevention: Tracks "seen news" in a MySQL database to avoid spamming users with the same content.

->Automated SMTP Delivery: Formatted email alerts sent via Gmail's secure SMTP protocol.

->Secure Configuration: Uses environment variables (.env) for sensitive credentials.

#Tech Stack

->Language: Python 3.12+

->Database: MySQL

->Scraping: BeautifulSoup4 / Requests

->Email: SMTP / MIME 

->Environment: Python-dotenv

#Instalation and Setup

1. Clone the repository
2. Install dependencies
3. Database Configuration
the database structure is provided in the repository. To set up your MySQL instance:
->Create a new database in your MySQL server.
->Run the commands found in the schema.sql (or your filename) file to create the necessary tables (users, user_keywords, seen_news).
4. Environment Variables
Create a .env file in the root directory with your credentials:
DB_HOST=localhost
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_NAME=your_db_name
BOT_sender_gmail=your_email@gmail.com
BOT_sender_password=your_app_password

#Usage
Run the main bot engine:
python main.pyw

The system will automatically scrape the latest news, cross-reference them with user preferences, and send email notifications for new matches.

#Dependencies

Run de comand "pip install -r requirements.txt"

Libraries included in requirements.txt:

->beautifulsoup4: For parsing HTML and extracting news.

->requests: To handle HTTP connections to the news source.

->mysql-connector-python: To communicate with your MySQL database.

->python-dotenv: To securely load your credentials from the .env file.
