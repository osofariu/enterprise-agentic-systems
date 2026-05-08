"""Canned reference data used by the API.

In a real system these would come from a personnel directory and a document
management system.  Here they're plain dicts so the API can return
human-readable names and maintenance documents without external dependencies.
"""

from utils.models import MaintenanceDoc

# ── Personnel names ──────────────────────────────────────────────────────
# Maps employee UUID → display name.  UUIDs match database/scaffold/seed.py.

PERSONNEL_NAMES: dict[str, str] = {
    # Managers
    "9974d75b-3338-44fe-a179-0134676b1b69": "Dana Whitfield",
    "221c4e00-3f99-41ee-baf2-7f802dc5fd3d": "Morgan Alvarez",
    "baa1c6f1-404b-4eaf-962a-01dec28753f8": "Casey Nakamura",
    # Line workers
    "b35331ce-af2e-49dd-87e3-55b26210b784": "Riley Chen",
    "9fb932d4-f039-4722-96ff-82e389e3995a": "Jordan Okafor",
    "b8e3c71f-6bf0-4d62-b310-57ca7d411fab": "Taylor Bergström",
    "cae8c077-3779-45b3-96a1-da2c9cfbba43": "Avery Kowalski",
    "d283eb3a-5fbd-438e-89cf-158de6e96d45": "Sam Petrov",
    "366c5acd-aeaf-4905-9c8a-c0bb635b4c41": "Jamie Osei",
    "2dd301c8-a91a-4a5c-b623-c4dd26fb984f": "Alex Ferreira",
    "153d3a3f-56bc-49cb-9121-5785d9977338": "Drew Johansson",
    "ad689cf8-8759-4153-b778-5728f2655b19": "Quinn Delacroix",
    "50fe3281-7812-4170-967a-34d0c643e653": "Reese Kapoor",
    "8ed5f036-44f7-48cd-8aeb-34f967124890": "Harper Volkov",
    "5ccedc77-3429-479c-acda-4ccb01f35efe": "Skyler Mbeki",
}


# ── Maintenance documents ────────────────────────────────────────────────
# Keyed by reason code UUID.  Each code has description, training, and
# support documents.  In a real system this would be a document store.

CANNED_DOCS: dict[str, list[MaintenanceDoc]] = {
    "af11c1e7-7946-4a34-abd2-ed1c05f73dba": [
        MaintenanceDoc(
            reason_code="af11c1e7-7946-4a34-abd2-ed1c05f73dba",
            reason_type="description",
            document="Hydraulic pressure loss in main cylinder assembly",
        ),
        MaintenanceDoc(
            reason_code="af11c1e7-7946-4a34-abd2-ed1c05f73dba",
            reason_type="training",
            document="Inspect hydraulic seals weekly. Replace seals showing wear or discoloration. Check fluid levels at start of each shift.",
        ),
        MaintenanceDoc(
            reason_code="af11c1e7-7946-4a34-abd2-ed1c05f73dba",
            reason_type="support",
            document="Contact HydraFix Inc. at 1-800-555-0101 for emergency cylinder repair.",
        ),
    ],
    "efca6c3a-14c6-495e-ab45-1936d1d5c42f": [
        MaintenanceDoc(
            reason_code="efca6c3a-14c6-495e-ab45-1936d1d5c42f",
            reason_type="description",
            document="Electrical fault in control panel wiring",
        ),
        MaintenanceDoc(
            reason_code="efca6c3a-14c6-495e-ab45-1936d1d5c42f",
            reason_type="training",
            document="Follow lockout/tagout before opening panels. Check terminal torque specs quarterly. Report any burning smell immediately.",
        ),
        MaintenanceDoc(
            reason_code="efca6c3a-14c6-495e-ab45-1936d1d5c42f",
            reason_type="support",
            document="Contact PowerPanel Solutions at 1-800-555-0102 for control panel diagnostics.",
        ),
    ],
    "2495da17-1605-4583-a1cb-b7236ce8571b": [
        MaintenanceDoc(
            reason_code="2495da17-1605-4583-a1cb-b7236ce8571b",
            reason_type="description",
            document="Bearing wear detected during routine vibration check",
        ),
        MaintenanceDoc(
            reason_code="2495da17-1605-4583-a1cb-b7236ce8571b",
            reason_type="training",
            document="Perform vibration analysis monthly. Grease bearings per schedule. Replace when vibration exceeds 4.5 mm/s RMS.",
        ),
        MaintenanceDoc(
            reason_code="2495da17-1605-4583-a1cb-b7236ce8571b",
            reason_type="support",
            document="Contact BearingPro Supply at 1-800-555-0103 for expedited bearing replacement.",
        ),
    ],
    "618d3f43-0173-445f-9e0d-54254f4f81b0": [
        MaintenanceDoc(
            reason_code="618d3f43-0173-445f-9e0d-54254f4f81b0",
            reason_type="description",
            document="Coolant leak in secondary cooling loop",
        ),
        MaintenanceDoc(
            reason_code="618d3f43-0173-445f-9e0d-54254f4f81b0",
            reason_type="training",
            document="Check coolant hose connections daily. Monitor coolant level gauge. Report puddles or wet spots under machine immediately.",
        ),
        MaintenanceDoc(
            reason_code="618d3f43-0173-445f-9e0d-54254f4f81b0",
            reason_type="support",
            document="Contact CoolFlow Systems at 1-800-555-0104 for cooling loop repair.",
        ),
    ],
    "67c3b9fe-85fd-4dc4-a2c4-d84f5467115b": [
        MaintenanceDoc(
            reason_code="67c3b9fe-85fd-4dc4-a2c4-d84f5467115b",
            reason_type="description",
            document="Belt misalignment on main drive assembly",
        ),
        MaintenanceDoc(
            reason_code="67c3b9fe-85fd-4dc4-a2c4-d84f5467115b",
            reason_type="training",
            document="Use laser alignment tool during belt changes. Check tension with gauge weekly. Listen for squealing at startup.",
        ),
        MaintenanceDoc(
            reason_code="67c3b9fe-85fd-4dc4-a2c4-d84f5467115b",
            reason_type="support",
            document="Contact DriveTech Services at 1-800-555-0105 for alignment and tensioning.",
        ),
    ],
    "f94cf6b0-c986-4a9f-a664-718333674334": [
        MaintenanceDoc(
            reason_code="f94cf6b0-c986-4a9f-a664-718333674334",
            reason_type="description",
            document="Overheating in motor winding insulation",
        ),
        MaintenanceDoc(
            reason_code="f94cf6b0-c986-4a9f-a664-718333674334",
            reason_type="training",
            document="Monitor motor temperature with IR gun each shift. Ensure ventilation openings are clear. Do not exceed rated load.",
        ),
        MaintenanceDoc(
            reason_code="f94cf6b0-c986-4a9f-a664-718333674334",
            reason_type="support",
            document="Contact MotorCare Specialists at 1-800-555-0106 for winding inspection and rewind.",
        ),
    ],
    "7166a9f5-3620-4dbc-a3f3-760f0e2eb028": [
        MaintenanceDoc(
            reason_code="7166a9f5-3620-4dbc-a3f3-760f0e2eb028",
            reason_type="description",
            document="Pneumatic valve sticking during cycle changeover",
        ),
        MaintenanceDoc(
            reason_code="7166a9f5-3620-4dbc-a3f3-760f0e2eb028",
            reason_type="training",
            document="Lubricate valve actuators weekly. Drain moisture from air lines daily. Replace valve seals at 6-month intervals.",
        ),
        MaintenanceDoc(
            reason_code="7166a9f5-3620-4dbc-a3f3-760f0e2eb028",
            reason_type="support",
            document="Contact AirLogic Controls at 1-800-555-0107 for pneumatic valve service.",
        ),
    ],
    "d33bf820-6770-4a78-8ba3-fb8041f089dc": [
        MaintenanceDoc(
            reason_code="d33bf820-6770-4a78-8ba3-fb8041f089dc",
            reason_type="description",
            document="Sensor calibration drift on temperature probe",
        ),
        MaintenanceDoc(
            reason_code="d33bf820-6770-4a78-8ba3-fb8041f089dc",
            reason_type="training",
            document="Calibrate temperature probes monthly against reference. Log drift readings. Replace probe if drift exceeds 2°C.",
        ),
        MaintenanceDoc(
            reason_code="d33bf820-6770-4a78-8ba3-fb8041f089dc",
            reason_type="support",
            document="Contact SensorTech Calibration at 1-800-555-0108 for on-site calibration.",
        ),
    ],
    "f0fc795a-5a93-41f6-a058-8857c3881083": [
        MaintenanceDoc(
            reason_code="f0fc795a-5a93-41f6-a058-8857c3881083",
            reason_type="description",
            document="Gearbox noise indicating worn tooth contact surface",
        ),
        MaintenanceDoc(
            reason_code="f0fc795a-5a93-41f6-a058-8857c3881083",
            reason_type="training",
            document="Check gearbox oil level and color weekly. Listen for grinding or whining. Schedule oil analysis every 3 months.",
        ),
        MaintenanceDoc(
            reason_code="f0fc795a-5a93-41f6-a058-8857c3881083",
            reason_type="support",
            document="Contact GearWorks Industrial at 1-800-555-0109 for gearbox rebuild or replacement.",
        ),
    ],
    "0e4a1175-ec15-4269-b9e4-8824b1eb72c8": [
        MaintenanceDoc(
            reason_code="0e4a1175-ec15-4269-b9e4-8824b1eb72c8",
            reason_type="description",
            document="Conveyor chain tension out of specification range",
        ),
        MaintenanceDoc(
            reason_code="0e4a1175-ec15-4269-b9e4-8824b1eb72c8",
            reason_type="training",
            document="Measure chain sag weekly with tension gauge. Adjust take-up bolts per spec. Lubricate chain with approved grease.",
        ),
        MaintenanceDoc(
            reason_code="0e4a1175-ec15-4269-b9e4-8824b1eb72c8",
            reason_type="support",
            document="Contact ConveyorParts Direct at 1-800-555-0110 for chain and sprocket replacement.",
        ),
    ],
}
