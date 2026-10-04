from fpdf import FPDF
import os

docs_dir = os.path.join(os.path.dirname(__file__), "docs")
os.makedirs(docs_dir, exist_ok=True)

class PDF(FPDF):
    def header(self):
        self.set_font('helvetica', 'B', 8)
        self.set_text_color(128)
        self.cell(0, 10, 'STRICTLY CONFIDENTIAL - ASI INTELLIGENCE INTERNAL USE ONLY', new_x="LMARGIN", new_y="NEXT", align='C')
        
    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica', 'I', 8)
        self.set_text_color(128)
        self.cell(0, 10, f'Page {self.page_no()}', align='C')

def add_lorem_ipsum(pdf, paragraphs=3):
    lorem = (
        "This section outlines the general provisions, covenants, and warranties customary in commercial real estate transactions of this magnitude. "
        "The Purchaser acknowledges that they have undertaken their own independent due diligence regarding the physical condition, environmental status, "
        "and statutory compliance of the improvements. Subject to the specific warranties detailed herein, the property is acquired on an 'as is, where is' basis. "
        "The Vendor warrants that, to the best of their knowledge, there are no outstanding statutory notices or encumbrances not previously disclosed in the "
        "data room. \n\n"
        "Furthermore, both parties agree to execute all necessary instruments, deeds, and documents required to effect the transfer of title. "
        "The deposit shall be held in trust by the Vendor's solicitor pending completion. In the event of default by the Purchaser, the deposit "
        "shall be forfeited, without prejudice to the Vendor's right to pursue damages for breach of contract. "
        "Any disputes arising from the interpretation of these clauses shall be resolved via binding arbitration in New South Wales. "
        "Market conditions remain subject to macro-economic volatility, including OCR adjustments by the RBA and global supply chain constraints affecting capital works.\n\n"
    )
    for _ in range(paragraphs):
        pdf.multi_cell(0, 5, text=lorem)
        pdf.ln(3)

def create_document(filename, title, pages_content, total_pages):
    pdf = PDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    for i in range(1, total_pages + 1):
        pdf.add_page()
        pdf.set_font('helvetica', 'B', 14)
        pdf.set_text_color(0, 51, 102)
        pdf.cell(0, 10, text=f"{title}", new_x="LMARGIN", new_y="NEXT", align="L")
        pdf.set_font('helvetica', 'I', 10)
        pdf.set_text_color(100)
        pdf.cell(0, 8, text=f"Section {i} / Page {i}", new_x="LMARGIN", new_y="NEXT", align="L")
        pdf.ln(5)
        
        pdf.set_font('helvetica', '', 10)
        pdf.set_text_color(0)
        
        if i in pages_content:
            pdf.multi_cell(0, 6, text=pages_content[i])
            pdf.ln(5)
            add_lorem_ipsum(pdf, 2)
        else:
            add_lorem_ipsum(pdf, 4)
            
    pdf.output(os.path.join(docs_dir, filename))

# 1. contract_summary.pdf
create_document(
    "contract_summary.pdf", 
    "COMMERCIAL PROPERTY ACQUISITION - CONTRACT SUMMARY", 
    {
        8: "SCHEDULE 3: CAPITAL EXPENDITURE & DEPRECIATION PLAN\n\nBased on the independent building inspection report, immediate rectification works are required prior to practical completion. Option A requires 250,000 AUD in Capex. This expenditure covers necessary roof membrane replacement and HVAC lifecycle upgrades to achieve a 4.5 NABERS rating.",
        12: "SCHEDULE 4: ALTERNATIVE ASSET ACQUISITIONS\n\nIn review of the secondary target profile, Option B requires 0 AUD in Capex. The facility at 88 Links Rd was completed within the last 12 months, and all structural, mechanical, and electrical services remain under the original builder's warranty."
    }, 
    24
)

# 2. independent_valuation.pdf
create_document(
    "independent_valuation.pdf", 
    "INDEPENDENT VALUATION REPORT - KNIGHT & FRANK", 
    {
        4: "SECTION 4: FINANCIAL ANALYSIS & PASSING YIELD\n\nProperty: 12 Wedgewood Rd, Eastern Creek (Option A)\n\nThe passing income for Option A is verified at 795,200 AUD/yr. This is supported by executed lease agreements. The asset is fully let to a single logistics tenant on a triple-net basis, minimizing outgoings leakage."
    }, 
    12
)

# 3. lease_schedule_rent_roll.pdf
create_document(
    "lease_schedule_rent_roll.pdf", 
    "MASTER LEASE SCHEDULE & TENANCY RENT ROLL", 
    {
        3: "OPTION B (88 Links Rd) - TENANCY SCHEDULE\n\nThe verified passing income for Option B is 684,369 AUD/yr. While the vendor's IM states a fully-leased target income of 963,900 AUD/yr, the leases for the remaining 29% (equating to 279,531 AUD/yr) are missing from the data room bundle and remain unverified. We cannot underwrite this unverified portion.",
        5: "OUTGOINGS & RECOVERY METRICS\n\nAn analysis of the executed lease structures across the portfolio indicates a gross outgoings recovery rate of 92%. The majority of leases are structured as net, with standard carve-outs for structural repairs and statutory land tax on a single-holding basis."
    }, 
    9
)

# 4. property_manager_annual_summary.pdf
create_document(
    "property_manager_annual_summary.pdf", 
    "ANNUAL PROPERTY MANAGEMENT & OPERATIONS SUMMARY", 
    {
        2: "FINANCIAL PERFORMANCE - OUTGOINGS RECONCILIATION\n\nDue to recent mid-term vacancies and caps on management fee recoveries, the actual outgoings recovery rate is currently 88%. This creates a historical discrepancy with the lease schedules.\n\nUnrecovered outgoings liabilities are calculated as follows:\n- Option A: 18,560 AUD/yr\n- Option B: 36,120 AUD/yr"
    }, 
    6
)

# 5. investment_policy_minute.pdf
create_document(
    "investment_policy_minute.pdf", 
    "INVESTMENT COMMITTEE MINUTE - POLICY HURDLES", 
    {
        1: "MACRO ASSUMPTIONS & TARGET RETURNS\n\nAny direct property acquisition must clear the 10-year Australian Government bond plus 350 bps unlevered. The current bond assumption to be utilized in all modelling is 4.65%. Therefore, the internal policy hurdle is set at an 8.15% unlevered 10-year IRR.",
        2: "REJECTED ALLOCATIONS\n\nThe committee has formally rejected Option C. Option C is a leaseback arrangement of 12 Wedgewood at $168 per sqm net (814,800 per year) with nil capital deployed. Because it offers no direct acquisition exposure or hard asset backing, it fails the primary mandate of this capital allocation."
    }, 
    2
)

# 6. portfolio_treasury_schedule.pdf
create_document(
    "portfolio_treasury_schedule.pdf", 
    "PORTFOLIO TREASURY & STATUTORY HOLDING COSTS", 
    {
        1: "STATUTORY TAX ASSESSMENTS (FY26/27)\n\nBased on the latest Valuer General assessments for the Western Sydney precinct, the projected statutory land tax obligations on a single-holding basis are:\n- Option A: 78,000 AUD\n- Option B: 96,000 AUD"
    }, 
    3
)

# 7. desktop_valuation_note.pdf
pdf = PDF()
pdf.add_page()
pdf.set_font('helvetica', 'B', 14)
pdf.cell(0, 10, text="INFORMAL DESKTOP NOTE", new_x="LMARGIN", new_y="NEXT", align="L")
pdf.set_font('helvetica', '', 11)
pdf.multi_cell(0, 6, text="This is an informal internal memo regarding the Eastern Creek sub-market.\n\nWe understand comparable Eastern Creek rates are currently transacting around $2,930 per sqm. However, this is based on anecdotal broker feedback and requires formal verification.\n\n[Note: Document is unsigned, undated, and carries no page references or formal appendices]")
pdf.output(os.path.join(docs_dir, "desktop_valuation_note.pdf"))

print("High-fidelity simulated PDFs generated successfully in docs/")
