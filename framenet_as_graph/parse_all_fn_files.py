from parse_single_fn_file import ReadSingleFileFrames
import glob

class ReadAllFileFrames(object):

    def __init__(self, directory):

        #TODO NTI__Taiwan_Introduction.xml in training folder has no CONLL counterpart
        filenames_xml = sorted(self.readDirectoryXML(directory))
        filenames_conll = sorted(self.readDirectoryCONLL(directory))
        self.combineFrameData(zip(filenames_xml, filenames_conll))

    @classmethod
    def readDirectoryXML(self, directory):
        filenames = glob.glob(directory + "*.xml")
        return filenames

    @classmethod
    def readDirectoryCONLL(self, directory):
        filenames = glob.glob(directory + "*.conll")
        return filenames

    @classmethod
    def combineFrameData(self, filenames):
        all_sentences = []
        all_frames = []

        for file in filenames:
            print(file)
            singleFrameFile = ReadSingleFileFrames(file)
            sentences = singleFrameFile.sentences
            all_sentences.extend(sentences)
            frames = singleFrameFile.frames
            all_frames.extend(frames)

        self.all_sentences = all_sentences
        self.all_frames = all_frames
