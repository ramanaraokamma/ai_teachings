declare module "cloudflare:workers" {
  export const env: {
    STUDENT_PASSCODE?: string;
    TEACHER_PASSCODE?: string;
    ACADEMY_SESSION_SECRET?: string;
    ASSETS: { fetch(request: Request): Promise<Response> };
    DB: Parameters<typeof import("drizzle-orm/d1").drizzle>[0];
  };
}
