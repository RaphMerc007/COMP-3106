
def naive_bayes_classifier(dataset_filepath, snake_measurements):
  # dataset_filepath is the full file path to a CSV file containing the dataset
  # snake_measurements is a list of [length, weight, speed] measurements for a snake

  most_likely_class = None
  class_probabilities = None



  # TODO: Read dataset.csv and train the model to get W
  
  # TODO: read snake_measurements.txt as X

  # TODO: we will loop through each class and run probability density function with the snake_measurements for each class


  
  # most_likely_class is a string indicating the most likely class, either "anaconda", "cobra", or "python"
  # class_probabilities is a three element list indicating the probability of each class in the order [anaconda probability, cobra probability, python probability]
  return most_likely_class, class_probabilities




def probability_density_function(dataset_filepath, snake_measurements, class_name):
  #TODO: P(feature | class) = 1/sqrt(2*pi*sigma^2) * e**(-(x-mu)^2 / (2*sigma^2))
  return

def get_sigma(dataset_filepath, class_name):
  #TODO: get the standard deviation for the given class
  return

def get_mu(dataset_filepath, class_name):
  #TODO: get the mean for the given class
  return