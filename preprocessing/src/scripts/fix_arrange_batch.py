import glob
import shutil

dir1 = "/home/dhorna/dev/psnc/shop4cf/data/raw/20210622/Trendy-2021-06-22 - FKT1C"
dir2 = "/home/dhorna/dev/psnc/shop4cf/data/raw/20210622/Trendy-2021-06-22 - TrendServer"
dir3 = "/home/dhorna/dev/psnc/shop4cf/data/raw/20210622/Trendy-2021-06-22 - VGL1"

if __name__ == '__main__':
    for date_dir in glob.glob(f"{dir1}/*/"):
        print(".")
        for f in glob.glob(f"{dir2}/{date_dir[-9:]}*.csv"):
            shutil.copy(f, date_dir)

        for f in glob.glob(f"{dir3}/{date_dir[-9:]}*.csv"):
            shutil.copy(f, date_dir)
