'''
Created on Oct 19, 2017
@author: jennifersikos
'''
import re
import codecs
from frame_instance import FrameInstance
from role_instance import RoleInstance
from sentence_instance import SentenceInstance
import xml.etree.ElementTree as et


class ReadSingleFileFrames(object):
    '''
    This class reads a single parsed, xml-style FN file
    '''
    def __init__(self, filename):

        filename_xml, filename_conll = filename[0], filename[1]

        #---GET THE DATA FROM THE ORIGINAL XML FILES---#
        frames, entire_sentences = self.readXMLSentences(filename_xml)
        frames.sort(key=lambda i: (i.sentence_index, i.indices[0]))
        self.frames = frames
        self.entire_sentences = entire_sentences

        #---GET THE DATA FROM THE PARSED CONLL FILES---#
        entire_file = self.readConllSentences(filename_conll)
        self.entire_file = entire_file

        #---SEPARATE THE SENTENCES AS LISTS OF LEMMAS OR TOKENS----#
        entire_sentences_conll = self.get_entireSentences(entire_file)
        self.entire_sentences_conll = entire_sentences_conll

        frames_conll = self.getFrames(entire_file, entire_sentences_conll)
        self.frames_conll = frames_conll
        sentences = self.getSentences(entire_file, entire_sentences_conll)
        self.sentences = sentences

        for frame in self.frames:
            # print frame.lu
            # print frame.sentence_index
            sentence_match = [s for s in self.sentences if s.sentence_index == frame.sentence_index]
            if sentence_match:
                sentence = sentence_match[0]
            else:
                continue
            sentence.lus.append(frame.lu)

    @classmethod
    def readXMLSentences(self, filename):
        file = et.parse(filename)
        root = file.getroot()

        frames = []
        entire_sentences = []

        sindex = 0
        for child in root.iter('{http://framenet.icsi.berkeley.edu}sentence'):
            stext = ""
            tokens = []
            indices = []
            posTags = []
            for t in child.iter('{http://framenet.icsi.berkeley.edu}text'):
                stext = t.text
            for sentence in child:
                for anno in sentence.iter('{http://framenet.icsi.berkeley.edu}annotationSet'):
                    frame = FrameInstance()
                    for layer in anno.iter('{http://framenet.icsi.berkeley.edu}layer'):

                        # PENN part of speech tags and tokenized text
                        if layer.get('name') == "PENN":
                            for label in layer.iter('{http://framenet.icsi.berkeley.edu}label'):
                                token = stext[int(label.get('start')): int(label.get('end'))+1]
                                tokens.append(token)
                                indices.append(label.get('start')+":"+label.get('end'))
                                posTags.append(label.get('name'))

                        #Frame Annotations
                        if layer.get('name') == "Target":
                            for label in layer.iter('{http://framenet.icsi.berkeley.edu}label'):
                                frame.lu = anno.get('luName')
                                frame.sentence = tokens
                                frame.frame_name = anno.get('frameName')
                                ind = label.get('start') + ":" + label.get('end')
                                try:
                                    predicate_index = indices.index(ind)
                                    frame.indices.append(predicate_index)
                                except:
                                    for i, idx in enumerate(indices):
                                        if re.search(r'\b' + label.get('start') + ':', idx):
                                            frame.indices.append(i)
                                        if re.search(':' + label.get('end') + r'\b', idx):
                                            frame.indices.append(i)
                                frame.sentence_index = sindex

                        #Frame elements
                        if layer.get('name') == "FE":
                            for label in layer.iter('{http://framenet.icsi.berkeley.edu}label'):
                                if label.get('itype') == "INI" or label.get('itype') == "CNI" or label.get('itype') == "DNI" or label.get('itype') == "INC":
                                    continue
                                role = RoleInstance()
                                role.role = label.get('name')
                                ind = label.get('start') + ":" + label.get('end')
                                try:
                                    role_index = indices.index(ind)
                                    role.indices.append(role_index)
                                except:
                                    for i, idx in enumerate(indices):
                                        if re.search(r'\b' + label.get('start') + ':', idx):
                                            role.indices.append(i)
                                        if re.search(':' + label.get('end') + r'\b', idx):
                                            role.indices.append(i)
                                frame.roles.append(role)

                    #make sure frame is not empty
                    if frame.lu and frame.indices and not frame.frame_name == "Test35":
                        frames.append(frame)

            entire_sentences.append(stext)
            sindex+=1
        return frames, entire_sentences

    @classmethod
    def readConllSentences(self, filename):
        f = codecs.open(filename, 'r', encoding='utf-8')
        entire_text = f.read()
        entire_corpus = entire_text.split('\n\n')
        entire_corpus = filter(None, entire_corpus)
        f.close()
        return entire_corpus

    @classmethod
    def get_entireSentences(self, entire_file):
        all_sentences = []
        for sentence in entire_file:
            raw_sentences = []
            lines = sentence.split("\n")
            for line in lines:
                if line.startswith("#"):
                    continue
                raw_sentences.append(line)
            all_sentences.append(raw_sentences)
        return all_sentences

    @classmethod
    def getFrames(cls, entire_file, entire_sentences):
        frames = []

        for idx, chunk in enumerate(entire_file):
            lines = chunk.split("\n")
            sentence = entire_sentences[idx]

            for lidx, line in enumerate(lines):

                length = len(line)

                # Create Single Frame Instance
                if line.startswith("#") and "FEE" in line:
                    frame = FrameInstance()
                    line_index = line.split(":")
                    fee_indices = [x - 1 for x in list(map(int, line_index[1].strip().split(",")))]
                    frame.set_indices(fee_indices)
                    name = getFrameName(lidx - 1, lines)
                    if name == "Test35":
                        continue
                    frame.set_frame_name(name)
                    lemmas = getLemmas(fee_indices, sentence)
                    frame.set_lemma(' '.join(lemmas))
                    pos = getPOS(fee_indices, sentence)
                    frame.set_pos(pos[0])
                    frame.set_sentence(getTokens(sentence))
                    # frame.set_sentence_lemmatized(getLemmatizedTokens(sentence))
                    frame.set_sentence_index(idx)

                    # Get Role Instances for the given frame
                    roles = []
                    i = lidx + 1
                    while i < length and "Mapped" not in lines[i] and "Frame" not in lines[i]:
                        if lines[i].startswith('#'):
                            role = RoleInstance()
                            role_object = lines[i].split(":")
                            role.set_role(role_object[0])
                            try:
                                role.set_indices([x - 1 for x in list(map(int, role_object[1].strip().split(",")))])
                            except:
                                i += 1
                                continue
                            role.set_lemma(' '.join(getLemmas(role.indices, sentence)))
                            role.set_pos(getPOS(role.indices, sentence))
                            roles.append(role)
                            i += 1

                    frame.set_roles(roles)
                    frames.append(frame)
        return frames

    @classmethod
    def getSentences(cls, entire_file, entire_sentences):
        sentences = []
        for idx, chunk in enumerate(entire_file):
            lines = chunk.split("\n")
            sentence = entire_sentences[idx]
            if sentence[0] == "SKIPPED":
                continue
            sentence_inst = SentenceInstance()
            sentence_inst.set_pos(getPOSTokens(sentence))
            sentence_inst.set_sentence(getTokens(sentence))
            sentence_inst.set_sentence_lemmatized(getLemmatizedTokens(sentence))
            sentence_inst.set_sentence_index(idx)
            frames = []
            # counter to keep track of how many tokens a sentence is reduced by (due to merging)
            reduce_count = 0
            for lidx, line in enumerate(lines):
                # Create Single Sentence Instance and associate it with FEE annotations
                if line.startswith("#") and "FEE" in line:
                    line_index = line.split(":")
                    frame = getFrameName(lidx - 1, lines)
                    if frame == "Test35":
                        continue
                    fee_indices = [x - 1 - reduce_count for x in list(map(int, line_index[1].strip().split(",")))]
                    if len(fee_indices) > 1 and (fee_indices[0]+1 == fee_indices[1]):
                        # print fee_indices
                        # print sentence_inst.sentence_lemmatized
                        mwe = "_".join([sentence_inst.sentence_lemmatized[x] for x in fee_indices])
                        del sentence_inst.sentence_lemmatized[fee_indices[0]:fee_indices[-1] + 1]
                        sentence_inst.sentence_lemmatized.insert(fee_indices[0], mwe)
                        # TODO write rules to select the proper POS tag per MWE
                        pos_mwe = [sentence_inst.pos[x] for x in fee_indices]
                        del sentence_inst.pos[fee_indices[0]:fee_indices[-1] + 1]
                        sentence_inst.pos.insert(fee_indices[0], pos_mwe[0])
                        reduce_count += len(fee_indices) - 1
                    sentence_inst.set_fee_idxs(fee_indices[0])
                    frames.append(frame)
            if len(frames) > 0:
                sentence_inst.set_frames(frames)
                sentences.append(sentence_inst)
        return sentences

def getPOS(indices, sentence):
    return [sentence[x].split("\t")[4] for x in indices]

def getLemmas(indices, sentence):
    return [sentence[x].split("\t")[2] for x in indices]

def getTokens(sentence):
    return [sentence[x].split("\t")[1] for x, element in enumerate(sentence)]

def getLemmatizedTokens(sentence):
    return [sentence[x].split("\t")[2] for x, element in enumerate(sentence)]

def getPOSTokens(sentence):
    return [sentence[x].split("\t")[4] for x, element in enumerate(sentence)]

def getFrameName(index, lines):
    frame_assignment = lines[index].strip().split("\"")
    frame_name = frame_assignment[1].strip("\"")
    return frame_name
