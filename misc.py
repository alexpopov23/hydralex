def num2pos(sense):
    if sense == "NULL":
        return "NULL"
    # if len(sense) < 9:
    #     return ""
    pos_id = sense.split("%")[1][0]
    # pos_id = sense[-9]
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