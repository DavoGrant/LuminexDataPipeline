import os
import glob


class DataInspector(object):
    """ Inspector for conducting pre-processing data checks and fixes. """

    def __init__(self, source, destination, verbose=False):
        self.verbose = verbose
        self.data_source = source
        self.data_destination = destination

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
