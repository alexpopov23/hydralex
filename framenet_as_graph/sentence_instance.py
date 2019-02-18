
class SentenceInstance:

    def __init__(self):
        self.type = "sentence"
        self.sentence_index = None
        self.frames = []
        self.fee_idxs = []
        self.lus = []
        self.pos = []
        self.sentence = []
        self.sentence_lemmatized = []

    def set_sentence_index(self, sentence_index):
        self.sentence_index = sentence_index

    def set_frames(self, frames):
        self.frames = frames

    def set_fee_idxs(self, fee_idx):
        self.fee_idxs.append(fee_idx)

    def set_pos(self, pos):
        self.pos = pos

    def set_sentence(self, sentence):
        self.sentence = sentence

    def set_sentence_lemmatized(self, sentence_lemmatized):
        self.sentence_lemmatized = sentence_lemmatized