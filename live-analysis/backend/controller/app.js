// import stuff
const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');
const axios = require('axios');
const math = require('mathjs');

// initialise express server
const app = express();

// set up stuff
app.use(bodyParser.json());
app.options('*', cors());
app.use(cors());

// endpoints
app.get('/', (req, res) => {
    res.status(200).send({'message' : 'hello world.'});
})

// prediction endpoint
app.post('/predict', (req, res) => {
    // collected signals
    records = req.body.data;

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

    // reshape records for prediction
    shape.push(1);
    records = math.reshape(records, shape);

    // send record for prediction
    var address = 'http://localhost:8501/v1/models/resnet:predict';

    axios.post(address, {
        "signature_name": "serving_default", 
        "instances": records
    }).then(response => {
        // return correct results
        predictions = response.data.predictions;

        // load signal names from file
        var signalNames = require('./signalNames.json');
        signalNames.sort();

        // return predictions
        res.status(200).send({
            'message' : 'Prediction successful.',
            'signalNames' : signalNames,
            'predictions' : predictions
        })
    }).catch(err => {
        console.log(err);
        res.status(500).send({'message': 'Error: Prediction unsuccessful.', 'errorMsg': err.stack});
        return;
    })
})

module.exports = app;