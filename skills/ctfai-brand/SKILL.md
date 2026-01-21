---
name: ctf-claude-code-primitives:ctfai-brand
description: Apply Coding the Future with AI brand styling. Use this skill when the user asks to create branded content, apply brand colors, style documents with CTFAI branding, create presentations/websites/themes with company branding, or generate branded PDFs with fillable fields.
user-invocable: true
---

# CTFAI Brand Skill

Apply Coding the Future with AI (CTFAI) brand styling to any artifact. Generate branded PDFs with real fillable AcroForm fields.

## Brand Identity

**Company**: Coding the Future with AI (CTFAI)
**Principal**: Tim Kitchens
**Domain**: AI strategy consulting, implementation, and education

**Voice & Tone**:
- Professional but approachable
- Confident without arrogance
- Clear and direct - avoid jargon unless speaking to technical audience
- Forward-looking - emphasize transformation and possibilities
- Favor active voice

---

## Color Palette

| Name | Hex | Usage |
|------|-----|-------|
| Navy | `#1a365d` | Headers, primary brand |
| Orange | `#dd6b20` | Accents, CTAs |
| Blue | `#3182ce` | Links, secondary |
| Purple | `#6b46c1` | AI/innovation themes |
| Light Gray | `#f7fafc` | Backgrounds |
| Dark Gray | `#2d3748` | Body text |

---

## Typography

**Primary**: Helvetica (PDF-safe, no font embedding needed)

**Hierarchy**:
- H1: 18pt, Helvetica-Bold, Navy
- H2: 14pt, Helvetica-Bold, Navy
- H3: 12pt, Helvetica-Bold, Dark Gray
- Body: 11pt, Helvetica, Dark Gray
- Small: 9pt, Helvetica, Gray

---

## Visual Patterns

**Header**:
- Navy background bar spanning full width
- White text for document title
- Logo in top-left corner
- Orange accent line below (3px)

**Sections**:
- Navy section titles
- Orange left border (4px)
- Generous whitespace between sections

**Footer**:
- Light gray background
- Orange accent line above
- Centered text

---

## Assets

| Asset | Path | Usage |
|-------|------|-------|
| Logo | `<skill_dir>/assets/CTF-logo.jpg` | Headers, letterheads |
| Banner | `<skill_dir>/assets/CTF-banner.png` | Hero sections |
| CSS | `<skill_dir>/assets/brand.css` | Web artifacts |

---

## Script Management

**Scripts go in**: `<skill_dir>/generated/` (implementation detail, hidden from user)

**PDFs go where the user wants**: Always ask "Where would you like me to save the PDF?" Default to current working directory if user says "here" or doesn't specify a preference.

**Before generating a new script**:
1. Check `<skill_dir>/generated/` for existing scripts
2. If a similar script exists (e.g., `generate_csa_pdf.py` for consulting agreements), reuse/adapt it
3. Only create a new script if the document type is genuinely different

**Cleanup**: If `generated/` contains more than 5 scripts, notify the user: "There are X scripts in the generated folder. Would you like me to clean up old ones?"

---

## PDF Generation with reportlab AcroForm

**CRITICAL: Always use the skill's virtual environment. NEVER install to global Python.**

**First-time setup** (creates venv in skill directory - cross-platform):
```bash
# Find skill directory first, then:
cd <skill_dir>
python3 -m venv .venv
# On macOS/Linux:
.venv/bin/pip install reportlab
# On Windows:
.venv\Scripts\pip install reportlab
```

**Running scripts** (always use the venv):
```bash
# macOS/Linux:
<skill_dir>/.venv/bin/python <skill_dir>/generated/script_name.py
# Windows:
<skill_dir>\.venv\Scripts\python <skill_dir>\generated\script_name.py
```

### Creating Fillable Text Fields

```python
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import HexColor

# Brand colors
NAVY = HexColor("#1a365d")
ORANGE = HexColor("#dd6b20")
LIGHT_GRAY = HexColor("#f7fafc")
DARK_GRAY = HexColor("#2d3748")
WHITE = HexColor("#ffffff")

c = canvas.Canvas("output.pdf", pagesize=letter)
form = c.acroForm

# Text field with brand styling
form.textfield(
    name='client_name',           # Unique field identifier
    tooltip='Enter client name',  # Hover help text
    x=150, y=700,                 # Position (points from bottom-left)
    width=300, height=20,         # Field size
    borderStyle='underlined',     # Options: solid, inset, bevelled, underlined
    borderColor=NAVY,
    fillColor=WHITE,
    textColor=DARK_GRAY,
    fontSize=11,
    fontName='Helvetica',
    forceBorder=True
)
```

### Multiline Text Area

```python
form.textfield(
    name='scope_notes',
    x=72, y=400,
    width=468, height=100,
    fieldFlags='multiline',       # Enables multi-line input
    borderColor=LIGHT_GRAY,
    fillColor=WHITE,
    textColor=DARK_GRAY,
    forceBorder=True
)
```

### Key Parameters

| Parameter | Purpose |
|-----------|---------|
| `name` | Unique field ID (required) |
| `value` | Pre-filled text |
| `x`, `y` | Position in points (72 points = 1 inch) |
| `width`, `height` | Field dimensions |
| `maxlen` | Character limit |
| `borderStyle` | solid, inset, bevelled, underlined |
| `fieldFlags` | multiline, password, readOnly, required |
| `tooltip` | Hover text |
| `forceBorder` | Always show border |

### Drawing Branded Elements

```python
# Navy header bar
c.setFillColor(NAVY)
c.rect(0, 756, 612, 56, fill=True, stroke=False)

# Orange accent line
c.setStrokeColor(ORANGE)
c.setLineWidth(3)
c.line(0, 756, 612, 756)

# Logo
c.drawImage("path/to/CTF-logo.jpg", 36, 765, width=72, height=36,
            preserveAspectRatio=True, mask='auto')

# White text in header
c.setFillColor(WHITE)
c.setFont("Helvetica-Bold", 14)
c.drawCentredString(306, 778, "CONSULTING SERVICES AGREEMENT")

# Section title with orange left border
c.setStrokeColor(ORANGE)
c.setLineWidth(4)
c.line(72, 650, 72, 630)
c.setFillColor(NAVY)
c.setFont("Helvetica-Bold", 12)
c.drawString(80, 635, "1. Scope of Services")

# Body text
c.setFillColor(DARK_GRAY)
c.setFont("Helvetica", 11)
c.drawString(72, 610, "Consultant agrees to provide the following services:")

# Finalize page and save
c.showPage()
c.save()
```

### Complete Minimal Example

```python
import sys
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import HexColor

# Cross-platform paths - script lives in <skill_dir>/generated/
SCRIPT_DIR = Path(__file__).parent
SKILL_DIR = SCRIPT_DIR.parent
ASSETS_DIR = SKILL_DIR / "assets"

NAVY = HexColor("#1a365d")
ORANGE = HexColor("#dd6b20")
WHITE = HexColor("#ffffff")
DARK_GRAY = HexColor("#2d3748")

def create_branded_form(output_path, logo_path):
    c = canvas.Canvas(str(output_path), pagesize=letter)
    width, height = letter  # 612 x 792 points

    # Header
    c.setFillColor(NAVY)
    c.rect(0, height - 60, width, 60, fill=True, stroke=False)
    c.setStrokeColor(ORANGE)
    c.setLineWidth(3)
    c.line(0, height - 60, width, height - 60)

    # Logo
    c.drawImage(str(logo_path), 36, height - 50, width=80, height=40,
                preserveAspectRatio=True, mask='auto')

    # Doc title
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width/2, height - 38, "CONSULTING AGREEMENT")

    # Form field: Client Name
    c.setFillColor(DARK_GRAY)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(72, height - 100, "Client Name:")

    form = c.acroForm
    form.textfield(
        name='client_name',
        x=170, y=height - 112,
        width=350, height=20,
        borderStyle='underlined',
        borderColor=NAVY,
        textColor=DARK_GRAY,
        forceBorder=True
    )

    # Form field: Date
    c.drawString(72, height - 140, "Effective Date:")
    form.textfield(
        name='effective_date',
        x=170, y=height - 152,
        width=150, height=20,
        borderStyle='underlined',
        borderColor=NAVY,
        textColor=DARK_GRAY,
        forceBorder=True
    )

    c.showPage()
    c.save()
    print(f"Created: {output_path}")

if __name__ == "__main__":
    # Accept output path as command line argument
    output_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd() / "agreement.pdf"
    create_branded_form(output_path, ASSETS_DIR / "CTF-logo.jpg")
```

---

## Workflow

When user requests a branded PDF:

1. **Check for existing scripts**: Look in `<skill_dir>/generated/` for reusable scripts
2. **Understand the need**: Interview user about document purpose, sections, what fields should be fillable
3. **Ask output location**: "Where would you like me to save the PDF?" (default: current working directory)
4. **Propose structure**: List sections, identify fillable fields (client name, date, signature, etc.)
5. **Get approval**: User confirms structure before generation
6. **Ensure venv exists**: If `.venv` doesn't exist in skill directory, create it and install reportlab
7. **Generate code**: Write Python script to `<skill_dir>/generated/` (pass output path as argument)
8. **Execute with venv**: Run script using `<skill_dir>/.venv/bin/python script.py <output_path>`
9. **Deliver**: Confirm PDF location to user

**The goal is a reusable template** - user fills in fields for each new client, not regenerating the PDF.

---

## For HTML/Web Artifacts

Include `assets/brand.css` or apply these CSS variables:

```css
:root {
  --ctfai-navy: #1a365d;
  --ctfai-orange: #dd6b20;
  --ctfai-blue: #3182ce;
  --ctfai-purple: #6b46c1;
  --ctfai-light: #f7fafc;
  --ctfai-dark: #2d3748;
  --ctfai-white: #ffffff;
}
```
