# Academic Task Manager  
**Student Productivity Tool (BCA Minor Project)**

---

## Project Overview

Academic Task Manager is a desktop-based task management application developed using the Python programming language. The system is designed to assist students and individuals in organizing academic tasks efficiently, managing multiple deadlines, and reducing decision fatigue through intelligent task prioritization.

The application uses a rule-based smart priority mechanism that evaluates task urgency along with user-defined priority levels to identify important and time-sensitive tasks. Unlike traditional to-do list applications that merely record tasks, this system actively supports decision-making by providing visual indicators, priority scores, and real-time productivity feedback, helping users focus on the most critical tasks first.

The Academic Task Manager integrates Object-Oriented Programming (OOP) principles, a Tkinter-based graphical user interface, and SQLite-based local data storage to deliver a structured, reliable, and user-friendly desktop application. By combining intelligent logic with visual feedback and offline data persistence, the system aims to enhance productivity, focus, and effective time management.

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


---


 **Screenshots of the working application are provided in the final project report.**
  ## Dashboard Preview
<img width="1914" height="1018" alt="image" src="https://github.com/user-attachments/assets/4cd9abec-e21d-49aa-8b7f-633998807a6d" />


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

# How to Run the Project
1. Make sure **Python 3.x** is installed on your system  
2. Download or clone this repository  
3. Open the project folder  
4. Run the application using the command:
```bash
   python app.py

Tested on Windows OS.
---


Author: Shraddha 
