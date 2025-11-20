# Name this file assignment4.py when you submit
import os 
import math
import numpy as np

class bag_of_words_model:

  # Stores all vocabulary words andn their corresponding idf value
  vocabularyIdfValues = {}
  labels = ["business", "entertainment", "politics"]

  def __init__(self, directory):
    # directory is the full path to a directory containing trials through state space

    # Extract and iterate through training documents
    trainingDocuments = os.listdir(directory)
    numTrainingDocuments = len(trainingDocuments)

    # Iterate through each document
    for document in trainingDocuments:

      # Temporarily store all words found in current document
      documentWords = {}

      # Iterate through and store all words
      with open(os.path.join(directory, document), 'r') as file:
        for line in file:
          words = line.split()

          # Add each word that appears at least once to the dictionary of document words
          for word in words:
            documentWords[word] = 1

      # Increment number of documents a word (key) appears in for the vocabularyIdfValues dict
      for key in documentWords:
        self.vocabularyIdfValues[key] = self.vocabularyIdfValues.get(key, 0) + 1

    # Iterate through each word/key in vocabularyIdfValues, take its value (representing the # of documents
    # the word appears in) and updating its value with its Idf value
    for key in self.vocabularyIdfValues:
      self.vocabularyIdfValues[key] = math.log2(numTrainingDocuments/self.vocabularyIdfValues[key])

    # Return nothing

  # Return tf-idf vector in sorted order
  def tf_idf(self, document_filepath):
    # document_filepath is the full file path to a test document

    tf_idf_vector = []

    # Get a dictionary containing the word and its corresponding tf value from the input document
    tfs = getTfDictionary(document_filepath)
    idfs = self.vocabularyIdfValues

    # Iterate through all words in sorted order, calculating tf-idf values (tfidf = tf x idf)
    for word in sorted(idfs.keys()):
      # Only calculate tfidf if word exists in tfs, else append 0
      if (word in tfs):
        tfIdf = idfs[word] * tfs[word]
        tf_idf_vector.append(tfIdf)
      else:
        tf_idf_vector.append(0)

    # Return the term frequency-inverse document frequency vector for the document
    return tf_idf_vector


  def predict(self, document_filepath, business_weights, entertainment_weights, politics_weights):
    # document_filepath is the full file path to a test document
    # business_weights is a list of weights for the business artificial neuron
    # entertainment_weights is a list of weights for the entertainment artificial neuron
    # politics_weights is a list of weights for the politics artificial neuron

    # Get tf-idf for all words in the document
    tfIdfs = self.tf_idf(document_filepath)

    # calculate y - hat for each neuron using the sum of weights * inputs
    yHat = []
    yHat.append(np.dot(business_weights, tfIdfs))
    yHat.append(np.dot(entertainment_weights, tfIdfs))
    yHat.append(np.dot(politics_weights, tfIdfs))

    # Apply softmax function
    expValues = np.exp(yHat)
    scores = expValues / np.sum(expValues)

    # Get the highest score and its corresponding label
    predicted_label = self.labels[np.argmax(scores)]

    # Return the predicted label from the neural network model
    # Return the score from each neuron
    return predicted_label, scores

# Given a document, return a dictionary representing a vector of the term frequency of each word
def getTfDictionary(document_filepath):

  documentWords = {}
  numWords = 0

  # Extract all words and add the # of times it occurs to a dictionary
  with open(document_filepath, 'r') as file:
    for line in file:
      words = line.split()
      numWords += len(words)

      # increment count of each word found in the document
      for word in words:
        documentWords[word] = documentWords.get(word, 0) + 1

  # Use value stored in dict (# of times word appears) to get TF values for all words
  for word in documentWords:
    documentWords[word] = documentWords[word]/numWords

  return documentWords

# Helper function to return a list of weights for a corresponding class type
def extractWeights(filePath):
  weights = []

  # Open input file and append all weights to a list that gets returned
  with open(filePath, 'r') as file:
    for line in file:
      weights.extend(map(float, line.split(","))) 

  return weights

# Test functions
def testBagOfWordsModel():

  example = 0
  documentFile = f"Examples/Example{example}/test_document.txt"
  businessWeightsFile = f"Examples/Example{example}/business_weights.txt"
  entertainmentWeightsFile = f"Examples/Example{example}/entertainment_weights.txt"
  politicsWeightsFile = f"Examples/Example{example}/politics_weights.txt"

  bowm = bag_of_words_model(f"Examples/Example{example}/training_documents/")
  # print(getTfDictionary(f"Examples/Example{example}/test_document.txt"))
  # print(bowm.tf_idf(file))
  # print(bowm.predict())

  # extract weights for each neuron type (business, entertainment, politics)
  businessWeights = extractWeights(businessWeightsFile)
  entertainmentWeights = extractWeights(entertainmentWeightsFile)
  politicsWeights = extractWeights(politicsWeightsFile)

  print(bowm.predict(documentFile, businessWeights, entertainmentWeights, politicsWeights))


# testBagOfWordsModel()