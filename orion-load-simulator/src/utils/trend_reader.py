import glob
import pandas as pd


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