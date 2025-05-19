#UI class

import tkinter as tk
from tkinter import messagebox
from validator import Validator
from patientRecordManager import PatientRecordManager
from admin import Admin
from manager import Manager
from healthProfessional import HealthProfessional
import datetime
import utils

USER_CREDENTIALS_FILE_NAME = "../data/Credentials.csv"
PATIENT_NOTES_FILE_NAME = "../data/Notes.csv"
PATIENT_DATA_FILE_NAME = "../data/Patient_data.csv"
OUTPUT_LOG_FILE_NAME = "../output/usage_log.csv"

class App:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Clinical Data Warehouse UI")
        self.user = None
        self.patient_record_manager = PatientRecordManager(PATIENT_DATA_FILE_NAME, PATIENT_NOTES_FILE_NAME)
        self.create_login_screen()

    def create_login_screen(self):
        self.clear_window()
        tk.Label(self.window, text="Username").pack()
        self.username_entry = tk.Entry(self.window)
        self.username_entry.pack()
        tk.Label(self.window, text="Password").pack()
        self.password_entry = tk.Entry(self.window, show="*")
        self.password_entry.pack()
        tk.Button(self.window, text="Login", command=self.handle_login).pack()

    def handle_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        validator = Validator(USER_CREDENTIALS_FILE_NAME)

        if validator.validate_credentials(username, password):
            role = validator.get_user_role(username)

            if role == "admin":
                self.user = Admin(role, self.patient_record_manager)
            elif role in ["nurse", "clinician"]:
                self.user = HealthProfessional(role, self.patient_record_manager)
            elif role == "management":
                self.user = Manager(role, self.patient_record_manager)
            else:
                messagebox.showerror("Login Failed", "Invalid role type.")
                return

            self.log_action(username, role, "login_success")
            self.create_main_menu()
        else:
            self.log_action(username, "unknown", "login_failed")
            messagebox.showerror("Login Failed", "Invalid credentials")

    def create_main_menu(self):
        self.clear_window()
        tk.Label(self.window, text=f"Logged in as: {self.user._role}").pack()

        if isinstance(self.user, HealthProfessional):
            tk.Button(self.window, text="Add Patient", command=self.add_patient_ui).pack()
            tk.Button(self.window, text="Remove Patient", command=self.remove_patient_ui).pack()
            tk.Button(self.window, text="Retrieve Patient", command=self.retrieve_patient_ui).pack()
            tk.Button(self.window, text="View Note", command=self.view_note_ui).pack()
            tk.Button(self.window, text="Count Visits", command=self.count_visits_ui).pack()

        elif isinstance(self.user, Admin):
            tk.Button(self.window, text="Count Visits", command=self.count_visits_ui).pack()

        elif isinstance(self.user, Manager):
            tk.Button(self.window, text="Generate Statistics", command=self.generate_statistics_ui).pack()

        tk.Button(self.window, text="Exit", command=self.window.quit).pack()

    def clear_window(self):
        for widget in self.window.winfo_children():
            widget.destroy()

    def run(self):
        self.window.mainloop()

    def log_action(self, username, role, action):
        with open(OUTPUT_LOG_FILE_NAME, "a") as f:
            time = datetime.datetime.now().isoformat()
            f.write(f"{username},{role},{action},{time}\n")

    def prompt(self, msg):
        win = tk.Toplevel()
        win.title("Input")
        tk.Label(win, text=msg).pack()
        entry = tk.Entry(win)
        entry.pack()
        output = []
        def submit():
            output.append(entry.get())
            win.destroy()
        tk.Button(win, text="Submit", command=submit).pack()
        win.grab_set()
        win.wait_window()
        return output[0] if output else ""

    # ========== UI Wrappers Around Class Methods ==========

    def add_patient_entries_gui(self, window):
        top = tk.Toplevel(window)
        top.title("Add Patient")

        fields = ["Patient_ID", "Visit_time", "Visit_department", "Race", "Gender",  "Ethnicity", "Age", "Insurance", "Zip_code", "Chief complaint", "Note_ID", "Note_type"]
        entries = {}

        for field in fields:
            tk.Label(top, text=field).pack()
            entry = tk.Entry(top)
            entry.pack()
            entries[field] = entry

        def submit():
            try:
                data = {k.strip(): e.get().strip() for k, e in entries.items()}

                patient_id = data["Patient_ID"]
                visit_id = self.user._patient_record_manager.add_patient_with_attributes(data["Patient_ID"],
                                                      utils.parse_date(data["Visit_time"]),
                                                      data["Visit_department"],
                                                      data["Race"],
                                                      data["Gender"],
                                                      data["Ethnicity"],
                                                      data["Age"],
                                                      data["Insurance"],
                                                      data["Zip_code"],
                                                      data["Chief complaint"],
                                                      data["Note_ID"],
                                                      data["Note_type"])

                messagebox.showinfo("Success", f"Patient {patient_id} added with Visit ID {visit_id}")
                self.log_action(self.user._role, self.user._role, "add_patient")
                top.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        tk.Button(top, text="Submit", command=submit).pack()

    def add_patient_ui(self):
        entries = self.add_patient_entries_gui(self.window)

    def remove_patient_ui(self):
        pid = self.prompt("Enter Patient ID to remove")
        if self.user._patient_record_manager.remove_patient(pid):
            messagebox.showinfo("Remove Patient", f"Patient {pid} removed successfully.")
        else:
            messagebox.showinfo("Remove Patient", f"No record found for patient {pid}.")
        self.log_action(self.user._role, self.user._role, "remove_patient")

    def retrieve_patient_ui(self):
        pid = self.prompt("Enter Patient ID")
        attr = self.prompt("Enter attribute (gender, race, etc.)")
        data = self.user._patient_record_manager.get_patient_data_for_attribute(pid, attr)
        messagebox.showinfo("Patient Info", f"{attr}: {data}")
        self.log_action(self.user._role, self.user._role, "retrieve_patient")

    def view_note_ui(self):
        pid = self.prompt("Enter Patient ID")
        visit_time = self.prompt("Enter Visit Date (YYYY-MM-DD)")
        note = self.user._patient_record_manager.get_note_of_patient_visit_for_date(pid, visit_time)
        if note:
            messagebox.showinfo("Clinical Note", note)
        else:
            messagebox.showinfo("Clinical Note", "No note found for given date.")
        self.log_action(self.user._role, self.user._role, "view_note")

    def count_visits_ui(self):
        visit_time = self.prompt("Enter Visit Date (YYYY-MM-DD)")
        count = self.user._patient_record_manager.get_count_of_patient_visits_for_date(visit_time)
        messagebox.showinfo("Visit Count", f"Total number of visits on {visit_time}: {count}")
        self.log_action(self.user._role, self.user._role, "count_visits")

    def generate_statistics_ui(self):
        self.user.do_action()  # Manager's do_action generates and shows plots
        self.log_action(self.user._role, self.user._role, "generate_statistics")
