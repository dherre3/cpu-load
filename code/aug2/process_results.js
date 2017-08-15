const fs = require('fs');
var path = require('path');
const pathToDataCpu = "/Users/davidherrera/Documents/Research/cpu-loads/data/aug2/times";
const pathToWu = "/Users/davidherrera/Documents/Research/wu-wei-benchmarking-toolkit/runs";
let arrFiles = fs.readdirSync(pathToWu);
arrFiles.forEach((dir,index)=>{
    if(index!==arrFiles.length-1&&dir.indexOf("2017-08-02")!==-1)
    {
        let file = fs.readFileSync(path.join(pathToWu,dir,"run.json"));
        file = JSON.parse(file);
        let key = Object.keys(file.results);
         
        let run = file.results[key];
        let a = run.times;
        let filename = `bench=${run.benchmark['short-name']}-impl=${run.implementation['short-name']}-comp=${run.compiler['short-name']}-env=${run.environment['short-name']}-times.csv`;
        //if(fs.existsSync(filename))fs.unlinkSync(filename);
        let fullPath = path.join(pathToDataCpu,filename)
        if(!fs.existsSync(fullPath))
        {
            fs.writeFileSync(fullPath,"times\n");
        }else{
            fs.appendFileSync(fullPath,"\n");
        }
        fs.appendFileSync(fullPath, a.join(',\n'));
    }
});