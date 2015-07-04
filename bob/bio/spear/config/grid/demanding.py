import bob.bio.base

# define a queue with demanding parameters
grid = bob.bio.base.grid.Grid(
  number_of_preprocessing_jobs=48,
  number_of_extraction_jobs=48,
  number_of_projection_jobs=48,
  number_of_enrollment_jobs=48,
  number_of_scoring_jobs=48,
  training_queue = '32G',
  preprocessing_queue = '8G-io-big',
  extraction_queue = '8G-io-big',
  projection_queue = '8G-io-big',
  enrollment_queue = '8G-io-big',
  scoring_queue = '8G-io-big'
)
