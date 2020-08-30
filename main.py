# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings
from scipy import io
import os
import glob
import json
import numpy
from collections import OrderedDict
import pprint


class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, numpy.integer):
            return int(obj)
        elif isinstance(obj, numpy.floating):
            return float(obj)
        elif isinstance(obj, numpy.ndarray):
            return obj.tolist()
        else:
            return super(MyEncoder, self).default(obj)

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

def makeSummaryDictionary(matfile_dir):
    os.chdir(matfile_dir)
    matfile_list = glob.glob("*.mat")
    videodata_list = []

    for matfile in matfile_list:
        matdata = io.loadmat(matfile, squeeze_me=True)
        dic = {'type': matfile[0:2], 'filename': matfile, 'fps': matdata['fps'], 'resolution': matdata['resolution']}
        if dic['type'] == 'TV':
            dic['rebuf_duration'] = matdata['rebuf_duration']
            dic['rebuf_position'] = matdata['rebuf_position']
            dic['bitrate'] = matdata['bitrate']

        videodata_list.append(dic)

        print(matfile)

    videodata_dict = {'data': videodata_list}
    return videodata_dict

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # matfile_dir = "/home/jens/Documents/LFOVIA/QoE_matfiles"
    # output_dir = '/home/jens/Documents/matfile_read/output'
    matfile_dir = "./QoE_matfiles"
    output_dir = '../output'

    videodata_dict = makeSummaryDictionary(matfile_dir)

    with open(output_dir+'/lfovia_qos_data_3.json', 'w') as f:
        json.dump(videodata_dict, f, indent=4, cls=MyEncoder)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
