// import stuff
const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');
const axios = require('axios');
const math = require('mathjs');

// initialise express server
const app = express();

// set up stuff
app.use(bodyParser.json({limit : '200mb'}));
app.options('*', cors());
app.use(cors());

// prediction endpoint variables
// load external variables
let config = require('./config.json');
const { index, sign } = require('mathjs');

// load signal names from file
let signalNames = config['signalNames'];
signalNames.sort();

// load frequency bands and signal type bands
let frequencyBands = config['freqBands'];
let signalBands = config['signalBands'];


// --- endpoints ---
app.get('/', (req, res) => {
    res.status(200).send({'message' : 'hello world.'});
})

// prediction endpoint
app.post('/predict', (req, res) => {
    // collected signals
    let records = req.body.data;
    let frequency = req.body.frequency;
    let filter = req.body.filter == null ? false : req.body.filter;

    // --- Error Checking ---
    // check if frequency is passed
    if (frequency == null) {
        return res.status(500).send({'message' : 'Error: Frequency not passed.'});
    };

    // check if toggle is passed


    // check if all records are valid
    if (records == null) {
        res.status(400).send({'message' : 'Error: No records found.'});
        return;
    }

    // check if array shape is valid
    shape = math.size(records);
    
    if (JSON.stringify(shape.slice(-2)) != JSON.stringify([2, 1024])) {
        return res.status(500).send({'message' : 'Error: Data is not in correct format.'});
    }
    // --- Error Checking ---

    // reshape records for prediction
    shape.push(1);
    records = math.reshape(records, shape);

    // send record for prediction
    var address = 'http://localhost:8501/v1/models/serving_model:predict';

    axios.post(address, {
        "signature_name": "serving_default", 
        "instances": records
    }).then(response => {
        // return correct results
        let predictions = response.data.predictions;
        predictions = math.mean(predictions, 0);
        let filteredSignals = [];

        // filter results based on passed frequency
        if (filter) {
            for (const [name, freq] of Object.entries(frequencyBands)) {

                // identify correct frequency band from passed frequency
                if ((freq[0] <= frequency && frequency < freq[1])) {
                    let signalsOnFreq = signalBands[name];
                    filteredSignals = signalNames.filter(s => !signalsOnFreq.includes(s))
                    
                    if (signalsOnFreq != null) {
                        // get index positions of each signal in identified frequency band from prediction result order
                        let indexPositions = signalsOnFreq.map(signal => signalNames.indexOf(signal));
    
                        // filter out any prediction not in frequency band
                        predictions = predictions.map((pred, i) => {
                            if (!indexPositions.includes(i)) {
                                return 0;
                            } else {
                                return pred;
                            }
                        })
                    }
    
                    break;
                }
            }
        }

        // return predictions
        res.status(200).send({
            'message' : 'Prediction successful.',
            'signalNames' : signalNames,
            'predictions' : predictions,
            'filtered' : filter,
            'filteredSignals' : filteredSignals
        })
    }).catch(err => {
        console.log(err);
        res.status(500).send({'message': 'Error: Prediction unsuccessful.', 'errorMsg': err.stack});
        return;
    })
})

module.exports = app;