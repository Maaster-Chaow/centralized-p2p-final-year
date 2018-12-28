"""Test module for testing app/lib"""

import os
import sys
import unittest


__this_dir__ = os.path.dirname(os.path.realpath(__file__))
__app_dir__ = os.path.join(__this_dir__, '../app')
sys.path.append(__app_dir__)


from lib import DXFrmt


class FormatTypesTest(unittest.TestCase):
    """Test methods in FormatTypes."""
    def setUp(self):
        self.dtfrmt = DXFrmt.DATA_EXCHANGE_FORMATS[
                        DXFrmt.FormatTypes.CLIENT_INIT]
        self.client_init_obj = {
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


if __name__ == '__main__':
    unittest.main()
