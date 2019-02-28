import pickle
import os

import read_verbnet, read_framenet, read_fn_sense_repo

from  copy import copy

from read_predicate_matrix import PMClass
from senses2synsets import get_syn2sense
from misc import get_sense2freq

def num2pos(sense):
    if sense == "NULL":
        return "NULL"
    # if len(sense) < 7:
    #     print sense
    pos_id = sense[-9]
    if pos_id == "1":
        return "n"
    elif pos_id == "2":
        return "v"
    elif pos_id == "3":
        return "a"
    elif pos_id == "4":
        return "r"
    elif pos_id == "5":
        return "a"
    else:
        return ""

def get_vn_roles(vn_class_id, vn_classes, vn_class_hierarchy):
    vn_roles = set()
    if vn_class_id in vn_class_hierarchy:
        vn_roles.update(get_vn_roles(vn_class_hierarchy[vn_class_id], vn_classes, vn_class_hierarchy))
    roles = vn_classes[vn_class_id].them_roles
    for role in roles:
        vn_roles.add(role[0])
    return vn_roles


f_pred_matrix = "/home/lenovo/dev/KBWSD/knowledge-resources/hydralex/data/pred_matrix_mappings.pickle"
f_verbnet = "/home/lenovo/dev/KBWSD/knowledge-resources/hydralex/data/new_vn"
f_framenet = "/home/lenovo/dev/KBWSD/knowledge-resources/hydralex/data/framenet/"
f_fn_sense_repo = "/home/lenovo/dev/KBWSD/knowledge-resources/FrameNet-sense-repository-April-2012/FrameNet-sense-repository-April-2012/"
# f_out = "/home/lenovo/dev/KBWSD/knowledge-resources/hydralex/data/hydralex_fullysensed_incorporated.txt"
f_out = "/home/lenovo/dev/KBWSD/knowledge-resources/hydralex/data/"

def format_relations():

    vn_classes, vn_roles_compendium, vn_class_hierarchy, vn_num2class, wn_sense2vn_class = read_verbnet.read_verbnet(f_verbnet)
    pred_matrix = pickle.load(open(f_pred_matrix, "r"))
    framenet = read_framenet.read_framenet(f_framenet)
    frame2wn_synset = read_fn_sense_repo.read_fn_sense_repo(f_fn_sense_repo)

    # relation format: u: v: d: t: s: w:
    new_relations = set()

    # Get relations from Verbnet (vn_class to wn_senses, vn_class to vn_roles)
    print "*** Getting relations from VerbNet data ***"
    vn_class2wn_senses = {}
    vn_class2vn_roles = {}
    for wn_sense, vn_classes_mapped in wn_sense2vn_class.iteritems():
        for vn_class in vn_classes_mapped:
            if vn_class in vn_class2wn_senses:
                vn_class2wn_senses[vn_class].add(wn_sense)
            else:
                vn_class2wn_senses[vn_class] = set([wn_sense])
            vn_roles = get_vn_roles(vn_class, vn_classes, vn_class_hierarchy)
            if vn_class in vn_class2vn_roles:
                vn_class2vn_roles[vn_class].update(vn_roles)
            else:
                vn_class2vn_roles[vn_class] = vn_roles


    # Get mappings from the Predicate Matrix (WN-VN, WN-FN, FNRoles-VNRoles)
    print "*** Getting relations from Predicate Matrix data ***"
    wn_sense2fn_roles, vn_role2fn_roles, fn_frame2wn_senses, fn_role2wn_predicates = {}, {}, {}, {}
    for mapping in pred_matrix[0]:
        # Mapping between WN sense and and VN class
        if mapping.vn_subclass != "NULL":
            vn_class = mapping.vn_subclass
        else:
            vn_class = mapping.vn_class
        if mapping.wn_sense != "NULL" and vn_class != "NULL":
            vn_class = vn_num2class[vn_class]
            if vn_class in vn_class2wn_senses:
                vn_class2wn_senses[vn_class].add(wn_sense)
            else:
                vn_class2wn_senses[vn_class] = set([wn_sense])
            vn_roles = get_vn_roles(vn_class, vn_classes, vn_class_hierarchy)
            if vn_class in vn_class2vn_roles:
                vn_class2vn_roles[vn_class].update(vn_roles)
            else:
                vn_class2vn_roles[vn_class] = vn_roles
        # Mapping between WN sense and FN frame
        # if mapping.wn_sense != "NULL" and mapping.fn_frame != "NULL":
        #     fn_role = mapping.fn_frame + "::" + mapping.fn_role
        #     if mapping.wn_sense not in wn_sense2fn_roles:
        #         wn_sense2fn_roles[mapping.wn_sense] = set([fn_role])
        #     else:
        #         wn_sense2fn_roles.add(fn_role)
        # Mapping between VN role and FN role (frame element)
        if mapping.vn_role != "NULL" and mapping.fn_role != "NULL":
            vn_role = vn_num2class[mapping.vn_class] + "::" + mapping.vn_role
            fn_role = mapping.fn_frame + "::" + mapping.fn_role
            if vn_role not in vn_role2fn_roles:
                vn_role2fn_roles[vn_role] = set([fn_role])
            else:
                vn_role2fn_roles[vn_role].add(fn_role)

        if mapping.fn_frame != "NULL" and mapping.wn_sense != "NULL":
            if mapping.fn_frame not in fn_frame2wn_senses:
                fn_frame2wn_senses[mapping.fn_frame] = set([copy(mapping.wn_sense)])
            else:
                fn_frame2wn_senses[mapping.fn_frame].add(copy(mapping.wn_sense))

        if mapping.fn_role != "NULL" and mapping.wn_sense != "NULL":
            fn_role = mapping.fn_frame + "::" + mapping.fn_role
            if fn_role not in fn_role2wn_predicates:
                fn_role2wn_predicates[fn_role] = set([copy(mapping.wn_sense)])
            else:
                fn_role2wn_predicates[fn_role].add(copy(mapping.wn_sense))

    # Get relations from FrameNet (frame to frame, frame to roles)
    print "*** Getting relations from FrameNet data ***"
    frame2fn_roles, frame2frame = {}, {}
    for frame, roles in framenet.frame_core_roles.iteritems():
        for role in roles:
            role = frame + "::" + role
            if frame not in frame2fn_roles:
                frame2fn_roles[frame] = set([role])
            else:
                frame2fn_roles[frame].add(role)
    for frame, roles in framenet.frame_extrathematic_roles.iteritems():
        for role in roles:
            role = frame + "::" + role
            if frame not in frame2fn_roles:
                frame2fn_roles[frame] = set([role])
            else:
                frame2fn_roles[frame].add(role)
    for frame, roles in framenet.frame_peripheral_roles.iteritems():
        for role in roles:
            role = frame + "::" + role
            if frame not in frame2fn_roles:
                frame2fn_roles[frame] = set([role])
            else:
                frame2fn_roles[frame].add(role)

    for frame, related_frames in framenet.frame_relation_map.iteritems():
        for rel_frame in related_frames:
            if frame not in frame2frame:
                frame2frame[frame] = set([rel_frame])
            else:
                frame2frame[frame].add(rel_frame)

    # Get relations from the FrameNet sense repository (frame to frame, frame to roles)
    print "*** Getting relations from the FN-WN automatic mappings ***"
    syn2sense = get_syn2sense()
    fn_role2wn_entities = {}
    # TODO think whether to generate more or less coarse-grained FN roles (e.g. Frame+Role)
    for frame, mappings in frame2wn_synset.iteritems():
        for mapping in mappings:
            role = frame + "::" + mapping[0]
            if role not in fn_role2wn_entities:
                fn_role2wn_entities[role] = set([(syn2sense[mapping[1]], mapping[2])])
            else:
                fn_role2wn_entities[role].add((syn2sense[mapping[1]], mapping[2]))

    with open(os.path.join(f_out, "hydralex_dicts.pickle"), "wb") as f:
        pickle.dump(vn_class2wn_senses, f)
        pickle.dump(vn_class2vn_roles, f)
        pickle.dump(vn_role2fn_roles, f)
        pickle.dump(vn_class_hierarchy, f)
        pickle.dump(fn_frame2wn_senses, f)
        pickle.dump(fn_role2wn_predicates, f)
        pickle.dump(fn_role2wn_entities, f)
        pickle.dump(frame2fn_roles, f)
        pickle.dump(frame2frame, f)

if __name__ == "__main__":

    # format_relations()
    # exit()
    with open(os.path.join(f_out, "hydralex_dicts.pickle"), "rb") as f:
        vn_class2wn_senses = pickle.load(f)
        vn_class2vn_roles = pickle.load(f)
        vn_role2fn_roles = pickle.load(f)
        vn_class_hierarchy = pickle.load(f)
        fn_frame2wn_senses = pickle.load(f)
        fn_role2wn_predicates = pickle.load(f)
        fn_role2wn_entities = pickle.load(f)
        frame2fn_roles = pickle.load(f)
        frame2frame = pickle.load(f)

    to_write = ""

    # # Connect all WN senses in a VN class one-to-one
    # for vn_class, wn_senses in vn_class2wn_senses.iteritems():
    #     processed_nodes = set()
    #     for wn_sense in wn_senses:
    #         processed_nodes.add(wn_sense)
    #         wn_pos1 = num2pos(wn_sense)
    #         new_rel = "u:" + wn_sense + "-" + wn_pos1 + " v:" + vn_class + " d:0 t:vn_class_membership s:VerbNet&PredMatrix"
    #         to_write += new_rel + "\n"
    #         remaining_nodes = wn_senses.difference(processed_nodes)
    #         for node in remaining_nodes:
    #             wn_pos2 = num2pos(node)
    #             new_rel = "u:" + wn_sense + "-" + wn_pos1 + " v:" + node + "-" + wn_pos2 + \
    #                       " d:0 t:vn_class_membership s:VerbNet&PredMatrix"
    #             to_write += new_rel + "\n"
    # # Connect the classes to each other
    # for vn_class in vn_class_hierarchy:
    #     new_rel = "u:" + vn_class + " v:" + vn_class_hierarchy[vn_class] + " d:0 t:vn_class_membership s:VerbNet"
    #     to_write += new_rel + "\n"

    # # Connect all WN senses in a VN class, where the main class is the most frequent WN sense, and the rest are weighted accordingly
    # sense2freq, vn_class2wn_class = get_sense2freq(), {}
    # for vn_class, wn_senses in vn_class2wn_senses.iteritems():
    #     wn_senses_freq = []
    #     for wn_sense in wn_senses:
    #         wn_sense = wn_sense + "-" + num2pos(wn_sense)
    #         if wn_sense == "moult%2:39:00::-v":
    #             wn_sense = "moult%2:29:00::-v"
    #         wn_senses_freq.append((wn_sense, sense2freq[wn_sense] + 1))
    #     wn_senses_freq.sort(key=lambda x: x[1], reverse=True)
    #     total_freq = 0.0
    #     for wn_sense in wn_senses_freq[1:]:
    #         total_freq += wn_sense[1]
    #     class_name = wn_senses_freq[0][0]
    #     vn_class2wn_class[vn_class] = class_name
    #     for wn_sense in wn_senses_freq[1:]:
    #         new_rel = "u:" + class_name + " v:" + wn_sense[0] + " d:0 t:vn_class_membership s:VerbNet&PredMatrix w:" + str(wn_sense[1]/total_freq)
    #         to_write += new_rel + "\n"
    # # Connect the classes to each other
    # for vn_class in vn_class_hierarchy:
    #     if vn_class in vn_class2wn_class and vn_class_hierarchy[vn_class] in vn_class2wn_class:
    #         new_rel = "u:" + vn_class2wn_class[vn_class] + " v:" + vn_class2wn_class[vn_class_hierarchy[vn_class]] + " d:0 t:vn_class_membership s:VerbNet"
    #         to_write += new_rel + "\n"

    # # Connect all WN senses in a FN frame, where the main class is the most frequent WN sense, and the rest are weighted accordingly
    # sense2freq, fn_frame2wn_class = get_sense2freq(), {}
    # for fn_frame, wn_senses in fn_frame2wn_senses.iteritems():
    #     wn_senses_freq = []
    #     for wn_sense in wn_senses:
    #         wn_sense = wn_sense + "-" + num2pos(wn_sense)
    #         if wn_sense == "moult%2:39:00::-v":
    #             wn_sense = "moult%2:29:00::-v"
    #         wn_senses_freq.append((wn_sense, sense2freq[wn_sense] + 1))
    #     wn_senses_freq.sort(key=lambda x: x[1], reverse=True)
    #     total_freq = 0.0
    #     for wn_sense in wn_senses_freq[1:]:
    #         total_freq += wn_sense[1]
    #     class_name = wn_senses_freq[0][0]
    #     fn_frame2wn_class[fn_frame] = class_name
    #     for wn_sense in wn_senses_freq[1:]:
    #         new_rel = "u:" + class_name + " v:" + wn_sense[0] + " d:0 t:fn_frame_membership s:PredMatrix w:" + \
    #                   str(wn_sense[1] / total_freq)
    #         to_write += new_rel + "\n"
    # # Connect the classes to each other
    # for fn_frame, linked_frames in frame2frame.iteritems():
    #     for frame2 in linked_frames:
    #         if fn_frame in fn_frame2wn_class and frame2 in fn_frame2wn_class:
    #             new_rel = "u:" + fn_frame2wn_class[fn_frame] + " v:" + fn_frame2wn_class[frame2] + \
    #                       " d:0 t:fn_frame_connections s:FrameNet"
    #             to_write += new_rel + "\n"

    # # Connect all WN senses in a FN frame one-to-one
    # for fn_frame, wn_senses in fn_frame2wn_senses.iteritems():
    #     processed_nodes = set()
    #     for wn_sense in wn_senses:
    #         processed_nodes.add(wn_sense)
    #         wn_pos1 = num2pos(wn_sense)
    #         new_rel = "u:" + wn_sense + "-" + wn_pos1 + " v:" + fn_frame + " d:0 t:vn_class_membership s:PredMatrix"
    #         to_write += new_rel + "\n"
    #         remaining_nodes = wn_senses.difference(processed_nodes)
    #         for node in remaining_nodes:
    #             wn_pos2 = num2pos(node)
    #             new_rel = "u:" + wn_sense + "-" + wn_pos1 + " v:" + node + "-" + wn_pos2 + \
    #                       " d:0 t:fn_frame_membership s:PredMatrix"
    #             to_write += new_rel + "\n"
    # # Connect the frames to each other
    # for frame, linked_frames in frame2frame.iteritems():
    #     for frame2 in linked_frames:
    #         new_rel = "u:" + frame + " v:" + frame2 + " d:0 t:fn_frame_membership s:FrameNet"
    #         to_write += new_rel + "\n"


    # # Connect WN predicate senses mapped to FN roles (PredMatrix) to WN entities mapped to FN roles (FN sense repo)
    # for fn_role, wn_predicates in fn_role2wn_predicates.iteritems():
    #     if fn_role in fn_role2wn_entities:
    #         wn_entities = fn_role2wn_entities[fn_role]
    #         for wn_predicate in wn_predicates:
    #             for wn_entity in wn_entities:
    #                 wn_pos1 = num2pos(wn_predicate)
    #                 new_rel = "u:" + wn_predicate + "-" + wn_pos1 + " v:" + wn_entity[0] + \
    #                           " d:0 t:wn_v2wn_n_viaFrameNet s:PredMatrix&FNSenseRepo w:" + str(wn_entity[1])
    #                 to_write += new_rel + "\n"


    # Connect WN predicate senses in VN and FN to WN entity senses, via the Roles in FN and FN --> way too large
    for vn_class, wn_senses in vn_class2wn_senses.iteritems():
        vn_roles = vn_class2vn_roles[vn_class]
        fn_roles = set()
        for vn_role in vn_roles:
            vn_role = vn_class + "::" + vn_role
            if vn_role in vn_role2fn_roles:
                fn_roles.update(vn_role2fn_roles[vn_role])
        wn_entities = []
        for fn_role in fn_roles:
            if fn_role in fn_role2wn_entities:
                wn_entities.extend(fn_role2wn_entities[fn_role])
        for wn_sense in wn_senses:
            wn_pos1 = num2pos(wn_sense)
            for wn_entity in wn_entities:
                wn_pos2 = num2pos(wn_entity[0])
                new_rel = "u:" + wn_sense + "-" + wn_pos1 + " v:" + wn_entity[0] + \
                          " d:0 t:vn_predicate2wn_role s:VerbNet&PredMatrix&FNSenseRepo w:" + str(wn_entity[1])
                to_write += new_rel + "\n"


    with open(os.path.join(f_out, "hydralex_incorporated.txt"), "w") as f:
        f.write(to_write)



    print "This is the end."