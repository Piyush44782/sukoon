"""Front matter builder for SUKOON Project Report."""
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from pathlib import Path
from build_full_report_docx import (
    add_p, add_heading_1, add_heading_2, add_heading_3, add_bullet,
    format_table, VIPS_LOGO
)

def build_front_matter(doc):
    # -------------------------------------------------------------
    # PAGE 1: TITLE PAGE / COVER PAGE
    # -------------------------------------------------------------
    if VIPS_LOGO.exists():
        p_logo = doc.add_paragraph()
        p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_logo.paragraph_format.space_before = Pt(10)
        p_logo.paragraph_format.space_after = Pt(18)
        run_logo = p_logo.add_run()
        run_logo.add_picture(str(VIPS_LOGO), width=Inches(2.4))
    
    add_p(doc, "SUKOON: AI STUDENT MENTAL WELLNESS PLATFORM",
          size_pt=18, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=6)
    
    add_p(doc, "A SAFE SPACE. A LISTENING EAR. A BETTER TOMORROW.",
          size_pt=12, italic=True, bold=True, color_rgb=(75, 85, 99),
          align=WD_ALIGN_PARAGRAPH.CENTER, space_after=32)
    
    add_p(doc, "IN PARTIAL FULFILLMENT OF THE REQUIREMENT FOR THE AWARD OF DEGREE OF",
          size_pt=11, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=6)
    
    add_p(doc, "MASTER OF COMPUTER APPLICATIONS",
          size_pt=14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=4)
    
    add_p(doc, "[Minor Project-I (MCA-169)]",
          size_pt=12, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=40)
    
    add_p(doc, "Submitted By:", size_pt=12, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=4)
    add_p(doc, "Piyush Verma (10017704426)", size_pt=13, bold=True, color_rgb=(15, 23, 42),
          align=WD_ALIGN_PARAGRAPH.CENTER, space_after=44)
    
    add_p(doc, "VIVEKANANDA SCHOOL OF INFORMATION TECHNOLOGY",
          size_pt=12, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=3)
    add_p(doc, "VIVEKANANDA INSTITUTE OF PROFESSIONAL STUDIES-TC",
          size_pt=12, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=6)
    
    add_p(doc, "Affiliated to", size_pt=11, italic=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=3)
    add_p(doc, "(GURU GOBIND SINGH INDRAPRASTHA UNIVERSITY, DELHI)",
          size_pt=11.5, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=36)
    
    add_p(doc, "[Aug–Dec, 2026]", size_pt=11.5, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=0)
    doc.add_page_break()

    # -------------------------------------------------------------
    # PAGE 2: CERTIFICATE
    # -------------------------------------------------------------
    add_heading_1(doc, "CERTIFICATE")
    add_p(doc, "", space_after=18)
    
    cert_text = (
        "This is to certify that this project entitled “SUKOON: AI Student Mental Wellness Platform” "
        "submitted in partial fulfillment of the 1st semester of Master of Computer Applications to the "
        "Vivekananda Institute of Professional Studies – Technical Campus, done by Mr. Piyush Verma, "
        "Roll No. 10017704426, is an authentic work carried out by him at Vivekananda School of Information "
        "Technology, Vivekananda Institute of Professional Studies – Technical Campus, under my guidance "
        "during the academic session [Aug–Dec, 2026]."
    )
    add_p(doc, cert_text, size_pt=12, line_spacing=1.5, space_after=120)
    
    # Signature block
    tbl_cert = doc.add_table(rows=2, cols=2)
    tbl_cert.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_cert.rows[0].cells[0].paragraphs[0].text = "______________________"
    tbl_cert.rows[0].cells[1].paragraphs[0].text = "______________________"
    tbl_cert.rows[1].cells[0].paragraphs[0].text = "Signature of the Student\nPiyush Verma\n(10017704426)"
    tbl_cert.rows[1].cells[1].paragraphs[0].text = "Signature of the Guide\nDr. Neha Goel\nFaculty Guide, VSIT"
    
    for row in tbl_cert.rows:
        row.cells[0].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.LEFT
        row.cells[1].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
        for cell in row.cells:
            for p in cell.paragraphs:
                for r in p.runs:
                    r.font.name = "Times New Roman"
                    r.font.size = Pt(11)
                    r.font.bold = True
    doc.add_page_break()

    # -------------------------------------------------------------
    # PAGE 3: SELF CERTIFICATE
    # -------------------------------------------------------------
    add_heading_1(doc, "SELF CERTIFICATE")
    add_p(doc, "", space_after=18)
    
    self_cert_text = (
        "This is to certify that the project report entitled “SUKOON: AI Student Mental Wellness Platform” "
        "is an authentic work carried out by me for the partial fulfilment of the 1st semester of Master of "
        "Computer Applications under the guidance of Dr. Neha Goel. The matter embodied in this project work "
        "has not been submitted earlier for award of any degree or diploma to the best of my knowledge and belief."
    )
    add_p(doc, self_cert_text, size_pt=12, line_spacing=1.5, space_after=140)
    
    p_sc = doc.add_paragraph()
    p_sc.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_sc.paragraph_format.line_spacing = 1.25
    r_sc = p_sc.add_run(
        "______________________\n"
        "Signature of the Student\n"
        "Name of the Student: Piyush Verma\n"
        "Roll No.: 10017704426\n"
        "Programme: MCA (1st Semester)"
    )
    r_sc.font.name = "Times New Roman"
    r_sc.font.size = Pt(11.5)
    r_sc.font.bold = True
    doc.add_page_break()

    # -------------------------------------------------------------
    # PAGE 4: ACKNOWLEDGEMENT
    # -------------------------------------------------------------
    add_heading_1(doc, "ACKNOWLEDGEMENT")
    add_p(doc, "", space_after=14)
    
    ack1 = (
        "I, Piyush Verma, a student of the Master of Computer Applications (1st semester) programme at "
        "Vivekananda Institute of Professional Studies – Technical Campus, express my sincere gratitude to "
        "the Institute for providing me with the opportunity and the academic environment to undertake this minor project."
    )
    add_p(doc, ack1, space_after=12)
    
    ack2 = (
        "I am deeply indebted to my project guide, Dr. Neha Goel, Vivekananda School of Information "
        "Technology, for the valuable guidance, constructive criticism and constant encouragement extended to me "
        "throughout the course of this work. The direction received at every stage of the project helped me to "
        "shape both the system architecture and this report."
    )
    add_p(doc, ack2, space_after=12)
    
    ack3 = (
        "I also thank the faculty members of the Vivekananda School of Information Technology for their support, "
        "and the staff of the Institute library and computing facilities for the resources made available to me."
    )
    add_p(doc, ack3, space_after=12)
    
    ack4 = (
        "Finally, I express my gratitude to my family, friends and classmates, who have been a constant source "
        "of motivation during the preparation of this project."
    )
    add_p(doc, ack4, space_after=60)
    
    p_ack_sig = doc.add_paragraph()
    p_ack_sig.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r_as = p_ack_sig.add_run(
        "Piyush Verma\n"
        "10017704426\n"
        "Minor Project-I (MCA-169)"
    )
    r_as.font.name = "Times New Roman"
    r_as.font.size = Pt(11.5)
    r_as.font.bold = True
    doc.add_page_break()

    # -------------------------------------------------------------
    # PAGES 5-8: SYNOPSIS
    # -------------------------------------------------------------
    add_heading_1(doc, "SYNOPSIS")
    add_p(doc, "", space_after=6)
    
    add_heading_2(doc, "Title of the Project")
    add_p(doc, "SUKOON: AI Student Mental Wellness Platform (VIPS Pitampura)", bold=True, space_after=12)
    
    add_heading_2(doc, "Statement of the Problem")
    add_p(doc, 
          "University students frequently encounter acute psychological stressors—academic pressure, semester "
          "backlogs, placement uncertainty, social isolation, and escalating parental expectations. While educational "
          "institutions maintain counseling bodies, students routinely hesitate to seek formal help due to fear of stigma, "
          "lack of privacy, and administrative exposure. Existing digital wellness solutions often suffer from serious flaws: "
          "they either operate as black-box chatbots prone to clinical hallucinations, fail to guarantee end-to-end data privacy, "
          "or lack institutional integration. A platform is required that provides confidential, non-diagnostic empathetic listening, "
          "deterministic safety pre-filters with verified national crisis helplines, transparent sentiment analytics, and seamless "
          "triage to college counselors, faculty mentors, and peer mentors under strict student consent.", space_after=12)
    
    add_heading_2(doc, "Why this Topic was Chosen")
    add_p(doc, 
          "Mental health support within higher education is a pressing societal imperative. Integrating artificial "
          "intelligence with psychological guardrails offers an accessible, zero-stigma first point of contact. However, "
          "mental wellness requires unprecedented engineering rigor: language models must never diagnose or prescribe, "
          "suicidal ideation must trigger deterministic interventions rather than probabilistic text generation, and sensitive "
          "reflections must be cryptographically isolated. This project was chosen because it synergizes natural language "
          "processing, multi-provider LLM routing, symmetric field-level cryptography, empirical statistical trend modeling, "
          "and human-centered software engineering in an institutional system with real-world ethical impact.", space_after=12)
    
    add_heading_2(doc, "Objective and Scope of the Project")
    add_p(doc, "The objectives of the project are to:", space_after=4)
    add_bullet(doc, "Provide an empathetic, 24/7 conversational AI wellness companion governed by non-clinical boundaries.")
    add_bullet(doc, "Implement deterministic regex-based crisis detection that bypasses the AI layer and delivers verified emergency helplines (Tele-MANAS 14416, KIRAN, 112).")
    add_bullet(doc, "Provide transparent lexicon-based NLP for sentiment, affective emotions, and six concern domains with clear disclosures that signals are imperfect indicators.")
    add_bullet(doc, "Offer quantitative wellness check-ins (1–5 scale) with least-squares polynomial trend modeling (np.polyfit) and week-over-week comparisons.")
    add_bullet(doc, "Guarantee data sovereignty via AES-128 Fernet field-level encryption for all chat transcripts, journals, and private notes.")
    add_bullet(doc, "Enable multi-tier appointment scheduling with college counselors, faculty mentors, and trained peer mentors.")
    add_bullet(doc, "Incorporate student-controlled parent inclusion with selective exports, timestamped audit records, and instant revocation.")
    add_bullet(doc, "Provide administrators with k-anonymized macro statistics (k >= 5) to protect student anonymity.")
    
    add_p(doc, "Scope — Implemented:", bold=True, space_after=4)
    add_p(doc, "A full-stack, responsive Streamlit platform with role-based routing (Student, Counsellor, Mentor, Admin), "
               "PBKDF2-HMAC-SHA256 authentication with brute-force lockout, 16 relational SQLite tables, Fernet encryption at rest, "
               "multi-provider LLM connectors (Groq API, local private Ollama, Claude fallback), and an automated test suite of 18 passing tests.", space_after=8)
    
    add_p(doc, "Scope — Deliberately Excluded:", bold=True, space_after=4)
    add_p(doc, "Clinical medical diagnosis, drug/pharmacological prescription, commercial psychometric testing, non-consensual "
               "parental surveillance dashboards, and unencrypted external cloud data synchronization.", space_after=12)
    
    add_heading_2(doc, "Methodology & Process Description")
    add_p(doc, 
          "The system architecture is structured into two primary operational workflows. The Wellness & Companionship Workflow "
          "captures self-reported check-in metrics and chat messages. Each message is intercepted by the Regex Safety Engine; if acute "
          "crisis triggers match, national helplines are returned immediately. If safe, a transparent lexicon analyzer extracts sentiment, "
          "emotions, and concern categories, appending a subtle contextual hint to the system prompt before dispatching to the LLM. "
          "The Triage & Human-in-the-Loop Workflow manages appointment slots for campus counselors and mentors, enforcing anti-double-booking "
          "rules and creating private encrypted consultation channels.", space_after=12)
    
    add_heading_2(doc, "Hardware and Software to be Used")
    add_bullet(doc, "Hardware: 64-bit multi-core computer (x86_64 or ARM64) with 8 GB RAM and 1 GB available disk space. No dedicated GPU is mandatory.", bold_prefix="Hardware: ")
    add_bullet(doc, "Software: Python 3.12+, Streamlit 1.38+, SQLite3, Cryptography 42.0+ (Fernet), NumPy 1.26+, Anthropic Python SDK, Requests/HTTPX, Pytest 8.0+.", bold_prefix="Software: ")
    
    add_heading_2(doc, "Testing Technologies Used")
    add_p(doc, 
          "System verification is conducted via Pytest using automated unit and integration tests. Tests cover credential validation, "
          "salted PBKDF2 hashing, lockout thresholds (5 failed attempts), regex crisis triggers, lexicon negation handling, "
          "conversation cryptographic isolation, parent consent revocation, appointment concurrency, k-anonymity bounds, and "
          "API failure fallbacks. The test suite contains 18 comprehensive automated tests with 100% pass rate.", space_after=12)
    
    add_heading_2(doc, "Resources and Limitations")
    add_p(doc, 
          "The platform utilizes standard library and open-source packages. While Groq or Anthropic API keys enable high-capacity cloud inference, "
          "SUKOON features a local Ollama connector and an offline safe fallback message. Current limitations include reliance on in-app reminders "
          "rather than external SMS/WhatsApp push notifications, and restriction of self-registration to the institutional @vips.edu domain.", space_after=12)
    
    add_heading_2(doc, "Contribution of the Project")
    add_p(doc, 
          "SUKOON's primary contribution is an ethical, verifiable blueprint for campus digital wellness. By establishing deterministic "
          "crisis pre-filtering, field-level Fernet encryption, transparent lexicon NLP disclosures, and k-anonymized administrative reporting, "
          "the project proves that institutional AI platforms can deliver empathetic student support while upholding absolute user confidentiality "
          "and safety.", space_after=12)
    
    add_heading_2(doc, "Conclusion")
    add_p(doc, 
          "The project demonstrates that an accessible, non-diagnostic, privacy-first mental wellness system can be engineered successfully "
          "using open-source technologies, local cryptographic isolation, and responsible AI guardrails, significantly lowering the barrier "
          "for students to seek mental health assistance.", space_after=18)
    doc.add_page_break()

    # -------------------------------------------------------------
    # PAGES 9-11: TABLE OF CONTENTS
    # -------------------------------------------------------------
    add_heading_1(doc, "TABLE OF CONTENTS")
    add_p(doc, "", space_after=6)
    
    toc_data = [
        ("1.", "CHAPTER-1: INTRODUCTION", "1"),
        ("", "  1.1: OBJECTIVE AND SCOPE", "1"),
        ("", "  1.2: FEATURES", "2"),
        ("", "  1.3: BENEFITS", "3"),
        ("", "  1.4: MODULES", "4"),
        ("2.", "CHAPTER-2: THEORETICAL BACKGROUND", "6"),
        ("", "  2.1: LARGE LANGUAGE MODELS & CONVERSATIONAL AI", "6"),
        ("", "  2.2: DETERMINISTIC SAFETY & CRISIS INTERCEPTION", "6"),
        ("", "  2.3: LEXICAL SENTIMENT ANALYSIS & EMOTION DETECTION", "7"),
        ("", "  2.4: POLYNOMIAL REGRESSION & TREND MODELING (NUMPY)", "7"),
        ("", "  2.5: SYMMETRIC FIELD-LEVEL ENCRYPTION (AES-128 FERNET)", "8"),
        ("", "  2.6: PASSWORD HASHING & BRUTE-FORCE COUNTERMEASURES", "8"),
        ("", "  2.7: WEB APPLICATION ARCHITECTURE & STREAMLIT ENGINE", "9"),
        ("3.", "CHAPTER-3: DEFINITION OF PROBLEM", "10"),
        ("", "  3.1: PROBLEM STATEMENT", "10"),
        ("", "  3.2: SHORTCOMINGS OF EXISTING APPROACHES", "10"),
        ("", "  3.3: SPECIFIC CHALLENGES", "11"),
        ("", "  3.4: PROPOSED SOLUTION", "12"),
        ("4.", "CHAPTER-4: SYSTEM ANALYSIS AND DESIGN VIS-À-VIS USER REQUIREMENTS", "13"),
        ("", "  4.1: INTENDED USERS", "13"),
        ("", "  4.2: FUNCTIONAL REQUIREMENTS", "13"),
        ("", "  4.3: NON-FUNCTIONAL REQUIREMENTS", "14"),
        ("", "  4.4: FEASIBILITY STUDY", "15"),
        ("", "  4.5: USE CASE DIAGRAM", "16"),
        ("", "  4.6: SYSTEM ARCHITECTURE", "17"),
        ("", "  4.7: DESIGN OF KEY MECHANISMS", "18"),
        ("", "  4.8: FRONTEND DESIGN", "19"),
        ("", "  4.9: REQUIREMENT-TO-DESIGN TRACEABILITY", "21"),
        ("5.", "CHAPTER-5: SYSTEM PLANNING (PERT CHART)", "22"),
        ("", "  5.1: ACTIVITY IDENTIFICATION", "22"),
        ("", "  5.2: PERT CHART", "23"),
        ("6.", "CHAPTER-6: METHODOLOGY, SYSTEM IMPLEMENTATION AND DETAILS OF HARDWARE AND SOFTWARE", "24"),
        ("", "  6.1: METHODOLOGY ADOPTED", "24"),
        ("", "  6.2: HARDWARE REQUIREMENTS", "24"),
        ("", "  6.3: SOFTWARE REQUIREMENTS", "25"),
        ("", "  6.4: TECHNOLOGY STACK", "25"),
        ("", "  6.5: IMPLEMENTATION DETAILS", "27"),
        ("", "  6.6: IMPLEMENTATION STATUS AT THE TIME OF WRITING", "33"),
        ("7.", "CHAPTER-7: DETAILED LIFE CYCLE OF THE PROJECT", "34"),
        ("", "  7.1: LIFE CYCLE PHASES", "34"),
        ("", "  7.2: ENTITY-RELATIONSHIP DIAGRAM", "34"),
        ("", "  7.3: DATA FLOW DIAGRAMS", "36"),
        ("", "  7.4: PROCESS INVOLVED", "39"),
        ("", "  7.5: DATABASE SCHEMA & DATA CONTRACTS", "41"),
        ("", "  7.6: INPUT AND OUTPUT SCREEN DESIGN", "43"),
        ("", "  7.7: SELECTED IMPLEMENTATION EXCERPTS", "47"),
        ("8.", "CHAPTER-8: SYSTEM TESTING", "49"),
        ("", "  8.1: METHODOLOGY USED FOR TESTING", "49"),
        ("", "  8.2: TESTING TOOLS", "50"),
        ("", "  8.3: TEST ENVIRONMENT AND FIXTURES", "50"),
        ("", "  8.4: NOTABLE TEST DESIGNS", "50"),
        ("", "  8.5: TEST INVENTORY", "51"),
        ("", "  8.6: TEST AREAS BY COMPONENT", "52"),
        ("", "  8.7: TEST REPORT", "53"),
        ("", "  8.8: STATIC ANALYSIS & CODE INTEGRITY", "54"),
        ("9.", "CHAPTER-9: SYSTEM MAINTENANCE AND EVALUATION", "55"),
        ("", "  9.1: DESIGN FOR MAINTAINABILITY", "55"),
        ("", "  9.2: MAINTENANCE ACTIVITIES", "55"),
        ("", "  9.3: EVALUATION AGAINST OBJECTIVES", "56"),
        ("10.", "CHAPTER-10: COST AND BENEFIT ANALYSIS", "57"),
        ("", "  10.1: COST COMPONENTS", "57"),
        ("", "  10.2: BENEFITS", "57"),
        ("", "  10.3: ANALYSIS", "58"),
        ("11.", "CHAPTER-11: USER AND OPERATIONAL MANUAL", "59"),
        ("", "  11.1: PREREQUISITES", "59"),
        ("", "  11.2: APPLICATION INSTALLATION", "59"),
        ("", "  11.3: DATABASE INITIALIZATION & SEEDING", "60"),
        ("", "  11.4: ENVIRONMENT CONFIGURATION", "60"),
        ("", "  11.5: RUNNING THE APPLICATION", "61"),
        ("", "  11.6: USER WORKFLOW", "61"),
        ("", "  11.7: SECURITY ASPECTS", "62"),
        ("", "  11.8: ACCESS RIGHTS & RBAC", "63"),
        ("", "  11.9: BACKUP AND RECOVERY", "63"),
        ("", "  11.10: OPERATIONAL CONTROLS", "64"),
        ("12.", "CHAPTER-12: LIMITATIONS", "65"),
        ("13.", "CHAPTER-13: CONCLUSION AND FUTURE SCOPE", "66"),
        ("", "  13.1: CONCLUSION", "66"),
        ("", "  13.2: FUTURE SCOPE", "66"),
        ("14.", "ANNEXURE 1: DATA DICTIONARY", "68"),
        ("15.", "ANNEXURE 2: LIST OF ABBREVIATIONS, FIGURES AND TABLES", "72"),
        ("16.", "ANNEXURE 3: REFERENCES & WEBSITES", "75"),
        ("17.", "EXTENDED ABSTRACT", "78")
    ]
    
    tbl_toc = doc.add_table(rows=len(toc_data) + 1, cols=3)
    format_table(tbl_toc, [0.8, 5.0, 0.8], ["S. NO.", "TOPIC", "PAGE NO."], toc_data)
    doc.add_page_break()

print("doc_front_matter.py written.")
