# Clinical Data Warehouse UI  
**HI 741 Final Project**

This project is a Python-based desktop GUI application built with **Tkinter**, designed to facilitate interaction with clinical patient data. It supports different types of users (like clinicians, nurses, admins, and managers) by offering a **role-based login system** and tools to manage and analyze medical records stored in CSV files.

---

## Main Features

### Login & Roles
- User login credentials are stored in `data/Credentials.csv`
- Access is tailored by role: clinician, nurse, administrator, or management
- All login attempts, successful or not, are recorded for security tracking

### Patient Management & Analytics
- **View Patient Info**: Display the most recent visit details
- **Add New Patient**: Input patient details and create a new entry
- **Remove Patient**: Erase a patient and their data using their ID
- **Visit Counts by Date**: Calculate how many visits occurred on a chosen date
- **Read Clinical Notes**: Show visit-specific notes per patient and date
- **Race Distribution Chart**: Generate a bar graph showing demographic stats

### Logs & Outputs
- Logs are stored in `output/usage_log.csv`
- Any updates to patient records are saved in `output/updated_patient_data.csv`
- Generated charts are saved as `output/statistics_plot.png`

---

## Folder Layout

```
clinical-ui-project/
├── data/                         # Input CSVs: Credentials.csv, Patient_data.csv, Notes.csv
│   ├── Credentials.csv
│   ├── Patient_data.csv
│   └── Notes.csv
├── output/                       # Output files and generated visuals
│   ├── usage_log.csv
│   └── statistics.png
├── src/                          # Python source code
│   ├── main.py
│   ├── ui_app.py
│   ├── user.py
│   ├── patient.py
│   ├── validator.py
│   ├── visit.py
│   ├── patient_record_manager.py
│   ├── health_professional.py
│   ├── manager.py
│   ├── admin.py
│   └── utils.py
├── UML_diagram.png               # UML diagram image
├── README.md
└── requirements.txt
```
