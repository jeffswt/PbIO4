
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
        # Setting user name into local storage.
        if ret == True:
            storage.set(self.engine, 'user_id', username)
        else:
            storage.remove(self.engine, 'session_id')
        return ret

    def logout(self):
        # Sending request to remote.
        url = self.domain + 'logout.php'
        sessid = storage.get(self.engine, 'session_id')
        cookies = { 'PHPSESSID': sessid }
        req = requests.get(url, cookies=cookies)
        # Removing session ID from local storage
        storage.remove(self.engine, 'session_id')
        storage.remove(self.engine, 'user_id')
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
        # Getting submission token.
        userid = storage.get(self.engine, 'user_id')
        url = self.domain + 'status.php?user_id=%s' % userid
        # WARNING: THIS PROCEDURE WOULD BE MALFUNCTIONING IF YOU ARE SUBMITTING
        # A LARGE AMOUNT OF CODE MEANWHILE, WHICH IN THIS CASE YOU WOULDN'T BE
        # ABLE TO SINCE THE TIME LIMIT IS 1 SUBMISSION PER 10 SECONDS. THEREFORE
        # THIS PROCEDURE HAS MERELY A SLIGHT CHANCE OF BREAKING.
        req = requests.get(url, cookies=cookies)
        pattern = r'^<tr align=center class=\'evenrow\'><td>(\d*?)<td>'
        sub_id = re.findall(pattern, req.text, re.M)
        if len(sub_id) > 0:
            sub_id = int(sub_id[0])
        else:
            raise RuntimeError('Unable to retrieve submission token for problem submission.')
        return sub_id

    def get_submission_status(self, submission_token):
        raise NotImplementedError()
    pass
