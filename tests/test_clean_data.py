import unittest
from clean_data import clean_csv_string

class TestDataCleaner(unittest.TestCase):

    def test_clean_csv_str(self):
        messy_input = ("Name, City,Status\n"
                       "  Vakele  ,Cape Town,Active\n"
                       "\n"
                       "John, Johannesburg , Pending \n")
        
        expected_output = ("Name,City,Status\n"
            "Vakele,CAPE TOWN,Active\n"
            "John,JOHANNESBURG,Pending\n")
        
        actual_output = clean_csv_string(messy_input)

        self.assertEqual(actual_output, expected_output)



if __name__ == "__main__":
    unittest.main()