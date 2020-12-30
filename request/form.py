from request.form_data import FormData


class Form:
    def __init__(self, *fields: FormData):
        self.text_fields = {}
        self.file_fields = {}
        for field in fields:
            if field.file_name is None:
                self.text_fields[field.name] = field
            else:
                self.file_fields[field.name] = field
