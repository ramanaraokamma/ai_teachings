// Bind local fixtures to the compiled worker's env import for Node integration tests.
// This does not emulate workerd limits or Cloudflare deployment wiring.
export async function resolve(specifier, context, nextResolve) {
  if (specifier === 'cloudflare:workers') return {url:new URL('./cloudflare-env.mjs',import.meta.url).href,shortCircuit:true};
  return nextResolve(specifier,context);
}
