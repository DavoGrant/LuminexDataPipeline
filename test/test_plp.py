import unittest

from plp.core import PostLuminexProcessor
from plp.reservoir import DataReservoir


class TestLuminexProcessor(unittest.TestCase):
    """ Test plp. """

    def __init__(self, *args, **kwargs):
        super(TestLuminexProcessor, self).__init__(*args, **kwargs)
        self.verbose = False
        self.source = '/users/grantd/Data/LuminexDataPipeline/test/data/input'
        self.destination = '/users/grantd/Data/LuminexDataPipeline/test/data/output'
        self.number_of_bio_sheets = 3

    def test_read_in_excel(self):
        """ Check can read in excel spreadsheet to pandas. """
        # Instantiate plp class.
        plp = PostLuminexProcessor(
            self.source, self.destination, self.number_of_bio_sheets,
            save_model_img=True, verbose=False, draw=False)

        # Checks.
        self.assertIsInstance(plp._data_reservoir, DataReservoir)

    def test_process_luminex_data(self):
        """ Check can process plp data. """
        # Instantiate plp class.
        plp = PostLuminexProcessor(
            self.source, self.destination, self.number_of_bio_sheets,
            save_model_img=True, verbose=True, draw=True)

        # Process data.
        plp.process_data()


if __name__ == '__main__':
    unittest.main()
