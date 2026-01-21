#!/usr/bin/env python3
"""
Generic branded PDF renderer.
Takes a template + data (JSON/YAML) and outputs a branded PDF.

Usage:
    python render_pdf.py --template agreement --output contract.pdf
    python render_pdf.py --template sow --data sow_data.yaml --output sow.pdf
    python render_pdf.py --template custom.html --data data.json --output output.pdf
"""

import argparse
import json
import os
import sys
from pathlib import Path

import yaml
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML, CSS


def get_skill_paths():
    """Get paths relative to the skill directory."""
    script_dir = Path(__file__).parent.resolve()
    skill_dir = script_dir.parent
    return {
        "skill_dir": skill_dir,
        "templates_dir": skill_dir / "templates",
        "assets_dir": skill_dir / "assets",
        "css_path": skill_dir / "assets" / "brand.css",
        "logo_path": skill_dir / "assets" / "CTF-logo.jpg",
    }


def load_data(data_path: str) -> dict:
    """Load data from JSON or YAML file."""
    path = Path(data_path)
    if not path.exists():
        raise FileNotFoundError(f"Data file not found: {path}")

    content = path.read_text()
    if path.suffix in (".yaml", ".yml"):
        return yaml.safe_load(content) or {}
    elif path.suffix == ".json":
        return json.loads(content)
    else:
        # Try YAML first, then JSON
        try:
            return yaml.safe_load(content) or {}
        except yaml.YAMLError:
            return json.loads(content)


def get_default_data(template_name: str) -> dict:
    """Get default data for built-in templates."""
    if template_name == "agreement":
        return {
            "title": "Consulting Services Agreement",
            "doc_type": "Legal Agreement",
            "doc_name": "Consulting Services Agreement",
            "client_name": "",
            "effective_date": "",
            "sections": [
                {"title": "Services", "content": "Consultant will provide advisory, strategy, and related professional services as may be requested by Client and agreed upon in one or more written Statements of Work (\"SOWs\"). Services are advisory in nature and do not guarantee specific outcomes or results."},
                {"title": "Fees & Payment", "content": "Fees for services will be as specified in the applicable SOW. Unless otherwise stated, Consultant's standard rate will be specified in the applicable Statement of Work. Invoices are due within fifteen (15) days of receipt. For longer-term engagements, the Consultant may offer alternative pricing structures (e.g., prepaid blocks or packaged services) by mutual agreement and documented in a separate Statement of Work."},
                {"title": "Independent Contractor", "content": "Consultant is an independent contractor and not an employee, agent, or partner of Client. Nothing in this Agreement creates a partnership, joint venture, or employment relationship."},
                {"title": "Intellectual Property", "content": "Each party retains ownership of its pre-existing intellectual property. Consultant retains all right, title, and interest in its methodologies, frameworks, templates, workflows, prompts, tooling, and know-how, whether developed prior to or during the engagement. Subject to full payment, Client is granted a non-exclusive, perpetual, non-transferable license to use deliverables produced specifically for Client's internal business purposes."},
                {"title": "Confidentiality", "content": "Each party agrees to maintain the confidentiality of the other party's non-public, proprietary, or confidential information and to use such information solely for purposes of this engagement, except as required by law."},
                {"title": "No Warranty", "content": "Services are provided \"as is\" and without warranties of any kind, express or implied. Consultant does not warrant that services will meet Client's expectations or achieve specific business outcomes."},
                {"title": "Limitation of Liability", "content": "To the maximum extent permitted by law, Consultant shall not be liable for any indirect, incidental, consequential, or special damages. Consultant's total liability under this Agreement shall not exceed the fees paid by Client under the applicable SOW."},
                {"title": "Term & Termination", "content": "This Agreement shall remain in effect until terminated by either party upon written notice. Upon termination, Client shall pay Consultant for all services performed up to the effective date of termination."},
                {"title": "Governing Law", "content": "This Agreement shall be governed by and construed in accordance with the laws of the State of Texas, without regard to conflict-of-law principles."},
                {"title": "Entire Agreement", "content": "This Agreement, together with any SOWs, constitutes the entire agreement between the parties and supersedes all prior discussions or understandings."},
            ],
        }
    elif template_name == "sow":
        return {
            "title": "Statement of Work",
            "doc_type": "Statement of Work",
            "doc_name": "Statement of Work",
            "sow_title": "",
            "client_name": "",
            "effective_date": "",
            "sow_number": "",
            "sections": [
                {"title": "Scope of Services", "description": "Consultant will provide the following services as described in detail below. Services are advisory in nature and focus on AI strategy, implementation guidance, and knowledge transfer.", "show_field": True},
                {"title": "Deliverables", "description": "The following deliverables will be provided upon completion of services:", "show_field": True},
                {"title": "Timeline", "description": "Services will be performed according to the following schedule:", "show_field": True},
                {"title": "Fees & Payment", "description": "Client agrees to pay the following fees for services rendered under this SOW:", "show_field": True},
                {"title": "Out of Scope", "description": "The following items are explicitly excluded from this engagement and would require a separate SOW:", "show_field": True},
                {"title": "Assumptions", "description": "This SOW is based on the following assumptions. Changes to these assumptions may require adjustment to scope, timeline, or fees:", "show_field": True},
                {"title": "Acceptance", "description": "Deliverables will be deemed accepted unless Client provides written objection within five (5) business days of delivery.", "show_field": False},
            ],
        }
    return {}


def render_pdf(template_name: str, data: dict, output_path: str):
    """Render a template to PDF with given data."""
    paths = get_skill_paths()

    # Set up Jinja2 environment
    env = Environment(loader=FileSystemLoader(str(paths["templates_dir"])))

    # Determine template file
    if template_name in ("agreement", "sow"):
        template_file = f"{template_name}.html"
    elif template_name.endswith(".html"):
        template_file = template_name
    else:
        template_file = f"{template_name}.html"

    template = env.get_template(template_file)

    # Add asset paths to data
    data["css_path"] = paths["css_path"].as_uri()
    data["logo_path"] = paths["logo_path"].as_uri() if paths["logo_path"].exists() else None

    # Render HTML
    html_content = template.render(**data)

    # Convert to PDF
    html = HTML(string=html_content, base_url=str(paths["templates_dir"]))
    css = CSS(filename=str(paths["css_path"]))
    html.write_pdf(output_path, stylesheets=[css])

    print(f"Created: {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Render branded CTFAI PDFs from templates",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Built-in templates:
  agreement    Consulting Services Agreement
  sow          Statement of Work

Custom templates:
  Place .html files in the templates/ directory and reference by name.

Examples:
  %(prog)s --template agreement --output contract.pdf
  %(prog)s --template sow --data project.yaml --output sow.pdf
  %(prog)s --template custom.html --data data.json --output output.pdf
        """,
    )
    parser.add_argument("--template", "-t", required=True, help="Template name or file")
    parser.add_argument("--data", "-d", help="JSON or YAML file with template data")
    parser.add_argument("--output", "-o", required=True, help="Output PDF path")
    args = parser.parse_args()

    # Load data
    if args.data:
        data = load_data(args.data)
    else:
        data = {}

    # Merge with defaults for built-in templates
    template_name = args.template.replace(".html", "")
    defaults = get_default_data(template_name)
    merged_data = {**defaults, **data}

    # Render
    render_pdf(args.template, merged_data, args.output)


if __name__ == "__main__":
    main()
