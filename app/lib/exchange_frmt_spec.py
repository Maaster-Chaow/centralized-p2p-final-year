"""Specification for the client-server data exhange format

- FormatTypes: defines the types of data format and related methods.

- DATA_EXCHANGE_FORMATS: object containing the specification for
     the actual formats.
- DataFormatError: Exception raised on error in the format.
- DataFormatSpecs: utitlity class for handling data.
"""

import json
from enum import Enum


class FormatTypes(Enum):
    """Various format types for data exchange."""

    CLIENT_INIT = 1
    USR_REGISTRATION = 2
    # TODO

    @staticmethod
    def check_field(dtfrmt, obj):
        """Recursively check that various fields in data_format
        match that of obj.

        return True if fields match otherwise False."""

        if not isinstance(dtfrmt, dict):
            return isinstance(obj, dtfrmt)

        for field in obj:
            if field not in dtfrmt:
                return False
            if not FormatTypes.check_field(dtfrmt[field], obj[field]):
                return False

        return True


DATA_EXCHANGE_FORMATS = {
    FormatTypes.CLIENT_INIT: {
        'c_info': {
            'c_conn' : {
                'ip': str,
                'port' : int,
                },
            'user_id': str,
            },
        'to_peers': list,
        },
    }


class DataFormatError(Exception):
    """Raised when there is any error in the client data."""

    def __init__(self, err_data):
        super().__init__('Client data not in proper format:\n{}'
                         .format(err_data))

class DataCreationError(Exception):
    """Raised when there is any error during the creation
    of particular data format."""
    pass


class DataFormatSpecs(object):
    """Class for creation and validation of data formats for
    communication between client and server.
    """
    __field_sep__ = '0'
    def __init__(self, frmt_type, client_json_data=None):
        self.frmt_type = frmt_type
        if client_json_data is not None:
            self.parse_client_data(client_json_data)

    def parse_client_data(self, client_json_data):
        """Parse client_json_data and set appropriate
        attributes in the class.

        Throw error if there is any problem.
        """
        def setattr_from_fields(instance, d, init_s=''):
            """Set attributes in instance using the fields in d.

            @instance: a class instance.
            @d: dictionary.
            @init_s: initial string."""

            for field in d:
                if len(init_s) > 0:
                    new_s = self.__field_sep__.join([init_s, field])
                else:
                    new_s = field

                if not isinstance(d[field], dict):
                    setattr(instance, new_s, d[field])
                    continue

                setattr_from_fields(instance, d[field], new_s)

        try:
            client_json_obj = json.loads(client_json_data)
        except:
            raise DataFormatError(client_json_obj)

        #fields_match = check_field(data_format, client_json_obj)
        #if not fields_match: #raise exception
        dfrmt_ok = FormatTypes.check_field(DATA_EXCHANGE_FORMATS[self.frmt_type],
            client_json_obj)
        if not dfrmt_ok:
            raise DataFormatError(client_json_obj)

        # set appropriate attributes. Attributes are ste as
        # self.field_nextfield_1_.._nextfiled_n = non_filed.
        setattr_from_fields(self, client_json_obj, self.__field_sep__)

    def create_data(self):
        """Create data according to self.frmt_type.

        @return: dict object, with the appropriate fields set.
        """
        def setfields(d, stls, val):
            if len(stls) == 1:
                d[stls[0]] = val
                return
            if d.get(stls[0], None) is None:
                d[stls[0]] = {}
            setfields(d[stls[0]], stls[1:], val)

        attr_list = [attr for attr in dir(self)
                     if not attr.startswith('_')]
        data_obj = {}
        for attr in attr_list:
            setfields(data_obj, attr.split(__field_sep__), getattr(self, attr))

        return data_obj
