/**
 *  * Created by David Herrera on 2017-07-12.
 */
const shell = require('shelljs');
const os = require('os');
const mathjs = require('mathjs');
function runner() {
    return new Promise((resolve,reject)=>{
        let total = [];
        let meanCpu = null;
        let jsonOutput = null;
        console.log('start');
        const child_cpu = shell.exec('node ./cpu-collector.js', {async: true, silent: true});
        const child_runner = shell.exec('node ./timeout.js',{async: true, silent: true});

        child_runner.stdout.on('data',function(data)
        {
            child_cpu.kill();

            jsonOutput = data;
            console.log('Done running child');
        });
        child_cpu.stdout.on('data', function (data) {
            let val = data.split("\n");
            val.splice(total.length - 1, 1);
            val = val.map(Number);
            total.push(val);
        });
        child_cpu.on('close',function()
        {
            console.log('on close');
            meanCpu = mathjs.mean(total).toFixed(2);
            //console.log(`Mean CPU: ${meanCpu}, Total Number of Measurements: ${total.length}`);
            resolve({cpuMean:Number(meanCpu),output:jsonOutput});
        });

    });

    // if (shell.exec('node ./timeout.js').code !== 1) {
    //     //child.kill();
    //     clearInterval(inter);
    //
    //
    // }
}


function main()
{
    return new Promise(async function(resolve,reject)
    {
        //let promise = [];
        let i = 0;
        let results = [];
        while(i<10)
        {
            console.log(`----- ITERATION ${i}-------`);
            let res = await runner();
            //promise.push(runner());
            results.push(res);
            console.log(res);
            i++;
        }
        resolve(results);
    });


   // return Promise.resolve(res);
    // Promise.all(promise).then((results)=>{
    //     console.log(results);
    // });

}
main().then(function(res)
{
    console.log(res);
}).catch(function(err)
{
    console.log(err);
});



function listenerCpuLoad(child)
{
    return new Promise((resolve)=>{
        let total = [];

    });

}
