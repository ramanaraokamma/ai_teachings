import Link from "next/link";
import {notFound} from "next/navigation";
import {requireAccess} from "@/lib/access";
import {PortalHeader} from "@/components/portal-header";
import {PilotStudio} from "@/components/pilot-studio";
import tracks from "@/lib/pilot-data.json";
import type {PilotTrack} from "@/lib/learning/pilot";
export const dynamic="force-dynamic";
export default async function PilotPage({params}:{params:Promise<{role:string}>}){const{role}=await params;if(role!=="teacher")notFound();const sessionRole=await requireAccess('teacher');return <main className="portal-page"><PortalHeader mode="teacher" sessionRole={sessionRole}/><section className="classroom-panel" id="main-content" tabIndex={-1}><Link href="/learn/teacher">Back to teaching studio</Link><h1>Classroom pilot studio</h1><p>Prepare a lesson, observe real learners and use their evidence to improve the programme.</p></section><PilotStudio tracks={tracks as PilotTrack[]}/></main>;}
