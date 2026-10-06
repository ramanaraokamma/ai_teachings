import { ArrowRight, BookOpen, GraduationCap, LockKeyhole, Orbit, ShieldCheck, Sparkles } from "lucide-react";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

export const dynamic = "force-dynamic";

function AccessCard({ role, highlighted }: { role: "student" | "teacher"; highlighted?: boolean }) {
  const student = role === "student";
  const Icon = student ? GraduationCap : BookOpen;
  return (
    <section className={`access-card ${highlighted ? "access-card-highlighted" : ""}`} id={`${role}-access`}>
      <div className="access-card-heading"><span className={`access-icon access-${role}`}><Icon aria-hidden="true" /></span><div><p>{student ? "Learn & practice" : "Plan & teach"}</p><h2>{student ? "Student access" : "Teacher access"}</h2></div></div>
      <form action="/api/access" method="post" className="access-form">
        <input type="hidden" name="role" value={role} />
        <label htmlFor={`${role}-passcode`}>Passcode</label>
        <div className="passcode-row"><Input id={`${role}-passcode`} name="passcode" type="password" required autoComplete="current-password" placeholder="Enter passcode" /><Button type="submit" aria-label={`Enter ${role} mode`}><ArrowRight aria-hidden="true" /></Button></div>
      </form>
    </section>
  );
}

export default async function Home({ searchParams }: { searchParams: Promise<{ access?: string; role?: string }> }) {
  const query = await searchParams;
  const hasError = query.access === "incorrect" || query.access === "required";
  return (
    <main className="landing-page">
      <nav className="landing-nav"><div className="brand brand-light"><span className="brand-mark"><Sparkles aria-hidden="true" /></span><span><strong>AI Academy</strong><small>Grades 6–12 · Seven levels</small></span></div><div className="private-label"><LockKeyhole aria-hidden="true" /> Protected learning portal</div></nav>
      <div className="landing-shell">
        <section className="landing-story">
          <p className="eyebrow"><Orbit aria-hidden="true" /> From curiosity to capable creation</p>
          <h1>Curious minds.<br />Confident creators.</h1>
          <p className="landing-intro">Follow one seven-level pathway through foundations, Python and data, machine learning, neural networks, generative AI, engineering and research. Each level has 36 weeks with student lessons, practice and teacher guidance. Placement follows demonstrated readiness.</p>
          <div className="pathway-visual" aria-label="Seven connected learning levels">{["Foundations", "Python & data", "Machine learning", "Neural networks", "Generative AI", "AI engineering", "Research"].map((label, index) => <div className={`pathway-line pathway-${index + 1}`} key={label}><span>{index + 1}</span><p>{label}</p><i aria-hidden="true" /></div>)}</div>
          <div className="trust-line"><ShieldCheck aria-hidden="true" /><span>Learning materials stay hidden until the correct role passcode is entered.</span></div>
        </section>
        <section className="access-panel" aria-label="Choose access mode">
          <div className="access-panel-heading"><p>Choose your space</p><h2>Enter the academy</h2></div>
          {hasError && <div className="access-error" role="alert">{query.access === "incorrect" ? "That passcode didn’t match. Please try again." : "Enter the appropriate passcode to continue."}</div>}
          <AccessCard role="student" highlighted={query.role === "student" && hasError} />
          <AccessCard role="teacher" highlighted={query.role === "teacher" && hasError} />
        </section>
      </div>
      <footer className="landing-footer"><span>AI Academy · Grades 6–12 · Complete seven-level pathway</span><span>Learn deeply. Build responsibly.</span></footer>
    </main>
  );
}
