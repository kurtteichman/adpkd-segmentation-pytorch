import glob
import os

#########################################################################
############## Globbing Methods ##############
# %% Get files with a specific extention
def inference_scan_glob(ref_path, file_ext):
    """This puts together the above three functions:
    1) give me all of the files of given extension 'file_ext'
      in the given path 'ref_path'
    2) give me the the parent directories of the files
    3) return the unique parent directories."""
    all_files = glob.glob(ref_path + "/**/*" + file_ext, recursive=True)
    parents = [os.path.dirname(directory) for directory in all_files]
    unique_list = []
    for x in parents:
        if x not in unique_list:
            unique_list.append(x)

    return unique_list
