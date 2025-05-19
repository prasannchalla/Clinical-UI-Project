from user import User
import utils

class Admin(User):
    def __init__(self, role, patient_record_manager):
        super().__init__(role, patient_record_manager)

    # only can do count_visits
    def do_action(self):
        print(f"Current role: {self._role}")

        visit_time = utils.input_and_parse_date()
        count = self._patient_record_manager.get_count_of_patient_visits_for_date(visit_time)
        print("Total number of visits on", visit_time, ":", count)
