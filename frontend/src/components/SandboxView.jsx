import { useState } from "react";

export default function SandboxView() {
  const [inputs, setInputs] = useState({
    passing_income: 795200,
    unrecovered_outgoings: 18560,
    land_tax: 78000,
    holding_costs: 41000,
    capex: 250000,
    total_cost: 14450000,
    rent_growth: 0.025,
    exit_cap: 0.0455
  });

  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setInputs({
      ...inputs,
      [e.target.name]: parseFloat(e.target.value) || 0
    });
  };

  const handleSimulate = async () => {
    setLoading(true);
    try {
      const res = await fetch("/api/calculations/sandbox", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(inputs)
      });
      const data = await res.json();
      setResults(data);
    } catch (err) {
      console.error("Simulation failed", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6 animate-fade-in max-w-4xl mx-auto">
      <div>
        <h1 className="text-2xl font-bold text-slate-800 mb-2">Simulation Sandbox</h1>
        <p className="text-slate-600">
          Play around with property values and test various conditions. This is a temporary testing environment and does not alter the main evidence ledger.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        <div className="bg-white p-6 rounded-lg shadow-sm border border-slate-200">
          <h2 className="text-lg font-bold text-slate-800 mb-4 border-b border-slate-200 pb-2">Input Variables</h2>
          <div className="space-y-4">
            {Object.keys(inputs).map((key) => (
              <div key={key} className="flex flex-col">
                <label className="text-sm font-semibold text-slate-700 mb-1 capitalize">
                  {key.replace(/_/g, " ")}
                </label>
                <input
                  type="number"
                  name={key}
                  value={inputs[key]}
                  onChange={handleChange}
                  step={key.includes("growth") || key.includes("cap") ? "0.001" : "100"}
                  className="px-3 py-2 border border-slate-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
            ))}
            <button
              onClick={handleSimulate}
              disabled={loading}
              className="w-full mt-4 bg-blue-600 text-white font-bold py-2 px-4 rounded hover:bg-blue-700 disabled:opacity-50"
            >
              {loading ? "Calculating..." : "Run Simulation"}
            </button>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-sm border border-slate-200 h-fit">
          <h2 className="text-lg font-bold text-slate-800 mb-4 border-b border-slate-200 pb-2">Calculated Results</h2>
          {!results ? (
            <p className="text-slate-500 italic">Click 'Run Simulation' to see results.</p>
          ) : (
            <div className="space-y-4">
              <div className="flex justify-between border-b border-slate-100 pb-2">
                <span className="font-semibold text-slate-600">Net Operating Income (NOI):</span>
                <span className="font-bold text-slate-800">{results.noi.toLocaleString()} AUD</span>
              </div>
              <div className="flex justify-between border-b border-slate-100 pb-2">
                <span className="font-semibold text-slate-600">Total Capital Deployed:</span>
                <span className="font-bold text-slate-800">{results.total_capital.toLocaleString()} AUD</span>
              </div>
              <div className="flex justify-between border-b border-slate-100 pb-2">
                <span className="font-semibold text-slate-600">Net Initial Yield (NIY):</span>
                <span className="font-bold text-blue-600">{results.niy}</span>
              </div>
              <div className="flex justify-between border-b border-slate-100 pb-2">
                <span className="font-semibold text-slate-600">Approx. 10-Yr IRR:</span>
                <span className="font-bold text-green-600">{results.approx_irr}</span>
              </div>
              <div className="flex justify-between border-b border-slate-100 pb-2">
                <span className="font-semibold text-slate-600">Year 10 NOI:</span>
                <span className="font-bold text-slate-800">{results.year_10_noi.toLocaleString()} AUD</span>
              </div>
              <div className="flex justify-between pt-1">
                <span className="font-semibold text-slate-600">Terminal Value:</span>
                <span className="font-bold text-slate-800">{results.terminal_value.toLocaleString()} AUD</span>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
