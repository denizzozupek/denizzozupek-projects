# Simple To-Do List Application

def display_tasks(tasks):
    """Displays the list of tasks."""
    if not tasks:
        print("Your task list is empty!")
    else:
        print("\nTask List:")
        for i, task in enumerate(tasks, 1):
            print(f"{i}. {task}")

def main():
    """Main function for managing the to-do list."""
    tasks = []

    while True:
        print("\nChoose an option:")
        print("1 - Add a Task")
        print("2 - Remove a Task")
        print("3 - View Tasks")
        print("4 - Exit")

        choice = input("Enter your choice (1-4): ").strip()

        if choice == "1":
            task = input("Enter the task you want to add: ").strip()
            if task:
                tasks.append(task)
                print(f"Task added: {task}")
            else:
                print("Task cannot be empty!")

        elif choice == "2":
            display_tasks(tasks)
            if tasks:
                try:
                    task_num = int(input("Enter the task number to remove: "))
                    if 1 <= task_num <= len(tasks):
                        removed_task = tasks.pop(task_num - 1)
                        print(f"Task removed: {removed_task}")
                    else:
                        print("Invalid task number.")
                except ValueError:
                    print("Please enter a valid number.")

        elif choice == "3":
            display_tasks(tasks)

        elif choice == "4":
            print("Exiting... Have a productive day!")
            break

        else:
            print("Invalid choice, please enter a number between 1-4.")

if __name__ == "__main__":
    main()
