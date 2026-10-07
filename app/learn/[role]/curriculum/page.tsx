import { redirect, notFound } from "next/navigation";
export default async function Page({params}:{params:Promise<{role:string}>}) {const {role}=await params;if(role!=="student"&&role!=="teacher")notFound();redirect(`/learn/${role}`);}
