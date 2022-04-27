import glob
import pandas as pd
import os
import simplejson as json
import itertools
import numpy as np
from pathlib import Path
import joblib
import argparse

DATA_PATH = os.environ["DATA_PATH"]

base_path = DATA_PATH + "/processed/{}"
output_path = DATA_PATH + "/processed/{}_dfs"


def read_jsons_into_dataframes(base_path, num_interpolation_points):
    metadata, histograms, interpolations, tsfresh = [], [], [], []
    raw_data = {}

    # Read data into lists
    subfolders = glob.glob(f"{base_path}/*/")
    for subfolder in subfolders:
        json_files = glob.glob(f"{subfolder}*.json")
        for filepath in json_files:
            if Path(filepath).stat().st_size < 20000:  # Skip small files (probably bad extraction anyway)
                continue
            with open(filepath) as f:
                pr_result = json.load(f)

                # Prepare rows
                histograms_row = list(itertools.chain(*pr_result['payload']['histograms']))
                interpolations_row = list(itertools.chain(*pr_result['payload']['interpolationFeatures']))
                tsfresh_row = list(itertools.chain(*pr_result['payload']['tsfreshFeatures']))
                metadata_row = [
                    pr_result['payload']['metadata']['timeOfEvent'],
                    pr_result['payload']['metadata']['inOut'],
                    pr_result['payload']['metadata']['carBodyId'],
                    pr_result['payload']['metadata']['carBodyType'],
                    pr_result['payload']['metadata']['voltageProgramType'],
                    pr_result['payload']['metadata']['skidId'],
                    pr_result['payload']['metadata']['pendulumId'],
                    pr_result['payload']['metadata']['paintingCyclesCount'],
                    pr_result['payload']['metadata']['servicesCount']
                ]

                # Append rows if conditions met
                if (len(histograms_row), len(interpolations_row), len(tsfresh_row)) == (60, 4*num_interpolation_points, 104):
                    histograms.append(histograms_row)
                    interpolations.append(interpolations_row)
                    tsfresh.append(tsfresh_row)
                    metadata.append(metadata_row)
                    raw_data[pr_result['payload']['metadata']['timeOfEvent']] = {
                        "values": pr_result["rawData"]["values"],
                        "times": pr_result["rawData"]["times"]
                    }

    # Construct numpy arrays
    metadata_array, histograms_array, interpolations_array, tsfresh_array = np.array(metadata), np.array(
        histograms), np.array(interpolations), np.array(tsfresh)

    # Construct dataframes
    metadata_df = pd.DataFrame(data=metadata_array,
                               index=pd.to_datetime(metadata_array[:, 0]),
                               columns=['timeOfEvent',
                                        'inOut',
                                        'carBodyId',
                                        'carBodyType',
                                        'voltageProgramType',
                                        'skidId',
                                        'pendulumId',
                                        'paintingCyclesCount',
                                        'servicesCount'
                                        ])
    histograms_df = pd.DataFrame(data=histograms_array,
                                 index=pd.to_datetime(metadata_array[:, 0]))

    interpolations_df = pd.DataFrame(data=interpolations_array,
                                     index=pd.to_datetime(metadata_array[:, 0]))

    tsfresh_df = pd.DataFrame(data=tsfresh_array,
                              index=pd.to_datetime(metadata_array[:, 0]))

    return metadata_df, histograms_df, interpolations_df, tsfresh_df, raw_data


def save(obj, filename, directory_path):
    dir_path = f"{directory_path}"
    Path(dir_path).mkdir(parents=True, exist_ok=True)
    joblib.dump(obj, f"{dir_path}/{filename}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-points', help='defined number of interpolation points.', default=16, type=int)
    parser.add_argument('-dir', help='Output/input directory.', default='06072021', type=str)
    args = vars(parser.parse_args())
    base_path = base_path.format(args['dir'])
    output_path = output_path.format(args['dir'])

    metadata_df, histograms_df, interpolations_df, tsfresh_df, raw_data = read_jsons_into_dataframes(base_path,
                                                                                                     args['points'])

    # Deduplication
    metadata_df = metadata_df.loc[~metadata_df.index.duplicated(keep='last')]
    histograms_df = histograms_df.loc[~histograms_df.index.duplicated(keep='last')]
    interpolations_df = interpolations_df.loc[~interpolations_df.index.duplicated(keep='last')]
    tsfresh_df = tsfresh_df.loc[~tsfresh_df.index.duplicated(keep='last')]

    save(metadata_df, "metadata_df", output_path)
    save(histograms_df, "histograms_df", output_path)
    save(interpolations_df, "interpolations_df", output_path)
    save(tsfresh_df, "tsfresh_df", output_path)
    save(raw_data, "raw_data_dict", output_path)
