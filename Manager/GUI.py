import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import config
import add
import retrieve
import time
messagebox_text = "Here are requirements for master password:\n" \
                  "\n" \
                  "1. At least 8 characters long.\n" \
                  "2. At least one uppercase letter.\n" \
                  "3. At least one lowercase letter. \n" \
                  "4. At least one special character: !@#$%^&+=?.\n" \
                  "5. At least one digit.\n" \
                  "\n" \
                  "Remember, your master password is the most important password you'll ever create. \n" \
                  "Don't take shortcuts or use a weak password that could be easily guessed or cracked. \n" \
                  "Keep it safe, secure, and memorable, and you'll have peace of mind knowing that your\n" \
                  "sensitive information is protected."

class PasswordManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1000x700")
        self.root.title("Password Manager")
        self.root.iconbitmap("icons8-lock-50.ico")
        self.main_menu()

    def main_menu(self):
        self.main_menu_frame = tk.Frame(self.root, bg="#0ABaB5")

        database_created = False
        database_error = False

        # check if 'pm' database exists in SQL database
        try:
            database_created = config.checkConfig()
        except ValueError as e:
            self.error_label = tk.Label(self.main_menu_frame, text=str(e), fg='red', bg="#0ABaB5")
            self.error_label.place(relx=0.5, rely=0.2, anchor='center')
            database_error = True

        self.menu_label = tk.Label(self.main_menu_frame, text="Main menu",font=("Arial", 40, "bold"), bg="#0ABaB5" )
        self.menu_label.pack(pady=60)

        if not database_created and not database_error:
            self.success_label = tk.Label(self.main_menu_frame, text="Please create account", bg="#0ABaB5")
            self.success_label.pack(pady=20)

            # Create tooltip for main menu
            self.password_tip = tk.Label(self.main_menu_frame, text="?", fg='black', font=("Helvetica", 20),
                                         justify='center', bg="#0ABaB5")
            self.password_tip.bind("<Enter>", lambda event: self.show_tooltip(event,
                                                                              "This is password manager, where you can store\n"
                                                                              "passwords securely. For security reasons only\n"
                                                                              "one account can be created to the database at\n"
                                                                              "once. Please proceed to create account."))
            self.password_tip.bind("<Leave>", lambda event: self.hide_tooltip(event))
            self.password_tip.place(relx=0.7, rely=0.1, anchor='center')

            # Create Create Account button
            self.create_account_button = tk.Button(self.main_menu_frame, text="Create Account", command=self.create_account_menu, bg='#90EE90',
                                                   fg='#000000', relief="flat", borderwidth=0, highlightthickness=0, padx=10, pady=5, font=("Helvetica", 14))
            self.create_account_button.pack(pady=20)
        elif not database_error:
            self.success_label = tk.Label(self.main_menu_frame, text="Account already created, please log in", bg="#0ABaB5")
            self.success_label.pack(pady=20)
            # Create Login button
            self.login_button = tk.Button(self.main_menu_frame, text="Login", command=self.login_menu, bg='#90EE90',
                                          fg='#000000', relief="flat", borderwidth=0, highlightthickness=0, padx=10, pady=5, font=("Helvetica", 14))
            self.login_button.pack(pady=20)

        # Create Exit button
        self.exit_button = tk.Button(self.main_menu_frame, text="Exit", command=self.root.quit, bg='#FF5733',
                                     fg='#000000', relief="flat", borderwidth=0, highlightthickness=0, padx=10, pady=5, font=("Helvetica", 14))
        self.exit_button.pack(pady=20)

        self.main_menu_frame.pack(fill="both", expand=True)

    def create_account_menu(self):
        self.main_menu_frame.pack_forget() # remove main menu frame

        # Create Create Account frame
        self.create_account_frame = tk.Frame(self.root, bg="#0ABaB5")

        self.create_label = tk.Label(self.create_account_frame, text="Create account", font=("Arial", 40, "bold"), bg="#0ABaB5")
        self.create_label.pack(pady=20)

        self.reminder_label = tk.Label(self.create_account_frame,
                                       text="Your master password is the key to accessing all of your sensitive\n"
                                            "information stored in your password manager. Therefore, it's crucial\n"
                                            "that you choose a strong, unique, and memorable master password.\n"
                                            "There is no way to recover the master password!",
                                       fg='black', font=("Helvetica", 11), bg="#0ABaB5")
        self.reminder_label.pack(pady=20)

        # Create tooltip for the password entry widget
        self.password_tip = tk.Label(self.create_account_frame, text="?", fg='black', font=("Helvetica", 20), justify='center', bg="#0ABaB5")
        self.password_tip.bind("<Enter>", lambda event: self.show_tooltip(event,
                                                                          messagebox_text))
        self.password_tip.bind("<Leave>", lambda event: self.hide_tooltip(event))
        self.password_tip.place(relx=0.8, rely=0.1, anchor='center')

        # Create Password label and entry
        self.password_label = tk.Label(self.create_account_frame, text="Master password", bg="#0ABaB5")
        self.password_label.pack()

        self.password_entry = tk.Entry(self.create_account_frame, show="*")
        self.password_entry.pack()

        # Create Confirm Password label and entry
        self.confirm_password_label = tk.Label(self.create_account_frame, text="Confirm master password", bg="#0ABaB5")
        self.confirm_password_label.pack()
        self.confirm_password_entry = tk.Entry(self.create_account_frame, show="*")
        self.confirm_password_entry.pack()

        # Create Submit button
        self.submit_button = tk.Button(self.create_account_frame, text="Submit", command=self.submit_account, bg='#90EE90',
                                       fg='#000000', relief="flat", borderwidth=0, highlightthickness=0, padx=10, pady=5, font=("Helvetica", 14))

        self.submit_button.pack(pady=20)
        self.confirm_password_entry.bind('<Return>',
                                         lambda event: self.submit_button.invoke())  # Submit by pressing Enter
        # Create Back button
        self.back_button = tk.Button(self.create_account_frame, text="Back", command=lambda: self.to_main_menu(self.create_account_frame), bg='yellow',
                                     fg='#000000', relief="flat", borderwidth=0, highlightthickness=0, padx=10, pady=5, font=("Helvetica", 14))
        self.back_button.pack(pady=20)

        self.create_account_frame.pack(fill="both", expand=True)

    def show_tooltip(self, event, message):
        x, y, cx, cy = event.widget.bbox("insert")
        x = x + event.widget.winfo_rootx() + 25
        y = y + cy + event.widget.winfo_rooty() + 25
        self.tooltip = tk.Toplevel(event.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(self.tooltip, text=message, justify='left',
                      background='white', relief='solid', borderwidth=1,
                      font=("Helvetica", "8", "normal"))
        label.pack(ipadx=1)

    def hide_tooltip(self, event):
        if self.tooltip:
            self.tooltip.destroy()
        self.tooltip = None

    def submit_account(self):
        # Get passwords from entries
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        # Clear error labels
        for error_label in self.create_account_frame.winfo_children():
            if isinstance(error_label, tk.Label) and error_label['fg'] == 'red':
                error_label.destroy()

        # Create database
        try:
            config.make(password, confirm_password)
            # Create Success label
            self.success_label = tk.Label(self.create_account_frame, text="Account created successfully!", fg='#228b22', bg="#0ABaB5", font=("Helvetica", 11))
            self.success_label.pack(pady=20)
            self.submit_button.pack_forget()
        except ValueError as e:
            self.error_label = tk.Label(self.create_account_frame, text=str(e), fg='red', bg="#0ABaB5")
            self.error_label.pack(pady=20)
            self.password_entry.delete(0, tk.END)
            self.confirm_password_entry.delete(0, tk.END)

    def login_menu(self):
        self.main_menu_frame.pack_forget()  # remove main menu frame

        # Create login frame
        self.login_frame = tk.Frame(self.root, bg="#0ABaB5")

        self.login_label = tk.Label(self.login_frame, text="Login", font=("Arial", 40, "bold"), bg="#0ABaB5")
        self.login_label.pack(pady=60)

        # Create Password label and entry
        self.password_label = tk.Label(self.login_frame, text="Master password", bg="#0ABaB5")
        self.password_label.pack()
        self.password_entry = tk.Entry(self.login_frame, show="*")
        self.password_entry.pack()
        self.password_entry.bind('<Return>', lambda event: self.verify_login(True))

        # add login button
        self.login_button = tk.Button(self.login_frame, text="Login", command=lambda: self.verify_login(True), bg='#90EE90',
                                      fg='#000000', relief="flat", borderwidth=0, highlightthickness=0, padx=10, pady=5, font=("Helvetica", 14))
        self.login_button.pack(pady=20)

        self.back_button = tk.Button(self.login_frame, text="Back", command=lambda: self.to_main_menu(self.login_frame), bg='yellow',
                                     fg='#000000', relief="flat", borderwidth=0, highlightthickness=0, padx=10, pady=5, font=("Helvetica", 14))
        self.back_button.pack(pady=20)

        self.login_frame.pack(fill="both", expand=True)

        self.verify_login(False)  # To check that lockout time is zero

    # Function to verify the login, is_login tells if password is submitted
    def verify_login(self, is_login):
        mp = self.password_entry.get()
        self.password_entry.delete(0, tk.END)
        if retrieve.ValidateMasterPassword(mp):
            # Password was right, access password menu
            retrieve.update_attempts(0)
            retrieve.update_lockout_time(5)
            self.passwords_menu()
        else:
            # Remove previous fail label (if any)
            if hasattr(self, 'fail_label'):
                self.fail_label.destroy()
            # If wrong password is submitted, update attempt count
            if is_login == True:
                retrieve.update_attempts(retrieve.get_attempts()+1)
            # If too many attempts, set timeout to prevent brute force attacks
            if retrieve.get_attempts() >= retrieve.get_max_attempts():
                self.fail_label = tk.Label(self.login_frame, text="Account locked. Try again after {} seconds".format(retrieve.get_lockout_time()), fg='red', bg="#0ABaB5")
                self.fail_label.pack(pady=20)
                self.login_button.config(state="disabled")
                self.back_button.config(state="disabled")
                self.password_entry.config(state="disabled")
                for i in range(retrieve.get_lockout_time(), 0, -1):
                    self.fail_label.config(text="Account locked. Try again after {} seconds".format(i))
                    self.fail_label.update()
                    time.sleep(1)
                self.fail_label.destroy()
                self.login_button.config(state="normal")
                self.back_button.config(state="normal")
                self.password_entry.config(state="normal")
                retrieve.update_attempts(0)
                retrieve.update_lockout_time(retrieve.get_lockout_time()*2)
            else:
                if is_login == True:
                    # Show new fail label
                    self.fail_label = tk.Label(self.login_frame, text="Wrong password. Attempt {} of {}".format(retrieve.get_attempts(), retrieve.get_max_attempts()),
                                               fg='red', bg="#0ABaB5")
                    self.fail_label.pack(pady=20)

    def passwords_menu(self):
        self.login_frame.pack_forget()  # remove login frame

        # Create passwords frame
        self.passwords_menu_frame = tk.Frame(self.root, bg="#0ABaB5")

        self.pws_label = tk.Label(self.passwords_menu_frame, text="Passwords", font=("Arial", 40, "bold"), bg="#0ABaB5")
        self.pws_label.place(relx=0.5, rely=0.1, anchor='center')

        # Create tooltip for the password entry widget
        self.password_tip = tk.Label(self.passwords_menu_frame, text="?", fg='black', font=("Helvetica", 20),
                                     justify='center', bg="#0ABaB5")
        self.password_tip.bind("<Enter>", lambda event: self.show_tooltip(event,
                                                                          "Your password data is shown here. For your\n"
                                                                          "own privacy the passwords are never shown\n"
                                                                          "in plain text, but you can copy them to\n"
                                                                          "your clipboard by clicking 'Copy'-button.\n"
                                                                          "Here you can select to add password, logout, or\n"
                                                                          "delete your account or passwords."))
        self.password_tip.bind("<Leave>", lambda event: self.hide_tooltip(event))
        self.password_tip.place(relx=0.7, rely=0.1, anchor='center')

        buttons_frame = tk.Frame(self.passwords_menu_frame, bg="#0ABaB5")
        buttons_frame.place(relx=0.5, rely=0.25, anchor='center')

        self.add_button = tk.Button(buttons_frame, text="Add password", command=self.add_password_menu, bg='#90EE90',
                                    fg='#000000', relief="flat", borderwidth=0, highlightthickness=0, padx=10, pady=5,
                                    font=("Helvetica", 14))
        self.add_button.pack(side="left", padx=50)

        # Create Log out button
        self.back_button = tk.Button(buttons_frame, text="Log out",
                                     command=lambda: self.to_main_menu(self.passwords_menu_frame), bg='yellow',
                                     fg='#000000', relief="flat", borderwidth=0, highlightthickness=0, padx=10, pady=5,
                                     font=("Helvetica", 14))
        self.back_button.pack(side="left", padx=50)

        self.delete_account_button = tk.Button(buttons_frame, text="Delete account", command=self.delete_account,
                                               bg='#FF5733',
                                               fg='#000000', relief="flat", borderwidth=0, highlightthickness=0,
                                               padx=10, pady=5, font=("Helvetica", 14))
        self.delete_account_button.pack(side="left", padx=50)

        # Retrieve password entries from database
        result = retrieve.retrieve_entries()

        if result:
            # Create a new canvas to hold the password table
            self.table_canvas = tk.Canvas(self.passwords_menu_frame, bg="#0ABaB5", width=741)
            self.table_canvas.place(relx=0.5, rely=0.5, anchor='center')

            self.table_frame = tk.Frame(self.table_canvas, bg="#0ABaB5")
            self.table_canvas.create_window((0, 0), window=self.table_frame, anchor='nw')

            self.table_scrollbar = ttk.Scrollbar(self.passwords_menu_frame, orient='vertical',
                                                 command=self.table_canvas.yview)
            self.table_scrollbar.place(relx=0.95, rely=0.5, anchor='center', height=200)
            self.table_canvas.configure(yscrollcommand=self.table_scrollbar.set)

            # Create a new Label widget to display the headers
            sitename_label = tk.Label(self.table_frame, text="Sitename", font=("Arial", 12, "bold"), bg="#0ABaB5")
            sitename_label.grid(row=0, column=0, padx=20)

            siteurl_label = tk.Label(self.table_frame, text="URL address", font=("Arial", 12, "bold"), bg="#0ABaB5")
            siteurl_label.grid(row=0, column=1, padx=20)

            email_label = tk.Label(self.table_frame, text="Email", font=("Arial", 12, "bold"), bg="#0ABaB5")
            email_label.grid(row=0, column=2, padx=20)

            username_label = tk.Label(self.table_frame, text="Username", font=("Arial", 12, "bold"), bg="#0ABaB5")
            username_label.grid(row=0, column=3, padx=20)

            password_label = tk.Label(self.table_frame, text="Password", font=("Arial", 12, "bold"), bg="#0ABaB5")
            password_label.grid(row=0, column=4, padx=20)

            # Loop through the results and add them to the table
            for i, row in enumerate(result):
                sitename_text = row[0]
                sitename_text_widget = tk.Text(self.table_frame, height=1, width=16, font=("Arial", 10))
                sitename_text_widget.insert("1.0", sitename_text)
                sitename_text_widget.configure(state="disabled")
                sitename_text_widget.grid(row=i+1, column=0)

                siteurl_text = row[1]
                siteurl_text_widget = tk.Text(self.table_frame, height=1, width=16, font=("Arial", 10))
                siteurl_text_widget.insert("1.0", siteurl_text)
                siteurl_text_widget.configure(state="disabled")
                siteurl_text_widget.grid(row=i+1, column=1)

                email_text = row[2]
                email_text_widget = tk.Text(self.table_frame, height=1, width=16, font=("Arial", 10))
                email_text_widget.insert("1.0", email_text)
                email_text_widget.configure(state="disabled")
                email_text_widget.grid(row=i+1, column=2)

                username_text = row[3]
                username_text_widget = tk.Text(self.table_frame, height=1, width=16, font=("Arial", 10))
                username_text_widget.insert("1.0", username_text)
                username_text_widget.configure(state="disabled")
                username_text_widget.grid(row=i+1, column=3)

                password_label = tk.Label(self.table_frame, text="*********", font=("Arial", 10), bg="#0ABaB5")
                password_label.grid(row=i + 1, column=4)

                copy_button = tk.Button(self.table_frame, text="Copy", bg='#ADD8E6',
                                        command=lambda row=row: self.copy_password(row[4]), fg='#000000',
                                        relief="solid", borderwidth=1, highlightthickness=0, padx=10, pady=5,
                                        font=("Helvetica", 10))
                copy_button.grid(row=i + 1, column=5)

                delete_button = tk.Button(self.table_frame, text="Delete", bg='#FF5733',
                                          command=lambda row=row: self.delete_password(row[0], row[1], row[2], row[3],
                                                                                       row[4]), fg='#000000',
                                          relief="solid", borderwidth=1, highlightthickness=0, padx=10, pady=5,
                                          font=("Helvetica", 10))
                delete_button.grid(row=i + 1, column=6)

        else:
            self.fail_label = tk.Label(self.passwords_menu_frame, text="No passwords in the database.", bg="#0ABaB5")
            self.fail_label.place(relx=0.5, rely=0.4, anchor='center')

        self.passwords_menu_frame.pack(fill="both", expand=True)

    def copy_password(self, pw):
        password = retrieve.copy_password(pw)
        self.root.clipboard_clear()
        self.root.clipboard_append(password)

    def add_password_menu(self):
        self.passwords_menu_frame.pack_forget()  # remove passwords frame

        self.add_menu_frame = tk.Frame(self.root, bg="#0ABaB5") # create add menu frame

        self.add_label = tk.Label(self.add_menu_frame, text="Add password", font=("Arial", 40, "bold"), bg="#0ABaB5")
        self.add_label.pack(pady=30)

        self.sitename_label = tk.Label(self.add_menu_frame, text="Site/application name", bg="#0ABaB5")
        self.sitename_label.pack()
        self.sitename_entry = tk.Entry(self.add_menu_frame)
        self.sitename_entry.pack(pady=(0, 10))

        self.siteURL_label = tk.Label(self.add_menu_frame, text="URL address", bg="#0ABaB5")
        self.siteURL_label.pack()
        self.siteURL_entry = tk.Entry(self.add_menu_frame)
        self.siteURL_entry.pack(pady=(0, 10))

        self.email_label = tk.Label(self.add_menu_frame, text="Email", bg="#0ABaB5")
        self.email_label.pack()
        self.email_entry = tk.Entry(self.add_menu_frame)
        self.email_entry.pack(pady=(0, 10))

        self.username_label = tk.Label(self.add_menu_frame, text="Username", bg="#0ABaB5")
        self.username_label.pack()
        self.username_entry = tk.Entry(self.add_menu_frame)
        self.username_entry.pack(pady=(0, 10))

        self.password_label = tk.Label(self.add_menu_frame, text="Password", bg="#0ABaB5")
        self.password_label.pack()
        self.password_entry = tk.Entry(self.add_menu_frame, show="*")
        self.password_entry.pack(pady=(0, 10))

        self.password_confirm_label = tk.Label(self.add_menu_frame, text="Confirm password", bg="#0ABaB5")
        self.password_confirm_label.pack()
        self.password_confirm_entry = tk.Entry(self.add_menu_frame, show="*")
        self.password_confirm_entry.pack(pady=(0, 10))
        self.password_confirm_entry.bind('<Return>', lambda event: self.add_password()) #Submit by pressing Enter

        # Create Add button
        self.add_button = tk.Button(self.add_menu_frame, text="Add password", command=self.add_password, bg='#90EE90',
                                    fg='#000000', relief="flat", borderwidth=0, highlightthickness=0, padx=10, pady=5, font=("Helvetica", 14))
        self.add_button.pack(pady=20)

        # Create Back button
        self.back_button = tk.Button(self.add_menu_frame, text="Back", command=lambda: self.to_passwords_menu(self.add_menu_frame), bg='yellow',
                                     fg='#000000', relief="flat", borderwidth=0, highlightthickness=0, padx=10, pady=5, font=("Helvetica", 14))
        self.back_button.pack(pady=20)

        self.add_menu_frame.pack(fill="both", expand=True)

    def add_password(self):
        # Clear error labels
        for error_label in self.add_menu_frame.winfo_children():
            if isinstance(error_label, tk.Label) and error_label['fg'] == 'red':
                error_label.destroy()
        # Clear success labels
        for success_label in self.add_menu_frame.winfo_children():
            if isinstance(success_label, tk.Label) and success_label['fg'] == 'green':
               success_label.destroy()

        sitename = self.sitename_entry.get()
        siteurl = self.siteURL_entry.get()
        email = self.email_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()
        confirm_password = self.password_confirm_entry.get()

        # Add password to database
        try:
            result = retrieve.get_mp_ds()
            add.addEntry(result[0], result[1], sitename, siteurl, email, username, password, confirm_password)
        except ValueError as e:
            self.error_label = tk.Label(self.add_menu_frame, text=str(e), fg='red', bg="#0ABaB5")
            self.error_label.pack(pady=20)
        else:
            self.success_label = tk.Label(self.add_menu_frame, text="Added entry", fg='green', bg="#0ABaB5")
            self.success_label.pack(pady=20)

            self.sitename_entry.delete(0, tk.END)
            self.siteURL_entry.delete(0, tk.END)
            self.email_entry.delete(0, tk.END)
            self.username_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)
            self.password_confirm_entry.delete(0, tk.END)

    def delete_account(self):
        self.passwords_menu_frame.pack_forget()  # remove passwords menu frame

        # Create delete account frame
        self.delete_account_frame = tk.Frame(self.root, bg="#0ABaB5")

        self.delete_label = tk.Label(self.delete_account_frame, text="Delete account", font=("Arial", 40, "bold"), bg="#0ABaB5")
        self.delete_label.pack(pady=60)

        # Create verifying text
        self.are_you_sure_label = tk.Label(self.delete_account_frame, text="Are you sure you want to delete your account forever? All passwords will be removed.",
                                           font=("Arial", 14), fg = 'red', bg="#0ABaB5")
        self.are_you_sure_label.pack()

        # add delete button
        self.delete_account_button = tk.Button(self.delete_account_frame, text="Delete account", command=lambda: [config.delete(),
                                                                                              self.to_main_menu(self.delete_account_frame)], bg='#FF5733',
                                               fg='#000000', relief="flat", borderwidth=0, highlightthickness=0, padx=10, pady=5, font=("Helvetica", 14))
        self.delete_account_button.pack(pady=20)

        # Create back button
        self.back_button = tk.Button(self.delete_account_frame, text="Back", command=lambda: self.to_passwords_menu(self.delete_account_frame), bg='yellow',
                                     fg='#000000', relief="flat", borderwidth=0, highlightthickness=0, padx=10, pady=5, font=("Helvetica", 14))
        self.back_button.pack(pady=20)

        self.delete_account_frame.pack(fill="both", expand=True)

    def delete_password(self, sitename, siteurl, email, username, password):
        self.passwords_menu_frame.pack_forget()  # remove passwords menu frame

        # Create delete password frame
        self.delete_password_frame = tk.Frame(self.root, bg="#0ABaB5")

        self.delete_label = tk.Label(self.delete_password_frame, text="Delete password", font=("Arial", 40, "bold"), bg="#0ABaB5")
        self.delete_label.pack(pady=60)

        # Create verifying text
        self.are_you_sure_label = tk.Label(self.delete_password_frame,
                                           text="Are you sure you want to delete this password? You will not be able to retrieve it",
                                           font=("Arial", 14), fg='red', bg="#0ABaB5")
        self.are_you_sure_label.pack(pady=20)

        #Show first 16 characters on the screen
        max_len = 16
        sitename_short = sitename[:max_len] + "..." if len(sitename) > max_len else sitename
        siteurl_short = siteurl[:max_len] + "..." if len(siteurl) > max_len else siteurl
        email_short = email[:max_len] + "..." if email and len(email) > max_len else email
        username_short = username[:max_len] + "..." if username and len(username) > max_len else username

        self.entry_label = tk.Label(self.delete_password_frame,
                                    text="{}   {}   {}   {}?"
                                    .format(sitename_short, siteurl_short, email_short, username_short),
                                    font=("Arial", 12), fg='black', bg="#0ABaB5")
        self.entry_label.pack()

        # add delete button
        self.delete_password_button = tk.Button(self.delete_password_frame, text="Delete password",
                                                command=lambda: [retrieve.delete_entry(password),
                                                                 self.delete_password_frame.pack_forget(),
                                                                 self.passwords_menu()],
                                                bg='#FF5733', fg='#000000', relief="flat", borderwidth=0,
                                                highlightthickness=0, padx=10, pady=5, font=("Helvetica", 14))
        self.delete_password_button.pack(pady=20)

        # Create back button
        self.back_button = tk.Button(self.delete_password_frame, text="Back",
                                     command=lambda: self.to_passwords_menu(self.delete_password_frame), bg='yellow',
                                     fg='#000000', relief="flat", borderwidth=0, highlightthickness=0, padx=10, pady=5,
                                     font=("Helvetica", 14))
        self.back_button.pack(pady=20)

        self.delete_password_frame.pack(fill="both", expand=True)

    #Function to navigate to passwords menu
    def to_passwords_menu(self, current_frame):
        current_frame.pack_forget()
        self.passwords_menu()

    # Function to navigate to main menu
    def to_main_menu(self, current_frame):
        current_frame.pack_forget()
        self.main_menu()

    # Delete account
    def delete(self):
        config.delete()


if __name__ == '__main__':
    root = tk.Tk()
    PasswordManagerGUI(root)
    root.mainloop()