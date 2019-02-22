import argparse
import os

import numpy as np

from gensim.models import KeyedVectors
from sklearn.metrics.pairwise import cosine_similarity

from senses2synsets import get_syn2sense, get_sense2synset2

if __name__ == "__main__":

    parser = argparse.ArgumentParser(version='1.0',description='Calculate word similarities with word2vec and then'
                                                               'correlation with existing human datasets.')
    parser.add_argument('-synset_embeddings_model', dest='synset_embeddings_model', required=False, default="None",
                        help='The path to the model with the pretrained word embeddings.')
    parser.add_argument('-lemma_embeddings_model', dest='lemma_embeddings_model', required=False, default="None",
                        help='The path to the model with the pretrained word embeddings.')
    parser.add_argument('-f_relations', dest="f_relations", required=True, help='Path to the relations file')
    parser.add_argument('-f_new_relations', dest="f_new_relations", required=True, help='Path to the new relations file')

    args = parser.parse_args()
    synemb_path = args.synset_embeddings_model
    lemmaemb_path = args.lemma_embeddings_model
    f_relations = args.f_relations
    f_new_relations = args.f_new_relations
    # syn2sense = get_syn2sense()
    sense2synset = get_sense2synset2()

    if synemb_path != "None":
        syn_object = KeyedVectors.load_word2vec_format(synemb_path, binary=False)
        model_syn = syn_object.syn0
        id2src1 = syn_object.index2word
        src2id1 = {}
        for i, word in enumerate(id2src1):
            src2id1[word] = i
        if "UNK" not in src2id1:
            unk = np.zeros(300)
            src2id1["UNK"] = len(src2id1)
            model1 = np.concatenate((model_syn, [unk]))
    if lemmaemb_path != "None":
        lemma_object = KeyedVectors.load_word2vec_format(lemmaemb_path, binary=False)
        model_lemma = lemma_object.syn0
        id2src2 = lemma_object.index2word
        src2id2 = {}
        for i, word in enumerate(id2src2):
            src2id2[word] = i
        if "UNK" not in src2id2:
            unk = np.zeros(300)
            src2id2["UNK"] = len(src2id2)
            model2 = np.concatenate((model_lemma, [unk]))

    for filename in os.listdir(f_relations):
        count_missing = 0
        missing_nodes = set()
        with open(os.path.join(f_relations, filename), "r") as relations:
            to_write = ""
            for relation in relations.readlines():
                fields = relation.split()
                if len(fields) == 0:
                    continue
                u = fields[0][2:]
                v = fields[1][2:]
                if u not in sense2synset:
                    missing_nodes.add(u)
                if v not in sense2synset:
                    missing_nodes.add(v)
                if u not in sense2synset or v not in sense2synset:
                    continue
                synset_u, synset_v = sense2synset[u], sense2synset[v]
                lemma_u, lemma_v = u.split("%")[0], v.split("%")[0]
                if synemb_path != "None":
                    if synset_u in src2id1:
                        syn1 = model1[src2id1[synset_u]]
                    else:
                        syn1 = model1[src2id1["UNK"]]
                    if synset_v in src2id1:
                        syn2 = model1[src2id1[synset_v]]
                    else:
                        syn2 = model1[src2id1["UNK"]]
                if lemmaemb_path != "None":
                    if lemma_u in src2id2:
                        lemma1 = model2[src2id2[lemma_u]]
                    elif len(lemma_u.split("_")) > 1:
                        lemma1 = np.zeros(300)
                        count = 1
                        for lemma in lemma_u.split("_"):
                            if lemma in src2id2:
                                lemma1 += model2[src2id2[lemma]]
                                count += 1
                        lemma1 /= count
                    else:
                        lemma1 = model2[src2id2["UNK"]]
                    if lemma_v in src2id2:
                        lemma2 = model2[src2id2[lemma_v]]
                    elif len(lemma_v.split("_")) > 1:
                        lemma2 = np.zeros(300)
                        count = 1
                        for lemma in lemma_v.split("_"):
                            if lemma in src2id2:
                                lemma2 += model2[src2id2[lemma]]
                                count += 1
                        lemma2 /= count
                    else:
                        lemma2 = model2[src2id2["UNK"]]
                if synemb_path != "None" and lemmaemb_path != "None":
                    emb1 = np.concatenate((syn1, lemma1), axis=0)
                    emb2 = np.concatenate((syn2, lemma2), axis=0)
                elif synemb_path != "None":
                    emb1 = syn1
                    emb2 = syn2
                elif lemmaemb_path != "None":
                    emb1 = lemma1
                    emb2 = lemma2
                model_sim = abs(cosine_similarity(emb1.reshape(1, -1), emb2.reshape(1, -1))[0][0])
                new_relation = relation.rstrip() + " w:" + str(model_sim) + "\n"
                to_write += new_relation
            with open(os.path.join(f_new_relations, filename.replace(".txt", "_weights.txt")), "w") as f_new:
                f_new.write(to_write)
            # with open(os.path.join(f_new_relations, filename.replace(".txt", "_missing_nodes.txt")), "w") as f_missing:
            #     f_missing.write("\n".join(missing_nodes))