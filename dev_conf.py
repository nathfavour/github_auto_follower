import webbrowser

# Ask the user if they have a PythonAnywhere account
response = input("Do you have a PythonAnywhere account? (yes/no): ")

if response.lower() == "yes":
    # Open the PythonAnywhere login page
    print("Login here...")
    webbrowser.open("https://www.pythonanywhere.com/login/?next=/signup/")
else:
    # Open the PythonAnywhere signup page
    print("create a free account here...")
    webbrowser.open("https://www.pythonanywhere.com/registration/register/beginner/")