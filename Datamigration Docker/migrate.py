# Libraries
# from fileinput import filename
# import pandas as pd
import os
import hashlib
from pickle import TRUE
import shutil
import csv
import time
import logging
from os.path import exists

# Docker paths
source_path = "/data/source"
dest_path = "/data/dest"
tmp_path = "/data/tmp"
logging_path = "/data/logs"
python_log_file = "/data/logs/pythonlogs"

# Testing paths
# source_path = "C:/Repos/python-migration-container/test/source"
# dest_path = "C:/Repos/python-migration-container/test/dest"
# tmp_path = "C:/Repos/python-migration-container/test/tmp"
# logging_path = "C:/Repos/python-migration-container/test/logs"
# python_log_file = "C:/Repos/python-migration-container/test/logs/pythonlogs"

# Perform hashing and return a hash
def md5_hashing(path_to_hash_files):
  logging.info('Hashing ' + path_to_hash_files)
  hash = hashlib.md5()
  with open(path_to_hash_files, "rb") as f:
    data = f.read() #read file in chunk and call update on each chunk if file is large.
    hash.update(data)
  return hash.hexdigest()


# Create the base filename list from the source
def create_filename_list(path):
  logging.info("Creating the source list")
  filename_list = os.listdir(path)
  return filename_list


# Seperate function to create the list
def create_list(path_to_hash_files, filename_list):
  list = []

  # Create loop to run over above list
  for filename in filename_list:
    filename_path = path_to_hash_files + "/" + filename
    hash = md5_hashing(filename_path)
    filename_hash_list = [filename, hash, filename_path]
    list.append(filename_hash_list)

    # Create CSV file
    with open((logging_path + "/" + "src-hashing-list.csv"), 'a', newline='') as myfile:
      wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
      wr.writerow(filename_hash_list)

  return list


def compare_hashes(source_hash, target_hash):
  logging.info(source_hash + " : " + target_hash)
  if source_hash == target_hash:
    result = "SUCCESS"
  else:
    result = "ERROR"
  return result


# Function to copy files while also performing a hash check
def copy_files(source_list, target_path, source_path, csvname):
  target_list = []

  for entry in source_list:
    target_path_local = target_path + "/" + entry[0]
    from_path = source_path + "/" + entry[0]
    
    shutil.copy(from_path, target_path)
    filename_hash_list = []
    hash = md5_hashing(entry[2])

    # Add logging line here to describe the hash / file we are checking right now
    result = compare_hashes(entry[1], hash)

    if result == "SUCCESS":
      filename_hash_list = [entry[0], hash, target_path_local]
      target_list.append(filename_hash_list)
      with open((logging_path + "/" + csvname + "-success-move-to-FS-list.csv"), 'a', newline='') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow(filename_hash_list)
      logging.info(entry[0] + " - hashes are correct")
    else:
      with open((logging_path + "/" + csvname + "-error-move-to-FS-list.csv"), 'a', newline='') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow(filename_hash_list)
      logging.warning(entry[0] + " - will not be moved due to hashes not being correct")

  return target_list


def delete_files(files_list):
  for file_path in files_list:
    logging.info('deleting files in ' + file_path[2])
    if os.path.exists(file_path[2]):
      os.remove(file_path[2])
    else:
      print("The file does not exist")


# the main sequence to enact
def main():
  # Setup Logging config
  logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)-8s %(message)s', datefmt='%a, %d %b %Y %H:%M:%S', filename=python_log_file, filemode='a')

  while True:
    # Create empty lists
    source_list = []
    intermittent_list = []
    target_list = []
    filename_list = []

    filename_list = create_filename_list(source_path)

    source_list = create_list(source_path, filename_list)
    if source_list == []:
      logging.info('No files to copy, skipping this iteration')
    else:
      # Copy files too temporary location
      intermittent_list = copy_files(source_list, tmp_path, source_path, "tmp")

      # Move target files
      target_list = copy_files(intermittent_list, dest_path, tmp_path, "dest")

      # delete files tmp folder
      delete_files(intermittent_list)

      # delete files source folder
      delete_files(source_list)
    time.sleep(60)

# excecute the program
if __name__ == '__main__':
    main()