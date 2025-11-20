# Name this file assignment4.py when you submit
import os 


class bag_of_words_model:

  def __init__(self, directory):
    # directory is the full path to a directory containing trials through state space

    # TODO; Extract and iterate through training documents
    trainingDocuments = os.listdir(directory)


    # TODO: learn document vocabulary


    # TODO: learning idf vector


    # Return nothing
    return 0


  def tf_idf(self, document_filepath):
    # document_filepath is the full file path to a test document

    # TODO: grab each word in document and compute tfidf using
    # vocabulary andn idf vector computed during "training"

    # Return the term frequency-inverse document frequency vector for the document
    return tf_idf_vector


  def predict(self, document_filepath, business_weights, entertainment_weights, politics_weights):
    # document_filepath is the full file path to a test document
    # business_weights is a list of weights for the business artificial neuron
    # entertainment_weights is a list of weights for the entertainment artificial neuron
    # politics_weights is a list of weights for the politics artificial neuron


    # TODO: extract weights for each neuron type (business, entertainment, politics)

    # TODO: Get tf-idf for all words in the document

    # TODO: calculate y - hat for each neuron using the softmax activation
    # function and the sum of weights * inputs

    # TODO : return neuron with highest score and all neuron scores

    # Return the predicted label from the neural network model
    # Return the score from each neuron
    return predicted_label, scores


  