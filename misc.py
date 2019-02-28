f_dict = "/home/lenovo/dev/KBWSD/knowledge-resources/WN-graph-sensed-relations/wn30lmsense.lex"

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

"close_in close_in%2:35:00::-v:0 close_in%2:38:00::-v:7"

def get_sense2freq(f_dict=f_dict):
    sense2freq = {}
    with open(f_dict, "r") as dict:
        for line in dict.readlines():
            senses = line.split()[1:]
            for sense in senses:
                freq = sense.split(":")[-1]
                sense_id = sense[:-len(freq)-1]
                if sense_id not in sense2freq:
                    if len(freq) > 0:
                        sense2freq[sense_id] = int(freq)
                    else:
                        sense2freq[sense_id] = 0
    return sense2freq

if __name__ == "__main__":
    sense2freq = get_sense2freq()
    print "This is the end."