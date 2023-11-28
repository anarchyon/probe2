import models

class SortParams():
    
    def __init__(self):
        self.sort_column = models.Staff.staff_id
        self.is_sort_asc: bool = True