__author__ = 'gregChambers'

class SightingResponse(object):

    def __init__(self):
        """
        : attribute action_type : string
        : attribute action_token : string
        """
        self.action_type = None
        self.action_token = None


class BaseClass(object):

    def __init__(self):
        """
        : attribute sighting_response : array
        : attribute session_i_d : string
        : attribute expiration : string
        : attribute timestamp : string
        """
        self.sighting_response = None
        self.session_i_d = None
        self.expiration = None
        self.timestamp = None

