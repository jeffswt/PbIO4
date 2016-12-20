
import requests
import storage
import re

class BZOJ:
    """ 大视野在线测评, Hosted on http://www.lydsy.com/ """
    engine = 'BZOJ'

    def __init__(self):
        self.domain = 'http://www.lydsy.com/JudgeOnline/'
        return

    def check_problem_id(self, problem_id):
        convert_fail = False
        try:
            problem_id = int(problem_id)
        except Exception as err:
            convert_fail = True
        if convert_fail or problem_id < 1000:
            raise ValueError('The problem ID "%s" is evidently invalid.' % problem_id)
        return problem_id

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
        # Sending request to remote.
        url = self.domain + 'logout.php'
        sessid = storage.get(self.engine, 'session_id')
        cookies = { 'PHPSESSID': sessid }
        req = requests.get(url, cookies=cookies)
        # Removing session ID from local storage
        storage.remove(self.engine, 'session_id')
        return True

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

    def submit_code(self, problem_id, code_language, source_code):
        problem_id = self.check_problem_id(problem_id)
        # Translating standard language to HustOJ language IDs
        code_id = -1
        if code_language == 'C':
            code_id = 0
        elif code_language == 'C++':
            code_id = 1
        elif code_language == 'Pascal':
            code_id = 2
        elif code_language == 'Java':
            code_id = 3
        elif code_language == 'Python':
            code_id = 6
        # Unsupported language
        if code_id == -1:
            raise ValueError('Language "%s" is not supported on BZOJ.')
        # Uploading solution / source code to server
        url = self.domain + 'submit.php'
        sessid = storage.get(self.engine, 'session_id')
        cookies = { 'PHPSESSID': sessid }
        data = {
            'id': problem_id,
            'language': code_id,
            'source': str(source_code),
        }
        req = requests.post(url, cookies=cookies, data=data,
            allow_redirects=False) # Trick to prevent auto redirection.
        # Checking if successfully submitted
        if req.status_code != 302:
            raise PermissionError('Problem submission for problem "%s" failed.' % problem_id)
        # Successfully submitted problem.
        # TODO: Getting submission token.
        return True

    def get_submission_status(self, submission_token):
        raise NotImplementedError()
    pass
