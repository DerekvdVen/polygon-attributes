// Import modules, these must be installed
const d3plus = require("d3plus")
const fs = require('fs')

// Create array for polygon coordinates to be stored in
const INPUT_FOLDER = 'data/javascript_input/'
const OUTPUT_FOLDER = 'data/javascript_output/'

// Load in data
fs.readdirSync(INPUT_FOLDER).forEach(file => {
    let polyPoints = [];
    var array = fs.readFileSync(INPUT_FOLDER + file).toString().split("\r\n");

    // Write coordinate pairs to polyPoints
    for(i in array) {
    
            small_array = array[i].split(",");
            small_array_numbered = small_array.map(Number) ;
            polyPoints.push(small_array_numbered);
        }
    
    // Set options and try to calculate lRect with 100 tries
    let rectOptions = {maxAspectRatio: 1, nTries: 100}; 
    let lRect = d3plus.largestRect(polyPoints, rectOptions);
    
    
   // If this fails, try again with 1000 tries
   if (lRect == null) {

        console.log("no output found, polygon may be too slim, more tries");
        let rectOptions = {maxAspectRatio: 1, nTries: 1000}; 
        let lRect = d3plus.largestRect(polyPoints, rectOptions);
        
        // If this fails, try again with 10000 tries, this should not fail
        if (lRect==null) {

            console.log("still not output found, more tries");
            let rectOptions = {maxAspectRatio: 1, nTries: 10000}; 
            let lRect = d3plus.largestRect(polyPoints, rectOptions);

            // Write to file
            console.log(lRect.height);
            fs.writeFile(OUTPUT_FOLDER + file, String(lRect.height),function(err){
                if (err) return console.log(err);
                    console.log('wrote file');
            });

        } else {

            // Write to file
            console.log(lRect.height);
            fs.writeFile(OUTPUT_FOLDER + file, String(lRect.height),function(err){
                if (err) return console.log(err);
                    console.log('wrote file');
            });
        };

    } else {

        // Write to file
        console.log(lRect.height);
        fs.writeFile(OUTPUT_FOLDER + file, String(lRect.height),function(err){
            if (err) return console.log(err);
                console.log('wrote file');
        });
     }
    
    

})

