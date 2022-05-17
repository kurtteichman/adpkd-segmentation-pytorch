import json
from argparse import ArgumentParser
import os
import subprocess
from pathlib import Path

from ensemble_utils import inference_scan_glob

# Preliminary Data
print("Loading system and pipeline configuration...")
id_system = open("adpkd_segmentation/inference/ensemble_config.json", "r")
system_config = json.loads(id_system.read())
# Parser Setup
parser = ArgumentParser()
parser.add_argument(
    "-i",
    "--inference_path",
    type=str,
    help="path to input dicom data (replaces path in config file)",
    default=None,
)

parser.add_argument(
    "-o",
    "--output_path",
    type=str,
    help="path to output location",
    default=None,
)

args = parser.parse_args()

inference_path = args.inference_path
output_path = args.output_path
# Prep the output path
if inference_path is not None:
    inf_path = inference_path

if output_path is not None:
    out_path = output_path

################### Individual Organ Inference ######################
pred_load_dir = []
scan_folders = inference_scan_glob(inf_path, system_config["dicom_suffix"])
for idx_organ, name_organ in enumerate(system_config["organ_name"]):
    print("Run " + str(idx_organ + 1) + ": " + name_organ + " inference...\n")
    save_path = os.path.join(output_path, name_organ)
    pred_load_dir.append(save_path)  # The constructed inference save directory -> load
    cd_cmd = "cd " + system_config["pipeline_path"]
    run_python = (
        system_config["python_cmd"]
        + system_config["config_code"]
        + system_config["model_dir"]["T2"]["Axial"][idx_organ]
        + f"{system_config['input_code']}{inf_path}"
        + f"{system_config['output_code']}{save_path}"
    )
    full_command = f"{system_config['env']}; {cd_cmd}; {run_python}"
    subprocess.call(full_command, shell=True)
    print(system_config["organ_name"][idx_organ] + " inference complete")

#####################################################################
############## Addition Ensemble -- Will Add in v1.01 ###############

#####################################################################
# Save the output -- Add in v1.01 or v1.02
comb_parent_path = Path(os.path.join(out_path), system_config["combined_folder"]).mkdir(
    parents=True, exist_ok=True
)
