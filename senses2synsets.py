from misc import num2pos

f_id2lc = "/home/lenovo/tools/ukb-3.2/wsdeval/wn30/id2lc.map"
f_lc2id = "/home/lenovo/dev/KBWSD/knowledge-resources/WN-graph-sensed-relations/Version01/wn_sk.txt"
f_rels = "/home/lenovo/dev/KBWSD/knowledge-resources/hydralex_data/hydralex.txt"
f_new_rels = "/home/lenovo/dev/KBWSD/knowledge-resources/hydralex_data/hydralex_fullysensed.txt"

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

def get_sense2synset2(f_lc2id=f_lc2id):
    sense2synset= {}
    with open(f_lc2id, "r") as maps:
        for line in maps.readlines():
            fields = line.split()
            # print line
            synset = fields[0][2:]
            sense = fields[1][2:]
            sense2synset[sense] = synset
    return sense2synset

def get_syn2sense(f_lc2id=f_lc2id):
    synset2sense = {}
    with open(f_lc2id, "r") as maps:
        for line in maps.readlines():
            fields = line.split()
            # print line
            synset = fields[0][2:]
            sense = fields[1][2:]
            weight = float(fields[3][2:])
            if weight == 1:
                synset2sense[synset] = sense
    return synset2sense

def map_resource_sense2syn(f_rels, f_new_rels, sense2synset):
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

def map_resource_syn2sense(f_rels, f_new_rels, synset2sense):
    to_write = ""
    with open(f_rels, "r") as rels:
        for rel in rels.readlines():
            new_rel = rel
            fields = rel.split()
            u, v = fields[0][2:], fields[1][2:]
            # u_s = u + num2pos(u)
            # v_s = v + num2pos(v)
            if u in synset2sense:
                new_rel = new_rel.replace(u, synset2sense[u])
            if v in synset2sense:
                new_rel = new_rel.replace(v, synset2sense[v])
            to_write += new_rel
    with open(f_new_rels, "w") as new_rels:
        new_rels.write(to_write)

if __name__ == "__main__":
    sense2synset = get_sense2synset()
    synset2sense = get_syn2sense()
    map_resource_syn2sense(f_rels, f_new_rels, synset2sense)
    print "This is the end."
