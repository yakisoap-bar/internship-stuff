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



# import model
interpreter = tf.lite.Interpreter('../saved_models/sa_resnet.tflite')

# set up model
interpreter.allocate_tensors()

def predict(input_data, interpreter):
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    # output list
    output = []
    # ca = []
    # ba = []

    # print(f'Record\tMin Pred\tAvg Pred\tMax Pred\tMin Proc\tAvg Proc\tMax Proc')
    a = time.time()
    for record in input_data:

        # b = time.time()
        interpreter.set_tensor(input_details[0]['index'], record.reshape(input_details[0]['shape']))

        # c = time.time()
        interpreter.invoke()
        # ce = time.time()


        output_data = interpreter.get_tensor(output_details[0]['index'])

        output.append(output_data[0])
        # be = time.time()

        # ca.append((ce - c)*1000)
        # ba.append((be - b)*1000)

        if len(output) % 50 == 0:
            # print(f'{len(output):<7}\t{np.min(ca[-50:]):<8.3f}ms\t{np.average(ca[-50:]):<8.3f}ms\t{np.max(ca[-50:]):<8.3f}ms\t{np.min(ba[-50:]):<8.3f}ms\t{np.average(ba[-50:]):<8.3f}ms\t{np.max(ba[-50:]):<8.3f}ms\t')
            print(f'{len(output)} records predicted')

    ae = time.time()

    # print(f'Final\t{np.min(ca):<8.3f}ms\t{np.average(ca):<8.3f}ms\t{np.max(ca):<8.3f}ms\t{np.min(ba):<8.3f}ms\t{np.average(ba):<8.3f}ms\t{np.max(ba):<8.3f}ms\t')
    print(f'total time elapsed: {ae - a:.3f}s')
    return output



X_val = np.concatenate(df_test['record'].values).reshape((df_test.shape[0], 2, rlength, 1)).astype('float32')
y_val = df_test['tag'].values

preds = np.argmax(predict(X_val, interpreter), axis=1)

# model = tf.keras.models.load_model('../saved_models/SA_resnet')

# d = time.time()
# preds = np.argmax(model.predict(X_val), axis = 1)
# de = time.time()

# print(f'time taken: {de - d:.3f}s')

print(tf.math.confusion_matrix(y_val, preds, num_classes=5).numpy())