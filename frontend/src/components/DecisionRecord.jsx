import React, { useState } from "react";

const RECORD = {
  status: "NOT APPROVED",
  decision_line: "Commit AUD 14m–19m to Western Sydney light industrial exposure, or hold. Deadline: 14 November 2026.",
  options_considered: [
    { id: "A", name: "Acquire 12 Wedgewood Rd, Eastern Creek", included: true, status: "Under consideration" },
    { id: "B", name: "Acquire 88 Links Rd, Marsden Park", included: true, status: "Under consideration" },
    { id: "C", name: "Leaseback 12 Wedgewood — no acquisition", included: true, status: "Rejected — nil capital, no acquisition exposure" },
    { id: "D", name: "Hold — re-underwrite in 12 months", included: true, status: "Under consideration — contingent on M12 rezoning uplift" },
  ],
  criteria: [
    { criterion: "Clears policy hurdle (8.15% unlevered 10yr IRR)", weight: "Gate" },
    { criterion: "Net operating income", weight: "High" },
    { criterion: "WALE", weight: "High" },
    { criterion: "Total capital deployed", weight: "Medium" },
    { criterion: "Net initial yield", weight: "Medium" },
  ],
  assumptions: [
    { assumption: "Bond rate", value: "4.65%", evidence_class: "client stated", source: "investment_policy_minute.pdf p1", changeable: true },
    { assumption: "Policy hurdle (bond + 350bps)", value: "8.15%", evidence_class: "client stated", source: "investment_policy_minute.pdf p1", changeable: false },
    { assumption: "Rent growth (base)", value: "2.5% p.a.", evidence_class: "estimate", source: "Pack assumption", changeable: true },
    { assumption: "Exit cap — Option A (base)", value: "4.55%", evidence_class: "estimate", source: "Pack assumption (entry NIY)", changeable: true },
    { assumption: "Exit cap — Option B (base)", value: "4.13%", evidence_class: "estimate", source: "Pack assumption (entry NIY)", changeable: true },
  ],
  dissent: [
    { recorded_by: "Pending", basis: "No dissent recorded yet." },
  ],
  decision_rights: "Final decision: Investment Committee. Analysis: Analyst. Pack approval: Principal.",
  open_questions: [
    "Leases for 29% of Option B passing income not in bundle — coverage gap unresolved.",
    "Outgoings recovery conflict (92% lease schedule vs 88% PM summary) — awaiting human resolution.",
    "Comparable rate of A$ 2,930/sqm has no admissible source — excluded from all calculations.",
  ],
  expected_outcome: "If Option A or B proceeds: property allocated AUD 14–19m, unlevered 10yr IRR as per sensitivity grid, no re-leasing required within WALE.",
  review_dates: [
    { months: 3, date: "14 February 2027", milestone: "Settle and confirm acquisition costs" },
    { months: 6, date: "14 May 2027", milestone: "First rent review completed" },
    { months: 12, date: "14 November 2027", milestone: "Full year income vs underwrite" },
  ],
};

const REVIEW_ACTUAL = [
  { months: 3, expected: "Settle and confirm acquisition costs", actual: null },
  { months: 6, expected: "First rent review completed", actual: null },
  { months: 12, expected: "Full year income vs underwrite", actual: null },
];

function Section({ title, children }) {
  return (
    <section className="mb-8 animate-fade-in">
      <h2 className="text-lg font-bold text-slate-800 mb-3 pb-1 border-b-2 border-slate-200">{title}</h2>
      {children}
    </section>
  );
}

export default function DecisionRecord() {
  const [showReview, setShowReview] = useState(false);

  return (
    <div className="space-y-8 animate-fade-in">
      {/* Approval stamp */}
      <div className="inline-block border-4 border-rose-600 rounded-lg px-6 py-2 text-rose-600 font-black text-xl tracking-widest uppercase rotate-2 shadow-sm mb-6">
        {RECORD.status}
      </div>

      <header>
        <h1 className="text-2xl font-bold text-slate-800 mb-2">Decision Record</h1>
        <p className="text-slate-600 text-lg font-medium">{RECORD.decision_line}</p>
      </header>

      <Section title="Options Considered (including rejected)">
        <div className="bg-white rounded shadow-sm border border-slate-200 overflow-hidden">
          <table className="w-full text-left border-collapse">
            <thead className="bg-slate-50 border-b border-slate-200">
              <tr>
                <th className="px-4 py-3 font-semibold text-slate-700 w-12">#</th>
                <th className="px-4 py-3 font-semibold text-slate-700">Option</th>
                <th className="px-4 py-3 font-semibold text-slate-700">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {RECORD.options_considered.map((o) => (
                <tr key={o.id} className="hover:bg-slate-50">
                  <td className="px-4 py-3 font-medium text-slate-600">{o.id}</td>
                  <td className="px-4 py-3 text-slate-800 font-medium">{o.name}</td>
                  <td className={`px-4 py-3 font-medium ${o.status.startsWith("Rejected") ? "text-rose-600" : "text-slate-600"}`}>
                    {o.status}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Section>

      <Section title="Criteria & Weights">
        <div className="bg-white rounded shadow-sm border border-slate-200 overflow-hidden">
          <table className="w-full text-left border-collapse">
            <thead className="bg-slate-50 border-b border-slate-200">
              <tr>
                <th className="px-4 py-3 font-semibold text-slate-700">Criterion</th>
                <th className="px-4 py-3 font-semibold text-slate-700 w-32">Weight</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {RECORD.criteria.map((c, i) => (
                <tr key={i} className="hover:bg-slate-50">
                  <td className="px-4 py-3 text-slate-700">{c.criterion}</td>
                  <td className="px-4 py-3 font-bold text-slate-800">{c.weight}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Section>

      <Section title="Assumptions">
        <div className="bg-white rounded shadow-sm border border-slate-200 overflow-hidden overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead className="bg-slate-50 border-b border-slate-200">
              <tr>
                <th className="px-4 py-3 font-semibold text-slate-700 whitespace-nowrap">Assumption</th>
                <th className="px-4 py-3 font-semibold text-slate-700 whitespace-nowrap">Value</th>
                <th className="px-4 py-3 font-semibold text-slate-700 whitespace-nowrap">Class</th>
                <th className="px-4 py-3 font-semibold text-slate-700 whitespace-nowrap">Source</th>
                <th className="px-4 py-3 font-semibold text-slate-700 whitespace-nowrap">Changeable?</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {RECORD.assumptions.map((a, i) => (
                <tr key={i} className="hover:bg-slate-50">
                  <td className="px-4 py-3 text-slate-700">{a.assumption}</td>
                  <td className="px-4 py-3 font-bold text-slate-800">{a.value}</td>
                  <td className="px-4 py-3 text-slate-600">{a.evidence_class}</td>
                  <td className="px-4 py-3 text-slate-600 italic">{a.source}</td>
                  <td className="px-4 py-3 text-slate-600">{a.changeable ? "Yes" : "No"}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Section>

      <Section title="Open Questions">
        <div className="bg-rose-50 border border-rose-200 rounded p-4 text-rose-800 space-y-2">
          {RECORD.open_questions.map((q, i) => (
            <div key={i} className="flex gap-2 items-start">
              <span className="font-bold">⚠</span>
              <p className="font-medium">{q}</p>
            </div>
          ))}
        </div>
      </Section>

      <Section title="Recorded Dissent">
        <div className="bg-slate-100 p-4 rounded text-slate-700 border border-slate-200">
          {RECORD.dissent.map((d, i) => (
            <p key={i}><strong className="text-slate-900">{d.recorded_by}:</strong> {d.basis}</p>
          ))}
        </div>
      </Section>

      <Section title="Decision Rights">
        <p className="text-slate-700 bg-white p-4 rounded shadow-sm border border-slate-200">{RECORD.decision_rights}</p>
      </Section>

      <Section title="Expected Outcome (measurable)">
        <p className="text-slate-700 bg-white p-4 rounded shadow-sm border border-slate-200">{RECORD.expected_outcome}</p>
      </Section>

      <Section title="Review Dates">
        <div className="bg-white rounded shadow-sm border border-slate-200 overflow-hidden">
          <table className="w-full text-left border-collapse">
            <thead className="bg-slate-50 border-b border-slate-200">
              <tr>
                <th className="px-4 py-3 font-semibold text-slate-700 w-16">Month</th>
                <th className="px-4 py-3 font-semibold text-slate-700 w-40">Date</th>
                <th className="px-4 py-3 font-semibold text-slate-700">Milestone</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {RECORD.review_dates.map((r) => (
                <tr key={r.months} className="hover:bg-slate-50">
                  <td className="px-4 py-3 font-bold text-slate-600">M{r.months}</td>
                  <td className="px-4 py-3 text-slate-700">{r.date}</td>
                  <td className="px-4 py-3 text-slate-800">{r.milestone}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Section>

      {/* Expected vs Actual review */}
      <section className="pt-4 border-t border-slate-200">
        <button
          onClick={() => setShowReview(!showReview)}
          className="px-5 py-2 bg-slate-800 hover:bg-slate-700 text-white rounded shadow-sm font-semibold transition-colors mb-6"
        >
          {showReview ? "Hide" : "Show"} Expected vs Actual Review
        </button>
        
        {showReview && (
          <div className="bg-white rounded shadow-sm border border-slate-200 p-6 animate-fade-in">
            <h3 className="font-bold text-slate-800 text-lg mb-4">Expected vs Actual</h3>
            <div className="overflow-x-auto border border-slate-200 rounded">
              <table className="w-full text-left border-collapse">
                <thead className="bg-slate-50 border-b border-slate-200">
                  <tr>
                    <th className="px-4 py-3 font-semibold text-slate-700">Milestone</th>
                    <th className="px-4 py-3 font-semibold text-slate-700">Expected</th>
                    <th className="px-4 py-3 font-semibold text-slate-700">Actual</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100">
                  {REVIEW_ACTUAL.map((r) => (
                    <tr key={r.months} className="hover:bg-slate-50">
                      <td className="px-4 py-3 font-bold text-slate-600">M{r.months}</td>
                      <td className="px-4 py-3 text-slate-800">{r.expected}</td>
                      <td className="px-4 py-3 text-slate-400 italic font-medium">{r.actual ?? "Not yet reviewed"}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}
      </section>
    </div>
  );
}
