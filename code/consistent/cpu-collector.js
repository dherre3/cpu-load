/**
 *  * Created by David Herrera on 2017-07-12.
 */
const os = require('os');

//Module API
module.exports =
{
    collectData: collectData,
    totalCpuTimeTicks:totalCpuTimeTicks,
    computeMeanCpu:computeMeanCpu,
    collectDataInterval:collectDataInterval
};

collectData();

//@Flow
function collectData()
{
        let current = totalCpuTimeTicks();
        let prev = null;
        setInterval(()=>{
            if(prev!=null) console.log(computeMeanCpu(current, prev));
            prev = current;
            current = totalCpuTimeTicks();
        },300);
}
function collectDataInterval(arr)
{
    let current = totalCpuTimeTicks();
    let prev = null;
    let iter = setInterval(()=>{
        console.log(arr);
        if(prev!=null) console.log(computeMeanCpu(current, prev));
        if(prev!=null)arr.push(computeMeanCpu(current, prev));
        prev = current;
        current = totalCpuTimeTicks();
    },100);
    return iter;
}


function totalCpuTimeTicks() {

    //Initialise sum of idle and time of cores and fetch CPU info
    var totalIdle = 0, totalTick = 0;
    var cpus = os.cpus();

    //Loop through CPU cores
    for(var i = 0, len = cpus.length; i < len; i++) {

        //Select CPU core
        var cpu = cpus[i];

        //Total up the time in the cores tick
        for(type in cpu.times) {
            totalTick += cpu.times[type];
        }

        //Total up the idle time of the core
        totalIdle += cpu.times.idle;
    }

    //Return the average Idle and Tick times
    return {idle: totalIdle / cpus.length,  total: totalTick / cpus.length};
}

function computeMeanCpu(start,end)
{
    //Calculate the difference in idle and total time between the measures
    let idleDifference = end.idle - start.idle;
    let totalDifference = end.total - start.total;
    //Calculate the average percentage CPU usage
    let percentageCPU = 100 - (100 * idleDifference / totalDifference);
    return Number(percentageCPU.toFixed(2));

}


// class CpuTimings
// {
//     total = [];
//     collectData()
//     {
//         let current = this.totalCpuTimeTicks();
//         let prev = null;
//         setInterval(()=>{
//             if(prev!=null)
//             {
//                 this.total.push(this.computeMeanCpu(current,prev));
//                 console.log(this.computeMeanCpu(current,prev));
//             }
//
//             prev = current;
//             current = this.totalCpuTimeTicks();
//
//         },200);
//     }
//     constructor()
//     {
//         this.total = [];
//         collectData();
//     }
//
//     totalCpuTimeTicks()
//     {
//         //Initialise sum of idle and time of cores and fetch CPU info
//         var totalIdle = 0, totalTick = 0;
//         var cpus = os.cpus();
//
//         //Loop through CPU cores
//         for(var i = 0, len = cpus.length; i < len; i++) {
//
//             //Select CPU core
//             var cpu = cpus[i];
//
//             //Total up the time in the cores tick
//             for(type in cpu.times) {
//                 totalTick += cpu.times[type];
//             }
//
//             //Total up the idle time of the core
//             totalIdle += cpu.times.idle;
//         }
//
//         //Return the average Idle and Tick times
//         return {idle: totalIdle / cpus.length,  total: totalTick / cpus.length};
//     }
//     computeMeanCpu(start,end) {
//         //Calculate the difference in idle and total time between the measures
//         var idleDifference = end.idle - start.idle;
//         var totalDifference = end.total - start.total;
//         //Calculate the average percentage CPU usage
//         var percentageCPU = 100 - (100 * idleDifference / totalDifference);
//         return Number(percentageCPU.toFixed(2));
//     }
//
// }
// const cpu = new CpuTimings();
// cpu.collectData();