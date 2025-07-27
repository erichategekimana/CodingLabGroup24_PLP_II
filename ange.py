from effects import type_print, loading_spinner, styled_input

def view_child_progress(parent_id):
    type_print("Yello")

def view_messages(parent_id):
    type_print("Messages")

def parent_dashboard():
    parent_id = 1
    # Initialize database
    print("\nWelcome to the Teacher Dashboard!")
    # Main loop for dashboard menu
    while True:
        print("\n" + "="*35)
        print(" PARENT DASHBOARD ")
        print("="*35)
        print("1. View My Child Progress")
        print("2. View Messages")
        print("3. Logout")
        # Get user choice
        choice = input("\nSelect option (1-3): ").strip()
        if choice == "1":
            view_child_progress(parent_id)
        if choice == "2":
            view_messages(parent_id)
        elif choice == "3":
            print("Logging out...")
            break
        else:
            print("Invalid option. Try again.")
# Main function to initialize database and start dashboard
def main():
    # Ensure the database is initialized before starting the dashboard
    try:
        parent_dashboard()
    except Exception as e:
        print(f"Application error: {e}")
# Ensure the script runs only if executed directly
if __name__ == "__main__":
    main()