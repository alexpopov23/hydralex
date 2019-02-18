
class FrameInstance:

    def __init__(self):
        self.type = "frame"
        self.sentence_index = None
        self.frame_name = None
        self.lu = None
        self.lemma = None
        self.pos = None
        self.indices = []
        self.roles = []
        self.sentence = []

    def set_sentence_index(self, sentence_index):
        self.sentence_index = sentence_index

    def set_frame_name(self, frame_name):
        self.frame_name = frame_name

    def set_lemma(self, lemma):
        self.lemma = lemma

    def set_pos(self, pos):
        self.pos = pos

    def set_indices(self, indices):
        self.indices = indices

    def set_roles(self, roles):
        self.roles = roles

    def set_sentence(self, sentence):
        self.sentence = sentence
