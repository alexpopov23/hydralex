import os
import _elementtree
import copy

path_to_verbnet = "/home/lenovo/dev/KBWSD/knowledge-resources/verbnet"

class VNClass():

    def __init__(self):
        self.name = ""
        self.verbs = []
        self.them_roles = []

def dfs(vertex):
    not_visited, hierarchy, queue = [vertex], {}, [vertex]
    while not_visited:
        vb_class = not_visited.pop()
        vb_class_name = vb_class.get("ID")
        subclasses = vb_class.findall("SUBCLASSES")[0].findall("VNSUBCLASS")
        for subclass in subclasses:
            hierarchy[subclass.get("ID")] = vb_class_name
            subhierarchy, subqueue = dfs(subclass)
            hierarchy.update(subhierarchy)
            queue.extend(subqueue)
    return hierarchy, queue

def read_verbnet(path_to_verbnet):

    vn_classes = {}
    them_roles_compendium = set()
    verbnet_hierarchy = {}
    num2class = {}
    wn_sense2vn_class = {}
    for filename in os.listdir(path_to_verbnet):
        if not filename.endswith("xml"):
            continue
        f_class = os.path.join(path_to_verbnet, filename)
        tree = _elementtree.parse(f_class)
        them_roles_all = {}
        top_class = tree.getroot()
        class_hierarchy, queue = dfs(top_class)
        for i, class_elem in enumerate(queue):
            vn_class = VNClass()
            vn_class.name = class_elem.get("ID")
            num2class["-".join(vn_class.name.split("-")[1:])] = vn_class.name
            them_roles_elem = class_elem.findall("THEMROLES")[0].findall("THEMROLE")
            if i> 0:
                vn_class.them_roles = copy.copy(them_roles_all[class_hierarchy[vn_class.name]])
            for them_role in them_roles_elem:
                type = them_role.get("type")
                role_str = type
                sel_restrs = []
                sel_restr_elems = them_role.findall("SELRESTRS")[0].findall("SELRESTR")
                for sel_restr_elem in sel_restr_elems:
                    value_sr = sel_restr_elem.get("Value")
                    type_sr = sel_restr_elem.get("type")
                    role_str +=  value_sr + type_sr
                    sel_restrs.append(value_sr + type_sr)
                them_roles_compendium.add(role_str)
                vn_class.them_roles.append((type, sel_restrs))
            them_roles_all[vn_class.name] = copy.copy(vn_class.them_roles)
            members = class_elem.findall("MEMBERS")[0].findall("MEMBER")
            for member in members:
                lemma = member.get("name")
                if member.get("wn") != "":
                    wn_senses = set(member.get("wn").split(" "))
                    for wn_sense in wn_senses:
                        # TODO think further whether to excluse the ?-marked mappings
                        if wn_sense == "" or wn_sense.startswith("?"):
                            continue
                        wn_sense += "::"
                        if wn_sense not in wn_sense2vn_class:
                            wn_sense2vn_class[wn_sense] = set([vn_class.name])
                        else:
                            wn_sense2vn_class[wn_sense].add(vn_class.name)
                else:
                    wn_senses = set()
                grouping = member.get("grouping")
                on_senses = set(grouping.split(" ") if (grouping != "" and grouping is not None) else [])

                vn_class.verbs.append((lemma, wn_senses, on_senses))
            # TODO Implement extraction for syntactic and semantic frame patterns, analyze examples as annotated data
            vn_classes[vn_class.name] = (copy.copy(vn_class))
            verbnet_hierarchy.update(class_hierarchy)
        print "Done with file " + filename
    return vn_classes, them_roles_compendium, verbnet_hierarchy, num2class, wn_sense2vn_class

if __name__ == "__main__":
    vb_classes, them_roles_compendium, class_hierarchy, num2class, wn_sense2vn_class = read_verbnet(path_to_verbnet)
    print "Done"
