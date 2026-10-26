import {mkdir,copyFile,writeFile,readdir,readFile} from 'node:fs/promises';
import path from 'node:path';
const dist=path.resolve('dist');
// Never reuse a deployment output that may contain a private corpus.
try{if((await readdir(dist)).length)throw Error('dist is not empty. Use a fresh build checkout to prevent accidental corpus publication.')}catch(e){if(e.code!=='ENOENT')throw e}
await mkdir(path.join(dist,'library'),{recursive:true});
for(const name of ['index.html','style.css','app.js','library.js'])await copyFile(path.join('web',name),path.join(dist,name));
await writeFile(path.join(dist,'library/status.json'),JSON.stringify({available:false,expectedDocuments:72}));
console.log('Built application without PDF or extracted text. The fixed library remains unavailable until separately approved.');
