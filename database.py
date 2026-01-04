import sqlite3

# Database file for Academic Task Manager
# Handles all database operations using SQLite
class DatabaseManager:
    def __init__(self, db_name="academic_pro.db"):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.setup_db()

    # Create required tables if they do not exist
    def setup_db(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS courses (
                course_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                code TEXT UNIQUE
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                task_id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                due_date TEXT,
                priority TEXT,
                category TEXT,
                status TEXT DEFAULT 'Pending',
                course_id INTEGER,
                FOREIGN KEY(course_id) REFERENCES courses(course_id)
            )
        """)
        self.conn.commit()

    # Add new category/course to database
    def add_course(self, course_obj):
        try:
            self.cursor.execute(
                "INSERT INTO courses (name, code) VALUES (?, ?)",
                (course_obj.name, course_obj.code)
            )
            self.conn.commit()
        except Exception:
            pass   # Ignore duplicate category entry

    def delete_course(self, course_code):
        self.cursor.execute(
            "DELETE FROM tasks WHERE category = ?",
            (course_code,)
        )
        self.cursor.execute(
            "DELETE FROM courses WHERE code = ?",
            (course_code,)
        )
        self.conn.commit()

    def add_task(self, title, due, prio, cat, cid):
        self.cursor.execute(
            "INSERT INTO tasks (title, due_date, priority, category, course_id) VALUES (?, ?, ?, ?, ?)",
            (title, due, prio, cat, cid)
        )
        self.conn.commit()

    def update_task_details(self, tid, title, due, prio):
        self.cursor.execute(
            "UPDATE tasks SET title = ?, due_date = ?, priority = ? WHERE task_id = ?",
            (title, due, prio, tid)
        )
        self.conn.commit()

    def mark_done(self, tid):
        self.cursor.execute(
            "UPDATE tasks SET status = 'Done' WHERE task_id = ?",
            (tid,)
        )
        self.conn.commit()

    def delete_task(self, tid):
        self.cursor.execute(
            "DELETE FROM tasks WHERE task_id = ?",
            (tid,)
        )
        self.conn.commit()

    def get_tasks(self):
        return self.cursor.execute("""
            SELECT
                t.task_id,
                t.title,
                t.due_date,
                t.priority,
                t.category,
                t.status,
                t.course_id,
                c.code
            FROM tasks t
            LEFT JOIN courses c ON t.course_id = c.course_id
        """).fetchall()
