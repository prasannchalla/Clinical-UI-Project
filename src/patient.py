
class Patient:
    def __init__(self, id):
        self.patient_id = id
        self.visits = {}

    def add_note_text_to_visit_id(self, visit_id, note_text):
        if(self.visits.get(visit_id) is not None):
            self.visits[visit_id].note_text = note_text 
    
    def add_visit(self, visit_id, visit):
        self.visits[visit_id] = visit
    
    def to_dict(self):
        return {
        "patient_id": self.patient_id,
        "visits": [v.to_dict() for v in self.visits]
    }

    