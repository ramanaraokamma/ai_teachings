/** Cloudflare Worker entry point for the vinext-starter template. */
import handler from "vinext/server/app-router-entry";

interface Env {
  ASSETS: { fetch(request: Request): Promise<Response> };
  IMAGES: {
    input(stream: ReadableStream): {
      transform(options: Record<string, unknown>): {
        output(options: { format: string; quality: number }): Promise<{ response(): Response }>;
      };
    };
  };
}

interface ExecutionContext {
  waitUntil(promise: Promise<unknown>): void;
  passThroughOnException(): void;
}

// Image security config. SVG sources with .svg extension auto-skip the
// optimization endpoint on the client side (served directly, no proxy).
// To route SVGs through the optimizer (with security headers), set
// dangerouslyAllowSVG: true in next.config.js and uncomment below:
// const imageConfig: ImageConfig = { dangerouslyAllowSVG: true };

const worker = {
  async fetch(request: Request, env: Env, ctx: ExecutionContext): Promise<Response> {
    const url = new URL(request.url);

    // Protected resources never pass through the unauthenticated optimizer.
    if (url.pathname === "/_vinext/image" || url.pathname.startsWith("/academy-art/")) return new Response("Not found", { status: 404 });

    const original = await handler.fetch(request, env, ctx);
    const response = new Response(original.body, original);
    response.headers.set("X-Academy-Edition", "grade6-entry-2026-09-14");
    if (url.pathname.startsWith("/learn/") || url.pathname.startsWith("/api/")) {
      const protectedResponse = new Response(response.body, response);
      protectedResponse.headers.set("Cache-Control", "private, no-store");
      protectedResponse.headers.set("Vary", "Cookie");
      return protectedResponse;
    }
    return response;
  },
};

export default worker;
