import json
import schedule
import time
from datetime import datetime
import smtplib
from email.message import EmailMessage
from prompt_toolkit import prompt

TASKS_FILE = "tasks.json"

EMAIL = "monish282003@gmail.com"  # Replace with your email
PASSWORD = "mqkw ctrr gigt eqnl"  # Replace with your app password (generate from Google App Passwords)
TO_EMAIL = "monish.m2021@vitstudent.ac.in"  # Email to receive notifications

def load_tasks():
    try:
        with open(TASKS_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_tasks(tasks):
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=4)

def add_task():
    task_name = prompt("Task Name: ")
    due_date = prompt("Due Date (YYYY-MM-DD HH:MM): ")

    tasks = load_tasks()
    tasks.append({"task": task_name, "due_date": due_date, "completed": False})
    save_tasks(tasks)
    
    print(f"Task Added: {task_name}")
    
    send_email(TO_EMAIL, "New Task Added", f"A new task has been added:\n\nTask: {task_name}\nDue Date: {due_date}")

def list_tasks():
    tasks = load_tasks()
    print("\n Your To-Do List:")
    for i, task in enumerate(tasks, 1):
        status = "" if task["completed"] else ""
        print(f"{i}. {task['task']} - Due: {task['due_date']} [{status}]")

def complete_task():
    list_tasks()
    task_num = int(prompt("\nEnter Task Number to Complete: ")) - 1
    tasks = load_tasks()
    tasks[task_num]["completed"] = True
    save_tasks(tasks)
    
    print(f"Task Completed: {tasks[task_num]['task']}")

def remove_task():
    list_tasks()
    task_num = int(prompt("\nEnter Task Number to Remove: ")) - 1
    tasks = load_tasks()
    removed_task = tasks.pop(task_num)
    save_tasks(tasks)
    
    print(f"Task Removed: {removed_task['task']}")
    
    send_email(TO_EMAIL, "Task Removed", f"The task '{removed_task['task']}' has been removed.")

def check_due_tasks():
    tasks = load_tasks()
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    for task in tasks:
        if task["due_date"] == now and not task["completed"]:
            print(f"Task Reminder: {task['task']}")
            send_email(TO_EMAIL, "Task Reminder", f"Reminder: '{task['task']}' is due now!")

def check_due_tasks_at_2_15():
    tasks = load_tasks()
    now_date = datetime.now().strftime("%Y-%m-%d")
    
    due_tasks = [task for task in tasks if task["due_date"].startswith(now_date) and not task["completed"]]

    if due_tasks:
        task_list = "\n".join([task["task"] for task in due_tasks])
        print(f"Daily Task Reminder:\n{task_list}")
        send_email(TO_EMAIL, "Daily Task Reminder", f"The following tasks are due today:\n\n{task_list}")

def send_email(to_email, subject, body):
    try:
        msg = EmailMessage()
        msg["From"] = EMAIL
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.set_content(body)

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL, PASSWORD)
            server.send_message(msg)

        print("Email Sent!")
    except Exception as e:
        print(f"Email Error: {e}")

schedule.every().minute.do(check_due_tasks)  
schedule.every().day.at("14:15").do(check_due_tasks_at_2_15) 

def main():
    while True:
        print("\n📝 To-Do List CLI")
        print("Add Task")
        print("List Tasks")
        print("Complete Task")
        print("Remove Task")
        print("Exit")

        choice = prompt("\nEnter your choice: ")

        if choice == "1":
            add_task()
        elif choice == "2":
            list_tasks()
        elif choice == "3":
            complete_task()
        elif choice == "4":
            remove_task()
        elif choice == "5":
            print("Exiting To-Do List CLI...")
            break
        else:
            print("Invalid choice. Please try again.")

        # Run scheduled tasks
        schedule.run_pending()
        time.sleep(1)  # Avoids high CPU usage

if __name__ == "__main__":
    main()
