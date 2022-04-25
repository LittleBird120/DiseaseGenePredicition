import os.path
import json
import os

def readDIPfile(parent_path):
    edges = {}
    index = 0
    xmlfilepath = os.path.join(parent_path, r'data\Hsapi20170205CR.txt')
    f = open(xmlfilepath)
    lines = f.readlines()
    for line in lines:
        line_list = line.strip("\n").split("\t")
        if line_list[9] == "taxid:9606(Homo sapiens)" and line_list[10] == "taxid:9606(Homo sapiens)":
            source = line_list[0].split("|")[0]
            target = line_list[1].split("|")[0]
            if source != target:
                edges[index] = [source, target]
                index += 1
    print(len(edges))

    result_path = parent_path + r'\data\uploads\resultEdges.json'
    with open(result_path, 'w') as fw:
        json.dump(edges, fw)


if __name__ == '__main__':
    ROOT_DIR = os.path.dirname(os.path.abspath('__file__'))
    parent_path = os.path.dirname(ROOT_DIR)
    readDIPfile(parent_path)