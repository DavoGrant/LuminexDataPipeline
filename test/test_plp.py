import unittest

from plp.core import PostLuminexProcessor


class TestLuminexProcessor(unittest.TestCase):
    """ Test plp processing. """

    def test_read_in_excel(self):
        """ Check can read in excel spreadsheet to pandas. """
        # Input data source directory.
        source = '/users/grantd/Data/PostLuminexProcessor/test/data/input'

        # Output processed data directory.
        destination = '/users/grantd/Data/PostLuminexProcessor/test/data/output'

        # Instantiate plp class.
        plp = PostLuminexProcessor(
            source, destination, verbose=True, draw=True)

    def test_process_luminex_data(self):
        """ Check can process plp data. """
        # Input data source directory.
        source = '/users/grantd/Data/PostLuminexProcessor/test/data/input'

        # Output processed data directory.
        destination = '/users/grantd/Data/PostLuminexProcessor/test/data/output'

        # Instantiate plp class.
        plp = PostLuminexProcessor(
            source, destination, save_model_img=True,
            verbose=False, draw=False)

        # Process data.
        plp.process_data()


if __name__ == '__main__':
    unittest.main()
