# Academic Task Manager
# Main GUI application file
# Handles user interface, task logic, and database interaction
import tkinter as tk
from tkinter import ttk, messagebox
import datetime
from datetime import datetime as dt_obj # Date validation
from database import DatabaseManager # Import database manager and model classes
from models import Course, Task

# Main application class controlling GUI & logic
class AcademicManagerApp: 
    def __init__(self, root):
        # Constructor: initializes window, database and default settings
        self.root = root
        self.root.title("Academic Task Manager")
        self.root.geometry("1300x850")
        
        self.db = DatabaseManager() # Create database connection object
        self.is_widget = False
        self.is_dark_mode = False
        self.blink_state = True 
        self.editing_id = None 
        
        self.colors = {  # Color configuration used in UI
            "bg": "#ffffff",
            "sidebar": "#170A42",
            "accent": "#3b82F6",
            "header": "#ffffff",
            "urgent_red": "#f69d9d", 
            "medium_yellow": "#fef08a", 
            "low_green": "#bbf7d0",
            "clock_blue": "#3b82F6",
            "theme_dark": "#03327d",
            "widget_purple": "#a01bd0",
            "simulation_yellow": "#ECD139",
            "overdue_dark": "#7f1d1d"
        }

        # Creates and arranges all GUI components 
        self.setup_ui()
        self.update_clock()
        self.blink_effect() 
        self.refresh_tasks()

    def setup_ui(self):
        # Configure main background
        self.root.configure(bg=self.colors["bg"])
        
        # Sidebar
        self.sidebar = tk.Frame(self.root, bg=self.colors["sidebar"], width=300)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)
        # Sidebar title
        tk.Label(self.sidebar, text="DASHBOARD", fg=self.colors["accent"], bg=self.colors["sidebar"], 
                 font=("Helvetica", 20, "bold")).pack(pady=(25, 20))
        
        # Category / Goal Section 
        self.create_sidebar_header("ADD CATEGORY / GOAL")
        self.ent_course_code = self.create_sidebar_entry("e.g. Work, Gym")
        tk.Button(self.sidebar, text="+ Register Category", bg=self.colors["accent"], fg="white", font=("Helvetica", 9, "bold"), 
                  command=self.register_course, relief="flat", pady=5).pack(fill="x", padx=25, pady=(0, 5))
        tk.Button(self.sidebar, text="- Remove Selected", bg="#fc4e4e", fg="white", font=("Helvetica", 9, "bold"), 
                  command=self.remove_course, relief="flat", pady=5).pack(fill="x", padx=25, pady=(0, 20))

        # New task input section (title, category, deadline, priority)
        self.create_sidebar_header("NEW TASK")
        self.ent_title = self.create_sidebar_entry("Task Title")
        self.course_var = tk.StringVar()
        self.course_drop = ttk.Combobox(self.sidebar, textvariable=self.course_var, state="readonly")
        self.course_drop.pack(fill="x", padx=25, pady=(5, 15))
        
        self.ent_due = tk.Entry(self.sidebar, bg="#FFFFFF", fg="black", insertbackground="black", bd=0)
        self.ent_due.insert(0, str(datetime.date.today()))
        self.ent_due.pack(fill="x", padx=25, pady=(5, 15), ipady=8)
        
        self.prio_var = tk.StringVar(value="Medium")
        ttk.Combobox(self.sidebar, textvariable=self.prio_var, values=("High", "Medium", "Low"), state="readonly").pack(fill="x", padx=25, pady=(5, 15))
        
        tk.Button(self.sidebar, text="SAVE TO DATABASE", bg="#0abe13", fg="white", font=("Helvetica", 10, "bold"), 
                  command=self.save_task, relief="flat", pady=10).pack(fill="x", padx=25, pady=20)

        # Sticky note panel for quick reminders and task planning
        self.create_sidebar_header("QUICK REMINDER / SMART DECISION")
        self.sticky_frame = tk.Frame(self.sidebar, bg="#e0fcfa", padx=10, pady=10)
        self.sticky_frame.pack(padx=25, fill="x")
        self.sticky_text = tk.Text(self.sticky_frame, bg="#dcf3f8", fg="#4100E4", font=("Helvetica", 9), height=10, bd=0)
        self.sticky_text.pack(fill="both")

        # Main dashboard content area
        self.content = tk.Frame(self.root, bg=self.colors["bg"])
        self.content.pack(side="right", fill="both", expand=True)
        
        self.header = tk.Frame(self.content, bg=self.colors["header"], height=140)
        self.header.pack(fill="x")
        
        self.greet_frame = tk.Frame(self.header, bg="white")
        self.greet_frame.pack(side="left", padx=35, pady=15)
        self.greet_lbl = tk.Label(self.greet_frame, text="Hello!", font=("Helvetica", 20, "bold"), bg="white", fg="#0070fa")
        self.greet_lbl.pack(anchor="w")
        self.slogan_lbl = tk.Label(self.greet_frame, text="Ready to crush your goals today ? 🚀", font=("Helvetica", 12, "bold"), bg="white", fg="purple")
        self.slogan_lbl.pack(anchor="w")

        self.info_panel = tk.Frame(self.header, bg="white")
        self.info_panel.pack(side="left", padx=50, pady=15)
        
        self.badge_lbl = tk.Label(self.info_panel, text="🏅 Badge: None", font=("Helvetica", 11, "bold"), bg="white", fg="#555555")
        self.badge_lbl.pack(anchor="w")

        btn_container = tk.Frame(self.header, bg="white")
        btn_container.pack(side="right", padx=35)

        self.clock_lbl = tk.Label(btn_container, text="00:00:00 PM", font=("Consolas", 12, "bold"), bg=self.colors["clock_blue"], fg="white", padx=15, pady=5)
        self.clock_lbl.pack(side="right", padx=5)

        tk.Button(btn_container, text="🤔 WHAT IF I SKIP TODAY ?", bg=self.colors["simulation_yellow"], fg="#885A22", font=("Helvetica", 8, "bold"), command=self.simulate_skip, relief="flat", padx=10, pady=5).pack(side="right", padx=5)
        tk.Button(btn_container, text="THEME", bg=self.colors["theme_dark"], fg="white", font=("Helvetica", 8, "bold"), command=self.toggle_theme, relief="flat", padx=10, pady=5).pack(side="right", padx=5)
        tk.Button(btn_container, text="WIDGET", bg=self.colors["widget_purple"], fg="white", font=("Helvetica", 8, "bold"), command=self.toggle_widget, relief="flat", padx=10, pady=5).pack(side="right", padx=5)

        self.prog_container = tk.Frame(self.content, bg="white")
        self.prog_container.pack(fill="x", padx=35)
        
        self.header_prog_lbl = tk.Label(self.prog_container, text="Efficiency Score: 0%", font=("Helvetica", 10, "bold"), bg="white", fg="#201E1E")
        self.header_prog_lbl.pack(anchor="w")
        self.header_progress = ttk.Progressbar(self.prog_container, length=280, mode='determinate')
        self.header_progress.pack(anchor="w", pady=(2, 5))

        self.deadline_frame = tk.Frame(self.content, bg=self.colors["bg"])
        self.deadline_frame.pack(fill="x", padx=35, pady=(20, 0))
        self.countdown_lbl = tk.Label(self.deadline_frame, text="⏳ Nearest Deadline: None", font=("Helvetica", 11, "bold"), bg=self.colors["bg"], fg="red")
        self.countdown_lbl.pack(anchor="w")

        self.smart_panel = tk.Frame(self.content, bg=self.colors["bg"])
        self.smart_panel.pack(fill="x", padx=35, pady=(5, 20))

        self.notebook = ttk.Notebook(self.content)
        self.notebook.pack(fill="both", expand=True, padx=35, pady=10)

        self.pending_tree = self.create_task_tree(self.notebook)
        self.done_tree = self.create_task_tree(self.notebook)
        self.notebook.add(self.pending_tree.master, text=" ⏳ Pending Tasks ")
        self.notebook.add(self.done_tree.master, text=" ✅ Completed Tasks ")

        self.footer = tk.Frame(self.content, bg=self.colors["bg"])
        self.footer.pack(fill="x", padx=35, pady=20)
        tk.Button(self.footer, text="MARK FINISHED", bg="#0bab13", fg="white", command=self.mark_done).pack(side="left", padx=5)
        tk.Button(self.footer, text="EDIT TASK", bg="#4f8beb", fg="white", command=self.load_task_for_edit).pack(side="left", padx=5)
        tk.Button(self.footer, text="DELETE TASK", bg="#f53737", fg="white", command=self.delete_task).pack(side="left", padx=5)

        self.widget_view = tk.Frame(self.root, bg=self.colors["sidebar"])

    def load_task_for_edit(self):
        # Loads selected task details for editing
        sel = self.pending_tree.focus()
        if not sel:
            messagebox.showwarning("Selection Required", "Please select a task to edit!")
            return
        values = self.pending_tree.item(sel, 'values')
        self.editing_id = values[0] 
        self.ent_title.delete(0, tk.END); self.ent_title.insert(0, values[2])
        self.ent_due.delete(0, tk.END); self.ent_due.insert(0, values[4])
        self.prio_var.set(values[5])
        messagebox.showinfo("Edit Mode", "Modify details and click SAVE.")

    def save_task(self):
        # Saves a new task or updates an existing task
        t = self.ent_title.get().strip()
        d = self.ent_due.get().strip()
        p = self.prio_var.get()
        c = self.course_var.get()

        if not t or not c:
            messagebox.showerror("Validation Error", "Task Title and Category are required!")
            return

        try:
            dt_obj.strptime(d, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Invalid Date", "Use format: YYYY-MM-DD")
            return

        if self.editing_id:
            self.db.update_task_details(self.editing_id, t, d, p)
            self.editing_id = None
        else:
            res = self.db.cursor.execute("SELECT course_id FROM courses WHERE code=?", (c,)).fetchone()
            if res:
                self.db.add_task(t, d, p, c, res[0])

        self.ent_title.delete(0, tk.END)
        self.refresh_tasks()

    def refresh_tasks(self):
         # Refreshes task list, dashboard, and efficiency score
        if self.is_widget: return
        for i in self.pending_tree.get_children(): self.pending_tree.delete(i)
        for i in self.done_tree.get_children(): self.done_tree.delete(i)
        
        tasks = self.db.get_tasks()
        self.course_drop['values'] = [c[0] for c in self.db.cursor.execute("SELECT code FROM courses").fetchall()]
        
        # Prepares task lists for sticky note display
        high_prio_list = []
        other_prio_list = []

        total = len(tasks)
        if total == 0:
            self.update_sticky_note([], []) # Clear sticky note
            self.header_progress['value'] = 0
            self.header_prog_lbl.config(text="Efficiency Score: 0%")
            self.badge_lbl.config(text="🏅 Badge: None", fg="#888888") 
            self.countdown_lbl.config(text="⏳ Nearest Deadline: None")
            self.render_smart_dashboard([], 0) 
            return
        # Tracks completed tasks and nearest upcoming deadline
        done_count = 0; nearest_task = None; min_days = float('inf')
        for r in tasks:
            t_obj = Task(r[0], r[1], r[2], r[3], r[4], r[5], r[6])
            score = t_obj.calculate_smart_score(); days_left = t_obj.get_days_left()
            
            if r[5] != 'Done':
                # Categorizes pending tasks based on priority
                if r[3] == "High":
                    high_prio_list.append(r[1])
                else:
                    other_prio_list.append(r[1])

                if days_left < min_days: min_days = days_left; nearest_task = r[1]
                
                tag_list = []
                if days_left < 0: tag_list.append('overdue')
                elif r[3] == "High":
                    tag_list.append('high_prio')
                    if days_left <= 1: tag_list.append('blink_eligible')
                elif r[3] == "Medium": tag_list.append('med_prio')
                else: tag_list.append('low_prio')
                self.pending_tree.insert("", "end", values=(r[0], f"⭐ {score}", r[1], r[7], r[2], r[3]), tags=tuple(tag_list))
            else:
                done_count += 1
                self.done_tree.insert("", "end", values=(r[0], f"⭐ {score}", r[1], r[7], r[2], r[3]))
        
        # Updates efficiency score, badges, and nearest deadline display
        self.update_sticky_note(high_prio_list, other_prio_list)

        eff = int((done_count / total * 100)) if total > 0 else 0
        self.header_progress['value'] = eff; self.header_prog_lbl.config(text=f"Efficiency Score: {eff}%")
        
        if eff >= 80: self.badge_lbl.config(text="🏆 Badge: Top Performer", fg="#0fca18")
        elif eff >= 50: self.badge_lbl.config(text="👍 Badge: Consistent", fg="#f6b81b")
        else: self.badge_lbl.config(text="⚠ Badge: Needs Focus", fg="#555555")
        
        if nearest_task:
            day_text = "Today!" if min_days == 0 else f"({min_days} days left)"
            self.countdown_lbl.config(text=f"⏳ Nearest Deadline: {nearest_task} {day_text}")
        else: self.countdown_lbl.config(text="⏳ Nearest Deadline: None")
        self.render_smart_dashboard(tasks, eff)

    def update_sticky_note(self, high_tasks, other_tasks):
        # Displays top urgent and planned tasks in the sticky note
        self.sticky_text.config(state="normal")
        self.sticky_text.delete("1.0", tk.END)
        
        self.sticky_text.insert(tk.END, "• ⚡ Do Urgent:\n")
        if high_tasks:
            for task in high_tasks[:3]: # Show top 3
                self.sticky_text.insert(tk.END, f"  - {task}\n")
        else:
            self.sticky_text.insert(tk.END, "  (None)\n")
            
        self.sticky_text.insert(tk.END, "\n• 📅 Plan Later:\n")
        if other_tasks:
            for task in other_tasks[:3]: 
                self.sticky_text.insert(tk.END, f"  - {task}\n")
        else:
            self.sticky_text.insert(tk.END, "  (None)\n")
        self.sticky_text.config(state="disabled")

    def render_smart_dashboard(self, tasks, efficiency):
        # Displays focus task and system suggestions
        for w in self.smart_panel.winfo_children(): w.destroy()
        pending = [r for r in tasks if r[5] != 'Done']
        f_box_border = "#cccccc" if not pending else "red"
        f_box = tk.Frame(self.smart_panel, bg="white", highlightbackground=f_box_border, highlightthickness=2, padx=10, pady=10)
        f_box.pack(side="left", expand=True, fill="both", padx=10)
        tk.Label(f_box, text="⚡🎯 TODAY'S FOCUS", font=("Helvetica", 9, "bold"), fg="red" if pending else "#888888", bg="white").pack(anchor="w")
        focus_task = next((t for t in pending if t[3] == 'High'), pending[0] if pending else None)
        focus_text = focus_task[1] if focus_task else "Nothing to focus on! ✨"
        tk.Label(f_box, text=focus_text, font=("Helvetica", 11, "bold"), bg="white", wraplength=450).pack(anchor="w", pady=5)
        
        s_box = tk.Frame(self.smart_panel, bg="white", highlightbackground=self.colors["simulation_yellow"], highlightthickness=2, padx=10, pady=10)
        s_box.pack(side="left", expand=True, fill="both", padx=10)
        tk.Label(s_box, text="💡 SYSTEM SUGGESTION", font=("Helvetica", 9, "bold"), fg="#8f5d12", bg="white").pack(anchor="w")
        if not tasks: sugg_text = "Start adding your work! 🚀"
        elif not pending: sugg_text = "Relax, All completed! 🎉"
        elif efficiency < 50: sugg_text = "⚠️ Low efficiency! Plan High Priority tasks."
        else: sugg_text = "Good pace! Keep it up."
        tk.Label(s_box, text=sugg_text, font=("Helvetica", 10, "bold"), bg="white").pack(anchor="w", pady=5)

    def create_task_tree(self, parent): 
        # Creates task table with visual priority and status indicators
        container = tk.Frame(parent)
        cols = ("ID", "Score ⭐", "Title", "Category", "Deadline", "Priority")
        tree = ttk.Treeview(container, columns=cols, show="headings", height=10)
        for col in cols: tree.heading(col, text=col); tree.column(col, width=100, anchor="center")
        tree.column("Title", width=300, anchor="w"); tree.pack(fill="both", expand=True)
        tree.tag_configure('high_prio', background=self.colors["urgent_red"])
        tree.tag_configure('med_prio', background=self.colors["medium_yellow"])
        tree.tag_configure('low_prio', background=self.colors["low_green"])
        tree.tag_configure('blink', background="#fca5a5", foreground='red')
        tree.tag_configure('overdue', background=self.colors["overdue_dark"], foreground='white')
        return tree

    def toggle_widget(self): 
        # Toggles between full view and widget mode
        self.is_widget = not self.is_widget
        if self.is_widget:
            self.sidebar.pack_forget(); self.content.pack_forget(); self.root.geometry("300x480")
            self.root.attributes("-topmost", True); self.widget_view.pack(fill="both", expand=True); self.render_widget_content()
        else:
            self.widget_view.pack_forget(); self.root.attributes("-topmost", False); self.sidebar.pack(side="left", fill="y")
            self.content.pack(side="right", fill="both", expand=True); self.root.geometry("1300x850"); self.refresh_tasks()
    
    def render_widget_content(self): 
        # Displays compact widget interface
        for w in self.widget_view.winfo_children(): w.destroy()
        tk.Label(self.widget_view, text="STICKY NOTE", fg=self.colors["accent"], bg=self.colors["sidebar"], font=("Helvetica", 14, "bold")).pack(pady=10)
        note = tk.Text(self.widget_view, bg="#f9f9f9", fg="black", height=4, font=("Helvetica", 10))
        note.pack(padx=15, pady=5, fill="x"); note.insert("1.0", self.sticky_text.get("1.0", tk.END))
        self.widget_ent = tk.Entry(self.widget_view, bg="white", fg="black", font=("Helvetica", 10))
        self.widget_ent.pack(padx=15, pady=5, fill="x")
        tk.Button(self.widget_view, text="+ Add Urgent", bg="#0fca18", fg="white", font=("Helvetica", 8, "bold"), command=self.quick_add_task).pack(pady=5)
        for t in [t for t in self.db.get_tasks() if t[3]=="High" and t[5]!="Done"][:3]: 
            tk.Label(self.widget_view, text=f"• {t[1]}", fg="white", bg="#1e293b", font=("Helvetica", 9), anchor="w").pack(fill="x", padx=15)
        tk.Button(self.widget_view, text="CLOSE", bg=self.colors["accent"], fg="white", command=self.toggle_widget).pack(pady=15)

    def quick_add_task(self):
        # Quickly adds a high priority task
        title = self.widget_ent.get()
        if title:
            categories = [c[0] for c in self.db.cursor.execute("SELECT course_id FROM courses").fetchall()]
            if categories: self.db.add_task(title, str(datetime.date.today()), "High", "Urgent", categories[0]); self.render_widget_content()

    def update_clock(self):
        # Updates live clock and greeting message
        now = datetime.datetime.now()
        greeting = "Good Morning! ☀️" if now.hour < 12 else ("Good Afternoon! 🌤️" if now.hour < 17 else "Good Evening! 🌙")
        self.greet_lbl.config(text=greeting)
        self.clock_lbl.config(text=now.strftime("%I:%M:%S %p")); self.root.after(1000, self.update_clock)

    def blink_effect(self): 
        # Blinks urgent tasks for attention
        self.blink_state = not self.blink_state
        for i in self.pending_tree.get_children():
            tags = list(self.pending_tree.item(i, 'tags'))
            if 'blink_eligible' in tags:
                if self.blink_state:
                    if 'blink' not in tags: tags.append('blink')
                else:
                    if 'blink' in tags: tags.remove('blink')
                self.pending_tree.item(i, tags=tuple(tags))
        self.root.after(500, self.blink_effect)

    def mark_done(self): 
        # Marks selected task as completed
        sel = self.pending_tree.focus()
        if sel: self.db.mark_done(self.pending_tree.item(sel, 'values')[0]); self.refresh_tasks()

    def delete_task(self): 
        # Deletes selected task from database
        sel = self.pending_tree.focus() or self.done_tree.focus()
        if sel: 
            tree = self.pending_tree if self.pending_tree.focus() else self.done_tree
            self.db.delete_task(tree.item(sel, 'values')[0]); self.refresh_tasks()

    def remove_course(self): 
        # Removes selected category and its related tasks
        sel = self.course_var.get()
        if sel: self.db.delete_course(sel); self.course_var.set(""); self.refresh_tasks()

    def register_course(self):
         # Registers a new category in the database 
        c = self.ent_course_code.get().strip()
        if c: self.db.add_course(Course(None, c, c)); self.refresh_tasks()

    def toggle_theme(self): 
        # Toggles between light and dark theme
        self.is_dark_mode = not self.is_dark_mode
        c = "#170A42" if self.is_dark_mode else "#ffffff"
        self.root.configure(bg=c); self.content.configure(bg=c); self.refresh_tasks()

    def create_sidebar_entry(self, placeholder):
          # Creates reusable input field for sidebar
        ent = tk.Entry(self.sidebar, bg="#FFFFFF", fg="black", insertbackground="black", bd=0)
        ent.pack(fill="x", padx=25, pady=(0, 10), ipady=8); return ent

    def create_sidebar_header(self, text):
        # Creates section heading in sidebar 
        tk.Label(self.sidebar, text=text, fg="#ffffff", bg=self.colors["sidebar"], font=("Helvetica", 8, "bold")).pack(anchor="w", padx=25, pady=(15, 5))
    
    def simulate_skip(self):  
        # Checks the risk of postponing today's tasks
        tasks = self.db.get_tasks()
        pending = [t for t in tasks if t[5] != 'Done']
        total_p = len(pending)
        today_s = str(datetime.date.today())
        high_alert = any(t[3] == "High" or t[2] <= today_s for t in pending)
        if total_p == 0: messagebox.showinfo("Chill", "Safe to take a break! 🏖️")
        elif high_alert: messagebox.showerror("Stop", "Backlog danger! Critical tasks need attention. 🛑")
        elif total_p > 2: messagebox.showerror("Stop", "Backlog danger! Too many pending tasks. 🛑")
        elif total_p == 2: messagebox.showwarning("Risk", "Small risk, manageable backlog tomorrow. ⚖️")
        else: messagebox.showinfo("Chill", "Only one minor task left. Safe to rest! 🏖️")
        
 # Main execution block of the application
if __name__ == "__main__":
    root = tk.Tk()
    app = AcademicManagerApp(root)
    root.mainloop()
