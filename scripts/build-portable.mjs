import {spawnSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';
const root=fileURLToPath(new URL('../',import.meta.url));
const run=(command,args,timeout=180000)=>{
 const result=spawnSync(command,args,{cwd:root,stdio:'inherit',timeout,killSignal:'SIGTERM',env:process.env});
 if(result.error)throw result.error;
 if(result.status!==0)process.exit(result.status??1);
};
run(process.execPath,['scripts/compile-grade6-review.mjs']);
run(process.execPath,['scripts/compile-topic-plans.mjs']);
run(process.execPath,['scripts/verify-curriculum.mjs']);
run(`${root}node_modules/.bin/vinext`,['build']);
run(process.execPath,['scripts/protect-static-assets.mjs']);
