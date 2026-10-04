import os
import fitz

os.makedirs('fixtures', exist_ok=True)

# 1. Valid PDF
doc1 = fitz.open()
page1 = doc1.new_page()
page1.insert_text((50, 50), "This is a valid test document. The revenue is $50,000 and profit margin is 15%.")
doc1.save('fixtures/valid_doc.pdf')
doc1.close()

# 2. Rejected PDF (Desktop Valuation Note)
doc2 = fitz.open()
page2 = doc2.new_page()
page2.insert_text((50, 50), "Desktop valuation note for a property. Price is $300,000.")
doc2.save('fixtures/desktop_valuation_note.pdf')
doc2.close()

# 3. Empty PDF or another PDF
doc3 = fitz.open()
doc3.save('fixtures/empty_doc.pdf')
doc3.close()

print("Fixtures created.")

