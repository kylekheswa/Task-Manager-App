import datetime
import hashlib
# Dictionary to store user credentials
users = {}

# List to store task data
tasks = []



# Function to hash a password
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Function to check if a username and password match
def check_credentials(username, password):
    return username in users and users[username] == hash_password(password)

# During user registration, store the hashed password
def register_user(users):
    while True:
        new_username = input("Enter a new username: ")
        
        if username_exists(new_username, users):
            print("Username already exists.")
        else:
            new_password = input("Enter a new password: ")
            confirm_password = input("Confirm the password: ")

            if new_password == confirm_password:
                users[new_username] = hash_password(new_password)
                with open('user.txt', 'a') as user_file:
                    user_file.write(f"{new_username}, {hash_password(new_password)}\n")
                print("User registered successfully!")
                break
            else:
                print("Passwords do not match.")

# During login, compare the hashed password
def login():
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    # Load user data from user.txt file
    with open('user.txt', 'r') as user_file:
        for line in user_file:
            user_data = line.strip().split(', ')
            users[user_data[0]] = user_data[1]

    if check_credentials(username, password):
        print("Login successful!")
        return username
    else:
        print("Invalid login. Please try again.")
        return None

# Load task data from tasks.txt file
with open('tasks.txt', 'r') as task_file:
    for line in task_file:
        task_data = line.strip().split(', ')
        tasks.append(task_data)

def edit_task(username, task_title_to_edit):
    """
    Function to edit a task.
    """
    for task in tasks:
        if task[0] == username and task[1] == task_title_to_edit:
            new_status = input("Enter the new status (Yes/No): ")
            task[5] = new_status
            print("Task edited successfully!")
            break
    else:
        print("Task not found or you don't have permission to edit it.")

def generate_task_overview():
    """
    Function to generate task_overview.txt.
    """
    total_tasks = len(tasks)
    completed_tasks = sum(1 for task in tasks if task[5] == 'Yes')
    uncompleted_tasks = total_tasks - completed_tasks
    overdue_tasks = sum(1 for task in tasks if task[5] == 'No' and datetime.datetime.now() > datetime.datetime.strptime(task[4], '%d %b %Y'))
    overdue_percentage = (overdue_tasks / total_tasks) * 100 
    incomplete_percentage = (uncompleted_tasks / total_tasks) * 100 
    # Write task overview data to task_overview.txt
    with open('task_overview.txt', 'w') as overview_file:
        overview_file.write(f"Total number of tasks: {total_tasks}\n")
        overview_file.write(f"Total number of completed tasks: {completed_tasks}\n")
        overview_file.write(f"Total number of uncompleted tasks: {uncompleted_tasks}\n")
        overview_file.write(f"Total number of overdue tasks: {overdue_tasks}\n")
        overview_file.write(f"Percentage of tasks that are overdue: {overdue_percentage:.2f}%\n")
        overview_file.write(f"Percentage of tasks that are incomplete: {incomplete_percentage:.2f}%\n")

def generate_user_overview():
    """
    Function to generate user_overview.txt.
    """
    total_users = len(users)
    total_assigned_tasks = {}
    completed_assigned_tasks = {}
    uncompleted_assigned_tasks = {}
    overdue_assigned_tasks = {}

    # Calculate user-specific task statistics
    for task in tasks:
        assigned_to = task[0]
        if assigned_to not in total_assigned_tasks:
            total_assigned_tasks[assigned_to] = 0
            completed_assigned_tasks[assigned_to] = 0
            uncompleted_assigned_tasks[assigned_to] = 0
            overdue_assigned_tasks[assigned_to] = 0
        total_assigned_tasks[assigned_to] += 1
        if task[5] == 'Yes':
            completed_assigned_tasks[assigned_to] += 1
        elif task[5] == 'No':
            uncompleted_assigned_tasks[assigned_to] += 1
            if datetime.datetime.now() > datetime.datetime.strptime(task[4], '%d %b %Y'):
                overdue_assigned_tasks[assigned_to] += 1

    # Write user overview data to user_overview.txt
    with open('user_overview.txt', 'w') as user_overview_file:
        user_overview_file.write(f"Total number of users: {total_users}\n")
        user_overview_file.write(f"Total number of tasks: {len(tasks)}\n")
        for username in users:
            user_overview_file.write(f"User: {username}\n")
            user_overview_file.write(f"Total number of tasks assigned: {total_assigned_tasks.get(username, 0)}\n")
            user_overview_file.write(f"Percentage of total tasks assigned: {total_assigned_tasks.get(username, 0) / len(tasks) * 100:.2f}%\n")
            user_overview_file.write(f"Percentage of completed tasks: {completed_assigned_tasks.get(username, 0) / total_assigned_tasks.get(username, 1) * 100:.2f}%\n")
            user_overview_file.write(f"Percentage of uncompleted tasks: {uncompleted_assigned_tasks.get(username, 0) / total_assigned_tasks.get(username, 1) * 100:.2f}%\n")
            user_overview_file.write(f"Percentage of overdue tasks: {overdue_assigned_tasks.get(username, 0) / total_assigned_tasks.get(username, 1) * 100:.2f}%\n")
            user_overview_file.write("\n")

def username_exists(username, users):
    """
    Function to check if a username already exists.
    """
    return username in users

def register_user(users):
    """
    Function to register a new user.
    """
    while True:
        new_username = input("Enter a new username: ")
        
        if username_exists(new_username, users):
            print("Username already exists.")
        else:
            new_password = input("Enter a new password: ")
            confirm_password = input("Confirm the password: ")

            if new_password == confirm_password:
                users[new_username] = new_password
                with open('user.txt', 'a') as user_file:
                    user_file.write(f"{new_username}, {new_password}\n")
                print("User registered successfully!")
                break
            else:
                print("Passwords do not match.")

def add_task(username):
    """
    Function to add a task.
    """
    assigned_to = input("Enter the username of the person the task is assigned to: ")
    task_title = input("Enter the title of the task: ")
    task_description = input("Enter the description of the task: ")
    due_date = input("Enter the due date of the task (e.g., 31 Dec 2023): ")
    current_date = datetime.datetime.now().strftime('%d %b %Y')

    # Append the new task to the tasks list and write it to tasks.txt
    with open('tasks.txt', 'a') as task_file:
        task_file.write(f"{assigned_to}, {task_title}, {task_description}, {current_date}, {due_date}, No\n")

    print("Task added successfully!")

def view_all_tasks():
    """
    Function to view all tasks.
    """
    with open('tasks.txt', 'r') as task_file:
        for line in task_file:
            username, title, description, assigned_date, due_date, status = line.strip().split(', ')
            print(f"Username: {username}")
            print(f"Title: {title}")
            print(f"Description: {description}")
            print(f"Assigned Date: {assigned_date}")
            print(f"Due Date: {due_date}")
            print(f"Status: {status}")
            print()

def view_my_tasks(username):
    """
    Function to view tasks assigned to the user.
    """
    tasks_assigned_to_user = [task_data for task_data in tasks if task_data[0] == username]

    if not tasks_assigned_to_user:
        print("You have no tasks assigned.")
        return

    while True:
        print("Tasks assigned to you:")
        for i, task_data in enumerate(tasks_assigned_to_user):
            print(f"{i + 1}. Title: {task_data[1]}")
            print(f"   Description: {task_data[2]}")
            print(f"   Assigned Date: {task_data[3]}")
            print(f"   Due Date: {task_data[4]}")
            print(f"   Status: {task_data[5]}")
        print("-1. Return to the main menu")

        choice = input("Enter the number of the task to view (or -1 to return to the main menu): ")
        
        if choice == '-1':
            return
        elif choice.isdigit():
            choice = int(choice)
            if 1 <= choice <= len(tasks_assigned_to_user):
                task_data = tasks_assigned_to_user[choice - 1]
                print(f"Title: {task_data[1]}")
                print(f"Description: {task_data[2]}")
                print(f"Assigned Date: {task_data[3]}")
                print(f"Due Date: {task_data[4]}")
                print(f"Status: {task_data[5]}")
                print("1. Mark task as complete")
                print("2. Edit task")
                print("3. Return to task list")

                task_choice = input("Enter your choice (1/2/3): ")
                
                if task_choice == '1':
                    if task_data[5] == 'No':
                        task_data[5] = 'Yes'
                        print("Task marked as complete successfully!")
                        # Update the tasks.txt file with the changes
                        update_tasks_file()
                    else:
                        print("This task has already been completed.")
                elif task_choice == '2':
                    if task_data[5] == 'No':
                        edit_option = input("What would you like to edit (username/due date)? ").lower()
                        if edit_option == 'username':
                            new_assigned_to = input("Enter the new username: ")
                            task_data[0] = new_assigned_to
                            print("Username updated successfully!")
                        elif edit_option == 'due date':
                            new_due_date = input("Enter the new due date (e.g., 31 Dec 2023): ")
                            task_data[4] = new_due_date
                            print("Due date updated successfully!")
                        else:
                            print("Invalid edit option. Please choose 'username' or 'due date'.")
                    else:
                        print("This task has already been completed and cannot be edited.")
                elif task_choice == '3':
                    pass  # Return to the task list
                else:
                    print("Invalid choice. Please select 1, 2, or 3.")
            else:
                print("Invalid task number. Please try again.")
        else:
            print("Invalid input. Please enter a number or -1 to return to the main menu.")

def update_tasks_file():
    """
    Function to update the tasks.txt file with the changes made to tasks.
    """
    # Rewrite the tasks.txt file with the updated task data
    with open('tasks.txt', 'w') as task_file:
        for task_data in tasks:
            task_file.write(', '.join(task_data) + '\n')

def view_statistics(username, users):
    """
    Function to view statistics.
    """
    if username == 'admin':
        total_users = len(users)
        with open('tasks.txt', 'r') as task_file:
            total_tasks = sum(1 for _ in task_file)
        print(f"Total number of users: {total_users}")
        print(f"Total number of tasks: {total_tasks}")

# menu section
username = login()
if username:
    while True:
        menu = input('''Select one of the following options:
        r - register a user
        a - add task
        va - view all tasks
        vm - view my tasks
        s - statistics
        gr - generate reports
        e - exit
        : ''').lower()

        if menu == 'r':
            register_user(users)
        
        elif menu == 'a':
            add_task(username)
        
        elif menu == 'va':
            view_all_tasks()

        elif menu == 'gr':
            generate_user_overview()
            generate_task_overview()
            print("Reports generated successfully!")

        elif menu == 'vm':
            view_my_tasks(username)
        
        elif menu == 's':
            if username == 'admin':
                generate_user_overview()
                generate_task_overview()
                print("Reports generated successfully!")
                view_statistics(username, users)
            else:
                print("You do not have permission to view statistics.")

        elif menu == 'e':
            print('Goodbye!!!')
            break

        else:
            print("You have entered an invalid input. Please try again")
