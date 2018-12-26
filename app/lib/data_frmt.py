"""Utilities for data formats used in transfer.

Given a data format, parse input json string into python
objects and retrieve relevant info from the object.

1. client_init_data : dataformat when client initiates the
   connection with the server. the format is given as below;
       {'client_info': { 'conn_info': {
                          'ip': 'address'<string>,
                          'port': 'port'<int>
                         },
                         'user_id': 'id'<string>,
                       }
        'to_peers': { ['user_id' <string>, ...] },
       }
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

        if type(dtfrmt) is not dict:
            return type(obj) is dtfrmt

        for field in obj:
            if field not in dtfrmt: return False
            if not check_field(dtfrmt[field], obj[field]):
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
        


class DataFormatSpecs():
    """Data format specification for communication between
    the client and the server.
    """

    def __init__(self, frmt_type):
        self.frmt_type = frmt_type
    
    def parse_client_data(self, client_json_data):
        """Parse client_json_data and set appropriate
        fields in the class.
        
        Throw error if there is any problem.
        
        Fields:
        1. client_addr: set to client address.
        2. client_port: set to client port.
        3. client_uuid: set to client user_id.
        4. snd_to_peers: list of peer ids to send message.
        """
        try:
            client_json_obj = json.loads(client_json_data)
        except:
            raise DataFormatError(client_json_obj)
        
        #fields_match = check_field(data_format, client_json_obj)
        #if not fields_match: #raise exception
        dfrmt_ok = check_field(DATA_EXCHANGE_FORMATS[self.frmt_type]
                               , client_json_obj)
        if not dfrmt_ok:
            raise DataFormatError(client_json_obj)

        client_info = client_json_obj['c_info']
        self.client_addr = client_info['c_conn']['ip']
        self.client_port = client_info['c_conn']['port']
        self.client_uuid = client_info['uuid']
        self.snd_to_peers = client_json_obj['to_peers']

        if len(self.snd_to_peers) > 0:
            if type(self.snd_to_peers[0]) is not str:
                raise DataFormatError(client_json_obj)
