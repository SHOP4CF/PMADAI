from src.domain.metadata import Metadata
from src.preprocessors.preprocessor import Preprocessor
from src.preprocessors.time_based_preprocessor import TimeBasedPreprocessor
import pandas as pd
import glob
import numpy as np
import simplejson as json
from pathlib import Path
from multiprocessing import Process
import os
import argparse

DATA_PATH = os.environ["DATA_PATH"]

METADATA_PATHS = [f"{DATA_PATH}/raw/20200911/Metadata_2020-06-10_2020-09-11.xlsx",
                  f"{DATA_PATH}/raw/20201106/KTL_MDS_01102020_06112020.xlsx",
                  f"{DATA_PATH}/raw/20210120/KTL01122020-20012021.xlsx",
                  f"{DATA_PATH}/raw/20210225/KTL 20012021-25022021.xlsx",
                  f"{DATA_PATH}/raw/20210407/KTL.xlsx",
                  f"{DATA_PATH}/raw/20210622/zestawienie.xlsx"
                  ]
TRENDS_PATHS = [f"{DATA_PATH}/raw/20200911/Trendy-2020-09-11",
                f"{DATA_PATH}/raw/20201106/Trendy-2020-11-06",
                f"{DATA_PATH}/raw/20210120/Trendy-2021-01-20",
                f"{DATA_PATH}/raw/20210225/Trendy-2021-02-25",
                f"{DATA_PATH}/raw/20210407/Trendy-2021-04-07",
                f"{DATA_PATH}/raw/20210622/Trendy-2021-06-22 - FKT1C"
                ]
OUTPUT_PATHS = [DATA_PATH + "/processed/{}/20200911",
                DATA_PATH + "/processed/{}/20201106",
                DATA_PATH + "/processed/{}/20210120",
                DATA_PATH + "/processed/{}/20210225",
                DATA_PATH + "/processed/{}/20210407",
                DATA_PATH + "/processed/{}/20210622"
                ]

# METADATA_PATHS = ["/home/damianhorna/shop4cf/data/raw/20210622/zestawienie.xlsx"]
# TRENDS_PATHS = ["/home/damianhorna/shop4cf/data/raw/20210622/Trendy-2021-06-22 - FKT1C"]
# OUTPUT_PATHS = ["/home/damianhorna/shop4cf/data/processed/06072021/20210622"]

winter_times = [(pd.to_datetime("2020-10-25 02:00"), pd.to_datetime("2021-03-28 02:00"))]

proc_names = [str(i) for i in range(1, len(METADATA_PATHS) + 1)]


class TrendReader:
    @staticmethod
    def read(base_directory_path,
             trend_name):
        df_list = []
        folders = glob.glob(f"{base_directory_path}/*", recursive=True)

        # Iterate through folders and collect individual DataFrames into a list to later concatenate them all
        for folder in folders:
            datestr = folder[folder.rfind("/") + 1:]
            df = pd.read_csv(f'{folder}/{trend_name}.csv', sep=";", header=None)[[0, 1]]
            df[0] += f' {datestr}'
            df_list.append(df)

        # Concatenation of collected DataFrames
        df = pd.concat(df_list)
        df[0] = pd.to_datetime(df[0], format='%H:%M:%S %Y%m%d')
        df = df.sort_values(0)
        df.columns = ['dt', 'value']
        return df


class PreprocessingRunner:
    def __init__(self, no_interp_points, smoother_name, json_id, metadata_path, trends_path, output_path, process_name):
        self.smoother_name = smoother_name
        self.no_interp_points = no_interp_points
        self.json_id = json_id
        self.metadata_path = metadata_path
        self.trends_path = trends_path
        self.output_path = output_path
        self.process_name = process_name

    @staticmethod
    def int_like(s):
        try:
            int(s)
            return True
        except ValueError:
            return False

    def preprocess(self):
        # Read metadata
        print(f"Process: {self.process_name} reading metadata...")
        metadata_df = pd.read_excel(self.metadata_path, sheet_name="Arkusz1", engine="openpyxl")
        metadata_df['Punkt czasu'] = pd.to_datetime(metadata_df['Punkt czasu'])
        metadata_df = metadata_df.sort_values('Punkt czasu')

        # Read trends
        print(f"Process: {self.process_name} reading trends...")
        trends = {"CurrentTrends": {}}
        for i in range(1, 5):
            trend_values_df = TrendReader.read(self.trends_path, f"L1VGL1.C811KS_1HS_K{i}.AA.R2323_AVCuB")
            trends["CurrentTrends"][f"current_on_busbar_{i}"] = trend_values_df.set_index('dt').sort_index()

        # Run preprocessing
        print(f"Process: {self.process_name} start preprocessing...")
        try:
            for row in metadata_df.iterrows():
                # Check if "Punkt czasu" is winter time:
                if any([start < row[1]["Punkt czasu"] < end for start, end in winter_times]):  # -120 + 4 + 60 mins
                    time_of_event = (row[1]["Punkt czasu"] - np.timedelta64(6985 - 3600, 's')).strftime(
                        "%Y-%m-%d %H:%M:%S.%f")
                else:  # Summer time (-120 + 4 mins)
                    time_of_event = (row[1]["Punkt czasu"] - np.timedelta64(6985, 's')).strftime("%Y-%m-%d %H:%M:%S.%f")

                # Check if INOUT is in columns:
                if "IN/OUT" in metadata_df.columns:
                    if row[1]["IN/OUT"] != "IN":
                        continue

                metadata = Metadata({
                    "timeOfEvent": time_of_event,
                    "inOut": "IN",
                    "carBodyId": str(row[1]["Numer Karoserii"]),
                    "carBodyType": row[1]["Typ podstawowy"],
                    "voltageProgramType": str(row[1]["Rodzaj programu napiecia KTL"]),
                    "skidId": int(row[1]["ID Skida"]),
                    "pendulumId": int(row[1]["Numer wahadla"]) if self.int_like(row[1]["Numer wahadla"]) else -1,
                    "paintingCyclesCount": int(row[1]["Licznik cyklow pracy"]) if self.int_like(
                        row[1]["Licznik cyklow pracy"]) else -1,
                    "servicesCount": int(row[1]["Licznik konserwacji"]) if self.int_like(
                        row[1]["Licznik konserwacji"]) else -1
                })

                # Init preprocessor
                cfg = {
                    'general': {
                        'interpolation-points': self.no_interp_points,
                        'smoother': self.smoother_name
                    }
                }
                preprocessor: Preprocessor = TimeBasedPreprocessor(cfg=cfg)
                pr_result = preprocessor.preprocess(metadata, trends)

                # Save preprocessing result
                json_serialized = json.dumps(pr_result.to_dict())
                Path(f"{self.output_path}").mkdir(parents=True, exist_ok=True)
                with open(f"{self.output_path}/{self.json_id}.json", "w", encoding="utf-8") as f:
                    f.write(json_serialized)
                self.json_id += 1

                if self.json_id % 50 == 0:
                    print(f"Process: {self.process_name} just saved JSON with id: {self.json_id}")
        except Exception as e:
            print(f"Error in process #{self.process_name}")
            print(e)


if __name__ == '__main__':
    procs = []

    parser = argparse.ArgumentParser()
    parser.add_argument('-points', help='defined number of interpolation points.', default=16, type=int)
    parser.add_argument('-dir', help='Output directory.', default='06072021', type=str)
    parser.add_argument('-smoother', help='Smoother class name for data smoothing', type=str, default=None)
    args = vars(parser.parse_args())
    OUTPUT_PATHS = [out_path.format(args['dir']) for out_path in OUTPUT_PATHS]

    for proc_name, meta_path, trend_path, out_path in zip(proc_names, METADATA_PATHS, TRENDS_PATHS, OUTPUT_PATHS):
        prep_runner = PreprocessingRunner(args['points'], args['smoother'], 0, meta_path, trend_path,out_path, proc_name)
        procs.append(Process(target=prep_runner.preprocess))

    for proc in procs:
        proc.start()
