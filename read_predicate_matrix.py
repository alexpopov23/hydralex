import pickle

# f_pred_matrix = "./data/pred_matrix_sample.txt"
f_pred_matrix = '/home/lenovo/dev/KBWSD/knowledge-resources/PredicateMatrix.v1.3/PredicateMatrix.v1.3.txt'
f_output = "/home/lenovo/dev/KBWSD/knowledge-resources/hydralex/data/pred_matrix_mappings.pickle"

class PMClass():

    def __init__(self):
        self.pos = ""
        self.vn_class = ""
        self.vn_subclass = ""
        self.vn_lemma = ""
        self.vn_role = ""
        self.wn_sense = ""
        self.fn_frame = ""
        self.fn_le = ""
        self.fn_role = ""
        self.pb_pred = ""
        self.pb_arg = ""

def read_predicate_matrix(path_to_pm):

    pm_mappings = []
    fn_roles_compendium = set()
    with open(path_to_pm, "r") as pred_matrix:
        for line in pred_matrix.readlines():
            mapping = PMClass()
            columns = line.split("\t")
            # if columns[0] != "id:eng":
            #     continue
            mapping.pos = columns[1][3:]
            if mapping.pos == "D_POS":
                continue
            mapping.vn_class = columns[4][3:]
            mapping.vn_subclass = columns[6][3:]
            mapping.vn_lemma = columns[8][3:]
            mapping.vn_role = columns[9][3:]
            mapping.wn_sense = (columns[10][3:] + "::" if columns[10][3:] != "NULL" else "NULL")
            mapping.fn_frame = columns[12][3:]
            mapping.fn_le = columns[13][3:]
            mapping.fn_role = columns[14][3:]
            fn_roles_compendium.add(mapping.fn_role)
            mapping.pb_pred = columns[15][3:]
            mapping.pb_arg = columns[16][3:]
            pm_mappings.append(mapping)
    return pm_mappings, fn_roles_compendium

if __name__ == "__main__":
    pred_matrix = read_predicate_matrix(f_pred_matrix)
    pickle.dump(pred_matrix, open(f_output, 'w'))
    # pred_matrix = pickle.load(open(f_output, "r"))
    print "Done"
