"use client";
import { Printer } from "lucide-react";
export function PrintResource() {
  return <button type="button" className="resource-action" onClick={() => window.print()}><Printer aria-hidden="true" />Print this resource</button>;
}
