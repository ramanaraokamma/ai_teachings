import {loadPyodide} from './python-runtime/pyodide.mjs';
const base=new URL('./python-runtime/',import.meta.url);
const pyodide=await loadPyodide({indexURL:base.protocol==='file:'?decodeURIComponent(base.pathname):base.href});
self.postMessage({type:'ready',version:pyodide.version});
self.onmessage=async ({data})=>{
 if(data.type!=='run')return;
 let output=[],errors=[],size=0;
 const capture=(target,line)=>{size+=line.length;if(size>12000)throw Error('Output limit reached; reduce printing and try a smaller trace.');target.push(line);};
 pyodide.setStdout({batched:line=>capture(output,line)});pyodide.setStderr({batched:line=>capture(errors,line)});pyodide.setStdin({error:true});
 pyodide.FS.writeFile('/home/pyodide/durations.txt','12\n8\n');pyodide.FS.writeFile('/home/pyodide/minutes.txt','12\n8\n');
 pyodide.runPython("import os\nos.chdir('/home/pyodide')");
 const globals=pyodide.runPython("dict(__name__='__main__')");
 try{const value=await pyodide.runPythonAsync(data.code,{globals});value?.destroy?.();self.postMessage({type:'result',stdout:output.join('\n'),stderr:errors.join('\n'),error:''});}
 catch(error){self.postMessage({type:'result',stdout:output.join('\n'),stderr:errors.join('\n'),error:String(error).slice(0,12000)});}
 finally{globals.destroy();}
};
