from plp.core import PostLuminexProcessor


# Input data source directory.
source = 'path/to/input/data/dir'

# Output processed data directory.
destination = 'path/to/output/data/dir'

# Integer number of bio-sheets.
number_of_bio_sheets = 3

# Instantiate plp class.
plp = PostLuminexProcessor(
    source, destination, number_of_bio_sheets,
    save_model_img=True, verbose=False, draw=False)

# Process data.
plp.process_data()
