import argparse
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.units import inch

def create_teaser(output):
    doc = SimpleDocTemplate(output, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    # Header
    story.append(Paragraph("CONFIDENTIAL", styles["Heading1"]))
    story.append(Spacer(1, 0.2*inch))
    story.append(Paragraph("11Street Korea Divestiture", styles["Title"]))
    story.append(Spacer(1, 0.3*inch))
    
    # Body
    content = [
        "Transaction Overview:",
        "- Acquirer: Sea Limited (NYSE: SE)",
        "- Target: 11Street Korea (SK Telecom subsidiary)",
        "- Deal Value: ~$2.3 billion",
        "- Structure: 60% cash + 40% stock",
        "- Synergies: $75 million estimated",
        "",
        "Strategic Rationale:",
        "- Expands SEA's presence in Korean e-commerce market",
        "- Cross-border logistics synergies",
        "- Diversification from gaming revenue"
    ]
    
    for line in content:
        story.append(Paragraph(line, styles["BodyText"]))
        story.append(Spacer(1, 0.1*inch))
    
    doc.build(story)

def create_brief(output):
    doc = SimpleDocTemplate(output, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    story.append(Paragraph("Macro & Geopolitical Brief", styles["Title"]))
    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph("Korea-Singapore Cross-Border M&A", styles["Heading2"]))
    story.append(Spacer(1, 0.2*inch))
    
    content = [
        "Key Economic Indicators:",
        "- Korea GDP Growth: 2.6% (2024 est.)",
        "- Singapore GDP Growth: 3.2% (2024 est.)",
        "- USD/KRW Exchange Rate: 1,350",
        "- USD/SGD Exchange Rate: 1.36",
        "",
        "Regulatory Considerations:",
        "- Korea FTC approval required",
        "- Singapore MAS notification",
        "- Cross-border data transfer regulations",
        "",
        "Geopolitical Factors:",
        "- US-China trade tensions impact",
        "- Regional supply chain diversification",
        "- Digital economy cooperation agreements"
    ]
    
    for line in content:
        story.append(Paragraph(line, styles["BodyText"]))
        story.append(Spacer(1, 0.1*inch))
    
    doc.build(story)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PDF Writer")
    parser.add_argument("--type", choices=["teaser", "brief"], required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    
    if args.type == "teaser":
        create_teaser(args.output)
    else:
        create_brief(args.output)
    
    print(f"✅ {args.type} saved to {args.output}")