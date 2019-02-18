from framenet_as_graph import read_fn_database, parse_all_fn_files

f_framenet = "/home/lenovo/dev/KBWSD/knowledge-resources/hydralex/data/framenet/"

def read_framenet(path_to_fn):
    data = read_fn_database.LoadFrameNet(path_to_fn)
    return data

if __name__ == "__main__":
    framenet = read_framenet(f_framenet)