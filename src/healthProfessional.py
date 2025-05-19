from user import User
from visit import Visit

import utils

class HealthProfessional(User):
    def __init__(self, role, patient_record_manager):
        super().__init__(role, patient_record_manager)

    def do_action(self):
        print(f"Current role: {self._role}")

        while True:
            action = input("Please enter desired action (Add_patient, Remove_patient, Retrieve_patient, Count_visits, View_note, Stop): ")

            if(action == "Add_patient"):
                self.__do_add_patient_action()
            elif(action == "Remove_patient"):
                self.__do_remove_patient_action()
            elif(action == "Retrieve_patient"):
                self.__do_retrieve_patient_action()
            elif(action == "Count_visits"):
                self.__do_count_visits_action()
            elif(action == "View_note"):
                self.__do_view_note_action()
            elif(action == "Stop"):
                break;
            else:
                print("Invalid action, try again!")

    # add new patient if does not exit and record visit details
    def __do_add_patient_action(self):
        patient_id = input("Please enter Patient_Id: ")
        self._patient_record_manager.add_patient(patient_id)
        print(f"Patient added with patient id: {patient_id}")


    # add patient data from records
    def __do_remove_patient_action(self):
        patient_id = input("Please enter Patient_Id: ")
        if(self._patient_record_manager.remove_patient(patient_id)):
            print(f"Patient record patient id: {patient_id} removed succesfully")
        else:
            print(f"No records exist for patient id: {patient_id}")     


    # retrieve patient information for a given patient id
    def __do_retrieve_patient_action(self):
        patient_id = input("Please enter Patient_Id: ")
        if(self._patient_record_manager.get_patient(patient_id) is None):
            print(f"No records exist for patient id: {patient_id}")
        else:
            attribute = input("Please enter required data (gender, race, ethnicity, zipcode, insurance, age, visit_time, visit_department, chief_complaint): ")
            attribute_value = self._patient_record_manager.get_patient_data_for_attribute(patient_id, attribute)
            print(f"Requested data {attribute}: {attribute_value}")

    # return number of patient visits on a given date
    def __do_count_visits_action(self):
        visit_time = utils.input_and_parse_date()
        count = self._patient_record_manager.get_count_of_patient_visits_for_date(visit_time)
        print("Total number of visits on", visit_time, ":", count)

    # view clinical note of a patient on a given date
    def __do_view_note_action(self):
        patient_id = input("Please enter Patient_Id: ")

        if(self._patient_record_manager.get_patient(patient_id) is None):
            print(f"No records exist for patient id: {patient_id}")
        else:
            visit_time = utils.input_and_parse_date()
            cur_note = self._patient_record_manager.get_note_of_patient_visit_for_date(patient_id, visit_time)
            if cur_note is "":
                print(f"No note found for given date: {visit_time}")
            else:
                print(f"Requested note: {cur_note}")
                