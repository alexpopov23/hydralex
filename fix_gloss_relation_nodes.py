from misc import num2pos

f_gloss = "/home/lenovo/dev/KBWSD/knowledge-resources/WN-graph-sensed-relations/Version02GlossMD/GlossDD.txt"
f_gloss_fixed = "/home/lenovo/dev/KBWSD/knowledge-resources/WN-graph-sensed-relations/Version02GlossMD/GlossDD_fixed.txt"

with open(f_gloss, "r") as gloss_rels:
    to_write = ""
    for rel in gloss_rels:
        # Get rid of these relations
        if "purposefully_ignored%0:00:00" in rel:
            continue
        if "brown-vose" in rel:
            rel = rel.replace("brown-vose", "brown-nose")
        if "dry-vurse" in rel:
            rel = rel.replace("dry-vurse", "dry-nurse")
        fields = rel.split()
        if len(fields) < 2:
            continue
        u, v = fields[0], fields[1]
        # u_pos_num, v_pos_num = u.split("%")[1][0], v.split("%")[1][0]
        u_pos, v_pos = u[-1], v[-1]
        # if u_pos == ":" or v_pos == ":":
        #     to_write += rel
        #     continue
        if len(fields[0].split(":")[-1]) == 2 and fields[0].split(":")[-1][-2] != "-" or fields[0].endswith("::"):
            fields[0] += "-" + num2pos(fields[0])
        elif u_pos != num2pos(u[2:]):
            new_field = list(fields[0])
            new_field[-1] = num2pos(u[2:])
            fields[0] = "".join(new_field)
        if len(fields[0].split(":")[-1]) == 4:
            sub_fields = fields[0].split("%")
            new_field = list(sub_fields[1])
            new_field[0] = "5"
            sub_fields[1] = "".join(new_field)
            fields[0] = "%".join(sub_fields)
        if len(fields[1].split(":")[-1]) == 2 and fields[1].split(":")[-1][-2] != "-" or fields[1].endswith("::"):
            fields[1] += "-" + num2pos(fields[1])
        elif v_pos != num2pos(v[2:]):
            new_field = list(fields[1])
            new_field[-1] = num2pos(v[2:])
            fields[1] = "".join(new_field)
        if len(fields[1].split(":")[-1]) == 4:
            sub_fields = fields[1].split("%")
            new_field = list(sub_fields[1])
            new_field[0] = "5"
            sub_fields[1] = "".join(new_field)
            fields[1] = "%".join(sub_fields)
        new_rel = " ".join(fields)
        to_write += new_rel + "\n"

with open(f_gloss_fixed, "w") as gloss_rels_fixed:
    gloss_rels_fixed.write(to_write)