import React, { useEffect, useState } from "react";

const FIXTURE = {
  decision_line: "Commit AUD 14m–19m to one of four Western Sydney light industrial options, or hold. Deadline: 14 November 2026.",
  policy_hurdle: "8.15% unlevered 10yr IRR (bond 4.65% + 350 bps)",
  standing_question: "Are leases for the remaining 29% of Option B's passing income available?",
  coverage_pct: 71,
  documents: [
    { name: "contract_summary.pdf", pages: 24, status: "ADMISSIBLE" },
    { name: "independent_valuation.pdf", pages: 12, status: "ADMISSIBLE" },
    { name: "lease_schedule_rent_roll.pdf", pages: 9, status: "ADMISSIBLE" },
    { name: "property_manager_annual_summary.pdf", pages: 6, status: "ADMISSIBLE" },
    { name: "investment_policy_minute.pdf", pages: 2, status: "ADMISSIBLE" },
    { name: "portfolio_treasury_schedule.pdf", pages: 3, status: "ADMISSIBLE" },
    { name: "desktop_valuation_note.pdf", pages: null, status: "REJECTED — unsigned, undated, no page refs" },
  ],
};

export default function IntakeView() {
  const [data, setData] = useState(null);
  const [apiError, setApiError] = useState(null);

  useEffect(() => {
    fetch("/api/decision-pack")
      .then((r) => r.json())
      .then(setData)
      .catch(() => setApiError("Backend not available — showing fixture data."));
  }, []);

  const view = data && data.documents ? data : FIXTURE;

  return (
    <div className="space-y-8 animate-fade-in">
      {/* Standing Question Banner */}
      <div className="bg-amber-50 border-l-4 border-amber-500 rounded-r shadow-sm p-5">
        <strong className="text-amber-700 uppercase tracking-wider text-xs font-bold mb-1 block">Standing Question for Principal</strong>
        <p className="text-amber-900 font-medium">{view.standing_question}</p>
      </div>

      <section>
        <h2 className="text-xl font-bold text-slate-800 mb-2 border-b border-slate-200 pb-2">Decision</h2>
        <p className="text-lg text-slate-700 font-medium">{view.decision_line}</p>
        <p className="text-slate-600 mt-2"><strong className="text-slate-800">Policy Hurdle:</strong> {view.policy_hurdle}</p>
      </section>

      {apiError && <p className="text-rose-500 text-sm italic">{apiError}</p>}

      <section>
        <h2 className="text-xl font-bold text-slate-800 mb-4 border-b border-slate-200 pb-2">Document Bundle</h2>
        <div className="bg-white rounded shadow-sm border border-slate-200 overflow-hidden">
          <table className="w-full text-left border-collapse">
            <thead className="bg-slate-50 border-b border-slate-200">
              <tr>
                <th className="px-4 py-3 font-semibold text-slate-700">Document</th>
                <th className="px-4 py-3 font-semibold text-slate-700">Pages</th>
                <th className="px-4 py-3 font-semibold text-slate-700">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {view.documents.map((doc) => (
                <tr key={doc.name} className="hover:bg-slate-50">
                  <td className="px-4 py-3 text-slate-700">{doc.name}</td>
                  <td className="px-4 py-3 text-slate-500">{doc.pages ?? "—"}</td>
                  <td className={`px-4 py-3 font-bold text-sm ${doc.status === "ADMISSIBLE" ? "text-emerald-600" : "text-rose-600"}`}>
                    {doc.status}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>

      <section>
        <h2 className="text-xl font-bold text-slate-800 mb-4 border-b border-slate-200 pb-2">Coverage Meter</h2>
        <div className="w-full max-w-md bg-slate-200 rounded-full h-6 overflow-hidden shadow-inner">
          <div 
            className={`h-full flex items-center justify-center text-white text-xs font-bold transition-all duration-500 ${view.coverage_pct < 80 ? "bg-amber-500" : "bg-emerald-600"}`}
            style={{ width: `${view.coverage_pct}%` }}
          >
            {view.coverage_pct}% verified
          </div>
        </div>
      </section>
    </div>
  );
}
