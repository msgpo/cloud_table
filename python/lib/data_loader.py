import pandas as pd
import numpy as np
from torch.utils.data import Dataset
import glob
from pyntcloud import PyntCloud

def load_ply(file_name):
    cloud = PyntCloud.from_file(file_name)
    return cloud.points.values

def load_obj(file_name):
    vertices = []
    with open(file_name) as f:
        for line in f:
            if line[:2] == 'v ':
                index1 = line.find(' ') + 1
                index2 = line.find(' ', index1 + 1)
                index3 = line.find(' ', index2 + 1)

                vertex = (float(line[index1:index2]), float(line[index2:index3]), float(line[index3:-1]))
                vertex = [round(vertex[0], 2), round(vertex[1], 2), round(vertex[2], 2)]
                vertices.append(np.array(vertex))
                
    return np.array(vertices)

def load_off(file_name):
    vertices = []
    with open(file_name) as f:
        for i, line in enumerate(f):
            vals = line.split(' ')
            if i > 2 and len(vals) == 3:
                vertex = [float(vals[0]), float(vals[1]), float(vals[2])]
                vertices.append(np.array(vertex))

    return np.random.permutation(np.array(vertices))[:2048]


def rotate_point_cloud(batch_data):

    rotated_data = np.zeros(batch_data.shape, dtype=np.float32)
    for k in range(batch_data.shape[0]):
        rotation_angle = np.random.uniform() * 2 * np.pi
        cosval = np.cos(rotation_angle)
        sinval = np.sin(rotation_angle)
        rotation_matrix = np.array([[cosval, 0, sinval],
                                    [0, 1, 0],
                                    [-sinval, 0, cosval]])
        shape_pc = batch_data[k, ...].T
        
        rotated_data[k, ...] = np.dot(shape_pc.reshape((-1, 3)), rotation_matrix).T
        
    return rotated_data

class PointCloudDataset(Dataset):
    """Point cloud dataset."""

    def __init__(self, number=-1, directory='./data/04379243'):
        
        file_names = sorted(glob.glob('%s/*.ply' % directory))

        if number > 0 and len(file_names) > number:
            file_names = file_names[:number]
        
        point_clouds = []
        for file_name in file_names:

            points = load_ply(file_name)
            point_clouds.append(points)

        self.point_clouds = np.array(point_clouds, dtype='float64')
        self.point_clouds = np.transpose(self.point_clouds, (0, 2, 1))
        
    def __len__(self):
        return len(self.point_clouds)

    def __getitem__(self, idx):
        return self.point_clouds[idx]


def load_point_clouds(index_list, directory='./data/04379243'):
    
    file_names = sorted(glob.glob('%s/*.ply' % directory))
    point_clouds = []
    for i in index_list:
        
        file_name = file_names[i]
        points = load_ply(file_name)
        point_clouds.append(points)

    point_clouds = np.array(point_clouds, dtype='float64')
    return np.transpose(point_clouds, (0, 2, 1))