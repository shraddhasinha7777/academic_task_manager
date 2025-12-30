import datetime
# Course class represents academic category / goals.
class Course:
    def __init__(self, course_id, name, code, instructor="N/A", credits=0):
        self.course_id = course_id
        self.name = name
        self.code = code
        self.instructor = instructor
        self.credits = credits
        
# Task class represents an academic task with deadline and priority
class Task:
    def __init__(self, task_id, title, due_date, priority, category,
                 status="Pending", course_id=None, description=""):
        self.task_id = task_id
        self.title = title
        self.due_date = due_date
        self.priority = priority
        self.category = category
        self.status = status
        self.course_id = course_id
        self.description = description
        self.created_at = datetime.datetime.now().strftime("%Y-%m-%d")

    # Calculate remaining days before deadline
    def get_days_left(self):
        try:
            due = datetime.datetime.strptime(str(self.due_date), "%Y-%m-%d").date()
            today = datetime.date.today()
            return (due - today).days
        except:
            # If date format is wrong, return 0
            return 0

    # Calculate smart priority score based on urgency and importance
    def calculate_smart_score(self):
        try:
            days_left = self.get_days_left()

            # Urgency calculation
            if days_left <= 0:
                urgency = 100 + abs(days_left) * 10
            else:
                urgency = max(0, 100 - (days_left * 10))

            # Importance based on priority
            if self.priority == "High":
                p_val = 3
            elif self.priority == "Medium":
                p_val = 2
            else:
                p_val = 1

            importance = p_val * 10

            # Final smart score
            score = (urgency * 0.7) + (importance * 0.3)
            return int(score)
        except:
            return 0
