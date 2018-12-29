"""Test module for testing app/lib"""

import os
import sys
import unittest
import json


__this_dir__ = os.path.dirname(os.path.realpath(__file__))
__app_dir__ = os.path.join(__this_dir__, '../app')
sys.path.append(__app_dir__)


from lib import DXFrmt


class TestFormatTypes(unittest.TestCase):
    """Test methods in FormatTypes."""
    def setUp(self):
        self.dtfrmt = DXFrmt.DATA_EXCHANGE_FORMATS[
                        DXFrmt.FormatTypes.CLIENT_INIT]
        self.client_init_obj = {
            'd_head': 'client_init',
            'c_info' : {
                'c_conn': {
                    'ip': '127.0.0.1',
                    'port': 12345,
                    },
                'user_id': '8123145534',
                },
            'to_peers': ['1', '2', '3'],
            }

    def test_check_field_method(self):
        self.assertTrue(DXFrmt.FormatTypes.check_field(
                        self.dtfrmt, self.client_init_obj))
        self.assertFalse(DXFrmt.FormatTypes.check_field(
                        self.dtfrmt, {'a':[],'b':'happy'}))


class TestDataFormatSpecs(unittest.TestCase):
    """Test DataFormatSpecs class in lib."""

    def setUp(self):
        self.dtfrmt = DXFrmt.DATA_EXCHANGE_FORMATS[
                        DXFrmt.FormatTypes.CLIENT_INIT]
        self.client_init_obj = {
            'd_head' : 'client_init',
            'c_info' : {
                'c_conn': {
                    'ip': '127.0.0.1',
                    'port': 12345,
                    },
                'user_id': '8123145534',
                },
            'to_peers': ['1', '2', '3'],
            }
        self.fields = {
            '00d_head': 'client_init',
            '00c_info0c_conn0ip': '127.0.0.1',
            '00c_info0c_conn0port': 12345,
            '00c_info0user_id': '8123145534',
            '00to_peers': ['1', '2', '3']
        }
        self.client_init_json = json.dumps(self.client_init_obj)

    def test_parse_client_data(self):
        frmt = DXFrmt.FormatTypes.CLIENT_INIT
        oDxfrmt = DXFrmt.DataFormatSpecs(frmt, self.client_init_json)
        field_sep = DXFrmt.DataFormatSpecs.__field_sep__
        fields_set = [f for f in dir(oDxfrmt) if f.startswith(field_sep)]
        self.assertTrue(len(fields_set), len(self.fields))
        for f in fields_set:
            self.assertEqual(self.fields[f], getattr(oDxfrmt, f))

    def test_create_data(self):
        frmt = DXFrmt.FormatTypes.CLIENT_INIT
        oDxfrmt = DXFrmt.DataFormatSpecs(frmt, self.client_init_json)
        oData = oDxfrmt.create_data()
        self.assertEqual(self.client_init_obj, oData)



if __name__ == '__main__':
    unittest.main()
