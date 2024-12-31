# Progress Tracker

A simple web application built with Flask to track tasks associated with different months. This app allows users to add tasks, update their status, and delete tasks and months. 

## Features:
- **View Tasks by Month**: Display tasks for each month.
- **Add New Tasks**: Add new tasks for any month.
- **Update Task Status**: Update task status (Not Started, In Progress, Done, Stuck).
- **Delete Tasks and Months**: Delete tasks from specific months or delete entire months.

## Prerequisites:
- Python 3.x
- Flask
- SQLite

## Installation

### 1. Clone the Repository:

```bash
git clone https://github.com/your-username/progress-tracker.git
cd progress-tracker
```

### 2. Set up a Virtual Environment:

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies:

```bash
pip install -r requirements.txt
```

### 4. Set up the Database:

Run the Flask app once to create the database:

```bash
flask run
```

This will automatically initialize the database (`tasks.db`) with the necessary tables.

## Usage

1. **Starting the Application**:

   Run the Flask application using the following command:

   ```bash
   flask run
   ```

2. **Access the App**:

   Open your browser and navigate to [http://127.0.0.1:5000](http://127.0.0.1:5000) to interact with the app.

3. **Managing Tasks**:
   - **Add Tasks**: On the home page, you can enter a new month name and add tasks to it.
   - **Update Task Status**: Click on a month name to view its tasks and update their status (Not Started, In Progress, Done, Stuck).
   - **Delete Tasks**: You can delete individual tasks from the month view.
   - **Delete Months**: You can delete an entire month, which removes all tasks associated with it.

## Folder Structure

```
progress-tracker/
├── app.py                # Main Flask application
├── templates/
│   ├── base.html         # Base HTML template
│   ├── index.html        # Index page for month overview
│   └── month.html        # Detailed page for tasks in a specific month
├── static/
│   └── style.css         # Styles for the web pages
└── requirements.txt      # List of dependencies
```

## Routes

- **GET `/`**: Displays the list of months and tasks.
- **POST `/month/<name>`**: Adds tasks to a specific month.
- **GET `/month/<name>`**: Displays tasks for a specific month.
- **POST `/update_task/<name>/<task_id>`**: Updates the status of a task.
- **POST `/delete_task/<name>/<task_id>`**: Deletes a specific task.
- **POST `/delete_month/<month>`**: Deletes an entire month and its tasks.

## Requirements

- Python 3.x
- Flask
- SQLite

### `requirements.txt` Example

```
Flask
Flask-SQLAlchemy
```

# To-Do

The following features are planned for future development:

1. User Authentication

- **Sign Up**: Allow users to create an account with email and password.  
- **Login**: Add a login page where users can authenticate with credentials.  
- **Logout**: Add a logout feature to end the user's session.  
- **Session Management**: Implement session management to keep track of the logged-in user's state.  
- **Password Recovery**: Implement password reset functionality for users who forget their passwords.  

2. User Services

- **User-Specific Data**: Implement functionality so that each user can view and manage their own tasks and months.  
- **Admin Access**: Provide admin privileges to manage all users' tasks and data.  
- **User profiles**: Create a profile page where users can view and update their information.  

3. Additional Features

- **Task Categories**: Allow tasks to be categorized (Work, Personal, School) for better organization.
- **Task Priority**: Implement a priority system to mark tasks as High, Medium, or Low.  
- **Task Deadline**: Add deadlines to tasks and notify users when deadlines are approaching:.
- **Analytics**: Provide analytics for users to track their progress over time (tasks completed per month, task status breakdown)  

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make changes and commit them (`git commit -am 'Add new feature'`).
4. Push to your branch (`git push origin feature-branch`).
5. Open a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Flask documentation: [https://flask.palletsprojects.com/](https://flask.palletsprojects.com/)
