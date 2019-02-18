import os

f_fn_sense_repo = "/home/lenovo/dev/KBWSD/knowledge-resources/FrameNet-sense-repository-April-2012/FrameNet-sense-repository-April-2012/"

def read_fn_sense_repo(path_to_repo):
    frame2wn_synset = {}
    count = 0
    for file_name in os.listdir(path_to_repo):
        mappings = open(os.path.join(path_to_repo, file_name), "r")
        fn_info = file_name[:-4].split("---")
        frame, fn_role = fn_info[0], fn_info[1]
        if frame not in frame2wn_synset:
            frame2wn_synset[frame] = []
        for mapping in mappings.readlines():
            fields = mapping.split(",")
            synset, weight = fields[0][-9:], float(fields[2].rstrip())
            if synset[0] == "1":
                synset = synset[1:] + "-n"
            elif synset[0] == "2":
                synset = synset[1:] + "-v"
            elif synset[0] == "3":
                synset = synset[1:] + "-a"
            elif synset[0] == "4":
                synset = synset[1:] + "-r"
            count += 1
            frame2wn_synset[frame].append([fn_role, synset, weight])
    return frame2wn_synset

