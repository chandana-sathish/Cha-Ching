import numpy as np
from torch.utils import data
import torch
import random

class TDData(data.Dataset):
    def __init__(self):
        self.list = self.read_files()

    def read_files(self):
        '''
        Use this function to append each transaction onto d.
        '''
        d = []
        txt_file = os.path.join('/home/rexma/Desktop/JesseSun/ac17_seg/data/data_series.txt')
        split_range = list(range((self.k_split-1)*self.split_len, self.k_split*self.split_len))
        with open(txt_file, 'r') as f:
            for i, line in enumerate(f):
                l = line.split(' ')
                key, val = int(l[0]), int(l[1])
                # append as train set
                if self.split == 'train' and i not in split_range:
                    d.append([key, val])

                #append as val set
                elif self.split == 'val' and i in split_range:
                    d.append([key, val])
                    if i > split_range[-1]: #do not need to iterate through rest of file
                        return d
        return d

    def __len__(self):
        return len(self.list)

    def __getitem__(self, i): # i is index
        '''
        Load up the vector here. It'll be a dictionary.
        '''
        type = self.list[i]["food"]

        input = torch.from_numpy(input)
        label = self.list[i]["amount_spent"]/500

        data_dict = {
            "input_data": input,
            "label": label
        }

        return data_dict

if __name__ == "__main__":
    data = TDData()
    dataloader = data.DataLoader(data, batch_size=1)
    for idx, batch in enumerate(dataloader):
        print(batch["input_data"].shape, batch["label"])
        if idx > 10:
            break
