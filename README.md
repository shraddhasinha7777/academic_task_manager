# Academic Task Manager  
**Student Productivity Tool (BCA Minor Project)**

---

## Project Overview
**Academic Task Manager is a desktop-based task management application developed using Python.**
It is designed to help students and individuals organize academic tasks efficiently, prioritize work intelligently, and reduce decision fatigue.

**The application uses a rule-based smart priority system to highlight urgent and important tasks, making daily planning easier and more effective.  
Unlike traditional to-do list applications, this system evaluates task urgency and importance to guide users toward the most important work first, improving focus, productivity, and time management.
This project is developed as a BCA Minor Project to demonstrate practical implementation of Object-Oriented Programming, GUI development, and database management.
****
---

## Key Features
- **Smart Priority Score (Star-Score Algorithm)**  
  Automatically ranks tasks based on deadline urgency and priority level.

- **Efficiency Tracker**  
  Displays a real-time progress bar and assigns motivational badges such as *Top Performer* based on task completion.

- **Urgency Visual Indicators**  
  Highlights overdue tasks and uses blinking alerts for tasks due within 24 hours.

- **What If I Skip Today? Simulation**  
  Analyzes the risk of postponing tasks and warns users about potential backlog.

- **Sticky Note & Widget Mode**  
  Provides a compact, always-on-top widget for quick access to urgent tasks.

- **Theme Support**  
  Includes both Light and Dark modes for better user experience.

- **Local Data Storage**  
  All tasks and categories are stored securely using a local SQLite database.
  
  Screenshots of the working application are provided in the final project report.
  
<img width="1914" height="1018" alt="image" src="https://github.com/user-attachments/assets/4cd9abec-e21d-49aa-8b7f-633998807a6d" />
<img width="1432" height="522" alt="image" src="https://github.com/user-attachments/assets/3441f6cf-6347-4cb6-937b-04dc25b3d220" />
<img width="1192" height="619" alt="image" src="https://github.com/user-attachments/assets/c4edf85b-7ab4-49ff-8385-29099d04472e" />
<img width="1415" height="376" alt="image" src="https://github.com/user-attachments/assets/d9931361-7695-4b62-b81e-9e713a2773ee" />
<img width="1421" height="615" alt="image" src="https://github.com/user-attachments/assets/ce62e23e-4761-4441-8ba4-ec8e1cec47ac" />
<img width="412" height="417" alt="image" src="https://github.com/user-attachments/assets/ea5febea-07b5-44f9-9644-37f3705182b9" />
---

## Technologies Used
- **Programming Language:** Python 3.x  
- **GUI Framework:** Tkinter  
- **Database:** SQLite  
- **IDE:** Visual Studio Code  
- **Standard Libraries:** sqlite3, datetime  

---

## Project Structure
```Academic-Task-Manager/
│
├── app.py
│ Main application file
│ Handles GUI, task logic, dashboard, and user interactions
│
├── models.py
│ Contains Task and Course classes
│ Implements Object-Oriented Programming concepts
│
├── database.py
│ Manages SQLite database
│ Handles create, read, update, and delete operations
│
└── README.md
|   Project documentation & Guide
└── .gitattributes
|   Git configuration file (Auto-generated)

---

## How to Run the Project
1. Make sure **Python 3.x** is installed on your system  
2. Download or clone this repository  
3. Open the project folder  
4. Run the application using the command:
```bash
   python app.py

---


Author: Shraddha (BCA Student)
