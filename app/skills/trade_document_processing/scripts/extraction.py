from app.models.schemas import LCData, InvoiceData, BLData

# --- Extraction Scripts (The "Pick" Logic) ---

def pick_lc_data(file_path: str) -> LCData:
    """Extracts structured data from the Letter of Credit."""
    # Mocking extraction from 'mock_documents/1_APPLE_IPHONE_IMPORT/LC_LC-2026-001-HSBC.md'
    return LCData(
        lc_number="LC-2026-001-HSBC",
        amount=500000.00,
        currency="USD",
        expiry_date="2026-05-20",
        port_of_loading="Los Angeles",
        port_of_discharge="Hong Kong",
        latest_shipment_date="2026-05-01",
        goods_description="Apple iPhone 15 Pro Max smartphones",
        beneficiary="Apple Distribution International",
        applicant="TechWorld Distribution Ltd",
        incoterms="CIF"
    )

def pick_invoice_data(file_path: str) -> InvoiceData:
    """Extracts structured data from the Commercial Invoice."""
    # Mocking extraction from 'mock_documents/1_APPLE_IPHONE_IMPORT/INVOICE_INV-2026-00145.md'
    return InvoiceData(
        invoice_number="INV-2026-00145",
        amount=500000.00,
        currency="USD",
        goods_description="Apple iPhone 15 Pro Max, 256GB, Space Black", # Specific
        buyer="TechWorld Distribution Ltd",
        seller="Apple Distribution International"
    )

def pick_bl_data(file_path: str) -> BLData:
    """Extracts structured data from the Bill of Lading."""
    # Mocking extraction from 'mock_documents/1_APPLE_IPHONE_IMPORT/BL_MAEU123456789.md'
    return BLData(
        bl_number="MAEU123456789",
        port_of_loading="Los Angeles Port",
        port_of_discharge="Hong Kong Port",
        shipped_on_board_date="2026-04-25",
        goods_description="Electronic Devices - Apple iPhone", # Generic (ISBP 745 Art. E26)
        carrier="Maersk Line"
    )
