import React, { useState } from "react";

const OPTIONS = [
  { id: "A", name: "Acquire 12 Wedgewood", cost: 14450000, noi: 657640, niy: "4.55%", wale: "3.4" },
  { id: "B", name: "Acquire 88 Links Rd", cost: 18900000, noi: 779780, niy: "4.13%", wale: "6.1" },
  { id: "C", name: "Leaseback 12 Wedgewood", cost: null, noi: null, niy: null, wale: null },
  { id: "D", name: "Hold", cost: null, noi: null, niy: null, wale: null },
];

const SENSITIVITY = {
  A: [
    { cap: "4.05%", r15: "7.03%", r25: "8.04%", r35: "9.05%" },
    { cap: "4.55% (base)", r15: "6.05%", r25: "7.05%", r35: "8.05%" },
    { cap: "5.05%", r15: "5.20%", r25: "6.19%", r35: "7.18%" },
  ],
  B: [
    { cap: "3.63%", r15: "6.73%", r25: "7.74%", r35: "8.76%" },
    { cap: "4.13% (base)", r15: "5.63%", r25: "6.63%", r35: "7.63%" },
    { cap: "4.63%", r15: "4.67%", r25: "5.66%", r35: "6.65%" },
  ]
};

export default function OptionsSensitivity() {
  const [activeSens, setActiveSens] = useState("A");
  const gridData = SENSITIVITY[activeSens];

  return (
    <div className="space-y-8 animate-fade-in">
      {/* Policy Hurdle Banner */}
      <div className="bg-rose-50 border-l-4 border-rose-600 rounded-r shadow-sm p-5">
        <strong className="text-rose-800 uppercase tracking-wider text-xs font-bold mb-1 block">Policy Verdict</strong>
        <p className="text-rose-900 font-medium">On base assumptions neither acquisition clears the 8.15% policy hurdle unlevered over ten years. A is stronger on income, B on WALE. The pack does not say which to choose.</p>
      </div>

      <section>
        <h2 className="text-xl font-bold text-slate-800 mb-4 border-b border-slate-200 pb-2">Options Computed</h2>
        <div className="bg-white rounded shadow-sm border border-slate-200 overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead className="bg-slate-50 border-b border-slate-200">
              <tr>
                <th className="px-4 py-3 font-semibold text-slate-700 whitespace-nowrap">#</th>
                <th className="px-4 py-3 font-semibold text-slate-700 whitespace-nowrap">Option</th>
                <th className="px-4 py-3 font-semibold text-slate-700 whitespace-nowrap">Total Cost</th>
                <th className="px-4 py-3 font-semibold text-slate-700 whitespace-nowrap">NOI</th>
                <th className="px-4 py-3 font-semibold text-slate-700 whitespace-nowrap">NIY</th>
                <th className="px-4 py-3 font-semibold text-slate-700 whitespace-nowrap">WALE</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {OPTIONS.map((opt) => (
                <tr key={opt.id} className="hover:bg-slate-50">
                  <td className="px-4 py-3 text-slate-700 font-medium">{opt.id}</td>
                  <td className="px-4 py-3 text-slate-800 font-medium">{opt.name}</td>
                  <td className="px-4 py-3 text-slate-600">{opt.cost != null ? opt.cost.toLocaleString() : "nil"}</td>
                  <td className="px-4 py-3 text-slate-600">{opt.noi != null ? opt.noi.toLocaleString() : "n/a"}</td>
                  <td className="px-4 py-3 text-slate-600">{opt.niy ?? "n/a"}</td>
                  <td className="px-4 py-3 text-slate-600">{opt.wale ?? "n/a"}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>

      <section>
        <div className="flex items-center justify-between mb-4 border-b border-slate-200 pb-2">
          <h2 className="text-xl font-bold text-slate-800">Sensitivity Grid (Unlevered 10yr IRR)</h2>
          <div className="flex bg-slate-200 rounded p-1">
            <button
              onClick={() => setActiveSens("A")}
              className={`px-4 py-1.5 rounded text-sm font-bold transition-colors ${activeSens === "A" ? "bg-white text-blue-600 shadow-sm" : "text-slate-600 hover:text-slate-800"}`}
            >
              Option A
            </button>
            <button
              onClick={() => setActiveSens("B")}
              className={`px-4 py-1.5 rounded text-sm font-bold transition-colors ${activeSens === "B" ? "bg-white text-blue-600 shadow-sm" : "text-slate-600 hover:text-slate-800"}`}
            >
              Option B
            </button>
          </div>
        </div>

        <div className="bg-white rounded shadow-sm border border-slate-200 overflow-x-auto">
          <table className="w-full text-left border-collapse text-center">
            <thead className="bg-slate-50 border-b border-slate-200">
              <tr>
                <th className="px-4 py-3 font-semibold text-slate-700 text-left">Exit Cap</th>
                <th className="px-4 py-3 font-semibold text-slate-700">Rent 1.5%</th>
                <th className="px-4 py-3 font-semibold text-slate-700">Rent 2.5%</th>
                <th className="px-4 py-3 font-semibold text-slate-700">Rent 3.5%</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {gridData.map((row, i) => (
                <tr key={i} className="hover:bg-slate-50">
                  <td className="px-4 py-3 font-medium text-slate-700 text-left">{row.cap}</td>
                  <td className={`px-4 py-3 font-medium ${parseFloat(row.r15) >= 8.15 ? "bg-emerald-100 text-emerald-900 border border-emerald-300" : "text-slate-600"}`}>
                    {row.r15}
                  </td>
                  <td className={`px-4 py-3 font-medium ${parseFloat(row.r25) >= 8.15 ? "bg-emerald-100 text-emerald-900 border border-emerald-300" : "text-slate-600"}`}>
                    {row.r25}
                  </td>
                  <td className={`px-4 py-3 font-medium ${parseFloat(row.r35) >= 8.15 ? "bg-emerald-100 text-emerald-900 border border-emerald-300" : "text-slate-600"}`}>
                    {row.r35}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <p className="text-sm text-slate-500 mt-3 italic">
          * Highlighted cells clear the 8.15% policy hurdle.
        </p>
      </section>
    </div>
  );
}
