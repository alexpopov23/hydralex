import pickle

import read_verbnet, read_framenet, read_fn_sense_repo
from read_predicate_matrix import PMClass
from senses2synsets import get_syn2sense

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

f_pred_matrix = "/home/lenovo/dev/KBWSD/knowledge-resources/hydralex/data/pred_matrix_mappings.pickle"
f_verbnet = "/home/lenovo/dev/KBWSD/knowledge-resources/hydralex/data/new_vn"
f_framenet = "/home/lenovo/dev/KBWSD/knowledge-resources/hydralex/data/framenet/"
f_fn_sense_repo = "/home/lenovo/dev/KBWSD/knowledge-resources/FrameNet-sense-repository-April-2012/FrameNet-sense-repository-April-2012/"
f_out = "/home/lenovo/dev/KBWSD/knowledge-resources/hydralex/data/hydralex_fullysensed.txt"

vn_classes, vn_roles_compendium, vn_class_hierarchy, vn_num2class, wn_sense2vn_class = read_verbnet.read_verbnet(f_verbnet)
pred_matrix = pickle.load(open(f_pred_matrix, "r"))
framenet = read_framenet.read_framenet(f_framenet)
frame2wn_synset = read_fn_sense_repo.read_fn_sense_repo(f_fn_sense_repo)

# relation format: u: v: d: t: s: w:
new_relations = set()

# Get mappings from the Predicate Matrix (WN-VN, WN-FN, FNRoles-VNRoles)
print "*** Getting relations from Predicate Matrix data ***"
count_vn_class, count_fn_frame, count_vn_fn_role = 0, 0, 0
for mapping in pred_matrix[0]:
    wn_pos = num2pos(mapping.wn_sense)
    # Mapping between WN sense and and VN class
    if mapping.vn_subclass != "NULL":
        vn_class = mapping.vn_subclass
    else:
        vn_class = mapping.vn_class
    if mapping.wn_sense != "NULL" and vn_class != "NULL":
        wn2vn = "u:" + mapping.wn_sense + "-" + wn_pos + " v:" + vn_num2class[vn_class] + " d:0 t:wn_sense2vn_class s:PredicateMatrix"
        if wn2vn not in new_relations:
            new_relations.add(wn2vn)
            count_vn_class += 1
    # Mapping between WN sense and FN frame
    if mapping.wn_sense != "NULL" and mapping.fn_frame != "NULL":
        wn2fn = "u:" + mapping.wn_sense + "-" + wn_pos + " v:" + mapping.fn_frame + " d:0 t:wn_sense2fn_frame s:PredicateMatrix"
        if wn2fn not in new_relations:
            new_relations.add(wn2fn)
            count_fn_frame += 1
    # Mapping between VN role and FN role (frame element)
    # vn_role = mapping.vn_role
    if mapping.vn_role != "NULL" and mapping.fn_frame != "NULL":
        for role in vn_classes[vn_num2class[vn_class]].them_roles:
            if role[0] == mapping.vn_role:
                vn_role = role[0] + "".join(role[1])
                # if vn_role != mapping.vn_role:
                vn_role2fn_role = "u:" + vn_role + " v:" + mapping.fn_frame + " d:0 t:vn_role2fn_role s:PredicateMatrix"
                if vn_role2fn_role not in new_relations:
                    new_relations.add(vn_role2fn_role)
                    count_vn_fn_role += 1
print "Extracted relations of type *WN-sense to VN-class*: " + str(count_vn_class)
print "Extracted relations of type *WN-sense to FN-frame*: " + str(count_fn_frame)
print "Extracted relations of type *VN-role to FN-role*: " + str(count_vn_fn_role)

# Get relations from Verbnet (wn_sense to class, class to roles, class to class)
print "*** Getting relations from VerbNet data ***"
count_vn_class = 0
for wn_sense, vn_classes_mapped in wn_sense2vn_class.iteritems():
    for vn_class in vn_classes_mapped:
        wn_pos = num2pos(wn_sense)
        wn2vn = "u:" + wn_sense + "-" + wn_pos + " v:" + vn_class + " d:0 t:wn_sense2vn_class s:VerbNet"
        if wn2vn not in new_relations:
            new_relations.add(wn2vn)
            count_vn_class += 1
print "Extracted relations of type *WN-sense to VN-class* (not in Predicate Matrix): " + str(count_vn_class)
count = len(new_relations)
for vn_class_name, vn_class in vn_classes.iteritems():
    for role in vn_class.them_roles:
        # TODO think whether d should be 0 here
        vn_class2vn_role = "u:" + vn_class.name + " v:" + "".join((role[0], "".join(role[1]))) + " d:0 t:vn_class2vn_role s:VerbNet"
        new_relations.add(vn_class2vn_role)
print "Extracted relations of type *VN-class to VN-role*: " + str(len(new_relations) - count)
count = len(new_relations)
for key, value in vn_class_hierarchy.iteritems():
    vn_class2vn_class = "u:" + key + " v:" + value + " d:0 t:vn_class2vn_class s:VerbNet"
    new_relations.add(vn_class2vn_class)
print "Extracted relations of type *VN-class to VN-class*: " + str(len(new_relations) - count)
count = len(new_relations)

# Get relations from FrameNet (frame to frame, frame to roles)
print "*** Getting relations from FrameNet data ***"
for frame, roles in framenet.frame_core_roles.iteritems():
    for role in roles:
        frame2core_role = "u:" + frame + " v:" + role + " d:0 t:fn_frame2fn_core_role s:FrameNet"
        new_relations.add(frame2core_role)
print "Extracted relations of type *FN-frame to FN-role (core)*: " + str(len(new_relations) - count)
count = len(new_relations)
for frame, roles in framenet.frame_extrathematic_roles.iteritems():
    for role in roles:
        frame2xtrathem_role = "u:" + frame + " v:" + role + " d:0 t:fn_frame2fn_extrathematic_role s:FrameNet"
        new_relations.add(frame2xtrathem_role)
print "Extracted relations of type *FN-frame to FN-role (extrathematic)*: " + str(len(new_relations) - count)
count = len(new_relations)
for frame, roles in framenet.frame_peripheral_roles.iteritems():
    for role in roles:
        frame2peripheral_role = "u:" + frame + " v:" + role + " d:0 t:fn_frame2fn_peripheral_role s:FrameNet"
        new_relations.add(frame2peripheral_role)
print "Extracted relations of type *FN-frame to FN-role (peripheral)*: " + str(len(new_relations) - count)
count = len(new_relations)
for frame, related_frames in framenet.frame_relation_map.iteritems():
    for rel_frame in related_frames:
        frame2frame = "u:" + frame + " v:" + rel_frame + " d:0 t:fn_frame2fn_frame s:FrameNet"
        new_relations.add(frame2frame)
print "Extracted relations of type *FN-frame to FN-frame*: " + str(len(new_relations) - count)
count = len(new_relations)

# Get relations from the FrameNet sense repository (frame to frame, frame to roles)
print "*** Getting relations from the FN-WN automatic mappings ***"
syn2sense = get_syn2sense()
count = len(new_relations)
count_duplicates = 0
count_maps = 0
# TODO think whether to generate more or less coarse-grained FN roles (e.g. Frame+Role)
for frame, mappings in frame2wn_synset.iteritems():
    for mapping in mappings:
        count_maps += 1
        fn_role2wn_synset = "u:" + mapping[0] + " v:" + syn2sense[mapping[1]] + " d:0 t:fn_role2wn_synset s:FN-sense-repository w:" + str(mapping[2])
        if fn_role2wn_synset in new_relations:
            count_duplicates += 1
        new_relations.add(fn_role2wn_synset)
print "Extracted relations of type *FN-role to WN-synset*: " + str(len(new_relations) - count)
print "number of duplicates in the repo: " + str(count_duplicates)
count = len(new_relations)

print "Total number of new relations extracted: " + str(count)

new_relations = sorted(new_relations, key=lambda rel: rel.split(" ")[4])
with open(f_out, "w") as output:
    for rel in new_relations:
        output.write(rel+"\n")

print "Done"