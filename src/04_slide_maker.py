#!/usr/bin/env python3
"""
Fixed Version - PowerPoint Generator with Path Handling
"""

import argparse
import os
import sys
import tempfile
import shutil
import logging
from pathlib import Path
import pandas as pd
from pptx import Presentation
from pptx.util import Inches
import matplotlib.pyplot as plt
import matplotlib as mpl
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('slide_maker.log'),
        logging.StreamHandler()
    ]
)

def configure_matplotlib():
    """Set professional matplotlib styles"""
    mpl.rcParams['figure.facecolor'] = 'white'
    mpl.rcParams['axes.prop_cycle'] = mpl.cycler(color=['#2A5CAA', '#6CACE4', '#FFB81C'])
    mpl.rcParams['axes.titleweight'] = 'bold'

def validate_inputs(args):
    """Check all input files exist and are valid"""
    if not os.path.exists(args.valuation):
        logging.error(f"Valuation file not found: {args.valuation}")
        sys.exit(1)
        
    if args.template and not os.path.exists(args.template):
        logging.warning(f"Template not found, using default: {args.template}")
        args.template = None

def create_valuation_chart(df, output_path):
    """Generate DCF chart"""
    try:
        configure_matplotlib()
        plot_df = df[df.index != "Enterprise Value"].copy()
        plot_df['PV'] = plot_df['PV'] / 1e6  # Convert to millions
        
        fig, ax = plt.subplots(figsize=(10, 6))
        bars = ax.bar(plot_df.index.astype(str), plot_df['PV'], color='#2A5CAA')
        
        ax.set_title('DCF Valuation Components', pad=20)
        ax.set_ylabel('Present Value (USD millions)', labelpad=10)
        ax.grid(axis='y', linestyle='--', alpha=0.7)
        
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                    f'{height:,.0f}', ha='center', va='bottom', fontsize=9)
        
        plt.tight_layout()
        fig.savefig(str(output_path), dpi=150, bbox_inches='tight')  # Convert Path to string
        plt.close()
        
    except Exception as e:
        logging.error(f"Chart generation failed: {str(e)}")
        raise

def get_default_template():
    """Create a basic default template"""
    prs = Presentation()
    slide = prs.slides.add_slide(prs.slide_layouts[0])
    title = slide.shapes.title
    title.text = "Investment Thesis"
    return prs

def build_presentation(template_path, chart_path, valuation_path):
    """Create PowerPoint presentation"""
    try:
        # Convert Path objects to strings if needed
        template_path = str(template_path) if template_path else None
        chart_path = str(chart_path)
        
        if template_path and os.path.exists(template_path):
            prs = Presentation(template_path)
        else:
            prs = get_default_template()
        
        # Add slide with chart
        slide = prs.slides.add_slide(prs.slide_layouts[1])
        title = slide.shapes.title
        title.text = "Valuation Summary"
        
        # Add chart image (convert Path to string)
        left = Inches(0.5)
        top = Inches(1.5)
        slide.shapes.add_picture(str(chart_path), left, top, width=Inches(9))
        
        return prs
        
    except Exception as e:
        logging.error(f"Presentation build failed: {str(e)}")
        raise

def libreoffice_available():
    """Check if LibreOffice is installed"""
    return shutil.which("soffice") is not None
    
def convert_with_libreoffice(input_path, output_path):
    """Convert PPTX to PDF using LibreOffice"""
    try:
        import subprocess
        input_path = str(input_path)  # Convert Path to string
        output_dir = str(Path(output_path).parent)
        
        result = subprocess.run(
            ["soffice", "--headless", "--convert-to", "pdf", 
             input_path, "--outdir", output_dir],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode == 0:
            temp_pdf = Path(input_path).with_suffix('.pdf')
            if temp_pdf.exists():
                os.rename(str(temp_pdf), str(output_path))
                return True
        return False
        
    except Exception as e:
        logging.error(f"LibreOffice conversion error: {str(e)}")
        return False

def create_fallback_pdf(chart_path, output_path):
    """Create PDF directly when conversion fails"""
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.pdfgen import canvas
        
        c = canvas.Canvas(str(output_path), pagesize=letter)  # Convert Path to string
        c.setFont("Helvetica-Bold", 16)
        c.drawString(100, 750, "Valuation Summary")
        c.drawImage(str(chart_path), 100, 400, width=400, height=300)  # Convert Path to string
        c.setFont("Helvetica", 12)
        c.drawString(100, 380, "Note: Full presentation requires PowerPoint viewer")
        c.save()
        
    except Exception as e:
        logging.error(f"Fallback PDF creation failed: {str(e)}")
        raise

def main():
    parser = argparse.ArgumentParser(description="Pitchbook Generator")
    parser.add_argument("--template", help="PPTX template file")
    parser.add_argument("--valuation", required=True, help="Valuation Excel file")
    parser.add_argument("--output", required=True, help="Output PDF file")
    args = parser.parse_args()
    
    try:
        validate_inputs(args)
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            
            # Generate chart
            chart_path = tmpdir_path / "dcf_chart.png"
            dcf_data = pd.read_excel(args.valuation, sheet_name='DCF', index_col=0)
            create_valuation_chart(dcf_data, chart_path)
            
            # Build presentation
            pptx_path = tmpdir_path / "presentation.pptx"
            prs = build_presentation(args.template, chart_path, args.valuation)
            prs.save(str(pptx_path))  # Convert Path to string
            
            # Convert to PDF
            if libreoffice_available() and convert_with_libreoffice(pptx_path, output_path):
                logging.info("PDF successfully created via LibreOffice")
            else:
                logging.warning("Using fallback PDF method")
                create_fallback_pdf(chart_path, output_path)
                
        logging.info(f"Successfully created: {output_path}")
        
    except Exception as e:
        logging.error(f"Fatal error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()