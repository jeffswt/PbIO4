
import bs4
import datetime
import re
import time

import base
import storage
import common

class BZOJ(base.OnlineJudge):
    """ 大视野在线测评, Hosted on http://www.lydsy.com/ """
    engine = 'BZOJ'

    def __init__(self, bypass_proxy=False):
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
        req = common.request('get', url, cookies=cookies)
        # Matching valid section of the webpage.
        text = common.consq_sub(req.text,
            r'\r', r'', # Remove inproper line endings
            r'\u3000', r'  ', # Change full-width spaces to two half-width ones
            r'\n[ \t]*', r'\n', # Remove padding before line
            r'[ \t]*\n', r'\n', # Remove padding after line
        ) # Subsequently remove those.
        # Remove the end
        text = re.sub(r'<div class=content><p><a href=.*?\[<a href=\'bbs\.php\?id=.*?\'>Discuss</a>\](.|\n)*$', r'', text)
        # Remove the beginning
        text = re.sub(r'^(.|\n)*<title>.*?</title>', r'', text)
        return text

    def split_raw_problem_data(self, raw_data):
        # Processing document tags
        title = common.findone(r'<center><h2>\d*?: (.*?)</h2>', raw_data)
        time_limit = common.findone(r'<span class=green>Time Limit: </span>(\d+) Sec', raw_data)
        memory_limit = common.findone(r'<span class=green>Memory Limit: </span>(\d+) MB', raw_data)
        time_limit = int(time_limit) / 1.0
        memory_limit = int(memory_limit) * 1024 * 1024
        # Processing sample data. Inaccuracy guranteed when encountering multi
        # sample data. This is due to the various implementations of Definitions
        # when users upload the problem, and we cannot help.
        s_input = common.findone(r'<h2>Sample Input</h2>.?<div class=content>.?<span class=sampledata>(.*?)</span>.?</div>', raw_data, '', flags=re.S)
        s_output = common.findone(r'<h2>Sample Output</h2>.?<div class=content>.?<span class=sampledata>(.*?)</span>.?</div>', raw_data, '', flags=re.S)
        s_input = common.consq_sub(s_input,
            r'<br( /|/)?>', r'',
            r'\n[ \t]*', r'\n',
            r'[ \t]*\n', r'\n',
        )
        s_output = common.consq_sub(s_output,
            r'<br( /|/)?>', r'',
            r'\n[ \t]*', r'\n',
            r'[ \t]*\n', r'\n',
        )
        # Processing problem description. We only need to split it up, and nothing
        # more for us to do.
        desc = common.findone(r'<h2>Description</h2><div class=content>(.*?)</div><h2>', raw_data, flags=re.S)
        inp = common.findone(r'<h2>Input</h2><div class=content>(.*?)</div><h2>', raw_data, flags=re.S)
        outp = common.findone(r'<h2>Output</h2><div class=content>(.*?)</div><h2>', raw_data, flags=re.S)
        note = common.findone(r'<h2>HINT</h2>.*?<div class=content>(.*?)</div><h2>', raw_data, flags=re.S)
        # Building output
        result = {
            'tags': {
                'title': title,
                'time_limit': time_limit,
                'memory_limit': memory_limit,
            },
            'description': desc,
            'input': inp,
            'output': outp,
            'note': note,
            'sample_data': [ {
                'input': s_input,
                'output': s_output
            } ],
        }
        # Finished building, returning result
        return result

    def get_description_html5(self, data):
        def h5_process(data):
            if not data:
                data = ''
            # Some logical markers
            data = common.consq_sub(data,
                r'、', r', ', # Full width punctuations
                r'（', r' (',
                r'）', r') ',
                r'(&lt;|&gt;)[ ]+=', r'\1=',
                r'\( ([1-9a-zA-Z&=,.;，。；])', r'(\1',
                r'([1-9a-zA-Z&=,.;，。；]) \)', r'\1)',
                r'\) ([,.;，。；])', r')\1',
                r'>[ ]', r'>',
            )
            # Manipulate the rest in bs4
            bs = bs4.BeautifulSoup(data or '', 'html5lib')
            # For compatibility
            for div in bs.find_all('p'):
                div.name = 'div'
            # Removing abstruse formats
            for span in bs.find_all('span'):
                if 'font' not in span['style'] and 'color' not in span['style']:
                    continue
                found = True
                for i in span.children:
                    i.extract()
                    span.insert_before(i)
                span.extract()
            # Removing line-end breaks
            find_brs = bs.find_all('br')
            for cur_brk in find_brs:
                prev_str = cur_brk.previous_element
                next_str = cur_brk.next_element
                if prev_str:
                    prev_str.string = re.sub(r'^[ \n]*', r'', prev_str.string)
                    prev_str = prev_str.string
                else:
                    prev_str = ''
                if next_str:
                    next_str.string = re.sub(r'^[ \n]*', r'', next_str.string)
                    next_str = next_str.string
                else:
                    next_str = ''
                # Pre-define. This is necessary.
                do_remove = True
                len_a = common.get_string_width(prev_str)
                len_b = common.get_string_width(next_str)
                if len_a < len_b * 0.802:
                    do_remove = False
                if len_b < 60 and len_b > len(next_str) * 0.65:
                    do_remove = True
                if do_remove:
                    cur_brk.extract()
                pass
            # Rendering math objects
            m_char = r'[a-zA-Z0-9!&|+\-=^_*/\\%., <>()\[\]\{\}]' # Math characters
            m_only_char = ' ,.()[]{}!'
            sat_strs = bs.find_all(string=re.compile(r'%s+' % m_char))
            for cur_block in sat_strs:
                r_pat = re.compile(r'(%s+)' % m_char)
                o_spl = r_pat.split(cur_block)
                for i in range(0, len(o_spl)):
                    match_res = o_spl[i]
                    # Determining if it really was a math object
                    is_math = True
                    if i % 2 == 0:
                        is_math = False
                    if is_math:
                        is_math = False
                        for j in match_res:
                            if j not in m_only_char:
                                is_math = True
                    if not is_math:
                        cur_block.insert_before(str(match_res))
                        continue
                    # Is really a math object. Processing.
                    match_res = common.consq_sub(match_res,
                        # Arrows that are displayed with tricks
                        r'<[\-]+>', r' \\longleftrightarrow ',
                        r'<[=]+>', r' \\Longleftrightarrow ',
                        r'[\-]+>', r' \\longrightarrow ',
                        r'[=]+>', r' \\Longrightarrow ',
                        r'<[\-]+', r' \\longleftarrow ',
                        r'<[=]+', r' \\Longleftarrow ',
                        # Standarized LaTeX comparison symbols
                        '>=', r' \\geq ',
                        '<=', r' \\leq ',
                        '>', r' \\gt ',
                        '<', r' \\lt ',
                        '≈', r' \\approx ',
                        # Additional symbols
                        r'\*', r' \\times ',
                        r'\^([0-9a-zA-Z_])', r'^{\1}',
                        r'(\.\.\.+)', r' \\ldots ',
                        # Miscellaneous, formatting
                        r'([+\-=])', r' \1 ',
                        r'^(.*)$', r' \1 ', # Making extra space at beginning.
                        r'[ ]+', ' ', # Removing places with too much spaces
                        r'^ (.*) $', r'\1', # Removing extra space at ends
                    )
                    # Inserting before this block.
                    n_tag = bs.new_tag('span', **{'class': 'math inline'})
                    n_tag.string = match_res
                    cur_block.insert_before(n_tag)
                    pass
                # Removing this blob.
                cur_block.extract()
                pass
            # Removing line breaks
            for s_str in bs.find_all(string=re.compile(r'.*')):
                s_str.string = re.sub(r'\n', r'', s_str.string)
            # Prettify output
            data = '\n'.join(str(i) for i in bs.body.find_all('div'))
            data = data.replace('\n', '').replace('<br/>', '</div><div>')\
                .replace('<div></div>', '').replace('<div> </div>', '')
            print(data, '\n\n\n\n\n\n')
            # Re-work in bs4 and re-write output.
            bs = bs4.BeautifulSoup(data, 'html5lib')
            print(bs, '\n\n\n\n\n\n')
            data = '\n'.join(str(i) for i in bs.body.find_all('div'))
            return data
        description = {
            'description': h5_process(data['description']),
            'input': h5_process(data['input']),
            'output': h5_process(data['output']),
            'note': h5_process(data['note']),
        }
        return description

    def get_description_markdown(self, data, h5_data):
        description = {
            'description': '',
            'input': '',
            'output': '',
            'note': '',
        }
        return description
        raise NotImplementedError()

    def get_description_latex(self, data, h5_data):
        description = {
            'description': '',
            'input': '',
            'output': '',
            'note': '',
        }
        return description
        raise NotImplementedError()

    def get_objects__(self, data):
        img_idx = re.findall(
            r'<img .*?src=".*?"[^>]*?>',
            data)
        objects = []
        for img in img_idx:
            img_path = common.findone(r'src="(.*?)"', img)
            if not img_path:
                continue
            # Download image from remote server
            url = self.domain + img_path
            sessid = storage.get(self.engine, 'session_id')
            cookies = { 'PHPSESSID': sessid }
            req = common.request('get', url, cookies=cookies, stream=True)
            img_data = req.raw.read()
            # Converting into allowed formats and calculating hash
            img_data = common.convert_image(img_data)
            img_hash = common.sha256(img_data)
            # Generating new name
            n_name = img_hash[:8] + '.png'
            # Replacing descriptor in HTML
            data = data.replace(img, '<img src="%s">' % n_name)
            # Inserting into objects directory
            objects.append({
                'name': n_name,
                'hash': img_hash,
                'data': img_data,
            })
            pass
        return data, objects

    def login(self, username, password):
        # Retrieving session ID.
        url = self.domain + 'loginpage.php'
        req = common.request('get', url, cookies={'PHPSESSID': ''})
        sessid = req.cookies.get('PHPSESSID', '')
        storage.set(self.engine, 'session_id', sessid)
        # Setting initial data.
        url = self.domain + 'login.php'
        data = {
            'user_id': username,
            'password': password,
            'submit': 'Submit',
        }
        # Requesting, with retrieved session ID
        cookies = { 'PHPSESSID': sessid }
        req = common.request('post', url, cookies=cookies, data=data)
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
        req = common.request('get', url, cookies=cookies)
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
        req = common.request('get', url, cookies=cookies)
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
        req = common.request('post', url, cookies=cookies, data=data,
            allow_redirects=False)
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
        req = common.request('get', url, cookies=cookies)
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
                req = common.request('get', url, cookies=cookies)
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
            req = common.request('get', url, cookies=cookies)
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

b = BZOJ()
h = b.get_raw_problem_data(1001)
h, obj = b.get_objects(h)
s = b.split_raw_problem_data(h)
print(s, '\n\n\n')
# dec = s['description']
# dec = re.sub('<br />', '<br>', dec)
# bs = bs4.BeautifulSoup(dec, 'html5lib')
# ph = '\n'.join(i.prettify() for i in bs.body.find_all('p'))
h5 = b.get_description_html5(s)
for i in h5:
    print('================================\n',i,'\n',h5[i],'\n')
