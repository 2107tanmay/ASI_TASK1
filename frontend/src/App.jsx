import React, { useState } from "react";
import { BrowserRouter as Router, Routes, Route, Navigate, NavLink } from "react-router-dom";
import IntakeView from "./components/IntakeView";
import EvidenceLedger from "./components/EvidenceLedger";
import OptionsSensitivity from "./components/OptionsSensitivity";
import DecisionRecord from "./components/DecisionRecord";
import Chatbot from "./components/Chatbot";

function NavBar() {
  const links = [
    { to: "/intake", label: "Intake" },
    { to: "/evidence", label: "Evidence Ledger" },
    { to: "/options", label: "Options & Sensitivity" },
    { to: "/decision", label: "Decision Record" },
  ];
  return (
    <nav className="bg-slate-800 px-6 py-4 flex items-center gap-6 shadow-md">
      <span className="text-white font-bold text-lg mr-4 tracking-wide">Decision Pack</span>
      {links.map((l) => (
        <NavLink
          key={l.to}
          to={l.to}
          className={({ isActive }) =>
            `text-sm transition-colors ${isActive ? "text-amber-400 font-semibold" : "text-slate-300 hover:text-white"}`
          }
        >
          {l.label}
        </NavLink>
      ))}
    </nav>
  );
}

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-slate-50 font-sans text-slate-800 flex flex-col relative pb-20">
        <NavBar />
        <main className="flex-1 p-8 max-w-7xl mx-auto w-full">
          <Routes>
            <Route path="/" element={<Navigate to="/intake" replace />} />
            <Route path="/intake" element={<IntakeView />} />
            <Route path="/evidence" element={<EvidenceLedger />} />
            <Route path="/options" element={<OptionsSensitivity />} />
            <Route path="/decision" element={<DecisionRecord />} />
          </Routes>
        </main>
        <Chatbot />
      </div>
    </Router>
  );
}

export default App;
