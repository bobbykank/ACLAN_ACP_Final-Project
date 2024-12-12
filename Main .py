from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk
import hashlib
import re
import mysql.connector

#for database connection with sql
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="finalproj"
    )

#declares the window dimensions as global for consistency of the app, quality of life change
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 700

#below are functions for logic checks, fetching database data, etc...
#checks if the given email in email entry has "@" and ".com"
def is_valid_email(email):
    # Check if the email contains "@" and ".com"
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email) is not None

# inserting of signed-up credentials to users table in database
def signup_user(name, email, password):
    if not name or not email or not password:
        messagebox.showinfo("Error", "Please fill in all fields.")
        return

    if not is_valid_email(email):  # Check if the email is valid
        messagebox.showinfo("Error", "Please enter a valid email address.")
        return
    connection = get_db_connection()
    cursor = connection.cursor()
    hashed_password = hashlib.sha256(password.encode()).hexdigest()  #encrypts password
    try:
        query = "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)"
        cursor.execute(query, (name, email, hashed_password))
        connection.commit()
        messagebox.showinfo("Success", "Registration Successful!")
        signup.destroy()
        main_window()
    except mysql.connector.IntegrityError as e:
        messagebox.showinfo("Error", "Credentials already exist!")
    finally:
        cursor.close()
        connection.close()

#validation and checking of users table records to see if account already registered, also checks for existing accounts for sign-in and admin account (that is hard-coded not in database)
def signin_user(email, password):
    if not email or not password:
        messagebox.showinfo("Error", "Please fill in all fields.")
        return NONE
    if email == "admin" and password == "admin1":
        messagebox.showinfo("Success", "Welcome admin!")
        openadmin()
        return "admin"
    if not is_valid_email(email):  # Check if the email is valid
        messagebox.showinfo("Error", "Email or password incorrect, please try again.")
        return None
    connection = get_db_connection()
    cursor = connection.cursor()
    hashed_password = hashlib.sha256(password.encode()).hexdigest()  # Hashing the input password
    query = "SELECT * FROM users WHERE email = %s AND password = %s"
    cursor.execute(query, (email, hashed_password))
    user = cursor.fetchone()  # Fetch one row
    cursor.close()
    connection.close()
    if user:
        messagebox.showinfo("Success", "Sign-in Successful!")
        window.destroy()
        signin_page()
        return user
    else:
        messagebox.showinfo("Error", "Invalid account, try again!")
        return NONE

#insertion of data into path_info table in database
def submit_path_info(location, status, photo):
    connection = get_db_connection()
    cursor = connection.cursor()
    if not location or not status or not photo:
        messagebox.showinfo("Error", "Please fill in all fields.")
        return NONE
    try:
        # SQL Insert statement
        query = "INSERT INTO path_info (location, status, photo) VALUES (%s, %s, %s)"
        cursor.execute(query, (location, status, photo))
        connection.commit()
        messagebox.showinfo("Success", "Path information submitted successfully!")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error inserting data: {err}")
    finally:
        cursor.close()
        connection.close()

#takes and displays the submitted data into the pit page data table for users
def fetch_path_info():
    connection = get_db_connection()
    cursor = connection.cursor()
    query = """
    SELECT id, location, status, date_uploaded, photo
    FROM path_info;
    """
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    connection.close()
    return data

#function for always spawning the windows in the center of the screen, qol change for consistency too
def center_window(window):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x_position = (screen_width // 2) - (WINDOW_WIDTH // 2)
    y_position = (screen_height // 2) - (WINDOW_HEIGHT // 2)
    window.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{x_position}+{y_position}")

#function for previous page button/s
def navigate_to(current_window, page_func):
    current_window.destroy()  # Close the current window
    page_func()  # Call the new page function

#function for going to signup page
def signup_click(current_window):
    current_window.destroy()  # Close the current window
    signup_page()  # Call the signup page


#below are functions for the main windows themselves
#signup page window
def signup_page():
    global signup
    signup = Tk()
    signup.geometry("1000x700")
    signup.title("Sign-up Page")
    signup.resizable(False, False)
    signup.config(bg="#3ab19b")
    center_window(signup)  #calls the function for centering window

    #for left frame, design inverse consistent with first signin page
    topborder = Frame(signup, bg="#ebfffe", width=425)
    topborder.pack(side="left", fill="y")

    #for top icon and title card
    framepic = Image.open('pathfindericon.png')
    framepic = framepic.resize((30, 30))
    framepic_tk = ImageTk.PhotoImage(framepic)
    label = Label(signup, image=framepic_tk)
    label.img_tk = framepic_tk
    framepic_label = Label(signup, image=framepic_tk, bg="#ebfffe")
    framepic_label.place(x=9, y=9)
    frametitle = Label(signup, text="Path-Finder", font=("Corbel Light", 22), bg="#ebfffe", fg="Black")
    frametitle.place(x=45, y=4)

    #flavor text for sign-up in sign-in page
    framewelcome = Label(signup, text="Already got an account?", font=("Bahnschrift SemiLight", 25, "bold"),
                         bg="#ebfffe", fg="Black")
    framewelcome.place(x=25, y=250)

    #sign-in button for back functionality
    signinbutton = Button(signup, text="SIGN-IN")
    signinbutton.config(font="Arial", fg="Black")
    signinbutton.config(bg="#ebfffe", width=12)
    signinbutton.config(command=lambda: navigate_to(signup, main_window))
    signinbutton.place(x=150, y=310)

    #sign-up content
    signuptext = Label(signup, text="Create an Account", font=("Bahnschrift SemiLight", 34, "bold"), bg="#3ab19b",
                       fg="White")
    signuptext.place(x=520, y=165)
    signupflavort = Label(signup, text="Use your valid email account", font=("Corbel Light", 15), bg="#3ab19b",
                          fg="White")
    signupflavort.place(x=593, y=220)

    #sign-up credentials box
    signupcred = Frame(signup, bg="white", width=490, height=250, bd=2, relief="raised")
    signupcred.place(x=470, y=260)

    #for name
    signupname = Label(signupcred, text="Name", font=("Corbel Light", 15, "bold"), bg="white", fg="#3ab19b")
    signupname.place(x=30, y=40)
    signupnameentry = Entry(signupcred, font=("Arial", 13), relief="solid")
    signupnameentry.place(x=130, y=40, width=250, height=30)

    #for email
    signupemail = Label(signupcred, text="Email", font=("Corbel Light", 15, "bold"), bg="white", fg="#3ab19b")
    signupemail.place(x=30, y=80)
    signupemailentry = Entry(signupcred, font=("Arial", 13), relief="solid")
    signupemailentry.place(x=130, y=80, width=250, height=30)

    #for password
    signuppassword = Label(signupcred, text="Password", font=("Corbel Light", 15, "bold"), bg="white", fg="#3ab19b")
    signuppassword.place(x=30, y=120)
    signuppasswordentry = Entry(signupcred, font=("Arial", 13), show="*", relief="solid")
    signuppasswordentry.place(x=130, y=120, width=250, height=30)

    #sign-up button
    signupbutton = Button(signupcred, text="REGISTER")
    signupbutton.config(font="Arial", fg="Black")
    signupbutton.config(bg="#ebfffe", width=12)
    signupbutton.config(command=lambda: signup_user(
        signupnameentry.get(),
        signupemailentry.get(),
        signuppasswordentry.get()
    ))

    signupbutton.place(x=180, y=170)

    #run the second window loop
    signup.mainloop()

def signin_page():
    def open_photo_window(photo_path):

        #checks photo file directory if present, error if not
        if not photo_path:
            messagebox.showinfo("Error", "No photo available for this entry.")
            return

        photo_window = Toplevel(signin)
        photo_window.title("Photo Viewer")
        photo_window.geometry("500x500")
        photo_window.config(bg="white")
        center_window(photo_window)

        #displays the submitted photo if passes directory check above
        try:
            photo = Image.open(photo_path)
            photo = photo.resize((400, 400))
            photo_tk = ImageTk.PhotoImage(photo)

            photo_label = Label(photo_window, image=photo_tk, bg="white")
            photo_label.photo = photo_tk
            photo_label.pack(fill = BOTH, expand = True)

        except Exception as e:
            messagebox.showinfo("Error", f"Unable to open photo: {e}")
            photo_window.destroy()

    def on_photo_click(event):
        selected_item = table.selection()
        if not selected_item:
            return

        row_data = table.item(selected_item)["values"]
        photo_path = row_data[4]
        open_photo_window(photo_path)

    #sign-in page setup
    global signin
    signin = Tk()
    signin.geometry("1000x700")
    signin.title("Path Information Tab")
    signin.resizable(False, False)
    signin.config(bg="#3ab19b")
    center_window(signin)

    #top design and title again
    framepic = Image.open('pathfinder.png')
    framepic = framepic.resize((30, 30))
    framepic_tk = ImageTk.PhotoImage(framepic)
    label = Label(signin, image=framepic_tk)
    label.img_tk = framepic_tk
    framepic_label = Label(signin, image=framepic_tk, bg="#3ab19b")
    framepic_label.place(x=9, y=9)
    frametitle = Label(signin, text="Path-Finder", font=("Corbel Light", 22), bg="#3ab19b", fg="White")
    frametitle.place(x=45, y=4)
    infotitle = Label(signin, text="Path Information Tab", font=("Bahnschrift SemiLight", 22, "bold"), bg="#3ab19b",
                      fg="White")
    infotitle.place(x=70, y=40)

    #frame for the table
    dataframe = Frame(signin, bg="white", width=900, height=520, bd=2, relief="raised")
    dataframe.place(x=33, y=90)
    columns = ("Post ID", "Location", "Status", "Date Updated", "Photo")
    table = ttk.Treeview(dataframe, columns=columns, show="headings", height=20)
    for col in columns:
        table.heading(col, text=col)
        table.column(col, width=180, anchor="center")

    #inserts data into the table
    data = fetch_path_info()
    for row in data:
        table.insert("", "end", values=row)

    #click event binding
    table.bind("<Double-1>", on_photo_click)

    #fits table in the frame
    table.pack(fill="both", expand=True, padx=15, pady=15)

    #for submit path info button
    infobutton = Button(signin, text="SUBMIT PATH INFO", )
    infobutton.place(x=795, y=630)
    infobutton.config(command=lambda: navigate_to(signin, infoinput_page))
    infobutton.config(font="Arial", fg="Black")
    infobutton.config(bg="#ebfffe", width=18)

    #log out button
    logoutbutton = Button(signin, text="LOG OUT", )
    logoutbutton.place(x=34, y=630)
    logoutbutton.config(command=lambda: navigate_to(signin, main_window))
    logoutbutton.config(font="Arial", fg="Black")
    logoutbutton.config(bg="#ebfffe", width=9)

    signin.mainloop()

def infoinput_page():
    #create a new third window "path information table / PIT submission"
    global pit
    pit = Tk()
    pit.geometry("1000x700")
    pit.title("Submission Page")
    pit.resizable(False, False)
    pit.config(bg="#ebfffe")
    center_window(pit)  #calls the function for centering window

    #icon and title up top
    framepic = Image.open('pathfindericon.png')
    framepic = framepic.resize((30, 30))
    framepic_tk = ImageTk.PhotoImage(framepic)
    label = Label(pit, image=framepic_tk)
    label.img_tk = framepic_tk
    framepic_label = Label(pit, image=framepic_tk, bg="#ebfffe")
    framepic_label.place(x=9, y=9)
    frametitle = Label(pit, text="Path-Finder", font=("Corbel Light", 22), bg="#ebfffe", fg="Black")
    frametitle.place(x=45, y=4)
    pittitle = Label(pit, text="Path Status Submission", font=("Bahnschrift SemiLight", 22, "bold"), bg="#ebfffe",
                     fg="Black")
    pittitle.place(x=70, y=40)

    #frame for table for submitted information
    dataframe = Frame(pit, bg="#3ab19b", width=900, height=520, bd=2, relief="raised")
    dataframe.place(x=55, y=85)

    #for input of path/location
    path1 = Label(dataframe, text="Path / Location", font=("Corbel Light", 15, "bold"), bg="#3ab19b", fg="#ebfffe")
    path1.place(x=30, y=90)
    path1entry = Entry(dataframe, font=("Arial", 13), relief="solid")
    path1entry.place(x=175, y=90, width=600, height=30)

    #for input of status
    path2 = Label(dataframe, text="Status", font=("Corbel Light", 15, "bold"), bg="#3ab19b", fg="#ebfffe")
    path2.place(x=30, y=160)
    path2entry = Entry(dataframe, font=("Arial", 13), relief="solid")
    path2entry.place(x=175, y=160, width=600, height=30)

    #for the selection of the photo of the path
    path3 = Label(dataframe, text="Photo", font=("Corbel Light", 15, "bold"), bg="#3ab19b", fg="#ebfffe")
    path3.place(x=30, y=220)
    path3entry = Entry(dataframe, font=("Arial", 13), relief="solid")
    path3entry.place(x=175, y=220, width=600, height=30)
    choose_file_button = Button(dataframe, text="CHOOSE FILE",
                                command=lambda: path3entry.delete(0, END) or path3entry.insert(0,filedialog.askopenfilename(filetypes=(("Image Files","*.png;*.jpg;*.jpeg;*.bmp;*.gif"),("All Files","*.*")))),
                                font=("Arial", 11), bg="#ebfffe", fg="Black")
    choose_file_button.place(x=780, y=220)

    #button for submitting path info
    infobutton = Button(dataframe, text="SUBMIT")
    infobutton.place(x=400, y=280)
    infobutton.config(command=lambda: submit_path_info(path1entry.get(), path2entry.get(), path3entry.get()))
    infobutton.config(font="Arial", fg="Black")
    infobutton.config(bg="#ebfffe", width=8)


    #button for going first page (sign-in)
    logoutbutton = Button(pit, text="GO BACK")
    logoutbutton.place(x=55, y=630)
    logoutbutton.config(command=lambda: navigate_to(pit, signin_page))
    logoutbutton.config(font="Arial", fg="Black")
    logoutbutton.config(bg="#ebfffe", width=9)
    pit.mainloop()


#window for admin page, basic features like select, unselect, and delete rows. (no update tho)
def openadmin():
    window.destroy()
    global admin_window
    admin_window = Tk()
    admin_window.geometry("1000x700")
    admin_window.title("Admin Page")
    admin_window.resizable(False, False)
    admin_window.config(bg="White")
    center_window(admin_window)

    #frames for each table
    users_frame = Frame(admin_window, bg="White", bd=2, relief=SOLID)
    users_frame.place(x=20, y=20, width=960, height=250)

    path_info_frame = Frame(admin_window, bg="White", bd=2, relief=SOLID)
    path_info_frame.place(x=20, y=290, width=960, height=250)

    def unselect_all():
        users_tree.selection_set(())
        path_info_tree.selection_set(())

    #functions to call data
    def fetch_table_data(table_name):
        connection = get_db_connection()
        cursor = connection.cursor()
        query = f"SELECT * FROM {table_name}"
        cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()
        connection.close()
        return data

    #function for deletion
    def delete_row(table_name, row_id):
        connection = get_db_connection()
        cursor = connection.cursor()
        query = f"DELETE FROM {table_name} WHERE id = %s"
        cursor.execute(query, (row_id,))
        connection.commit()
        cursor.close()
        connection.close()

    #reload after deletion
    def reload_data():
        for tree in [users_tree, path_info_tree]:
            for item in tree.get_children():
                tree.delete(item)

        for row in fetch_table_data("users"):
            users_tree.insert("", "end", values=row)

        for row in fetch_table_data("path_info"):
            path_info_tree.insert("", "end", values=row)

    #users table
    Label(users_frame, text="Users Table", font=("Arial", 14), bg="White").pack(anchor="w", padx=10, pady=5)
    users_tree = ttk.Treeview(users_frame, columns=("id", "name", "email", "password"), show="headings", height=10)
    users_tree.heading("id", text="ID")
    users_tree.heading("name", text="Name")
    users_tree.heading("email", text="Email")
    users_tree.heading("password", text="Password")
    users_tree.column("id", width=50, anchor="center")
    users_tree.column("name", width=200, anchor="w")
    users_tree.column("email", width=250, anchor="w")
    users_tree.column("password", width=300, anchor="w")
    users_tree.pack(fill=BOTH, expand=True, padx=10, pady=10)

    #path-info table
    Label(path_info_frame, text="Path Info Table", font=("Arial", 14), bg="White").pack(anchor="w", padx=10, pady=5)
    path_info_tree = ttk.Treeview(path_info_frame, columns=("id", "user_id", "location", "status", "date_uploaded", "photo"), show="headings", height=10)
    path_info_tree.heading("id", text="ID")
    path_info_tree.heading("user_id", text="User ID")
    path_info_tree.heading("location", text="Location")
    path_info_tree.heading("status", text="Status")
    path_info_tree.heading("date_uploaded", text="Date Uploaded")
    path_info_tree.heading("photo", text="Photo")
    path_info_tree.column("id", width=50, anchor="center")
    path_info_tree.column("user_id", width=100, anchor="center")
    path_info_tree.column("location", width=200, anchor="w")
    path_info_tree.column("status", width=100, anchor="center")
    path_info_tree.column("date_uploaded", width=150, anchor="center")
    path_info_tree.column("photo", width=250, anchor="w")
    path_info_tree.pack(fill=BOTH, expand=True, padx=10, pady=10)

    #frame and buttons for actions "logout, delete, unselect"
    control_frame = Frame(admin_window, bg="White", bd=2, relief=SOLID)
    control_frame.place(x=20, y=560, width=500, height=100)

    unselectbutton = Button(control_frame, text="Unselect All", command=unselect_all, bg="White", fg="Black", font=("Arial", 12))
    unselectbutton.pack(side=LEFT, padx=20)

    def delete_selected():
        #asks for confirmation whether sure to delete, for selection security and assurance if mistaken
        confirm = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete the selected rows?")
        if not confirm:
            return

        selected_user = users_tree.selection()
        selected_path_info = path_info_tree.selection()

        #deletes from users table
        for item in selected_user:
            row_id = users_tree.item(item, "values")[0]
            delete_row("users", row_id)

        #deletes from path_info table
        for item in selected_path_info:
            row_id = path_info_tree.item(item, "values")[0]
            delete_row("path_info", row_id)

        reload_data()
        messagebox.showinfo("Success", "Selected rows have been deleted successfully.")

    Button(control_frame, text="Delete Selected Rows", command=delete_selected, bg="White", fg="Black", font=("Arial", 12)).pack(side=LEFT, padx=20)

    def logout():
        admin_window.destroy()
        main_window()

    Button(control_frame, text="Logout", command=logout, bg="White", fg="Black", font=("Arial", 12)).pack(side=LEFT, padx=20)

    #reload initial data
    reload_data()

#main window (sign-in page)
def main_window():
    global window
    window = Tk()
    window.geometry("1000x700")
    window.title("Sign-in or Sign-up")
    window.resizable(False, False)
    window.config(bg="#ebfffe")
    center_window(window)

    #for the window icon
    icon = PhotoImage(file='pathfindericon.png')
    window.iconphoto(True, icon)

    #for left color frame
    frame4title = Frame(window, bg="#3ab19b", width=425)
    frame4title.pack(side="left", fill="y")

    #left color frame logo
    framepic = Image.open('pathfinder.png')
    framepic = framepic.resize((30, 30))
    framepic_tk = ImageTk.PhotoImage(framepic)
    label = Label(window, image=framepic_tk)
    label.img_tk = framepic_tk
    framepic_label = Label(window, image=framepic_tk, bg="#3ab19b")
    framepic_label.place(x=9, y=9)

    #left color frame title card
    frametitle = Label(window, text="Path-Finder", font=("Corbel Light", 22), bg="#3ab19b", fg="White")
    frametitle.place(x=45, y=4)

    #left color frame welcome flavor text
    framewelcome = Label(window, text="New here?", font=("Bahnschrift SemiLight", 35, "bold"), bg="#3ab19b", fg="White")
    framewelcome.place(x=85, y=220)
    framewelcometext = Label(window, text="Click down below to get \nstarted on Path-Finder.",
                             font=("Corbel Light", 16), bg="#3ab19b", fg="White")
    framewelcometext.place(x=102, y=280)

    #sign-up button config
    framesignup = Button(window, text="SIGN-UP")
    framesignup.place(x=147, y=350)
    framesignup.config(command=lambda: signup_click(window))
    framesignup.config(font="Arial", fg="Black")
    framesignup.config(bg="#ebfffe", width=12)

    #sign-in config with flavor text
    signin = Label(window, text="Login to your Account", font=("Bahnschrift SemiLight", 35, "bold"), bg="#ebfffe",fg="black")
    signin.place(x=470, y=170)
    signinflavor = Label(window, text="Use your Path-Finder Account", font=("Corbel Light", 16, "bold"), bg="#ebfffe",fg="#638074")
    signinflavor.place(x=570, y=240)

    #account credentials container frame
    credsframe = Frame(window, bg="white", width=490, height=200, bd=2, relief="raised")
    credsframe.place(x=470, y=290)

    #email label and entry box
    signinemail = Label(credsframe, text="Email", font=("Corbel Light", 15, "bold"), bg="white", fg="#3ab19b")
    signinemail.place(x=30, y=30)
    signinemailentry = Entry(credsframe, font=("Arial", 13), relief="solid")
    signinemailentry.place(x=130, y=30, width=250, height=30)

    #password label and entry box
    signinpassword = Label(credsframe, text="Password", font=("Corbel Light", 15, "bold"), bg="white", fg="#3ab19b")
    signinpassword.place(x=30, y=80)
    signinpasswordentry = Entry(credsframe, font=("Arial", 13), show="*", relief="solid")
    signinpasswordentry.place(x=130, y=80, width=250, height=30)

    #account creds signin button
    signinbutton = Button(credsframe, text="SIGN-IN")
    signinbutton.config(font="Arial", fg="Black")
    signinbutton.config(bg="#ebfffe", width=12)
    signinbutton.config(command=lambda: signin_user(
        signinemailentry.get(),
        signinpasswordentry.get(),
    )or navigate_to(main_window, signin_page))
    signinbutton.place(x=200, y=130)
    window.mainloop()

#Starts main window
main_window()
