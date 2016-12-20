
class OnlineJudge:
    """ Default Online Judge template. """

    def __init__(self):
        self.domain = 'http://example.com/'
        return

    def get_raw_problem_data(self, problem_id):
        """ Gets problem data from remote server, without further processing.
        This returns the raw data as is from the server, without modifying the
        data. """
        raise NotImplementedError()

    def split_raw_problem_data(self, raw_data):
        """ This divides the raw data into several chunks of raw data and
        may reduce the burden of working on data, afterwards. The interchange
        format can be specified by the engine itself, since it does not require
        global compatibility. """
        raise NotImplementedError()

    def get_metadata(self, data):
        """ This gets the metadata, as in json_data.metadata.data. Return values
        must strictly follow the guidelines. """
        metadata = {
            'title': 'Unknown title',
            'time_limit': 1.0,
            'memory_limit': 67108864,
        }
        raise NotImplementedError()

    def get_description_markdown(self, data):
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

    def get_description_latex(self, data):
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

    def get_objects(self, data):
        """ This function should return a tuple, representing the modified
        data containing the new objects' name notation, unified with a list of
        objects, which must enforce the allowed types specified by the
        guidelines. """
        new_data = data
        new_objects = { }
        return new_data, new_objects

    pass
