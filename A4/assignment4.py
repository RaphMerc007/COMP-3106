# Name this file assignment4.py when you submit

class bag_of_words_model:

  def __init__(self, directory):
    # directory is the full path to a directory containing trials through state space
	
    # Return nothing


  def tf_idf(self, document_filepath):
    # document_filepath is the full file path to a test document

    # Return the term frequency-inverse document frequency vector for the document
    return tf_idf_vector


  def predict(self, document_filepath, business_weights, entertainment_weights, politics_weights):
    # document_filepath is the full file path to a test document
    # business_weights is a list of weights for the business artificial neuron
    # entertainment_weights is a list of weights for the entertainment artificial neuron
    # politics_weights is a list of weights for the politics artificial neuron

    # Return the predicted label from the neural network model
    # Return the score from each neuron
    return predicted_label, scores