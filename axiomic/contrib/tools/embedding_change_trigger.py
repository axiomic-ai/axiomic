import axiomic

import axiomic.utils.ops as ops

class EmbeddingChangeTrigger:
    ''' A class to help track changes to text and understanding how far it changed (moved in embedding space).
    '''

    def __init__(self, start_text, threshold=0.97):
        self.start_text = axiomic.Text(start_text)
        self.threshold = threshold
        self.start_embedding = self.start_text.embed().value()

    def get_similarity(self, text):
        ''' Get the distance between the start text and the given text.
        '''
        end_embedding = axiomic.Text(text).embed().value()
        return self.start_embedding.cosine_similarity(end_embedding)
    
    def would_trigger(self, text):
        ''' Return True if the given text would trigger a change.
        '''
        return self.get_similarity(text) < self.threshold

    def percent_towards_trigger(self, text):
        total_distance = 1 - self.threshold
        distance_gone = 1 - self.get_similarity(text)
        return int(((distance_gone / total_distance) * 100))
        # return self.get_similarity(text) / self.threshold

    def update(self, text):
        ''' Update the start text to the given text.
        '''
        self.start_text = axiomic.Text(text)
        self.start_embedding = self.start_text.unweave_embedding()


        


    