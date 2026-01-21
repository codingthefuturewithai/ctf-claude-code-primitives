---
name: ctf-claude-code-primitives:ctfai-brand
description: Apply Coding the Future with AI brand styling. Use this skill when the user asks to create branded content, apply brand colors, style documents with CTFAI branding, create presentations/websites/themes with company branding, or generate branded PDFs.
user-invocable: true
---

# Coding the Future with AI - Brand Guidelines

Apply consistent branding to any artifact: PDFs, websites, presentations, themes, and more.

## Brand Colors

| Name | Hex | CSS Variable | Usage |
|------|-----|--------------|-------|
| Navy | `#1B2838` | `--navy` | Primary backgrounds, text |
| Orange | `#F5A623` | `--orange` | Primary accent, CTAs, section numbers |
| Blue | `#7DD3FC` | `--blue` | Secondary accent, labels |
| Purple | `#C084FC` | `--purple` | Tertiary accent, gradients |
| White | `#FFFFFF` | `--white` | Text on dark backgrounds |
| Light Gray | `#F0F5FA` | `--light-gray` | Light backgrounds, boxes |
| Text Gray | `#2d3748` | `--text-gray` | Body text |

## Typography

- **Headings**: System sans-serif, bold
- **Body**: System sans-serif, regular
- **Sizes**: H1: 22pt, H2: 16pt, Body: 10pt

## Visual Patterns

- **Header**: Navy background, logo left, gradient bar (orange→blue→purple)
- **Sections**: Orange numbered circles, navy titles
- **Info boxes**: Light gray with orange left border
- **Footer**: Navy with tagline

## Tagline

> "Empowering teams with AI tools, knowledge, and strategy"

---

## Assets

| Asset | Path | Usage |
|-------|------|-------|
| Logo | `assets/CTF-logo.jpg` | Headers, dark backgrounds (45px typical) |
| Banner | `assets/CTF-banner.png` | Hero sections, social covers |
| Brand CSS | `assets/brand.css` | All brand styles for HTML/PDF |

---

## PDF Generation (Template-Based)

Generate branded PDFs using HTML templates + CSS. Easy to customize or create new templates.

### First-Time Setup

If `.venv` doesn't exist in the skill directory:
```bash
python scripts/bootstrap.py
```

### Usage

```bash
# Built-in templates
.venv/bin/python scripts/render_pdf.py --template agreement --output contract.pdf
.venv/bin/python scripts/render_pdf.py --template sow --output sow.pdf

# With custom data
.venv/bin/python scripts/render_pdf.py --template sow --data project.yaml --output sow.pdf

# Custom template
.venv/bin/python scripts/render_pdf.py --template mytemplate.html --data data.json --output output.pdf
```

### Built-in Templates

| Template | Description |
|----------|-------------|
| `agreement` | Consulting Services Agreement (10 sections) |
| `sow` | Statement of Work (7 sections with detail fields) |

### Data Files (YAML/JSON)

Override template defaults with a data file:

```yaml
# For agreement
client_name: "Acme Corp"
effective_date: "2026-01-21"
sections:
  - title: "Custom Section"
    content: "Custom content here"

# For sow
sow_title: "AI Strategy Session"
client_name: "Acme Corp"
sow_number: "SOW-001"
sections:
  - title: "Scope"
    description: "We will provide..."
    items:
      - "Strategy assessment"
      - "Implementation roadmap"
```

### Creating Custom Templates

1. Create an HTML file in `templates/`
2. Extend `base.html` for header/footer/branding
3. Use Jinja2 syntax for dynamic content
4. Reference with `--template yourtemplate.html`

Example:
```html
{% extends "base.html" %}
{% block content %}
<h1>{{ title }}</h1>
<p>{{ description }}</p>
{% endblock %}
```

### File Structure

```
skills/ctfai-brand/
├── SKILL.md
├── assets/
│   ├── CTF-logo.jpg
│   ├── CTF-banner.png
│   └── brand.css          # All brand styles
├── templates/
│   ├── base.html          # Base template (header, footer)
│   ├── agreement.html     # Consulting agreement
│   └── sow.html           # Statement of work
└── scripts/
    ├── bootstrap.py       # Set up venv
    └── render_pdf.py      # Generic renderer
```
