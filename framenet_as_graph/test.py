import parse_all_fn_files

variable_name = parse_all_fn_files.ReadAllFileFrames("/home/lenovo/dev/FrameNet/datasplit/training/")
frame_annotations = variable_name.all_frames
for annotation in frame_annotations:
    frame_name = annotation.frame_name
    sentence = annotation.sentence