import assert from 'node:assert/strict';
import {youtubeEmbedURL} from '../lib/youtube-player.ts';
const u=new URL(youtubeEmbedURL('TjzAlY3rLg0','https://academy.test',125.5));
assert.equal(u.origin,'https://www.youtube-nocookie.com');assert.equal(u.pathname,'/embed/TjzAlY3rLg0');assert.equal(u.searchParams.get('start'),'125');assert.equal(u.searchParams.get('enablejsapi'),'1');assert.equal(u.searchParams.get('origin'),'https://academy.test');assert.equal(new URL(youtubeEmbedURL('TjzAlY3rLg0','https://academy.test',-1)).searchParams.get('start'),'0');assert.throws(()=>youtubeEmbedURL('bad','https://academy.test'));
console.log('Privacy-enhanced embed URLs, origin/JS API parameters, chapter start and invalid-ID checks passed.');
