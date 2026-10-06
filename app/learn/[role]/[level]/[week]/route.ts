import { requireAccess } from "@/lib/access";
import coverage from "@/curriculum-v3/edition-coverage.json";
// Read the original request directly so resource selection survives bookmark redirects.
export async function GET(request:Request,{params}:{params:Promise<{role:string;level:string;week:string}>}) {
 const {role,level,week}=await params;
 if(role!=="student"&&role!=="teacher")return new Response("Not found",{status:404});
 await requireAccess(role);
 const match=coverage.find(row=>row.legacy===`${level}/${week}`);
 if(!match)return new Response("Not found",{status:404});
 const resource=new URL(request.url).searchParams.get("resource")??(role==="teacher"?"guide":"lesson");
 if(!["lesson","workbook","guide"].includes(resource)||(resource==="guide"&&role!=="teacher"))return new Response("Not found",{status:404});
 return Response.redirect(new URL(`/learn/${role}/curriculum/${match.destination}?resource=${resource}`,request.url),307);
}
