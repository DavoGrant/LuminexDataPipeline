import glob
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from plp.reservoir import DataReservoirObject


class PostLuminexProcessor(object):
    """
    Core post plp processing class.

    Looks in source directory for xls files. Iterates over each file
    over each tab. Fits model data. Uses fit to infer concentrations
    of tracer fro observed data. Results are sent to a data reservoir
    class for concatenation and writing.

    Args:
    ====

    source : string,
        absolute path to the root directory containing the plp
        xls files that the user wants processing.

    destination : string,
        absolute path to the directory the user wants the processed
        plp data to be written to.

    Optional:
    ========

    draw : boolean, default False,
        toggle the plotting of the fitted model graphs.

    verbose : boolean, default False,
        toggle verbosity of console printing during the reading,
        processing and writing of the plp processing class.

    """

    def __init__(self, source, destination, save_model_img=True,
                 draw=False, verbose=False):
        # Inputs.
        self.verbose = verbose
        self.draw = draw
        self.save_model_img = save_model_img
        self.data_source = source
        self.data_destination = destination

        # Private attributes.
        self._input_files = []
        self._xls_name = None
        self._xls_data = pd.DataFrame()
        self._bio_marker = None
        self._tab_data = pd.DataFrame()
        self._model_data = pd.DataFrame()
        self._model_func = None
        self._observed_data = pd.DataFrame()
        self._processed_data = pd.Series()

        # Init methods.
        self._find_data()

    def __repr__(self):
        """ String repr of object. """
        return 'Post Luminex processor.'

    def _find_data(self):
        """ Build list of source data files. """
        # Walk source directory building list of xls files.
        target_extension = '/*.xls'
        target_paths = self.data_source + target_extension
        self._input_files = glob.glob(target_paths)

        # Speak.
        if self.verbose:
            print('Found input files:')
            print(self._input_files)

    def _fit_model(self):
        """ Fit model data. """
        # Find data known for the model.
        self._model_data = \
            self._tab_data[np.isfinite(self._tab_data['Exp Conc'])]

        # Set x and y data.
        x = self._model_data['FI - Bkgd'].values
        y = self._model_data['Exp Conc'].values

        # Optimize polynomial coefficients.
        coefficients = np.polyfit(x, y, deg=3)

        # Speak.
        if self.verbose:
            print('Model polynomial coefficients:')
            print(coefficients)

        # Fitted function.
        self._model_func = np.poly1d(coefficients)

        # Speak.
        if self.verbose:
            print('Model polynomial function:')
            print(self._model_func)

        # Draw.
        if self.draw:
            # Create data to draw model fit function.
            x_test = np.linspace(x[0], x[-1], 50)
            y_test = self._model_func(x_test)

            # Add plot to figure.
            fig = plt.figure()
            ax1 = fig.add_subplot(111)

            # Build and show plot.
            ax1.plot(x, y, 'o', x_test, y_test)
            ax1.set_title('Model')
            ax1.set_xlabel('FI - Bkgd')
            ax1.set_ylabel('Exp Conc')
            plt.show()

    def _infer_values_from_model(self):
        """ Infer values from data. """
        # Find data not known yet for processing by the model.
        self._observed_data = \
            self._tab_data[np.isnan(self._tab_data['Exp Conc'])]

        # Remove background row.
        self._observed_data = self._observed_data.drop(
            self._observed_data[self._observed_data['Type'] == 'B'].index)

        # Calculate expected concentration from model.
        self._observed_data['Exp Conc'] = \
            self._observed_data['FI - Bkgd'].apply(
                lambda x: self._model_func(x))

        # Speak.
        if self.verbose:
            print('Calculated concentrations from model:')
            print(self._observed_data['Exp Conc'])

    def _calculate_final_quantity(self):
        """ Calculate final quantity in sample. """
        # Calculate final quantity in sample.
        self._processed_data = self._observed_data.apply(
                lambda row: row['Exp Conc'] * row['Dilution'], axis=1)

        # Speak.
        if self.verbose:
            print('Calculated final quantities in samples:')
            print(self._processed_data)

    def _reservoir_handling(self):
        """ Send the resulting processed data to the reservoir for handling. """
        # Send processed data along with xls file name and tab name to reservoir.
        DataReservoirObject.add_data(
            '_'.join(self._xls_name.split('_')[0:2]), self._bio_marker,
            self._processed_data)

        # Speak.
        if self.verbose:
            print('Finished processing bio marker: {}'.format(self._bio_marker))
            print('from xls file: {}'.format(self._xls_data))

        # Check reservoir and write data to xls files if ready.
        DataReservoirObject.check_reservoir()

    def process_data(self):
        """ Process plp data. """
        # Iterate input files.
        for file in self._input_files:

            # Xls file name.
            self._xls_name = file.split('/')[-1].split('.')[0]

            # Read data in from xls to ordered dictionary of pandas dataframes.
            self._xls_data = pd.read_excel(
                file, sheet_name=None, header=8, skip_footer=9)

            # Speak.
            if self.verbose:
                print('Input file data:')
                print(self._xls_data)

            # Iterate tabs.
            for self._bio_marker, self._tab_data in self._xls_data.items():

                # Speak.
                if self.verbose:
                    print('Bio marker:')
                    print(self._bio_marker)

                # Fit model data.
                self._fit_model()

                # Infer values from data.
                self._infer_values_from_model()

                # Calculate final quantities in sample.
                self._calculate_final_quantity()

                # Send the resulting processed data to the reservoir for handling.
                self._reservoir_handling()

        # Make final check that reservoir is in expected state.
        DataReservoirObject.check_reservoir(final_check=True)

