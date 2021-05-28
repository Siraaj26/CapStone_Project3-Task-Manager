# Task 25: Task Manager 

# Function: Register new user - requires username and password
# Confirm password and write information to the user.txt file
# Only admin are allow to register new users

def reg_user():
    if username == "admin":
        print("Register New User")
        new_user = input("Please input the new user name: ")
        file = open("user.txt", "r+")

    # Prevent duplication of user names when registering a new user
        duplicate_found = False
        for line in file:
            split_line = line.split(",")
            user_check = split_line[0].strip()
            if new_user == user_check:
                print("That user name has already been taken")
                duplicate_found = True  

            # Checks passwords and confirms registration of the new user to the task text file
                new_password = input("Please input your password for the new user: ")
                if new_password == input("Confirm password: "):

                    # Writes back to user txt file
                    file.write("\n" + new_user + ", ") 
                    file.write(new_password)
                    file.close()
                    print("New user and password added")  
                else:
                    print("Password doesn't match.")
        else:
            print("\nOnly admins allowed to register users")
        

# Function - Add a task 
# If 'a' is chosen, ask for the username of the person who the task will be assigned to, title, description and due date of task
# Write the newly added task to the task.txt file
def add_task():
    print("Add A New Task")
    with open("user.txt") as fin:
        assigned_person = input("Who is the task assigned to: ")
        task_title = input("What is the title of task: ")
        task_detail = input("What is the details of the task: ")
        date_assigned = input("Please input today's date: ")
        task_due = input("Please input the task deadline: ")
        task_complete = input("Is the task completed? (Yes or No): ")
        with open("tasks.txt", "a") as task1:
            task1.write("\n" + assigned_person + ", " + task_title + ", " + task_detail + ", " + date_assigned + ", " + task_due + ", " + task_complete)
            print("New task added")

            
# Function - View all tasks
# If view all "va" is chosen, print all tasks for all users as output
def view_all():
    file = open("tasks.txt", "r+")
    for line in file:
        task = line.split(",")
        print("\nTask manager: " + task[0] + "\n" + "Task title: " + task[1] + "\n" + "Task details: " + task[2] + "\n" + "Date assigned: " + task[3] + "\n" + "Deadline: " + task[4] + "\n" + "Complete(Yes or No): " + task[5])


# Function - View tasks assigned to the user logged in
# Allow user to mark the task as complete (Yes), uncompleted tasks to be edited - task manager and due date  

# Algorithm
    # 1. Get list of lists of tasks of logged in user
    # 2. If the current index matches the task to edit
    # 3. Edit a task or return to menu

def view_mine():
    task_count = 0
    user_tasks = []
    not_user_task = []
    file = open("tasks.txt", "r+")
    print("")
    for line in file:
        task = line.split(", ")
        if task[0] == username:
            user_tasks.append(task)
            task_count+=1
            print(str(task_count) + "\nTask manager: " + task[0] + "\n" + "Task title: " + task[1] + "\n" + "Task details: " + task[2] + "\n" + "Date assigned: " + task[3] + "\n" + "Deadline: " + task[4] + "\n" + "Complete(Yes or No): " + task[5])
        else:
            not_user_task.append(task)

    choice = int(input("Select a task to amend or press '-1' to return to menu: "))
    # user selects -1 to return to menu
    if choice == -1: 
        menu()
    else:
        
        # Edit functionality below
        edit_type = input("Would you like to: \n(a) Mark the task as completed?\n(b) Mark the task as incomplete?\n(c) Edit the due date?\n(d) Edit the assigned task manager?\nEnter choice: ")
        current_index = 1

        print(user_tasks)
        print(not_user_task)

        if edit_type == "a":
            # user edits task as completed
            user_tasks[choice - 1][5] = "Yes\n"

        elif edit_type == "b":
            # user edits task as incomplete
            user_tasks[choice - 1][5] = "No\n"

        elif edit_type == "c":
            new_date = input("Enter the new due date")
            # user edits due date with a new date
            user_tasks[choice - 1][4] = f"{new_date}"
  
        elif edit_type == "d":
            # user edit the assigned task manager
            new_task_manager = input("Enter the new task manager")
            user_tasks[choice - 1][0] = f"{new_task_manager}"

        print(user_tasks)
        other_file = open("tasks.txt", "w")
        # open file to write back edited tasks

        for task in user_tasks:
            other_file.write(", ".join(task))
        other_file.write("\n")
        for task in not_user_task:
            other_file.write(", ".join(task))

        other_file.close()
                               

# Function - Display statistics for Admin user only 
# If display stats "ds" is chosen, display stats summary for users and tasks

def disp_stats():
    if username == "admin":
        print("Total number of users:")   
        file = open("user.txt", "r+")
        for line in file:
            file = file.readlines()
            print(len(file))

        print("Total number of tasks:")
        file = open("tasks.txt", "r+")
        for line in file:    
            file = file.readlines()
            print(len(file))


# Function - Log in
def login():
    # Boolean
    login_success = False

    # Request user inputs their username and password
    username = input("Please enter your username: ")
    password = input("Please enter your password: ")

    # Reads through the user text file for matches in username and password
    with open("user.txt", "r+") as file:
        # while login_success == False:
            for line in file:
                split_line = line.split(",")
                user_check = split_line[0].strip()
                pass_check = split_line[1].strip()
                if username == user_check and password == pass_check:
                    print("User logged in successfully")
                    return username
            file.seek(0)
    print("Incorrect credentials.")
    login()

     
# Function - Generate reports via two overview files (task and user)    
def gen_reports(username):

    # import package for overdue tasks calculation
    from datetime import datetime

    total_tasks = 0
    
    # open txt files and write back tasks to overview files for print out of statistics from overview files
    with open("task_overview.txt", "w") as write_task, open("user_overview.txt", "w") as write_user:
        with open("tasks.txt", "r+") as task_file, open("user.txt", "r+") as user_file:

            lines = task_file.readlines()
            total_tasks = len(lines)
            # counter for nos for calculations
            total_completed = 0
            total_incompleted = 0
            incomplete_overdue = 0
            num_tasks_user = 0
            completed_assigned_user = 0
            incomplete_overdue_user = 0
            
            for line in lines:
                tokens = line.strip("\n").split(", ")

                is_completed = tokens[5]
                print(tokens)

                if is_completed == "Yes":
                    # to determine completed tasks
                    total_completed += 1

                    if username == tokens[0]:
                        completed_assigned_user += 1
                                            
                else:
                    total_incompleted += 1

                # Get datetime objects of current date and deadline date
                current_date = datetime.now()
                deadline_str = tokens[4]

                deadline = datetime.strptime(deadline_str, "%d %b %Y")
                
                # print check to test correct data being passed for display later on under statistics
                is_overdue = current_date > deadline
                print(f"Is overdue? {is_overdue}")

                if is_completed == "No" and is_overdue:
                    # algo to determine no of overdue tasks
                    incomplete_overdue += 1

                    if tokens[0] == username:
                        incomplete_overdue_user =+1
                
                if username == tokens[0]:
                    num_tasks_user += 1
                                      
            task_file.seek(0)

            
            # print to check data is correct, to be removed once display statistics read from overview files
            print(total_tasks)
            print(total_completed)
            print(total_incompleted)
            print(incomplete_overdue)
                
        ############################################################################################################

            lines = user_file.readlines()
            total_user = len(lines)

            # percentage calculations

            # % user tasks against total tasks
            perc_user_tasks = (num_tasks_user / total_tasks) * 100

            # % completed user tasks against total completed tasks
            perc_user_tasks_completed = (completed_assigned_user / total_completed) * 100

            # % of tasks incompleted against total tasks
            perc_incomplete = (total_incompleted/ total_tasks) * 100

            # % user tasks incompleted against total tasks
            perc_incomplete_user = (incomplete_overdue_user/ total_tasks) * 100                        

            # print to check data is correct, to be removed once display statistics read from overview files
            print(f"user_tasks: {perc_user_tasks:.2f}")
            print(f"user_tasks_completed: {perc_user_tasks_completed:.2f}")
            print(f"Perc incomplete: {perc_incomplete:.2f}")


# Function - Menu items to displayed and selected by user
def menu(username):
    while True:
        print("\nPlease select one of the following options: ")
        print("r - register user") 
        print("a - add task") 
        print("va - view all tasks") 
        print("vm - view my tasks") 

        # only admin allowed to generate reports and statistics
        if username == "admin":
            print("gr - generate reports")
            print("ds - display statistics")
        print("e - exit")

        # user selection from menu choice
        menu_choice = input("\nWhat would you like to do: ").lower()
        if menu_choice == "r":
            reg_user()
        if menu_choice == "a":
            add_task()
        if menu_choice == "va":
            view_all()
        if menu_choice == "vm":
            view_mine()
        if menu_choice == "gr":
            gen_reports(username)
        if menu_choice == "ds":
            disp_stats()
        if menu_choice == "e":
            exit()
                
username = login()
menu(username)


# Function - Exit, to leave the program
def exit():
    pass
