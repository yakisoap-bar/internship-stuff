# **The** Report

Done by: `Ang Yak Hng, Koh Heng Woon`
> **Disclaimer**: this document assumes proficiency/familiarity with terms in the Anaconda data science python framework and Tensorflow.

## Table of Contents

- [The Report](#the-report)
  - [Table of Contents](#table-of-contents)
  - [Literature Review](#literature-review)
    - [Existing :sparkle:_Literature_:sparkle: of Signal Classification](#existing-sparkleliteraturesparkle-of-signal-classification)
    - [Open Set](#open-set)
  - [The Radio Part](#the-radio-part)
    - [Signals](#signals)
      - [Digitally Generated Signals](#digitally-generated-signals)
  - [The AI things](#the-ai-things)
    - [The Normal AI Things](#the-normal-ai-things)
      - [_Data Importing and Processing_](#data-importing-and-processing)
      - [_ResNet using SA data_](#resnet-using-sa-data)
    - [The special AI things](#the-special-ai-things)
  - [The A P P L I C A T I O N](#the-a-p-p-l-i-c-a-t-i-o-n)
  - [Links and shit](#links-and-shit)

## Literature Review

_Files of Interest: `resnet.ipynb` | `deep_resnet.ipynb` | `hybrid_conv_imgen.ipynb` | `hybrid_conv.ipynb` | `inception_resnet.ipynb`_
> Explained/Referenced in following subsections

### Existing :sparkle:_Literature_:sparkle: of Signal Classification

### Open Set

## The Radio Part

### Signals

> Did we need to learn signal processing techniques?
> Short answer: No but we read up on it a bit at the start of the project anyways and it was cool.

The project had 2 distinct phases in terms of signals that were trained. The first used clean digitally generated signals from the DeepSig dataset. The second from live signals collected from various sources in urban environments.

#### Digitally Generated Signals

These signals [DeepSig](https://www.deepsig.ai/datasets) were digitally sent and collected using SDR's, allowing for completely clean signals without any additional noise that could interfere with the training of the model.

DeepSig sorted their frequencies by modulation type. These were:
- 8PSK
- AM-DSB
- AM-SSB
- BPSK
- CPFSK
- GFSK
- PAM4
- QAM16
- QAM64
- QPSK
- WBFM

#### Live Signals

Phase 2 had us collect actual signals live using the Tektronix RSA RSA507A Spectrum Analyzer (SA). SignalVu-PC was used to interface with the spectrum analyzer to export the data.

With Singapore being an urban environment, it's not possible to collect entirely clean signals without a faraday cage setup. However if reasonable results could be obtained from noisy signal data, it would make a real-world application more feasable. For extra measure however, noise reduction can be easily automated using Matlab's signal processing library.  

Signal name/Radio model|Center Freq|Sampled Freq Range|Modulation Type|Locations
:---|:---:|:---:|:---:|---:
Bluethooth|2.44 Ghz|40Mhz|GFSK| Office, Meeting Room, Library
Wifi (5Ghz)|5.55000 Ghz|20 Mhz|QAM
LTE (Uplink)|1.775 GHz|20 MHz|QAM/QPSK
Radio Stations|98.7 MHz<br>100.3 MHz|5 MHz|FM
Thales Manpack Fixed Frequency (TMFF) (Voice)|80 MHz<br>40 MHz|1 MHz|FM
BNET|290MHz|10 MHz|
<p align="center">Collected Signal Properties</p>

Signals were collected in more than one location to have data on different noise environments (thought this is not the most comprehensive)e In DSTA, Level 2 and 12 have different benefits for signal collection. Level 12 is ideal but we occasionally encountered transmissions on certain frequencies asides from the ones we were expecting (70Mhz had an occasional transmission when we were collecting Thales and it definitely was not a radio station.) To avoid this, Level 2 meeting rooms were less likely but it had more reflection being that it was a closed indoor room.

### A visual on the data

[](./assets/plottedIQData.png)

## AI Models

_Files of Interest: `SA_data_import.ipynb` | `SA_resnet.ipynb` | `SA_resnet_unknown.ipynb` | `model_eval.ipynb` | `SA_inception_resnet.ipynb` | `SA_openres.ipynb`_
> These will be referenced in subsections below.

### Standard AI Classification

Once we had collected all of the data needed using the SA, we moved on to training of a model for the classification. There were many models that we could use, but we decided to make use of the _ResNet_ model experimented on during the literature review as part of the `resnet.ipynb` file, as it was trained on data in the same format as our collected data while still providing accurate results, with less data pre-processing needed like in `hybrid_conv.ipynb`, which required the data to be processed into images before use. It also used records that were only 1/4 the length of our own collected data, so we thought that by increasing the length of our collected records, we could improve its accuracy.

#### _Data Importing and Processing_

To start, we needed to actually convert the files collected during data collection into a format that is usuable for model training, so we created `SA_data_import.ipynb` for developing the functions and algorithms needed to process the files. First, the correct files to open are found using Python's built-in `pathlib` library, then each file's included signal data is extracted, which contains the collected signal's information like sampling frequency, samples per record and total number of records collected. Next, the raw records are temporarily stored into a `pandas DataFrame` object, or `df`, which itself is stored in a list of other `df`s of other signal files. This process is also repeated for the separate validation datasets used for verifying model performane. The lists of signal datasets are then processed, where based on the included dataset data, the IQ data is split into smaller chunks, where it is then processed into a list. Due to model limitations, it can only accept data that is exactly 1024 samples long, thus the smaller chunks of data are either padded or truncated before being processed into a list. Additional information like signal type and location of collection are added based on the original dataset's file name. This is then concatenated into a single `train_df` and `test_df` for training and validation respectively. **The process described is used for all models trained and validated using SA data.**

#### _Model Evaluation Notebook_

For the purposes of model evaluation due to the nature of our collected data, we decided to make a dedicated notebook `model_eval.ipynb` to evaluate models in greater detail. In the notebook, a detailed breakdown of the given model is generated with metrics beyond accuracy and loss, including precision, recall, and F1 score as well. Since the training and validation data was also collected in different environments, the notebook also generates a confusion matrix that shows both an overall confusion matrix, as well as confusion matrices from the different environments the data was collected in.

#### _ResNet using SA data_

This model was the first and by far the longest-used of all the models created. Its defining feature is the extensive use of _Skip Connections_, or skipcons, where a direct connection is made between a given first layer and a given third layer, skipping the second layer entirely, allowing the model to train much more effectively despite its larger size, as it is exposed to learned gradients from further down the model.

> You can refer to the exact model structure in the `SA_resnet.ipynb` notebook, cell 18 and 19.

Originally, it was trained with only 4 signal types, Bluetooth, Wifi, LTE, and FM. But, we later added 2 more, BNET and FNET, which brought the signal count up to 6.

![SA ResNet confusion matrix](./assets/SA_resnet_confusion_matrix_eval.png)
> As seen, the model performs quite well with validation data, with only a minor overfit of FNET as Bluetooth, and Bluetooth as LTE.

The model performed well throughout the project duration, with its accuracy only dropping marginally as more data and signal types were added.

#### _Other models using SA data_

Throughout this project, we have also tested out other models with the collected data, but to little avail, as shown in the `SA_inception_resnet.ipynb` file. We tried training the models, but they would either not compile at all, costing anywhere from hours to days dedicated to debugging them, or they would not provide good performance, meaning the time spent implementing them would have gone to waste.

### Open-set AI Classification

#### _ResNet with omitted SA data_

During the development of the ResNet model, we were raised the question: _What would happen if the model was introduced to signals that it was not trained on?_ We hypothesized that the model would end up classifying the unknown signal as one of the signals it was trained on. To test this, we trained our ResNet model and omitted 2 of the 5 signal types we had collected at the time using the `SA_resnet.ipynb` notebook. After training, the model performed well with the known signal types as expected, but also exhibited our hypothesized behaviour on the unknown signals. This led us to begin research on open-set classification.

#### _Open-set ResNet with omitted SA data_

After some research, we came across a research paper [^1] that experimented on using open-set classification to detect signals from unknown transmittors, which we thought could be adapted to our own open-set problem. 

## The A P P L I C A T I O N

For better visualisation of progress ~~but really more for a cooler demo~~, the scope was expanded to develop an application that would allow for the live collection of 

### How to use
`
> Very skippable. At most just click through and find out :eyes:

### Architecture

The app went through several changes in architecture in stage of development.

#### POC

![Implementation 1](./assets/appArchitecture_1.png)

To allow for portability, 

### Using SDRs

### GUI

#### Web Version

#### PyQt

# Links, sinks, and other hijinks

[^1]: Deep Learning Approaches for Open Set Wireless
Transmitter Authorization: https://arxiv.org/pdf/2002.07777.pdf

## Future Work??