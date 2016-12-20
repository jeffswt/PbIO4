
class BZOJ:
    """ 大视野在线测评, Hosted on http://www.lydsy.com/ """
    engine = 'BZOJ'

    def __init__(self):
        self.domain = 'http://www.lydsy.com/JudgeOnline/'
        return

    def get_raw_problem_data(self, problem_id):
        raise NotImplementedError()

    def split_raw_problem_data(self, raw_data):
        raise NotImplementedError()

    def get_description_markdown(self, data):
        description = {
            'description': '',
            'input': '',
            'output': '',
            'note': '',
        }
        raise NotImplementedError()

    def get_description_latex(self, data):
        description = {
            'description': '',
            'input': '',
            'output': '',
            'note': '',
        }
        raise NotImplementedError()

    def get_description_html5(self, data):
        description = {
            'description': '',
            'input': '',
            'output': '',
            'note': '',
        }
        raise NotImplementedError()

    def get_objects(self, data):
        new_data = data
        new_objects = []
        return new_data, new_objects

    def login_server(self, username, password):
        return False

    def logout_server(self):
        return False
    
    def get_login_status(self):
        return False

    def submit_code(self, problem_id, source_code, code_language):
        raise NotImplementedError()

    def get_submission_status(self, submission_token):
        raise NotImplementedError()
    pass
