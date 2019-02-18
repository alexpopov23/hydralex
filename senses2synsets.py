from misc import num2pos

f_id2lc = "/home/lenovo/tools/ukb-3.2/wsdeval/wn30/id2lc.map"
f_rels = "/home/lenovo/dev/KBWSD/knowledge-resources/hydralex/data/hydralex.txt"
f_new_rels = "/home/lenovo/dev/KBWSD/knowledge-resources/hydralex/data/hydralex_synsets.txt"

def get_sense2synset(f_id2lc=f_id2lc):
    sense2synset = {}
    with open(f_id2lc, "r") as id2lc:
        for line in id2lc.readlines():
            synset, senses = line.split("\t")
            senses = senses.split(" ")
            for sense in senses:
                sense = sense.rstrip()
                sense += "-" + num2pos(sense)
                sense2synset[sense] = synset
    return sense2synset

def map_resource(f_rels, f_new_rels, sense2synset):
    to_write = ""
    with open(f_rels, "r") as rels:
        for rel in rels.readlines():
            new_rel = rel
            fields = rel.split()
            u, v = fields[0][2:], fields[1][2:]
            # u_s = u + num2pos(u)
            # v_s = v + num2pos(v)
            if u in sense2synset:
                new_rel = new_rel.replace(u, sense2synset[u])
            if v in sense2synset:
                new_rel = new_rel.replace(v, sense2synset[v])
            to_write += new_rel
    with open(f_new_rels, "w") as new_rels:
        new_rels.write(to_write)

if __name__ == "__main__":
    sense2synset = get_sense2synset()
    map_resource(f_rels, f_new_rels, sense2synset)
    print "This is the end."
