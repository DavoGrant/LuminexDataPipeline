import os
import glob
import numpy as np
from itertools import groupby


class DataInspector(object):
    """ Inspector for conducting pre-processing data checks and fixes. """

    def __init__(self, source, destination, verbose=False):
        self.verbose = verbose
        self.data_source = source
        self.data_destination = destination
        self._required_bio_sheets = 3

    def __repr__(self):
        """ String repr of object. """
        return 'Pre-processing data inspector object.'

    def check_destination_status(self):
        """ Perform checks and fixes on data destination. """
        # Check destination folder exists, if not make it.
        if not os.path.exists(self.data_destination):
            os.makedirs(self.data_destination)
        else:
            # Require empty destination folder.
            if glob.glob(os.path.join(self.data_destination, '*')):
                raise OSError('The destination directory is not empty. \n'
                              'Please select an empty folder to avoid '
                              'overwriting data.')

        # Speak.
        if self.verbose:
            print('Destination checks and fixes complete.')

    def check_data_source(self, input_paths):
        """ Perform checks on data source. """
        # Check source folder exists.
        if not os.path.exists(self.data_source):
            raise OSError('The directory selected as the data source '
                          'does not exist.')

        # Check data has been found.
        if not input_paths:
            raise OSError('No .xls files have been found in the data '
                          'source directory selected.')

        # Check all three bio-sheets present for each sample/analyte.
        input_files = [os.path.split(f)[1] for f in input_paths]

        # Sorting and grouping key. By file name (run), tab name (bio marker).
        key = lambda x: x.split('_')[0]

        # Sort then group.
        groups_object = groupby(sorted(input_files, key=key), key=key)

        # Unpack groups from object to list of numpy arrays.
        groups = list([np.array(list(val)) for key, val in groups_object])

        # Iterate groups.
        for group in groups:

            # Check if reservoir contains a complete group.
            if not group.shape[0] == self._required_bio_sheets:
                raise OSError(
                    'Only {} out of the {} bio-sheets were '
                    'found for the {} samples.'.format(
                        str(group.shape[0]), str(self._required_bio_sheets),
                        str(group[0].split('_')[0])))

        # Speak.
        if self.verbose:
            print('Data source checks complete.')
