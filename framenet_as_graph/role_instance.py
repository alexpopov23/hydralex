
class RoleInstance:

    def __init__(self):
        self.type = "role"
        self.lemma = None
        self.role = None
        self.indices = []

    def set_lemma(self, lemma):
        self.lemma = lemma

    def set_role(self, role):
        self.role = role

    def set_pos(self, pos):
        self.pos = pos

    def set_indices(self, indices):
        self.indices = indices

