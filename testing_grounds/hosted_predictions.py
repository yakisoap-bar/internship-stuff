import tensorflow as tf
# import libraries
import pandas as pd
import numpy as np
import pathlib
import time

print(f'pandas version: {pd.__version__}')
print(f'numpy version: {np.__version__}')

# define one hot encode function
def one_hot(arr, n_cat):
    output = []
    for n in arr:
        result = np.zeros(n_cat)
        result[n] = 1

        output.append(result)

    return np.array(output, dtype=int)

# import data for testing
# paths to load datasets from
val_store_path = '../datasets/sa/validation'

# convert to pathlib Path objects
val_dir = pathlib.Path(val_store_path)

# get list of datasets in dir
val_ds_paths = sorted(list(val_dir.glob('*.csv')))

# extract classification target from file names
val_ds_type = np.array([x.parts[-1].split('_')[:2] for x in val_ds_paths])
val_ds_order = [s.upper() for s in val_ds_type[:,0]]
val_ds_loc = [s.upper() for s in val_ds_type[:, 1]]

# generate signal type tags
signal_tags = {k : i for i, k in enumerate(np.unique(sorted([s.upper() for s in val_ds_order])))}

# load the dataset(s)

# load dataset information
specs = []
datasets = []

for path in val_ds_paths:
    print(f'loading {path}...', end=' ')

    # load dataset details
    df_spec = pd.read_csv(path, nrows=10, header=None, index_col=0, names=['info'])
    df_spec = df_spec.drop(['Version', 'DateTime', 'TimestampOffset', 'TriggerPosition', 'FastFrameID', 'IDInFastFrame', 'TotalInFastFrame'], axis=0).astype('int')

    specs.append(df_spec)

    # load data, strip unnecessary bits out
    df = pd.read_csv(path, skiprows=10, names=['I', 'Q'])
    df = df.loc[~df['I'].isin(['TimestampOffset', 'TriggerPosition', 'FastFrameID', 'IDInFastFrame', 'TotalInFastFrame'])]
    df['I'] = df['I'].astype('float')

    print(f'loaded')

    datasets.append(df)
    
print('done.')

# split dataset(s) into records, extract test dataset
processed = []

# number of test records to extract
ntest = 100
rlength = 1024

    
print(f'\nType\t\tLocation\tTotal Records\tSamples/Record')
for i in range(len(datasets)):
    nrecords = 400
    nsamples = specs[i].loc['NumberSamples']['info']
    ds_length = datasets[i].shape[0]

    # make life easier
    ds_order = val_ds_order
    ds_loc = val_ds_loc

    # sanity check
    print(f'{ds_order[i]:<13}\t{ds_loc[i]:<15}\t{nrecords:<7}\t\t{nsamples:<7}')

    # loop through dataset to split 
    for j in range(nrecords):
        # extract sample length worth of samples for each record, then transpose for easier access later
        record = datasets[i].iloc[(nsamples * j):(nsamples * (j+1))].values.T

        # pad shorter records with random padding to rlength
        if nsamples < rlength:
            # deterine pad amount
            pad_length = rlength - nsamples
            lpad_length = np.random.randint(0, pad_length+1)
            rpad_length = pad_length - lpad_length

            # generate pad
            lpad = np.zeros((2, lpad_length))
            rpad = np.zeros((2, rpad_length))

            # concatenate pad
            record = np.concatenate([lpad, record, rpad], axis=1)

        # truncate longer records to rlength
        elif nsamples > rlength:
            record = record[:,:rlength]

        # add processed record to list
        processed.append([ds_order[i], signal_tags[ds_order[i]], ds_loc[i], record])
            

# convert list into dataframes for later use, randomise, extract test records
df_test = pd.DataFrame(processed, columns=['signal_type', 'tag', 'location', 'record']).sample(frac=1, random_state=42)

# print dataset statistics
print(f'\n{"Stats":^30}')
print(f'Dataset\tLength\tRecords/Sample')
print(f'Test\t{df_test.shape[0]:<5}\t{df_test["record"].iloc[0].shape[1]}')

import json
import requests

test_data = np.concatenate(df_test.sample(3)['record'].values)
test_data = test_data.reshape((test_data.shape[0]//2, 2, 1024, 1)).tolist()

data = json.dumps({"signature_name": "serving_default", "instances": list(test_data)})
print('Data: {} ... {}'.format(data[:50], data[len(data)-52:]))

headers = {"content-type": "application/json"}
json_response = requests.post('http://localhost:8501/v1/models/resnet:predict', data=data, headers=headers)

predictions = np.argmax(json.loads(json_response.text)['predictions'], axis=1)

print(predictions)
