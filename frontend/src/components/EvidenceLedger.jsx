import React, { useEffect, useState } from "react";

const STATUS_COLORS = {
  "verified": "#059669",
  "conflict": "#dc2626",
  "no source": "#9ca3af",
  "coverage gap": "#f59e0b",
  "unverified": "#f59e0b",
};

const FIXTURE = [
  { id: "ev1", metric: "Passing income — Option A", value: 795200, unit: "AUD/yr", source: "independent_valuation.pdf", page: 4, evidence_class: "measured", status: "verified" },
  { id: "ev2", metric: "Passing income — Option B", value: 963900, unit: "AUD/yr", source: "lease_schedule_rent_roll.pdf", page: 3, evidence_class: "measured", status: "verified" },
  { id: "ev3", metric: "Unrecovered outgoings — Option A", value: 18560, unit: "AUD/yr", source: "property_manager_annual_summary.pdf", page: 2, evidence_class: "measured", status: "verified" },
  { id: "ev4", metric: "Unrecovered outgoings — Option B", value: 36120, unit: "AUD/yr", source: "property_manager_annual_summary.pdf", page: 2, evidence_class: "measured", status: "verified" },
  { id: "ev5", metric: "Land tax — Option A", value: 78000, unit: "AUD/yr", source: "portfolio_treasury_schedule.pdf", page: 1, evidence_class: "client stated", status: "verified" },
  { id: "ev6", metric: "Land tax — Option B", value: 96000, unit: "AUD/yr", source: "portfolio_treasury_schedule.pdf", page: 1, evidence_class: "client stated", status: "verified" },
  { id: "ev7", metric: "Capex — Option A", value: 250000, unit: "AUD", source: "contract_summary.pdf", page: 8, evidence_class: "estimate", status: "verified" },
  { id: "ev8", metric: "Capex — Option B", value: 0, unit: "AUD", source: "contract_summary.pdf", page: 12, evidence_class: "measured", status: "verified" },
  { id: "ev9", metric: "Comparable rate (Eastern Creek)", value: 2930, unit: "AUD/sqm", source: null, page: null, evidence_class: null, status: "no source" },
  { id: "ev10", metric: "Outgoings recovery (lease schedule)", value: 0.92, unit: "ratio", source: "lease_schedule_rent_roll.pdf", page: 5, evidence_class: "measured", status: "conflict" },
  { id: "ev11", metric: "Outgoings recovery (PM summary)", value: 0.88, unit: "ratio", source: "property_manager_annual_summary.pdf", page: 2, evidence_class: "measured", status: "conflict" },
  { id: "ev12", metric: "Option B passing income — unsourced portion", value: 279531, unit: "AUD/yr", source: null, page: null, evidence_class: null, status: "coverage gap" },
  { id: "ev13", metric: "Bond rate (pack assumption)", value: 0.0465, unit: "%", source: "investment_policy_minute.pdf", page: 1, evidence_class: "client stated", status: "verified" },
];

export default function EvidenceLedger() {
  const [rows, setRows] = useState([]);
  const [apiError, setApiError] = useState(null);
  const [selected, setSelected] = useState(null);

  useEffect(() => {
    fetch("/api/evidence")
      .then((r) => r.json())
      .then((data) => {
        if (Array.isArray(data) && data.length > 5) setRows(data);
        else { setRows(FIXTURE); setApiError("Backend data incomplete — showing fixture data."); }
      })
      .catch(() => { setRows(FIXTURE); setApiError("Backend not available — showing fixture data."); });
  }, []);

  return (
    <div className="space-y-6 animate-fade-in">
      <div>
        <h1 className="text-2xl font-bold text-slate-800 mb-2">Evidence Ledger</h1>
        {apiError && <p className="text-rose-500 text-sm italic mb-3">{apiError}</p>}
        <p className="text-slate-600">
          Every figure has a ledger row. Unverified and conflicted figures are <strong className="text-slate-800">excluded from all calculations</strong> until a human resolves them.
        </p>
      </div>

      <div className="bg-white rounded shadow-sm border border-slate-200 overflow-x-auto">
        <table className="w-full text-left border-collapse">
          <thead className="bg-slate-50 border-b border-slate-200">
            <tr>
              <th className="px-4 py-3 font-semibold text-slate-700 whitespace-nowrap">Metric</th>
              <th className="px-4 py-3 font-semibold text-slate-700 whitespace-nowrap">Value</th>
              <th className="px-4 py-3 font-semibold text-slate-700 whitespace-nowrap">Unit</th>
              <th className="px-4 py-3 font-semibold text-slate-700 whitespace-nowrap">Source Document</th>
              <th className="px-4 py-3 font-semibold text-slate-700 whitespace-nowrap">Page</th>
              <th className="px-4 py-3 font-semibold text-slate-700 whitespace-nowrap">Class</th>
              <th className="px-4 py-3 font-semibold text-slate-700 whitespace-nowrap">Status</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100">
            {rows.map((ev) => {
              const isSelected = selected?.id === ev.id;
              
              // Dynamic status color
              let statusColor = "text-slate-700";
              if (ev.status === "verified") statusColor = "text-emerald-600";
              if (ev.status === "conflict") statusColor = "text-rose-600";
              if (ev.status === "no source") statusColor = "text-slate-400";
              if (ev.status === "coverage gap" || ev.status === "unverified") statusColor = "text-amber-500";

              return (
                <tr
                  key={ev.id}
                  className={`cursor-pointer transition-colors ${isSelected ? "bg-blue-50" : "hover:bg-slate-50"}`}
                  onClick={() => setSelected(ev)}
                >
                  <td className="px-4 py-3 text-slate-700 align-top">{ev.metric}</td>
                  <td className="px-4 py-3 align-top">
                    {ev.value != null ? (
                      <span className="font-medium text-slate-800">{ev.value.toLocaleString()}</span>
                    ) : (
                      <span className="text-rose-600 font-bold text-sm">NOT SOURCED</span>
                    )}
                  </td>
                  <td className="px-4 py-3 text-slate-500 align-top">{ev.unit ?? "—"}</td>
                  <td className="px-4 py-3 text-slate-600 align-top">{ev.source ?? <span className="text-slate-400">—</span>}</td>
                  <td className="px-4 py-3 text-slate-500 align-top">{ev.page ?? "—"}</td>
                  <td className="px-4 py-3 text-slate-500 align-top">{ev.evidence_class ?? "—"}</td>
                  <td className={`px-4 py-3 font-bold text-xs uppercase tracking-wider align-top ${statusColor}`}>
                    {ev.status}
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>

      {selected && (
        <div className="mt-8 p-5 border border-blue-200 bg-blue-50 rounded-lg shadow-sm">
          <p className="text-slate-800 font-medium text-lg mb-2"><strong className="text-blue-900">Selected figure:</strong> {selected.metric}</p>
          
          {selected.source ? (
            <p className="text-slate-700">Source: <strong className="text-slate-900">{selected.source}</strong>{selected.page ? `, page ${selected.page}` : ""}</p>
          ) : (
            <p className="text-rose-600 font-medium">⚠ No admissible source — excluded from all calculations.</p>
          )}
          
          {selected.status === "conflict" && (
            <p className="mt-2 text-rose-600 font-medium">⚠ CONFLICT — two sources disagree. A human resolution is required before this figure enters any calculation.</p>
          )}
          
          {selected.status === "coverage gap" && (
            <p className="mt-2 text-amber-600 font-medium">⚠ COVERAGE GAP — this portion of income has no supporting lease documentation. It is excluded and marked, not estimated.</p>
          )}
          
          <button
            onClick={() => setSelected(null)}
            className="mt-4 px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded shadow transition-colors"
          >
            Close Panel
          </button>
        </div>
      )}
    </div>
  );
}
