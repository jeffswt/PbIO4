
import requests
import storage
import re

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

    def login(self, username, password):
        # Setting initial data.
        url = self.domain + 'login.php'
        data = {
            'user_id': username,
            'password': password,
            'submit': 'Submit',
        }
        # Requesting, without previous session ID
        req = requests.post(url, data=data)
        # Retrieving and setting session ID.
        sessid = req.cookies.get('PHPSESSID', '')
        storage.set(self.engine, 'session_id', sessid)
        # Checking if login works
        ret = self.logged_in()
        return ret

    def logout(self):
        return False

    def logged_in(self):
        # Defining pattern, might change from time to time.
        pattern = r"<th><a href=\./modifypage\.php><b>ModifyUser</b></a>&nbsp;&nbsp;<a href=\'userinfo\.php\?user="
        # Getting main page for determination
        url = self.domain
        sessid = storage.get(self.engine, 'session_id')
        cookies = { 'PHPSESSID': sessid }
        req = requests.get(url, cookies=cookies)
        # Matching with RegEx
        if re.findall(pattern, req.text):
            return True
        # User is not logged in, in my point of view
        return False

    def submit_code(self, problem_id, source_code, code_language):
        raise NotImplementedError()

    def get_submission_status(self, submission_token):
        raise NotImplementedError()
    pass
