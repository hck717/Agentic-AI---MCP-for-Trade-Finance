from app.models.schemas import LCData, InvoiceData, BLData, PackingListData

# --- MOCK DATA REPOSITORY ---

MOCK_DB = {
    "apple": {
        "lc": LCData(
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
        ),
        "inv": InvoiceData(
            invoice_number="INV-2026-00145",
            amount=500000.00,
            currency="USD",
            goods_description="Apple iPhone 15 Pro Max, 256GB, Space Black",
            buyer="TechWorld Distribution Ltd",
            seller="Apple Distribution International"
        ),
        "bl": BLData(
            bl_number="MAEU123456789",
            port_of_loading="Los Angeles Port",
            port_of_discharge="Hong Kong Port",
            shipped_on_board_date="2026-04-25",
            goods_description="Electronic Devices - Apple iPhone",
            carrier="Maersk Line",
            gross_weight="1500 KGS"
        ),
        "pl": PackingListData(
            pl_number="PL-2026-00145",
            goods_description="Apple iPhone 15 Pro Max",
            gross_weight="1500 KGS",
            net_weight="1200 KGS",
            total_packages="100 Cartons"
        )
    },
    "silk": {
        "lc": LCData(
            lc_number="LC-2026-VN-STT",
            amount=85000.00,
            currency="EUR",
            expiry_date="2026-06-30",
            port_of_loading="Ho Chi Minh City",
            port_of_discharge="Hamburg",
            latest_shipment_date="2026-06-15",
            goods_description="100% Silk Scarves, Hand Woven",
            beneficiary="Vietnamese Silk Trading Co Ltd",
            applicant="EuroFashion GmbH",
            incoterms="FOB"
        ),
        "inv": InvoiceData(
            invoice_number="VST-INV-2026-0089",
            amount=85000.00,
            currency="EUR",
            goods_description="100% Silk Scarves, Grade A, Multicolor",
            buyer="EuroFashion GmbH",
            seller="Vietnamese Silk Trading Co Ltd"
        ),
        "bl": BLData(
            bl_number="VCTL202602001",
            port_of_loading="Ho Chi Minh City Port",
            port_of_discharge="Hamburg Port",
            shipped_on_board_date="2026-06-10",
            goods_description="Textile Products - Silk", # Generic
            carrier="Hapag-Lloyd",
            gross_weight="500 KGS"
        ),
        "pl": PackingListData(
            pl_number="PL-VST-2026-0089",
            goods_description="Silk Scarves",
            gross_weight="500 KGS",
            net_weight="450 KGS",
            total_packages="50 Boxes"
        )
    },
    "auto": {
        "lc": LCData(
            lc_number="LC-2026-AU-PMI",
            amount=250000.00,
            currency="AUD",
            expiry_date="2026-09-30",
            port_of_loading="Chennai",
            port_of_discharge="Melbourne",
            latest_shipment_date="2026-09-15",
            goods_description="Automotive Transmission & Gearbox Parts",
            beneficiary="Precision Manufacturing India Pvt Ltd",
            applicant="OzAuto Spares Pty Ltd",
            incoterms="CIF"
        ),
        "inv": InvoiceData(
            invoice_number="PMI-INV-AU-2026-0047",
            amount=250000.00,
            currency="AUD",
            goods_description="Automotive Transmission Components, Model X-500",
            buyer="OzAuto Spares Pty Ltd",
            seller="Precision Manufacturing India Pvt Ltd"
        ),
        "bl": BLData(
            bl_number="PMI-2026-BLG-001",
            port_of_loading="Chennai Port",
            port_of_discharge="Melbourne Port",
            shipped_on_board_date="2026-09-10",
            goods_description="Auto Parts", # Generic
            carrier="MSC",
            gross_weight="5000 KGS"
        ),
        "pl": PackingListData(
            pl_number="PL-PMI-AU-2026-047",
            goods_description="Transmission Parts",
            gross_weight="5000 KGS",
            net_weight="4800 KGS",
            total_packages="20 Pallets"
        )
    }
}

# --- Extraction Scripts (The "Pick" Logic) ---

def pick_lc_data(file_path: str, scenario_id: str = "apple") -> LCData:
    """Extracts structured data from the Letter of Credit."""
    return MOCK_DB.get(scenario_id, MOCK_DB["apple"])["lc"]

def pick_invoice_data(file_path: str, scenario_id: str = "apple") -> InvoiceData:
    """Extracts structured data from the Commercial Invoice."""
    return MOCK_DB.get(scenario_id, MOCK_DB["apple"])["inv"]

def pick_bl_data(file_path: str, scenario_id: str = "apple") -> BLData:
    """Extracts structured data from the Bill of Lading."""
    return MOCK_DB.get(scenario_id, MOCK_DB["apple"])["bl"]

def pick_packing_list_data(file_path: str, scenario_id: str = "apple") -> PackingListData:
    """Extracts structured data from the Packing List."""
    return MOCK_DB.get(scenario_id, MOCK_DB["apple"])["pl"]
