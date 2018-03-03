from plp.core import PostLuminexProcessor


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
