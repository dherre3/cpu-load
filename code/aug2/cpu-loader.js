const shelljs = require('shelljs');
let i = 0;
while(true)
{
   let res = shelljs.exec("./builds/a86ca5e4587a9d1f1752f72749fe8060784c1ddb/runner 10000000",{silent:true});
   console.log(i, res.stdout);
   i++;
}