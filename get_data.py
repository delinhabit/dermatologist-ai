import os
import zipfile
import shutil
from urllib.request import urlretrieve

from tqdm import tqdm


class TqdmUrlRetrieve(tqdm):

    def reporthook(self, blocks_transfered, block_size, total_size):
        if total_size is not None:
            self.total = total_size
        self.update(blocks_transfered * block_size - self.n)


def download_file_from_url(url, local_filename, description=None):
    with TqdmUrlRetrieve(unit='B', unit_scale=True, miniters=1, desc=description) as t:
        urlretrieve(
            url, 
            filename=local_filename,
            reporthook=t.reporthook
        )


def download_dataset(url, directory):
    dataset_name, file_ext = os.path.splitext(os.path.basename(url))
    file_name = "{}{}{}".format(directory, dataset_name, file_ext)
    if not os.path.exists(file_name):
        description = "Downloading '{}' dataset".format(dataset_name)
        download_file_from_url(url, file_name, description=description)
    else:
        print("{} dataset already downloaded".format(dataset_name), flush=True)


def extract_dataset(dataset, directory):
    zip_file_name = "data/source/{}.zip".format(dataset)
    print("Extracting '{}' dataset to '{}'".format(dataset, directory))
    with zipfile.ZipFile(zip_file_name, "r") as zip_ref:
        zip_ref.extractall(directory)	

# Download the datasets
os.makedirs("data/source/", exist_ok=True)
for dataset in ("train", "valid", "test"):    
    download_dataset(
        "https://s3-us-west-1.amazonaws.com/udacity-dlnfd/datasets/skin-cancer/{}.zip".format(dataset),
        "data/source/"
    )

# Extract the train and valid datasets into the train folder and the test
# dataset into the test folder (since the Tensorflow retrain tool does the
# splits for us).
if not os.path.exists("data/train/"):
    os.makedirs("data/train/", exist_ok=True)
    extract_dataset("train", "data/train/")
    extract_dataset("valid", "data/train/")

if not os.path.exists("data/test"):
    os.makedirs("data/test/", exist_ok=True)
    extract_dataset("test", "data/test/")
