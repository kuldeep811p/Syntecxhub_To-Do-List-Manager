"""
===========================================
  PROJECT 3 - To-Do List Manager
  By: SyntecxHub Student
===========================================
  Features:
    - Add tasks with optional due dates & tags
    - View all tasks (with filters)
    - Mark tasks as done
    - Delete tasks
    - Tasks are saved to a JSON file (persist after restart)
===========================================
"""

import json
import os
from datetime import datetime

# ─────────────────────────────────────────
#  CONSTANTS
# ─────────────────────────────────────────

FILE_NAME = "tasks.json"   # The file where tasks are stored


# ─────────────────────────────────────────
#  FILE I/O FUNCTIONS  (Input / Output)
# ─────────────────────────────────────────

def load_tasks():
    """
    Read tasks from the JSON file.
    If the file doesn't exist yet, return an empty list.
    """
    if not os.path.exists(FILE_NAME):
        return []                          # First run — no file yet

    try:
        with open(FILE_NAME, "r") as f:
            return json.load(f)            # Parse JSON → Python list
    except (json.JSONDecodeError, IOError):
        print("⚠️  Could not read tasks file. Starting fresh.")
        return []


def save_tasks(tasks):
    """
    Write the tasks list to the JSON file.
    indent=2 makes the file human-readable.
    """
    try:
        with open(FILE_NAME, "w") as f:
            json.dump(tasks, f, indent=2)
    except IOError:
        print("⚠️  Could not save tasks. Check file permissions.")


# ─────────────────────────────────────────
#  LOGIC FUNCTIONS  (the brains)
# ─────────────────────────────────────────

def create_task(title, due_date=None, tags=None):
    """
    Build a single task dictionary.
    Each task looks like:
    {
        "id"       : 1,
        "title"    : "Buy groceries",
        "done"     : False,
        "due_date" : "2025-12-31",   ← optional
        "tags"     : ["shopping"]    ← optional
        "created"  : "2025-05-07"
    }
    """
    tasks = load_tasks()

    # Auto-increment ID
    new_id = max((t["id"] for t in tasks), default=0) + 1

    task = {
        "id"      : new_id,
        "title"   : title,
        "done"    : False,
        "due_date": due_date,
        "tags"    : tags if tags else [],
        "created" : datetime.today().strftime("%Y-%m-%d"),
    }

    tasks.append(task)
    save_tasks(tasks)
    return task


def get_all_tasks():
    """Return all tasks from the file."""
    return load_tasks()


def find_task_by_id(task_id, tasks):
    """
    Search for a task by its ID.
    Returns the task dict, or None if not found.
    """
    for task in tasks:
        if task["id"] == task_id:
            return task
    return None


def mark_task_done(task_id):
    """
    Set done=True for the task with the given ID.
    Returns True if successful, False if not found.
    """
    tasks = load_tasks()
    task  = find_task_by_id(task_id, tasks)

    if task is None:
        return False

    task["done"] = True
    save_tasks(tasks)
    return True


def delete_task(task_id):
    """
    Remove a task from the list by its ID.
    Returns True if successful, False if not found.
    """
    tasks    = load_tasks()
    new_list = [t for t in tasks if t["id"] != task_id]

    if len(new_list) == len(tasks):
        return False   # Nothing was removed → ID didn't exist

    save_tasks(new_list)
    return True


# ─────────────────────────────────────────
#  DISPLAY HELPERS  (pretty printing)
# ─────────────────────────────────────────

def display_task(task):
    """Print a single task in a readable format."""
    status   = "✅" if task["done"]     else "⬜"
    due      = f"  📅 Due: {task['due_date']}" if task["due_date"] else ""
    tag_list = f"  🏷️  Tags: {', '.join(task['tags'])}" if task["tags"] else ""

    print(f"  {status} [{task['id']}] {task['title']}{due}{tag_list}")


def display_all_tasks(tasks, show_filter="all"):
    """
    Print all tasks with a header.
    show_filter can be: 'all' | 'pending' | 'done'
    """
    if show_filter == "pending":
        filtered = [t for t in tasks if not t["done"]]
        header   = "📋  PENDING TASKS"
    elif show_filter == "done":
        filtered = [t for t in tasks if t["done"]]
        header   = "✅  COMPLETED TASKS"
    else:
        filtered = tasks
        header   = "📋  ALL TASKS"

    print(f"\n  {'─'*35}")
    print(f"  {header}  ({len(filtered)} tasks)")
    print(f"  {'─'*35}")

    if not filtered:
        print("  (nothing here)")
    else:
        for task in filtered:
            display_task(task)

    print(f"  {'─'*35}\n")


# ─────────────────────────────────────────
#  MENU & USER INPUT  (CLI interface)
# ─────────────────────────────────────────

def get_int_input(prompt):
    """
    Ask the user for an integer.
    Keeps asking until a valid number is entered.
    """
    while True:
        value = input(prompt).strip()
        if value.isdigit():
            return int(value)
        print("  ⚠️  Please enter a valid number.")


def menu_add_task():
    """Handle the 'Add Task' flow."""
    print("\n  ── ADD NEW TASK ──")
    title = input("  Task title: ").strip()

    if not title:
        print("  ⚠️  Title cannot be empty!")
        return

    # Optional due date
    due_date = input("  Due date (YYYY-MM-DD) or press Enter to skip: ").strip()
    if due_date:
        # Validate the date format
        try:
            datetime.strptime(due_date, "%Y-%m-%d")
        except ValueError:
            print("  ⚠️  Invalid date format. Due date will be skipped.")
            due_date = None
    else:
        due_date = None

    # Optional tags
    raw_tags = input("  Tags (comma-separated) or press Enter to skip: ").strip()
    tags = [tag.strip() for tag in raw_tags.split(",") if tag.strip()] if raw_tags else []

    task = create_task(title, due_date, tags)
    print(f"\n  ✅ Task added! (ID: {task['id']})")


def menu_view_tasks():
    """Handle the 'View Tasks' flow."""
    print("\n  ── VIEW TASKS ──")
    print("  1. All tasks")
    print("  2. Pending only")
    print("  3. Done only")

    choice = input("\n  Choose filter (1-3): ").strip()
    tasks  = get_all_tasks()

    if choice == "2":
        display_all_tasks(tasks, show_filter="pending")
    elif choice == "3":
        display_all_tasks(tasks, show_filter="done")
    else:
        display_all_tasks(tasks, show_filter="all")


def menu_mark_done():
    """Handle the 'Mark as Done' flow."""
    print("\n  ── MARK TASK AS DONE ──")

    # Show pending tasks first so user can see IDs
    tasks = get_all_tasks()
    display_all_tasks(tasks, show_filter="pending")

    if not any(not t["done"] for t in tasks):
        return   # No pending tasks, nothing to mark

    task_id = get_int_input("  Enter Task ID to mark done: ")
    success = mark_task_done(task_id)

    if success:
        print(f"  ✅ Task {task_id} marked as done!")
    else:
        print(f"  ⚠️  Task with ID {task_id} not found.")


def menu_delete_task():
    """Handle the 'Delete Task' flow."""
    print("\n  ── DELETE TASK ──")

    tasks = get_all_tasks()
    display_all_tasks(tasks, show_filter="all")

    if not tasks:
        return

    task_id = get_int_input("  Enter Task ID to delete: ")

    # Confirm before deleting
    confirm = input(f"  Are you sure you want to delete task {task_id}? (y/n): ").strip().lower()
    if confirm != "y":
        print("  Deletion cancelled.")
        return

    success = delete_task(task_id)
    if success:
        print(f"  🗑️  Task {task_id} deleted.")
    else:
        print(f"  ⚠️  Task with ID {task_id} not found.")


def show_menu():
    """Print the main menu."""
    print("""
  ╔══════════════════════════════════╗
  ║       📝  TO-DO LIST MANAGER     ║
  ╠══════════════════════════════════╣
  ║  1.  ➕  Add a task              ║
  ║  2.  📋  View tasks              ║
  ║  3.  ✅  Mark task as done       ║
  ║  4.  🗑️   Delete a task           ║
  ║  5.  🚪  Exit                    ║
  ╚══════════════════════════════════╝""")


# ─────────────────────────────────────────
#  MAIN PROGRAM  (entry point)
# ─────────────────────────────────────────

def main():
    """
    The main loop — keeps showing the menu
    until the user chooses to exit.
    """
    print("\n  Welcome to the To-Do List Manager! 🎯")

    while True:
        show_menu()
        choice = input("  Enter your choice (1-5): ").strip()

        if choice == "1":
            menu_add_task()

        elif choice == "2":
            menu_view_tasks()

        elif choice == "3":
            menu_mark_done()

        elif choice == "4":
            menu_delete_task()

        elif choice == "5":
            print("\n  👋 Goodbye! Your tasks have been saved.\n")
            break   # Exit the while loop → program ends

        else:
            print("  ⚠️  Invalid choice. Please enter 1 to 5.")


# ─────────────────────────────────────────
#  Run the program
# ─────────────────────────────────────────
if __name__ == "__main__":
    main()
