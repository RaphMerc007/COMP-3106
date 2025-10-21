import pandas as pd
import numpy as np


def naive_bayes_classifier(dataset_filepath, snake_measurements):
  # dataset_filepath is the full file path to a CSV file containing the dataset
  # snake_measurements is a list of [length, weight, speed] measurements for a snake

  most_likely_class = None
  class_probabilities = None



  # TODO: Read dataset.csv and train the model to get W

  # Read dataset.csv and get the corresponding y vector and X matrix for its data
  y, X = extract_data(dataset_filepath)

  # Extract rows corresponding to a certain snake
  # cobra_rows = X[y == "cobra"]
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


def probability_density_function(dataset_filepath, snake_measurements, class_name):
  #TODO: P(feature | class) = 1/sqrt(2*pi*sigma^2) * e**(-(x-mu)^2 / (2*sigma^2))
  return

def get_sigma(dataset_filepath, class_name):
  #TODO: get the standard deviation for the given class
  return

def get_mu(dataset_filepath, class_name):
  #TODO: get the mean for the given class
  return


naive_bayes_classifier(f"./Examples/Example0/dataset.csv", 0)