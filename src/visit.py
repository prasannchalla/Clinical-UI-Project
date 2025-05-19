class Visit:
    def __init__(self, visit_id, visit_time, visit_department, race, gender, ethnicity, age, insurance, zipcode, chief_complaint, note_id, note_type):
        self.visit_id = visit_id
        self.visit_time = visit_time
        self.visit_department = visit_department
        self.race = race
        self.gender = gender
        self.ethnicity = ethnicity
        self.age = age
        self.insurance = insurance
        self.zipcode = zipcode
        self.chief_complaint = chief_complaint
        self.note_id = note_id
        self.note_type = note_type
        self.note_text = ""

    def to_dict(self):
        return self.__dict__