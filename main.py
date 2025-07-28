from login import login
from signup import signup
from effects import type_print, loading_spinner

def landing():
    loading_spinner("Connected")
    type_print("")
    type_print("=" * 50)
    type_print(" STUDENT PROGRESS TRACKER ", delay=0.05)
    print("=" * 50)
    print("1. Login")
    print("2. Signup")
    print("3. Exit")

    while True:
        choice = input("Enter your choice(1-3): ").strip()
        if choice == '1':
            loading_spinner("Authenticating")
            login()
            break
        elif choice == '2':
            loading_spinner("Signing up")
            signup()
            break
        elif choice == '3':
            type_print("Goodbye. See you next time!")
            break
        else:
            print("Invalid choice. Please try again.")

landing()