import pandas as pd
import numpy as np

# Global constants
ANACONDA = "anaconda"
COBRA = "cobra"
PYTHON = "python"

def naive_bayes_classifier(dataset_filepath, snake_measurements):
  # dataset_filepath is the full file path to a CSV file containing the dataset
  # snake_measurements is a list of [length, weight, speed] measurements for a snake

  most_likely_class = None
  class_probabilities = None

  # TODO: Read dataset.csv and train the model to get W

  # Read dataset.csv and get the corresponding y vector and X matrix for its data
  y, X = extract_data(dataset_filepath)

  cobra_density = get_probability_density_function(y, X, snake_measurements, COBRA)
  print(cobra_density)
  conda_density = get_probability_density_function(y, X, snake_measurements, ANACONDA)
  print(conda_density)
  python_density = get_probability_density_function(y, X, snake_measurements, PYTHON)
  print(python_density)


  # Extract rows corresponding to a certain snake
  # cobra_rows = X[y == COBRA]
  # print(cobra_rows)
  
  # TODO: read snake_measurements.txt as X

  # TODO: we will loop through each class and run probability density function with the snake_measurements for each class


  
  # most_likely_class is a string indicating the most likely class, either "anaconda", "cobra", or "python"
  # class_probabilities is a three element list indicating the probability of each class in the order [anaconda probability, cobra probability, python probability]
  return most_likely_class, class_probabilities


# Extract data from dataset.csv, and return the corresponding y vector and X matrix
def extract_data(dataset_filepath):

  # Load CSV file and assign column names
  csv = pd.read_csv(dataset_filepath, header=None, names=["class", "length", "weight", "speed"]) 

  # Extract our labels and features seperately as an y vector and X matrix
  y = csv["class"].values 
  X = csv[["length", "weight", "speed"]].values

  return y, X


#TODO: P(feature | class) = 1/sqrt(2*pi*sigma^2) * e**(-(x-mu)^2 / (2*sigma^2))
def get_probability_density_function(y, X, snake_measurements, class_name):

  # Get all data rows associated with the input class
  class_data = X[y == class_name]

  # Find the means and standard deviations for all features of a given input class
  means = class_data.mean(axis=0)
  stds = class_data.std(axis=0)

  # Calculate the probability that a feature is equal to the input snake_measurements given the input class
  probabilities = (1 / (np.sqrt(2 * np.pi) * stds)) * np.exp(-0.5 * ((snake_measurements - means)/stds) ** 2)

  return probabilities

naive_bayes_classifier(f"./Examples/Example0/dataset.csv", [350, 42, 13])