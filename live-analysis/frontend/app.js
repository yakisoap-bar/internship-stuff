// Loading dotenv 
require('dotenv').config();

// Importing express and app
const express = require('express');
const app = express();

// Making public folder to host
app.use(express.static('public'));

// Start server on port
const PORT = process.env.PORT;
app.listen(PORT, function(err){
    console.log(`Public Hosting frontend is listening on port: ${PORT}`);
});