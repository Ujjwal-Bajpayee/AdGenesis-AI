import os
from typing import Dict, Any
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from app.core.logger import logger

class PDFExporter:
    def generate_pdf_report(self, analysis_data: Dict[str, Any], output_path: str) -> str:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        doc = SimpleDocTemplate(
            output_path,
            pagesize=letter,
            rightMargin=36,
            leftMargin=36,
            topMargin=36,
            bottomMargin=36
        )

        styles = getSampleStyleSheet()
        
        title_style = ParagraphStyle(
            'ReportTitle',
            parent=styles['Heading1'],
            fontSize=22,
            leading=26,
            textColor=colors.HexColor('#1E293B'),
            spaceAfter=12
        )
        
        h2_style = ParagraphStyle(
            'ReportH2',
            parent=styles['Heading2'],
            fontSize=14,
            leading=18,
            textColor=colors.HexColor('#2563EB'),
            spaceBefore=12,
            spaceAfter=6
        )

        body_style = ParagraphStyle(
            'ReportBody',
            parent=styles['Normal'],
            fontSize=10,
            leading=14,
            textColor=colors.HexColor('#334155'),
            spaceAfter=8
        )

        story = []

        title_text = f"AdGenesis AI - Marketing Intelligence Report"
        story.append(Paragraph(title_text, title_style))
        story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor('#2563EB'), spaceAfter=15))

        goal = analysis_data.get('campaign_goal', 'Direct Response')
        filename = analysis_data.get('video_filename', 'marketing_creative.mp4')
        meta_text = f"<b>Video File:</b> {filename} &nbsp;&nbsp;|&nbsp;&nbsp; <b>Campaign Goal:</b> {goal}"
        story.append(Paragraph(meta_text, body_style))
        story.append(Spacer(1, 10))

        story.append(Paragraph("1. Executive Summary & Predictions", h2_style))
        pred = analysis_data.get('prediction', {})
        
        pred_table_data = [
            ["Metric", "Estimated Performance"],
            ["Overall Quality Score", f"{pred.get('overall_quality_score', 0)} / 100"],
            ["Expected Engagement Rate", str(pred.get('expected_engagement_rate', 'N/A'))],
            ["Expected Watch Time", str(pred.get('expected_watch_time_seconds', 'N/A'))],
            ["Expected Click-Through Rate (CTR)", str(pred.get('expected_ctr', 'N/A'))],
            ["Expected Conversion Lift", str(pred.get('expected_conversions_estimate', 'N/A'))]
        ]
        
        t = Table(pred_table_data, colWidths=[200, 300])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#F1F5F9')),
            ('TEXTCOLOR', (0,0), (-1,0), colors.HexColor('#0F172A')),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
            ('TOPPADDING', (0,0), (-1,-1), 6),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ]))
        story.append(t)
        story.append(Spacer(1, 12))

        reasoning = pred.get('reasoning', '')
        if reasoning:
            story.append(Paragraph(f"<b>Predictive Rationale:</b> {reasoning}", body_style))
            story.append(Spacer(1, 10))

        story.append(Paragraph("2. Creative Evaluation & Diagnostics", h2_style))
        synth = analysis_data.get('creative_synthesis', {})
        story.append(Paragraph(f"<b>Opening Hook:</b> {synth.get('hook_evaluation', 'N/A')}", body_style))
        story.append(Paragraph(f"<b>Storytelling Quality:</b> {synth.get('storytelling_quality', 'N/A')}", body_style))
        story.append(Paragraph(f"<b>Brand Messaging:</b> {synth.get('brand_messaging', 'N/A')}", body_style))
        
        strengths = synth.get('strengths', [])
        if strengths:
            story.append(Paragraph("<b>Key Strengths:</b>", body_style))
            for st in strengths:
                story.append(Paragraph(f"• {st}", body_style))
                
        weaknesses = synth.get('weaknesses', [])
        if weaknesses:
            story.append(Paragraph("<b>Key Weaknesses:</b>", body_style))
            for wk in weaknesses:
                story.append(Paragraph(f"• {wk}", body_style))

        story.append(Spacer(1, 10))

        story.append(Paragraph("3. Optimization Recommendations", h2_style))
        recs = analysis_data.get('recommendations', {})
        story.append(Paragraph(f"<b>Recommended Hook:</b> {recs.get('better_hook', 'N/A')}", body_style))
        story.append(Paragraph(f"<b>Recommended CTA:</b> {recs.get('better_cta', 'N/A')}", body_style))
        story.append(Paragraph(f"<b>Recommended Pacing:</b> {recs.get('better_pacing', 'N/A')}", body_style))

        story.append(Spacer(1, 10))

        story.append(Paragraph("4. Budget Allocation Strategy", h2_style))
        budget = analysis_data.get('budget_recommendation', {})
        story.append(Paragraph(f"<b>Recommended Allocation Tier:</b> {budget.get('recommended_budget_tier', 'Standard')}", body_style))
        story.append(Paragraph(f"<b>Strategic Justification:</b> {budget.get('justification', 'N/A')}", body_style))

        doc.build(story)
        return output_path

pdf_exporter = PDFExporter()
