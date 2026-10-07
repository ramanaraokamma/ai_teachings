import { redirect, notFound } from "next/navigation";
export default async function Page({params}:{params:Promise<{role:string;level:string;week:string}>}) {const {role,level,week}=await params;if(role!=="student"&&role!=="teacher")notFound();redirect(`/learn/${role}/${level}/${week}`);}
