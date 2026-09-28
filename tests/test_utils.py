"""Focused tests that can run in CI without the large CSV or ML libraries."""

import unittest

from utils import get_position_group


class PositionMappingTests(unittest.TestCase):
    def test_one_position_from_each_group(self):
        self.assertEqual(get_position_group("GK"), "Goalkeeper")
        self.assertEqual(get_position_group("CB"), "Defender")
        self.assertEqual(get_position_group("CM"), "Midfielder")
        self.assertEqual(get_position_group("ST"), "Forward")

    def test_full_position_mapping(self):
        from utils import POSITION_MAPPING

        self.assertEqual(len(POSITION_MAPPING), 15)
        self.assertEqual(set(POSITION_MAPPING.values()), {
            "Goalkeeper", "Defender", "Midfielder", "Forward"
        })

    def test_whitespace_and_unknown(self):
        self.assertEqual(get_position_group("  ST  "), "Forward")
        self.assertIsNone(get_position_group("UNKNOWN"))
        self.assertIsNone(get_position_group(None))


if __name__ == "__main__":
    unittest.main()
