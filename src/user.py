class User:
    def __init__(self, role, patient_record_manager):
        self._role = role
        self._patient_record_manager = patient_record_manager

    def do_action(self):
        print(f"No defined action")