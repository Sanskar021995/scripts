import boto3
import os
from typing import Tuple, List
from tqdm import tqdm
import pathlib
import json
from concurrent.futures import ThreadPoolExecutor
from tqdm.notebook import tqdm

import numpy as np

DEFAULT_NUM_THREAD = 8
S3_BUCKET = 'origin-redbrick-trial'
AWS_ACCESS_KEY_ID = '='
AWS_SECRET_ACCESS_KEY = ''
DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S.%f'


class S3IO:
    def __init__(self, bucket) -> None:
        self._client = boto3.client(
            's3',
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY
        )

        self._bucket = bucket

    # TODO: might need a lazy loading approach (generator) if dataset is huge
    def _get_uploaded_data(self, prefix: str) -> Tuple[List, List]:
        keys = []
        dirs = []
        next_token = ''
        base_kwargs = {
            'Bucket': self._bucket,
            'Prefix': prefix,
        }
        while next_token is not None:
            kwargs = base_kwargs.copy()
            if next_token != '':
                kwargs.update({'ContinuationToken': next_token})
            results = self._client.list_objects_v2(**kwargs)
            contents = results.get('Contents')
            
            for i in contents:
    
                k = i.get('Key')
                if k[-1] != '/':
                    keys.append(k)
                else:
                    dirs.append(k)
            next_token = results.get('NextContinuationToken')
        return keys, dirs

    def _check_and_download(self, key: str,
                            local: str) -> None:

        dest_pathname = os.path.join(local, key)
        if not os.path.exists(os.path.dirname(dest_pathname)):
            try:
                os.makedirs(os.path.dirname(dest_pathname))
            except Exception:
                pass
        # Possible corner case: modified local file will still get ignored
        if not os.path.exists(dest_pathname):
            self._client.download_file(self._bucket, key, dest_pathname)

    # Modified solution from
    # https://stackoverflow.com/questions/31918960/boto3-to-download-all-files-from-a-s3-bucket
    def download_directory(self, prefix: str,
                           local: str) -> None:
        keys, dirs = self._get_uploaded_data(prefix)

        for d in dirs:
            dest_pathname = os.path.join(local, d)
            if not os.path.exists(os.path.dirname(dest_pathname)): 
                os.makedirs(os.path.dirname(dest_pathname))

        def download_function(key: str, local_dir: str = local) -> None:
            self._check_and_download(key, local_dir)  # type: ignore

        with ThreadPoolExecutor(
                max_workers=DEFAULT_NUM_THREAD) as executor:
            executor.map(download_function, keys)

    def _upload_file(self, file: str,
                     prefix: str) -> None:
        num_dir_to_skip = len(prefix.split('/')[:-1])

        target_dir = '/'.join(file.split('/')[num_dir_to_skip:])

        self._client.upload_file(file, self._bucket,
                                 target_dir)

    def upload_directory(self, local_prefix: str, cloud_prefix: str,
                         num_local_dir_to_skip: int) -> None:
        local_files = [str(file) for file
                       in pathlib.Path(local_prefix + '/').rglob('*')
                       if file.is_file()]
    # while counting the num_local_dir_to_skip count the num of backslash in the local path    

        def upload_function(file: str,
                            prefix_dir: str = cloud_prefix
                            ) -> None:
            local_dir = '/'.join(file.split('/')[num_local_dir_to_skip:])
            self.upload_file(file, prefix_dir + local_dir)

        with ThreadPoolExecutor(
                max_workers=DEFAULT_NUM_THREAD) as executor:
            list(tqdm(executor.map(
                upload_function, local_files),
                total=len(local_files), leave=False))

    def upload_file(self, local_file_path: str, cloud_file_path: str) -> None:
        self._client.upload_file(local_file_path, self._bucket,
                                 cloud_file_path)
        
    def download_from_list(file_list, local_target, max_workers=DEFAULT_NUM_THREAD):
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            list(tqdm(executor.map(
                s3.download_directory, file_list,
                [local_target] * len(file_list)),
                total=len(file_list)))          

s3 = S3IO(S3_BUCKET)


# import pandas as pd
# df = pd.read_csv("")
# raw_files = df['image_path'].values.tolist()
# print(type(raw_files))
# print(len(raw_files))

# f = open('/home/ubuntu/OH/testing_data/first_trimester_jsons/ai-dev/classifier/model_catalog_first_trimester/dataset_1/datajsons/Nova_Presorter_MC_V2_test.json')
 
# # returns JSON object as 
# # a dictionary
# data = json.load(f)

# file_list = []
# for obj in data['data']:
#     file_list.append(obj['image_path'])
    
    
# download_target = '/home/ubuntu/OH/OH-Classifier-Framework-Basics/first_trimester_data/test'   

# def download_from_list(file_list, local_target, max_workers=DEFAULT_NUM_THREAD):
#     with ThreadPoolExecutor(max_workers=max_workers) as executor:
#         list(tqdm(executor.map(
#             s3.download_directory, file_list,
#             [local_target] * len(file_list)),
#             total=len(file_list)))
        
        
        
# download_from_list(file_list, download_target)     


s3_client = S3IO(S3_BUCKET)
local_file_path = "/home/ubuntu/OH/temp_stuff/Machine2_batch2"
cloud_file_path = "project_pixel_resolution/cropped_images_v2/machine_2/"

s3_client.upload_directory(local_file_path, cloud_file_path,6)   