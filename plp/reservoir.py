import os
import numpy as np
import pandas as pd
from itertools import groupby
from openpyxl import load_workbook


class DataReservoir(object):
    """ Reservoir for handling data as it is processed. """

    def __init__(self, data_destination, verbose=False):
        self.verbose = verbose
        self._data_destination = data_destination
        self._required_bio_sheets = 3
        self._reservoir = pd.DataFrame()

    def __repr__(self):
        """ String repr of object. """
        return 'Post Luminex processed data reservoir.'

    def add_data(self, xls_name, bio_marker, processed_data):
        """ Add processed data to reservoir. """
        # Add processed data as new column in data reservoir.
        self._reservoir[xls_name + '_' + bio_marker] = processed_data

        # Speak.
        if self.verbose:
            print('Processed data currently in reservoir:')
            print(self._reservoir.columns)

    def _write_data(self, reservoir_column_names):
        """ Write data from reservoir to xls files. """
        # Select destination for data.
        file_path = os.path.join(
            self._data_destination, reservoir_column_names[0].split('_')[0] + '.xlsx')
        tab = reservoir_column_names[0].split('_')[2]

        # If destination is not empty, read in so don't overwrite.
        book = None
        book_flag = False
        if os.path.exists(file_path):
            book = load_workbook(file_path)
            book_flag = True

        # Assert in correct bio sheet order.
        key = lambda x: x.split('_')[1]
        reservoir_column_names = sorted(reservoir_column_names, key=key)

        # Concatenate group into one output column of a df.
        reservoir_columns = [self._reservoir[column] for column in reservoir_column_names]
        output_series = pd.concat(reservoir_columns, ignore_index=True)
        output_df = output_series.to_frame(name=tab + ' (pg/mL)')

        # Write data to specific file, tab - without overwriting.
        writer = pd.ExcelWriter(file_path)
        if book_flag:
            writer.book = book
        output_df.to_excel(writer, tab)
        writer.save()
        writer.close()

        # Speak.
        if self.verbose:
            print('Wrote {} to {}.'.format(tab, file_path))

        # Drop written data from reservoir.
        self._reservoir.drop(reservoir_column_names, axis=1, inplace=True)

    def check_reservoir(self, final_check=False):
        """ Check reservoir data and operate accordingly. """
        # Get reservoir columns.
        reservoir_data = self._reservoir.columns.values

        # Sorting and grouping key. By file name (run), tab name (bio marker).
        key = lambda x: x.split('_')[0] + x.split('_')[2]

        # Sort then group.
        groups_object = groupby(sorted(reservoir_data, key=key), key=key)

        # Unpack groups from object to list of numpy arrays.
        groups = list([np.array(list(val)) for key, val in groups_object])

        # Iterate groups.
        for group in groups:

            # Check if reservoir contains a complete group.
            if group.shape[0] == self._required_bio_sheets:

                # Write group out of reservoir to file.
                self._write_data(group)

        if final_check:
            print('All data has been processed.')
