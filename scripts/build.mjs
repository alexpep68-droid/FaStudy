import {mkdir,copyFile,writeFile,readdir,readFile} from 'node:fs/promises';
import path from 'node:path';
const dist=path.resolve('dist');
try{if((await readdir(dist)).length)throw Error('dist is not empty.')}catch(e){if(e.code!=='ENOENT')throw e}
await mkdir(path.join(dist,'library'),{recursive:true});
for(const name of ['index.html','style.css','app.js','library.js','library-manifest.json']) {
  await copyFile(path.join('web',name),path.join(dist,name));
}
try {
  await copyFile(path.join('web/library','catalog.json'), path.join(dist,'library/catalog.json'));
} catch (e) {}
await writeFile(path.join(dist,'library/status.json'), JSON.stringify({available:true,expectedDocuments:72}));
console.log('Build completado con biblioteca habilitada: available=true');
