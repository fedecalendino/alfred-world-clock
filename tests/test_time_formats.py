import unittest
import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from main import convert_to_time


class TestTimeFormats(unittest.TestCase):
    
    def test_hh_mm_ss_format(self):
        """Test HH:MM:SS format"""
        hour, minute, second = convert_to_time("14:30:45")
        self.assertEqual(hour, 14)
        self.assertEqual(minute, 30)
        self.assertEqual(second, 45)
    
    def test_hh_mm_format(self):
        """Test HH:MM format"""
        hour, minute, second = convert_to_time("14:30")
        self.assertEqual(hour, 14)
        self.assertEqual(minute, 30)
        self.assertEqual(second, 0)
    
    def test_hhmmss_format(self):
        """Test HHMMSS format (new feature)"""
        hour, minute, second = convert_to_time("143045")
        self.assertEqual(hour, 14)
        self.assertEqual(minute, 30)
        self.assertEqual(second, 45)
    
    def test_hhmm_format(self):
        """Test HHMM format (new feature)"""
        hour, minute, second = convert_to_time("1430")
        self.assertEqual(hour, 14)
        self.assertEqual(minute, 30)
        self.assertEqual(second, 0)
    
    def test_edge_cases(self):
        """Test edge cases with leading zeros"""
        # Test early morning time
        hour, minute, second = convert_to_time("0830")
        self.assertEqual(hour, 8)
        self.assertEqual(minute, 30)
        self.assertEqual(second, 0)
        
        # Test midnight
        hour, minute, second = convert_to_time("0000")
        self.assertEqual(hour, 0)
        self.assertEqual(minute, 0)
        self.assertEqual(second, 0)
        
        # Test just before midnight
        hour, minute, second = convert_to_time("2359")
        self.assertEqual(hour, 23)
        self.assertEqual(minute, 59)
        self.assertEqual(second, 0)
    
    def test_invalid_formats(self):
        """Test that invalid formats raise ValueError"""
        with self.assertRaises(ValueError):
            convert_to_time("25:00")  # Invalid hour
        
        with self.assertRaises(ValueError):
            convert_to_time("abc")    # Non-numeric
        
        with self.assertRaises(ValueError):
            convert_to_time("123")    # Too short for HHMM
        
        with self.assertRaises(ValueError):
            convert_to_time("12345")  # Too long for HHMM but too short for HHMMSS


if __name__ == '__main__':
    unittest.main()