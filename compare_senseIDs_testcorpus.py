f_missing = "/home/lenovo/dev/KBWSD/knowledge-resources/WN-graph-sensed-relations/Version02GlossMD/weighted/post/GlossMD_missing_nodes.txt"
f_corpus = "/home/lenovo/tools/ukb-3.2/wsdeval/wsdeval_src/WSD_Unified_Evaluation_Datasets/ALL/ALL.gold.key.txt"
f_intersect = "/home/lenovo/dev/KBWSD/knowledge-resources/WN-graph-sensed-relations/Version02GlossMD/weighted/post/GlossMD_missing_nodes_corpusIntersection.txt"

missing = set()
senses_corpus = set()
common_nodes = set()
with open(f_missing, "r") as f_m:
    for node in f_m.readlines():
        missing.add(node.rstrip())
with open(f_corpus, "r") as f_c:
    for line in f_c.readlines():
        senses = line.split()[1:]
        senses_corpus.update(set(senses))
for node in missing:
    if node[:-2] in senses_corpus:
        common_nodes.add(node)
# common_nodes = senses_corpus.intersection(missing)

with open(f_intersect, "w") as f_i:
    f_i.write("\n".join(common_nodes))

print "This is the end"