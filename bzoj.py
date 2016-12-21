
import datetime
import re
import requests
import storage
import time

class BZOJ:
    """ 大视野在线测评, Hosted on http://www.lydsy.com/ """
    engine = 'BZOJ'
    default_timeout = 3.0

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
        problem_id = self.check_problem_id(problem_id)
        # Just requesting data
        url = self.domain + 'problem.php?id=%d' % problem_id
        sessid = storage.get(self.engine, 'session_id')
        if sessid:
            cookies = { 'PHPSESSID': sessid }
        else:
            cookies = { }
        # Safely request to remote server
        connection_established = True
        try:
            req = requests.get(url, cookies=cookies, timeout=self.default_timeout)
            req.encoding = 'utf-8'
        except Exception as err:
            connection_established = False
        if not connection_established:
            raise IOError('Remote server is unreachable.')
        # Matching valid section of the webpage.
        def consq_sub(text, *args):
            for i in range(0, int(len(args) / 2)):
                text = re.sub(args[i*2], args[i*2+1], text)
            return text
        text = consq_sub(req.text,
            r'\r', r'', # Remove inproper line endings
            r'\n[ \t]*', r'\n')
        return text

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
        # Safely request to remote server
        connection_established = True
        try:
            req = requests.post(url, data=data, timeout=self.default_timeout)
        except Exception as err:
            connection_established = False
        if not connection_established:
            raise IOError('Remote server is unreachable.')
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
        if not sessid:
            raise ValueError('User is not logged in.')
        cookies = { 'PHPSESSID': sessid }
        # Safely request to remote server
        connection_established = True
        try:
            req = requests.get(url, cookies=cookies, timeout=self.default_timeout)
        except Exception as err:
            connection_established = False
        if not connection_established:
            raise IOError('Remote server is unreachable.')
        # Removing session ID from local storage
        storage.remove(self.engine, 'session_id')
        storage.remove(self.engine, 'user_id')
        return True

    def logged_in(self):
        # Defining pattern, might change from time to time.
        pattern = r'<th><a href=\./modifypage\.php><b>ModifyUser</b></a>&nbsp;&nbsp;<a href=\'userinfo\.php\?user='
        # Getting main page for determination
        url = self.domain
        sessid = storage.get(self.engine, 'session_id')
        cookies = { 'PHPSESSID': sessid }
        # Safely request to remote server
        connection_established = True
        try:
            req = requests.get(url, cookies=cookies, timeout=self.default_timeout)
        except Exception as err:
            connection_established = False
        if not connection_established:
            raise IOError('Remote server is unreachable.')
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
        # Safely request to remote server
        connection_established = True
        try:
            req = requests.post(url, cookies=cookies, data=data,
                allow_redirects=False, timeout=self.default_timeout)
        except Exception as err:
            connection_established = False
        if not connection_established:
            raise IOError('Remote server is unreachable.')
        # Checking if successfully submitted
        if req.status_code != 302:
            # Retrieve error information
            pattern = r'^(.*?>)[^>]+<br>\r\n'
            match = re.findall(pattern, req.text, re.M)
            if len(match) > 0:
                if match[0] == 'You should not submit more than twice in 10 seconds.....<br>':
                    raise PermissionError('Your submission is too frequent.')
                elif match[0] == '<a href=\'loginpage.php\'>Please Login First!</a>':
                    raise PermissionError('You need to login before you could make any submissions.')
                else:
                    pass
            raise PermissionError('Problem submission failed (reason unknown).')
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
        # Converting submission token.
        convert_fail = False
        try:
            submission_token = int(submission_token)
        except Exception as err:
            convert_fail = True
        if convert_fail or submission_token < 1000:
            raise ValueError('The submission token is invalid.')
        # Requesting status.
        url = self.domain + 'status.php?top=%d' % submission_token
        sessid = storage.get(self.engine, 'session_id')
        cookies = { 'PHPSESSID': sessid }
        # Safely request to remote server
        connection_established = True
        try:
            req = requests.get(url, cookies=cookies, timeout=self.default_timeout)
        except Exception as err:
            connection_established = False
        if not connection_established:
            raise IOError('Remote server is unreachable.')
        # Matching values
        pattern = r'^<tr align=center class=\'evenrow\'><td>(.*?)<td><a href=\'userinfo\.php\?user=.*?\'>(.*?)</a><td><a href=\'problem\.php\?id=.*?\'>(.*?)</a><td>(.*?)<td>(.*?)<td>(.*?)<td>(.*?)<td>(.*?) B<td>(.*?)</tr>'
        match = re.findall(pattern, req.text, re.M)
        # Checking submission token validity
        if len(match) <= 0:
            raise ValueError('The submission token is invalid.')
        match = list(match[0])
        if int(match[0]) < submission_token:
            raise ValueError('The submission token is invalid.')
        # Generating result
        result = {
            'token': submission_token,
            'username': match[1],
            'problem_id': match[2],
            'time': int(re.sub(r' <font color=red>ms</font>', r'', match[5])) / 1000,
            'memory': int(re.sub(r' <font color=red>kb</font>', r'', match[4])) * 1024,
            'code_language': '', # Needs further processing
            'code_length': int(match[7]),
            'code': '', # Needs further processing
            'status': (), # Needs further processing
            'submit_time': datetime.datetime.fromtimestamp(
                time.mktime(time.strptime(match[8], '%Y-%m-%d %H:%M:%S')) - 8 * 60 * 60
                ).strftime('%Y-%m-%dT%H:%M:%S'),
        }
        # Processing code language
        lang_map = { 'C': 'C', 'C++': 'C++', 'Pascal': 'Pascal', 'Java': 'Java',
            'Python': 'Python3' }
        match[6] = re.sub(r'<a target=_blank href=showsource\.php\?id=.*?>(.*?)</a>/<a target=_self href=\"submitpage\.php\?id=.*?&sid=.*?\">Edit</a>',
            r'\1', match[6])
        result['code_language'] = lang_map[match[6]]
        # Processing status code
        status_map = {
            'Pending': ('Pending', 'Pending for judging.'),
            'Pending_Rejudging': ('Pending', 'Pending forr rejudging.'),
            'Compiling': ('Compiling', 'Compiling...'),
            'Running_&_Judging': ('Running', 'Running and judging...'),
            'Compile_Error': ('Compile Error', ''), # Needs to be further processed
            'Runtime_Error': ('Runtime Error', 'Runtime Error.'),
            'Time_Limit_Exceed': ('Time Limit Exceeded', 'Time Limit Exceeded'),
            'Memory_Limit_Exceed': ('Memory Limit Exceeded', 'Memory Limit Exceeded'),
            'Output_Limit_Exceed': ('Output Limit Exceeded', 'Output Limit Exceeded'),
            'Wrong_Answer': ('Wrong Answer', 'Wrong Answer.'),
            'Presentation_Error': ('Presentation Error', 'Presentation Error.'),
            'Accepted': ('Accepted', 'Accepted!'),
        }
        match[3] = re.sub(r'<font color=.*?>(.*?)</font>', r'\1', match[3])
        if 'Compile_Error' in match[3]:
            match[3] = re.sub(r'<a href=.*?>(.*?)</a>', r'\1', match[3])
        if match[3] not in status_map:
            status = 'Unknown'
        else:
            status = status_map[match[3]]
        if status[0] == 'Compile Error':
            if result['username'] == storage.get(self.engine, 'user_id'):
                url = self.domain + 'ceinfo.php?sid=%d' % submission_token
                sessid = storage.get(self.engine, 'session_id')
                cookies = { 'PHPSESSID': sessid }
                # Safely request to remote server
                connection_established = True
                try:
                    req = requests.get(url, cookies=cookies, timeout=self.default_timeout)
                except Exception as err:
                    connection_established = False
                if not connection_established:
                    raise IOError('Remote server is unreachable.')
                # Retrieve CE info
                ce_info = re.findall(r'<pre>(.*?)</pre>', req.text, re.S)
                if len(ce_info) <= 0:
                    ce_info = ''
                else:
                    ce_info = ce_info[0]
                status = ('Compile Error', ce_info)
            else:
                status = ('Compile Error', 'Compile Error')
            pass
        result['status'] = status
        # Retrieving source code
        if result['username'] == storage.get(self.engine, 'user_id'):
            url = self.domain + 'submitpage.php?id=%s&sid=%d' % (result['problem_id'], submission_token)
            sessid = storage.get(self.engine, 'session_id')
            cookies = { 'PHPSESSID': sessid }
            # Safely request to remote server
            connection_established = True
            try:
                req = requests.get(url, cookies=cookies, timeout=self.default_timeout)
            except Exception as err:
                connection_established = False
            if not connection_established:
                raise IOError('Remote server is unreachable.')
            # Retrieve CE info
            code = re.findall(r'<textarea.*?>(.*?)</textarea>', req.text, re.S)
            if len(code) <= 0:
                code = ''
            else:
                code = code[0]
            result['code'] = code
        # Submission status retrieval succeeded.
        return result
    pass
