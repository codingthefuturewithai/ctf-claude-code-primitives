#!/usr/bin/env python3
"""
Generate a fillable branded PDF for the Consulting Services Agreement.
Uses CTFAI brand colors and includes editable form fields.
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import HexColor
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import os

# Brand colors
NAVY = HexColor("#1B2838")
ORANGE = HexColor("#F5A623")
BLUE = HexColor("#7DD3FC")
PURPLE = HexColor("#C084FC")
WHITE = HexColor("#FFFFFF")
LIGHT_GRAY = HexColor("#F0F5FA")
TEXT_GRAY = HexColor("#2d3748")

# Page dimensions
PAGE_WIDTH, PAGE_HEIGHT = letter
MARGIN = 50

def draw_header(c, logo_path):
    """Draw the branded header with logo."""
    header_height = 80
    header_y = PAGE_HEIGHT - header_height

    # Header background
    c.setFillColor(NAVY)
    c.rect(0, header_y, PAGE_WIDTH, header_height, fill=1, stroke=0)

    # Gradient accent bar
    bar_height = 4
    bar_y = header_y
    gradient_width = PAGE_WIDTH / 3

    c.setFillColor(ORANGE)
    c.rect(0, bar_y, gradient_width, bar_height, fill=1, stroke=0)
    c.setFillColor(BLUE)
    c.rect(gradient_width, bar_y, gradient_width, bar_height, fill=1, stroke=0)
    c.setFillColor(PURPLE)
    c.rect(gradient_width * 2, bar_y, gradient_width, bar_height, fill=1, stroke=0)

    # Logo
    if os.path.exists(logo_path):
        logo = ImageReader(logo_path)
        logo_size = 45
        c.drawImage(logo, MARGIN, header_y + 18, width=logo_size, height=logo_size, mask='auto')

    # Company name
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(MARGIN + 55, header_y + 35, "Coding the Future")
    c.setFillColor(ORANGE)
    c.drawString(MARGIN + 55 + c.stringWidth("Coding the Future ", "Helvetica-Bold", 16), header_y + 35, "AI")

    # Document type label
    c.setFillColor(BLUE)
    c.setFont("Helvetica", 9)
    c.drawRightString(PAGE_WIDTH - MARGIN, header_y + 40, "LEGAL AGREEMENT")

    return header_y

def draw_footer(c):
    """Draw the branded footer."""
    footer_height = 35

    c.setFillColor(NAVY)
    c.rect(0, 0, PAGE_WIDTH, footer_height, fill=1, stroke=0)

    c.setFillColor(BLUE)
    c.setFont("Helvetica", 7)
    c.drawString(MARGIN, 14, "Coding the Future AI, LLC  •  Consulting Services Agreement")

    c.setFillColor(WHITE)
    c.setFont("Helvetica-Oblique", 7)
    c.drawRightString(PAGE_WIDTH - MARGIN, 14, "Empowering teams with AI tools, knowledge, and strategy")

def draw_section_number(c, x, y, number):
    """Draw an orange circle with section number."""
    c.setFillColor(ORANGE)
    c.circle(x + 10, y + 4, 10, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 10)
    num_str = str(number)
    c.drawCentredString(x + 10, y + 1, num_str)

def draw_text_field(c, name, x, y, width, height=18, value=""):
    """Draw an editable text field."""
    c.acroForm.textfield(
        name=name,
        x=x,
        y=y,
        width=width,
        height=height,
        borderWidth=0.5,
        borderColor=NAVY,
        fillColor=WHITE,
        textColor=NAVY,
        fontSize=10,
        fieldFlags='',
        value=value
    )

def create_agreement_pdf(output_path, logo_path):
    """Create the fillable consulting services agreement PDF."""
    c = canvas.Canvas(output_path, pagesize=letter)

    # ===== PAGE 1 =====
    header_y = draw_header(c, logo_path)
    draw_footer(c)

    content_top = header_y - 30
    y = content_top

    # Document title
    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 22)
    c.drawString(MARGIN, y, "Consulting Services Agreement")

    # Orange underline
    y -= 8
    c.setStrokeColor(ORANGE)
    c.setLineWidth(3)
    c.line(MARGIN, y, MARGIN + 320, y)

    # Intro text
    y -= 30
    c.setFillColor(TEXT_GRAY)
    c.setFont("Helvetica", 10)
    intro = "This Consulting Services Agreement (\"Agreement\") is entered into by and between the"
    c.drawString(MARGIN, y, intro)
    y -= 14
    c.drawString(MARGIN, y, "following parties and is effective as of the date specified below.")

    # Parties box
    y -= 30
    box_height = 75
    c.setFillColor(LIGHT_GRAY)
    c.roundRect(MARGIN, y - box_height + 15, PAGE_WIDTH - 2*MARGIN, box_height, 5, fill=1, stroke=0)
    c.setStrokeColor(ORANGE)
    c.setLineWidth(3)
    c.line(MARGIN, y - box_height + 15, MARGIN, y + 15)

    # Parties content
    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(MARGIN + 15, y, "Consultant:")
    c.setFont("Helvetica", 10)
    c.drawString(MARGIN + 85, y, "Coding the Future AI, LLC")

    y -= 20
    c.setFont("Helvetica-Bold", 10)
    c.drawString(MARGIN + 15, y, "Client:")
    draw_text_field(c, "client_name", MARGIN + 85, y - 4, 250, value="")

    y -= 20
    c.setFont("Helvetica-Bold", 10)
    c.drawString(MARGIN + 15, y, "Effective Date:")
    draw_text_field(c, "effective_date", MARGIN + 105, y - 4, 150, value="")

    # Sections
    sections = [
        ("Services", "Consultant will provide advisory, strategy, and related professional services as may be requested by Client and agreed upon in one or more written Statements of Work (\"SOWs\"). Services are advisory in nature and do not guarantee specific outcomes or results."),
        ("Fees & Payment", "Fees for services will be as specified in the applicable SOW. Unless otherwise stated, Consultant's standard rate will be specified in the applicable Statement of Work. Invoices are due within fifteen (15) days of receipt. For longer-term engagements, the Consultant may offer alternative pricing structures (e.g., prepaid blocks or packaged services) by mutual agreement and documented in a separate Statement of Work."),
        ("Independent Contractor", "Consultant is an independent contractor and not an employee, agent, or partner of Client. Nothing in this Agreement creates a partnership, joint venture, or employment relationship."),
        ("Intellectual Property", "Each party retains ownership of its pre-existing intellectual property. Consultant retains all right, title, and interest in its methodologies, frameworks, templates, workflows, prompts, tooling, and know-how, whether developed prior to or during the engagement. Subject to full payment, Client is granted a non-exclusive, perpetual, non-transferable license to use deliverables produced specifically for Client's internal business purposes."),
        ("Confidentiality", "Each party agrees to maintain the confidentiality of the other party's non-public, proprietary, or confidential information and to use such information solely for purposes of this engagement, except as required by law."),
    ]

    y -= 50
    text_width = PAGE_WIDTH - 2*MARGIN - 35

    for i, (title, content) in enumerate(sections, 1):
        if y < 100:  # Need new page
            c.showPage()
            header_y = draw_header(c, logo_path)
            draw_footer(c)
            y = header_y - 40

        draw_section_number(c, MARGIN, y, i)
        c.setFillColor(NAVY)
        c.setFont("Helvetica-Bold", 11)
        c.drawString(MARGIN + 30, y, title)

        y -= 18
        c.setFillColor(TEXT_GRAY)
        c.setFont("Helvetica", 9)

        # Word wrap
        words = content.split()
        line = ""
        for word in words:
            test_line = line + word + " "
            if c.stringWidth(test_line, "Helvetica", 9) < text_width:
                line = test_line
            else:
                c.drawString(MARGIN + 5, y, line.strip())
                y -= 12
                line = word + " "
        if line:
            c.drawString(MARGIN + 5, y, line.strip())

        # Divider
        y -= 15
        c.setStrokeColor(ORANGE)
        c.setLineWidth(0.5)
        c.line(MARGIN, y, MARGIN + 100, y)
        y -= 20

    # ===== PAGE 2 =====
    c.showPage()
    header_y = draw_header(c, logo_path)
    draw_footer(c)
    y = header_y - 40

    sections_page2 = [
        ("No Warranty", "Services are provided \"as is\" and without warranties of any kind, express or implied. Consultant does not warrant that services will meet Client's expectations or achieve specific business outcomes."),
        ("Limitation of Liability", "To the maximum extent permitted by law, Consultant shall not be liable for any indirect, incidental, consequential, or special damages. Consultant's total liability under this Agreement shall not exceed the fees paid by Client under the applicable SOW."),
        ("Term & Termination", "This Agreement shall remain in effect until terminated by either party upon written notice. Upon termination, Client shall pay Consultant for all services performed up to the effective date of termination."),
        ("Governing Law", "This Agreement shall be governed by and construed in accordance with the laws of the State of Texas, without regard to conflict-of-law principles."),
        ("Entire Agreement", "This Agreement, together with any SOWs, constitutes the entire agreement between the parties and supersedes all prior discussions or understandings."),
    ]

    for i, (title, content) in enumerate(sections_page2, 6):
        draw_section_number(c, MARGIN, y, i)
        c.setFillColor(NAVY)
        c.setFont("Helvetica-Bold", 11)
        c.drawString(MARGIN + 30, y, title)

        y -= 18
        c.setFillColor(TEXT_GRAY)
        c.setFont("Helvetica", 9)

        words = content.split()
        line = ""
        for word in words:
            test_line = line + word + " "
            if c.stringWidth(test_line, "Helvetica", 9) < text_width:
                line = test_line
            else:
                c.drawString(MARGIN + 5, y, line.strip())
                y -= 12
                line = word + " "
        if line:
            c.drawString(MARGIN + 5, y, line.strip())

        y -= 15
        c.setStrokeColor(ORANGE)
        c.setLineWidth(0.5)
        c.line(MARGIN, y, MARGIN + 100, y)
        y -= 20

    # Signature section
    y -= 10
    c.setStrokeColor(NAVY)
    c.setLineWidth(1.5)
    c.line(MARGIN, y, PAGE_WIDTH - MARGIN, y)

    y -= 25
    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(MARGIN, y, "IN WITNESS WHEREOF")

    y -= 18
    c.setFont("Helvetica", 9)
    c.setFillColor(TEXT_GRAY)
    c.drawString(MARGIN, y, "The parties have executed this Agreement as of the Effective Date.")

    # Signature boxes
    y -= 35
    box_width = (PAGE_WIDTH - 2*MARGIN - 30) / 2
    box_height = 145

    # Consultant signature box
    c.setFillColor(LIGHT_GRAY)
    c.roundRect(MARGIN, y - box_height, box_width, box_height, 5, fill=1, stroke=0)

    sig_y = y - 20
    c.setFillColor(ORANGE)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(MARGIN + 15, sig_y, "Consultant")
    c.setStrokeColor(ORANGE)
    c.setLineWidth(1.5)
    c.line(MARGIN + 15, sig_y - 5, MARGIN + 100, sig_y - 5)

    sig_y -= 25
    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(MARGIN + 15, sig_y, "Coding the Future AI, LLC")

    sig_y -= 25
    c.setFont("Helvetica", 8)
    c.setFillColor(TEXT_GRAY)
    c.drawString(MARGIN + 15, sig_y, "Signature")
    draw_text_field(c, "consultant_signature", MARGIN + 15, sig_y - 18, box_width - 40, 16)

    sig_y -= 35
    c.drawString(MARGIN + 15, sig_y, "Name")
    draw_text_field(c, "consultant_name", MARGIN + 15, sig_y - 18, box_width - 40, 16, value="Tim Kitchens")

    sig_y -= 35
    c.drawString(MARGIN + 15, sig_y, "Title")
    draw_text_field(c, "consultant_title", MARGIN + 15, sig_y - 18, box_width - 40, 16)

    sig_y -= 35
    c.drawString(MARGIN + 15, sig_y, "Date")
    draw_text_field(c, "consultant_date", MARGIN + 15, sig_y - 18, 100, 16)

    # Client signature box
    client_x = MARGIN + box_width + 30
    c.setFillColor(LIGHT_GRAY)
    c.roundRect(client_x, y - box_height, box_width, box_height, 5, fill=1, stroke=0)

    sig_y = y - 20
    c.setFillColor(ORANGE)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(client_x + 15, sig_y, "Client")
    c.setStrokeColor(ORANGE)
    c.setLineWidth(1.5)
    c.line(client_x + 15, sig_y - 5, client_x + 70, sig_y - 5)

    sig_y -= 25
    c.setFillColor(NAVY)
    c.setFont("Helvetica", 8)
    c.setFillColor(TEXT_GRAY)
    c.drawString(client_x + 15, sig_y, "Company (from above)")

    sig_y -= 25
    c.drawString(client_x + 15, sig_y, "Signature")
    draw_text_field(c, "client_signature", client_x + 15, sig_y - 18, box_width - 40, 16)

    sig_y -= 35
    c.drawString(client_x + 15, sig_y, "Name")
    draw_text_field(c, "client_signer_name", client_x + 15, sig_y - 18, box_width - 40, 16)

    sig_y -= 35
    c.drawString(client_x + 15, sig_y, "Title")
    draw_text_field(c, "client_title", client_x + 15, sig_y - 18, box_width - 40, 16)

    sig_y -= 35
    c.drawString(client_x + 15, sig_y, "Date")
    draw_text_field(c, "client_date", client_x + 15, sig_y - 18, 100, 16)

    c.save()
    print(f"Created fillable PDF: {output_path}")


def get_default_paths():
    """Get default paths relative to the skill directory."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    skill_dir = os.path.dirname(script_dir)  # Parent of scripts/
    assets_dir = os.path.join(skill_dir, "assets")
    logo_path = os.path.join(assets_dir, "CTF-logo.jpg")
    return skill_dir, assets_dir, logo_path


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Generate branded CTFAI PDF documents")
    parser.add_argument("--output", "-o", help="Output PDF path (default: current directory)")
    parser.add_argument("--logo", help="Custom logo path (default: uses skill assets)")
    args = parser.parse_args()

    skill_dir, assets_dir, default_logo = get_default_paths()

    logo_path = args.logo if args.logo else default_logo
    output_path = args.output if args.output else "Consulting_Services_Agreement_CTFAI.pdf"

    if not os.path.exists(logo_path):
        print(f"Warning: Logo not found at {logo_path}")

    create_agreement_pdf(output_path, logo_path)
