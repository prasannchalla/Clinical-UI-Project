import csv
import random
from patient import Patient
from visit import Visit 

import utils

class PatientRecordManager:
    
    # Initialize patient records as a dictionary stored in memory
    def __init__(self, patient_file_name, note_file_name):
        self.patient_file_name = patient_file_name
        self.__patients = {}
        self.__load_patient_and_note_data(patient_file_name, note_file_name)
    
    # create new patient if patient does not exist and return patient
    def __get_or_create_patient(self, patient_id):
        cur_patient = self.get_patient(patient_id)

        if cur_patient is None:
            cur_patient = Patient(patient_id)
            self.__patients[patient_id] = cur_patient

        return cur_patient

    def get_patient(self, patient_id):
        return self.__patients.get(patient_id)
    
    def add_patient(self, patient_id):       
        visit_time = utils.input_and_parse_date()
        visit_department = input("Enter department: ")
        race = input("Enter race: ")
        gender = input("Enter gender: ")
        ethnicity = input("Enter ethnicity: ")
        age = int(input("Enter age: "))
        insurance = input("Enter insurance: ")
        zip_code = input("Enter zip code: ")
        chief_complaint = input("Enter chief complaint: ")
        note_id = input("Enter note ID: ")
        note_type = input("Enter note type: ")
        self.add_patient_with_attributes(patient_id, visit_time, visit_department, race, gender, ethnicity, age, insurance, zip_code, chief_complaint, note_id, note_type)

    def add_patient_with_attributes(self, patient_id, visit_time, visit_department, race, gender, ethnicity, age, insurance, zip_code, chief_complaint, note_id, note_type):
        cur_patient = self.__get_or_create_patient(patient_id)
        visit_id = str(random.randint(1000000, 9999999))

        new_visit = Visit(
            visit_id, visit_time, visit_department, race, gender,
            ethnicity, age, insurance, zip_code,
            chief_complaint, note_id, note_type
        )
        cur_patient.add_visit(visit_id, new_visit)
        return visit_id
    
    # remove patient entry from our records
    def remove_patient(self, patient_id):
        if(self.__patients.get(patient_id) is None):
            return False
        else:
           del self.__patients[patient_id]
           return True;
        

    def get_count_of_patient_visits_for_date(self, visit_time):
        count = 0
        for patient in self.__patients.values():
            for visit in patient.visits.values():
                if visit.visit_time == visit_time:
                    count += 1
        return count

    def get_note_of_patient_visit_for_date(self, patient_id, visit_time):
        cur_note = ""
        cur_patient = self.__patients.get(patient_id)
        for patient_visit in cur_patient.visits.values():
                visit_dict = patient_visit.to_dict()
                if(visit_dict.get("visit_time") == visit_time):
                    cur_note = visit_dict["note_text"]
        return cur_note

    def get_patient_data_for_attribute(self, patient_id, attribute):
        attribute_values = []
        cur_patient = self.__patients.get(patient_id)
        for patient_visit in cur_patient.visits.values():
            visit_dict = patient_visit.to_dict()
            if(visit_dict.get(attribute) is not None):
                attribute_values.append(visit_dict[attribute])
        return attribute_values

    # load patient and note data from csv files
    def __load_patient_and_note_data(self, patient_file_name, note_file_name):
        #load patient data first
        with open(patient_file_name, newline='', encoding='utf-8') as csvfile:
            data = csv.DictReader(csvfile)
            for row in data:
                cur_patient = self.__get_or_create_patient(row['Patient_ID'])
                cur_visit = Visit(
                    row['Visit_ID'],
                    utils.parse_date(row['Visit_time']),
                    row['Visit_department'],
                    row['Race'],
                    row['Gender'],
                    row['Ethnicity'],
                    int(row['Age']),
                    row['Zip_code'],
                    row['Insurance'],
                    row['Chief_complaint'],
                    row['Note_ID'],
                    row['Note_type']
                )
                cur_patient.add_visit(cur_visit.visit_id, cur_visit)

        #update note text to visits
        with open(note_file_name, newline='', encoding='utf-8') as csvfile:
            data = csv.DictReader(csvfile)
            for row in data:
                cur_patient = self.__get_or_create_patient(row['Patient_ID'])
                cur_patient.add_note_text_to_visit_id(row['Visit_ID'], row['Note_text'])
                    
        
    