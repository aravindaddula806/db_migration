import os,sys
from configs import log_file_dir


def write_log(msg,file):
    file_name = f'{log_file_dir}/{file}'
    with open(file_name,'wb'):
        file_name.write(msg)
