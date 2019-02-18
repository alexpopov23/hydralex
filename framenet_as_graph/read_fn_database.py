# -*- coding: utf-8 -*-
"""
Created on Thu Jul 14 21:18:00 2016
Iterates over frame files, loads dictionaries containing the frame's lus and the frames for ea. unique lu

@author: sikos
"""
import xml.etree.ElementTree as et
import pkg_resources
from os import walk

frames = []
frames_for_lu = {}
lus_in_frame = {}
relation_map = {}
frame_relation_map = {}
frame_core_roles = {}
frame_peripheral_roles = {}
frame_extrathematic_roles = {}

class LoadFrameNet(object):

    def __init__(self, data_path):
        self.fillFNDictionaries(data_path)
        self.frames = frames
        self.lus_in_frame = lus_in_frame
        self.frames_for_lu = frames_for_lu
        self.relation_map = relation_map
        self.frame_relation_map = frame_relation_map
        self.frame_core_roles = frame_core_roles
        self.frame_peripheral_roles = frame_peripheral_roles
        self.frame_extrathematic_roles = frame_extrathematic_roles

    # Iterate over the file for filling the frame dictionaries
    def fillFNDictionaries(self, data_path):
        for dirpath, dirnames, filenames in walk(data_path):
            for file in filenames:
                if file.startswith("."):
                    continue
                frame_name = file.replace(".xml", "")
                frames.append(frame_name)
                path = dirpath + file
                file = et.parse(path)
                file_root = file.getroot()
                self.buildFrameLexicalUnitsDict(file_root)
                self.buildFramesForLexicalUnitsDict(file_root)
                self.generateRelationMap(file_root)
                self.generateFrameRelationMap(file_root)
                self.generate_frame_roles(file_root)


    # Frame-to-frame relation map
    def generateRelationMap(self, file_root):
        frame_name = file_root.get('name')

        for child in file_root.findall('{http://framenet.icsi.berkeley.edu}frameRelation'):
            for embed_child in child:
                single_relation = []
                single_relation.append(frame_name)
                single_relation.append(embed_child.text)

                if (child.get('type')) in relation_map:
                    relations = relation_map[child.get('type')]
                    relations.append(single_relation)
                    relation_map[child.get('type')] = relations

                if (child.get('type')) not in relation_map:
                    relations = []
                    relations.append(single_relation)
                    relation_map[child.get('type')] = relations


    # Frame-to-frame relation map
    def generateFrameRelationMap(self, file_root):
        frame_name = file_root.get('name')

        for child in file_root.findall('{http://framenet.icsi.berkeley.edu}frameRelation'):
            for embedded_child in child:

                if (frame_name) in frame_relation_map:
                    relations = frame_relation_map[frame_name]
                    relations.append(embedded_child.text)
                    frame_relation_map[frame_name] = relations

                if (frame_name) not in frame_relation_map:
                    relations = []
                    relations.append(embedded_child.text)
                    frame_relation_map[frame_name] = relations


    # Build dictionary for all LUs in a frame
    def buildFrameLexicalUnitsDict(self, file_root):
        frame_name = file_root.get('name')

        for child in file_root.findall('{http://framenet.icsi.berkeley.edu}lexUnit'):
            if frame_name in lus_in_frame:
                lus = lus_in_frame[frame_name]
                lus.append(child.get('name'))
                lus_in_frame[frame_name] = lus
            if frame_name not in lus_in_frame:
                lus = []
                lus.append(child.get('name'))
                lus_in_frame[frame_name] = lus


    # Build dictionary for all frames for a LU
    def buildFramesForLexicalUnitsDict(self, file_root):
        frame_name = file_root.get('name')

        for child in file_root.findall('{http://framenet.icsi.berkeley.edu}lexUnit'):
            predicate = child.get('name').lower()
            if predicate in frames_for_lu:
                frames = frames_for_lu[predicate]
                if frame_name in frames:
                    continue
                frames.append(frame_name)
                frames_for_lu[predicate] = frames
            if predicate not in frames_for_lu:
                frames = []
                frames.append(frame_name)
                frames_for_lu[predicate] = frames


    # Frame index is the arbitrary index number assigned to each frame
    def getFrameIndex(self, frames, frame):
        for index, item in enumerate(frames):
            frame_name = item.decode('utf-8').strip()
            if frame.lower() == frame_name.lower():
                return index

    # Author: apopov
    def generate_frame_roles(self, file_root):
        frame_name = file_root.get("name")
        frame_core_roles[frame_name] = set()
        frame_peripheral_roles[frame_name] = set()
        frame_extrathematic_roles[frame_name] = set()
        roles = file_root.findall("{http://framenet.icsi.berkeley.edu}FE")
        for role in roles:
            core_type = role.get("coreType")
            if core_type == "Core":
                frame_core_roles[frame_name].add(role.get("name").replace(" ", "_"))
            elif core_type == "Peripheral":
                frame_peripheral_roles[frame_name].add(role.get("name").replace(" ", "_"))
            elif core_type == "Extra-Thematic":
                frame_extrathematic_roles[frame_name].add(role.get("name").replace(" ", "_"))

def main():
    #plug in the path to the FN database as argument here
    data = LoadFrameNet()
    frame_relation_map = data.frame_relation_map
    lus_in_frame = data.lus_in_frame
    for key, values in frame_relation_map.iteritems():
        print(key)
        for value in values:
            try:
                print(value, lus_in_frame[value])
            except:
                print(value, " has no lexical units")

if __name__ == "__main__":
    main()