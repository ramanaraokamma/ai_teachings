// Create local-only sign-in configuration without replacing existing settings.
import { access, writeFile } from 'node:fs/promises';
import { randomBytes } from 'node:crypto';
try { await access('.dev.vars'); console.log('Existing .dev.vars kept.'); }
catch(error) {
 if(error.code !== 'ENOENT')throw error;
 await writeFile('.dev.vars',`STUDENT_PASSCODE=student1234\nTEACHER_PASSCODE=teacher1234\nACADEMY_SESSION_SECRET=${randomBytes(32).toString('hex')}\n`,{flag:'wx',mode:0o600});
 console.log('Local student and teacher sign-in configured. Run npm run dev.');
}
