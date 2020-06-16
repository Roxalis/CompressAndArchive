# -*- coding: utf-8 -*-

import datetime
import humanize
import os
import re
import statistics
import sys
import unicodedata
import zipfile

"""Be aware that this program will treat certain older Pages files as folders"""


def merge_dict(dict1, dict2):
    """Merge dictionaries and keep values of common keys in list"""
    dict3 = {**dict1, **dict2}
    for key, value in dict3.items():
        if key in dict1 and key in dict2:
            dict3[key] = [value, dict1[key]]
    return dict3


def compress_folder(path_to, path_from):
    """
    Void function that compresses a folder
    :param path_to: archive directory
    :param path_from: path to folder that will be zipped
    """
    print("Zipping folder...")
    with zipfile.ZipFile(path_to, 'w', zipfile.ZIP_DEFLATED) as new_zip:
        for root, sub_dirs, files in os.walk(path_from):
            for f in files:
                new_zip.write(os.path.join(root, f))
        new_zip.close()


def compress_file(path_to, path_from):
    """
    Void function that compresses a file
    :param path_to: archive directory
    :param path_from: path to file that will be zipped
    """
    print("Zipping file...")
    with zipfile.ZipFile(path_to, 'w', zipfile.ZIP_DEFLATED) as new_zip:
        new_zip.write(path_from)
        new_zip.close()


def get_zip_data_lists(path_to):
    """
    Fruitful function that provides the data for the log file
    :param path_to: archive directory
    :returns: file_ext_lst: list of file extensions
    :returns: file_factor_lst: list of average compression factors
    :returns: total_unzip: total size of data in the folder
    :returns: total_zip: total size of zipped data
    :returns: zip_file_lst: list of compressed files
    """
    zip_file = zipfile.ZipFile(path_to)
    zip_file_lst = zip_file.namelist()

    # generates list of file extensions, e.g. hidden files are 'other'
    file_ext_lst = []
    for f in zip_file_lst:
        file_extension = re.findall(r'[\w\s]+\.([A-Za-z]+$)', f)
        if len(file_extension) == 0:
            file_ext_lst += ['other']
        else:
            file_ext_lst += file_extension

    # calculates compression factor and generates archive size in zipped and unzipped state
    file_factor_lst = []
    total_unzip = 0
    total_zip = 0
    for file in zip_file_lst:
        info = zip_file.getinfo(file)
        file_factor_lst += [round(info.file_size / info.compress_size, 2)]
        total_unzip += info.file_size
        total_zip += info.compress_size
    return file_ext_lst, file_factor_lst, total_unzip, total_zip, zip_file_lst


def get_zip_dictionary(file_extensions, file_factors):
    """
    Fruitful function that generates and returns a dictionary with file extensions
    as keys and the values are lists containing number of files and
    compression factors.
    :param file_extensions: list of file extensions (strings)
    :param file_factors: list of compression factors (float numbers)
    :returns: f_dct: dictionary with file extensions as keys and lists of # of files and avg. factors
    """
    # generates dictionary with number of files as values (keys: file extensions)
    f_num_dct = {}
    for e in file_extensions:
        if e not in f_num_dct:
            f_num_dct[e] = 1
        else:
            f_num_dct[e] += 1

    # generates dictionary with compression factor lists as values (keys: file extension)
    f_ext_dct = {}
    for k, v in zip(file_extensions, file_factors):
        if k not in f_ext_dct:
            f_ext_dct[k] = [v]
        else:
            f_ext_dct[k] += [v]

    # calculates the average factor and returns it as a key-value pair.
    for k in f_ext_dct.keys():
        f_ext_dct[k] = round(statistics.mean(f_ext_dct[k]), 2)

    # merges the two dictionaries
    f_dct = merge_dict(f_num_dct, f_ext_dct)

    return f_dct


def write_zip_data(dictionary, total_unzip, total_zip, files, path_to_archive, folder_name):
    """
    Void function that writes a log file containing pivotal information about the zip process
    :param dictionary: dictionary with file extensions as keys and lists of # of files and avg. factors
    :param total_unzip: total size of data in the folder
    :param total_zip: total size of zipped data
    :param files: list of compressed files
    :param path_to_archive: path to archive
    :param folder_name: name of folder to be compressed
    """
    print("Writing log file...")
    with open(path_to_archive + folder_name + '_log.txt', 'w') as fin:
        fin.write("{}\n".format(datetime.datetime.now()))
        fin.write("\n")
        fin.write("Compressed folder: " + folder_name + "\n")
        fin.write("\n")
        fin.write("{:<20} {:<15} {:<20}\n".format('File', '#', 'Zip factor (avg.)'))
        total_num = 0
        for k, v in dictionary.items():
            total_num += v[1]
            fin.write("{:<20} {:<15} {:<20}\n".format(k, v[1], v[0]))
        fin.write("\n")
        fin.write("Total number of files: {}\n".format(total_num))
        fin.write("\n")

        factor = total_unzip / total_zip
        percent = (total_zip * 100) / total_unzip
        fin.write("Compression: {} --> {} "
                  "(factor: {}, percent: {})\n".format(humanize.naturalsize(total_unzip),
                                                       humanize.naturalsize(total_zip),
                                                       round(factor, 2), round(percent, 2)))
        fin.write("\n")
        fin.write("Files:\n")
        for e in files:
            fin.write(e + "\n")


def main(path_to):
    """Main program"""

    # test if path is a file:
    if os.path.isfile(path_to):
        # check if archive exists and then compress the file
        file = re.findall(u'([-A-Za-z0-9.\u00C0-\u017F ]+)\\.[a-z]+$', path_to)
        archive = '/Users/.../Documents/Archive/'
        # path to folder to create zip file:
        path_to_archive = archive + file[0] + '.zip'
        archive_file = file[0] + '.zip'
        # check if archive exists and then compress the file
        dir_lst = os.listdir(archive)
        if archive_file not in dir_lst:
            compress_file(path_to_archive, path_to)
            print("Process finished.")
        else:
            print("Archive already exists.")
            exit(0)

    # test if path is a folder:
    elif os.path.isdir(path_to):
        folder = re.findall(u'([-A-Za-z0-9.\u00C0-\u017F ]+$)', path_to)
        archive = '/Users/.../Documents/Archive/'
        # path to folder to create zip file:
        path_to_archive = archive + folder[0] + '.zip'
        archive_folder = folder[0] + '.zip'
        # check if archive exists and then compress the folder and write the log file
        dir_lst = os.listdir(archive)
        if archive_folder not in dir_lst:
            compress_folder(path_to_archive, path_to)
            zip_data_tuple = get_zip_data_lists(path_to_archive)
            zip_dct = get_zip_dictionary(zip_data_tuple[0], zip_data_tuple[1])
            write_zip_data(zip_dct, zip_data_tuple[2], zip_data_tuple[3], zip_data_tuple[4], archive, folder[0])
            print("Process finished.")
        else:
            print("Archive already exists.")
            exit(0)
    else:
        print("Not a file or folder.")
        exit(0)


if __name__ == '__main__':
    main(unicodedata.normalize("NFC", sys.argv[1]))
