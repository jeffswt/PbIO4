
import binascii
import time

class OnlineJudge:
    """ Default Online Judge template. """
    engine = 'Default' # Specify this on class inheritance

    def __init__(self):
        self.domain = 'http://example.com/'
        return

    ############################################################################
    #  Problems related
    ############################################################################

    def get_raw_problem_data(self, problem_id):
        """ Gets problem data from remote server, without further processing.
        This returns the raw data as is from the server, without modifying the
        data. """
        raise NotImplementedError()

    def split_raw_problem_data(self, raw_data):
        """ This divides the raw data into several chunks of raw data and
        may reduce the burden of working on data, afterwards. The interchange
        format can be specified by the engine itself, since it does not require
        global compatibility.

        This procedure should also filter out the metadata for the problem,
        as inserted in result.tags.*. """
        raise NotImplementedError()

    def get_description_html5(self, data):
        """ This gets the problem description in HTML5, as in
        json_data.problem.HTML5. Return values must strictly follow the
        guidelines. """
        description = {
            'description': '',
            'input': '',
            'output': '',
            'note': '',
        }
        raise NotImplementedError()

    def get_description_markdown(self, data, h5_data):
        """ This gets the problem description in Markdown, as in
        json_data.problem.Markdown. Return values must strictly follow the
        guidelines. """
        description = {
            'description': '',
            'input': '',
            'output': '',
            'note': '',
        }
        raise NotImplementedError()

    def get_description_latex(self, data, h5_data):
        """ This gets the problem description in LaTeX, as in
        json_data.problem.LaTeX. Return values must strictly follow the
        guidelines. """
        description = {
            'description': '',
            'input': '',
            'output': '',
            'note': '',
        }
        raise NotImplementedError()

    def get_objects(self, data):
        """ This function should return a tuple, representing the modified
        data containing the new objects' name notation, unified with a list of
        objects, which must enforce the allowed types specified by the
        guidelines. """
        new_data = data
        new_objects = []
        return new_data, new_objects

    def get_problem_json(self, problem_id):
        """ Retrieves a json of problem description, not compressed. Returns a
        standardized object notation, composed of dict() and list().

        This function **SHOULD NOT BE OVERRIDDEN**!"""
        # Getting raw data from server
        raw_data = self.get_raw_problem_data(problem_id) or ''
        # Retrieving objects
        raw_data, objects = self.get_objects(raw_data)
        for i in range(0, len(objects)):
            j = objects[i]
            j['data'] = binascii.hexlify(j['data']).decode('utf-8')
            objects[i] = j
        # Splitting data into separate objects
        split_data = self.split_raw_problem_data(raw_data) or {}
        # Rendering raw data to different languages
        dat_empty = {
            'description': '',
            'input': '',
            'output': '',
            'note': '',
        }
        dat_h5 = self.get_description_html5(split_data) or dat_empty
        dat_md = self.get_description_markdown(split_data, dat_h5) or dat_empty
        dat_ltx = self.get_description_latex(split_data, dat_h5) or dat_empty
        # Building objected output
        default_json = {
            'metadata': {
                'engine': self.engine,
                'id': problem_id,
                'time_created': time.strftime('%Y-%m-%dT%H:%M:%S', time.gmtime()),
                'tags': {
                    'title': split_data.get('tags',{}).get('title', 'Untitled'),
                    'time_limit': split_data.get('tags',{}).get('time_limit', 1.0),
                    'memory_limit': split_data.get('tags',{}).get('memory_limit', 67108864),
                },
            },
            'problem': {
                'HTML': raw_data,
                'HTML5': dat_h5,
                'Markdown': dat_md,
                'LaTeX': dat_ltx,
            },
            'sample_data': split_data.get('sample_data', []),
            'objects': objects,
        }
        # Finished construction
        return default_json

    ############################################################################
    #  User login related
    ############################################################################

    def login(self, username, password):
        """ Login to server with given username and password. Login status
        should be saved to local session storage. """
        return False

    def logout(self):
        """ Logout from server. Previous data should be removed from local
        session storage. """
        return False

    def logged_in(self):
        """ Returns if current client is logged into server with the specific
        tokens in local session storage. """
        return False

    ############################################################################
    #  Submissions related
    ############################################################################

    def submit_code(self, problem_id, source_code, code_language):
        """ Submits code to remote server, and returns the handle to this
        specif submission, if remote server supports this function. """
        raise NotImplementedError()

    def get_submission_status(self, submission_token):
        """ Returns a valid submission status, as defined in the guidelines.
        Must pass in a valid submission token. """
        raise NotImplementedError()
    pass
