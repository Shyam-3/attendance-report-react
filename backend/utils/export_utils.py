"""
Utilities for exporting attendance data to Excel and PDF with formatting.
Matches the layout shown in export_utils1.py (styled headers, auto widths, timestamped filenames),
while keeping the same public methods used by the app.
"""
import io
from datetime import datetime
import pandas as pd
from flask import make_response
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle


class ExportUtils:
    def _timestamp_for_filename(self) -> str:
        # Example: 01.10.2025 23 05 42
        return datetime.now().strftime("%d.%m.%Y %H %M %S")

    def generate_excel_export(self, data, filter_info=None, filename_prefix: str = "attendance"):
        """Generate formatted Excel from export-ready rows (list of dict)."""
        df = pd.DataFrame(data or [])

        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            sheet_name = 'Low Attendance Report'
            df.to_excel(writer, sheet_name=sheet_name, index=False)

            workbook = writer.book
            worksheet = writer.sheets[sheet_name]

            header_format = workbook.add_format({
                'bold': True,
                'text_wrap': True,
                'valign': 'top',
                'fg_color': '#D7E4BC',
                'border': 1,
            })

            # Apply header styling
            for col_num, value in enumerate(df.columns.values):
                worksheet.write(0, col_num, value, header_format)

            # Auto-fit columns
            for i, col in enumerate(df.columns):
                max_len = max(df[col].astype(str).apply(len).max() if not df.empty else 0, len(str(col))) + 2
                worksheet.set_column(i, i, max_len)

        output.seek(0)

        # Build dynamic filename based on filter_info
        if filter_info:
            filter_str = "_".join(str(f).replace(" ", "_").replace(":", "").replace(",", "").replace("|", "") for f in filter_info)
            filename = f"{filter_str}.xlsx"
        else:
            filename = "attendance.xlsx"
        
        # Sanitize filename to prevent header issues
        filename = filename.replace('"', '').replace("'", "")
        
        response = make_response(output.getvalue())
        response.headers['Content-Type'] = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        response.headers['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response

    def generate_pdf_export(self, records, filter_info=None, filename_prefix: str = "attendance"):
        """Generate formatted PDF table for AttendanceRecord rows."""
        output = io.BytesIO()
        doc = SimpleDocTemplate(output, pagesize=A4)

        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle', parent=styles['Heading1'], fontSize=18, spaceAfter=7, alignment=1
        )

        content = []
        content.append(Paragraph("Attendance Report", title_style))
        content.append(Spacer(1, 12))

        if filter_info:
            filter_text = "Filters Applied: " + " | ".join(filter_info)
            content.append(Paragraph(filter_text, styles['Normal']))
            content.append(Spacer(1, 12))

        table_data = [[
            'S.No', 'Registration No', 'Course Code', 'Course Name',
            'Attended', 'Total', 'Attendance %'
        ]]

        for i, r in enumerate(records or [], 1):
            table_data.append([
                str(i),
                r.student.registration_no,
                # r.student.name,
                r.course.course_code,
                r.course.course_name,
                str(r.attended_periods),
                str(r.conducted_periods),
                f"{r.attendance_percentage:.0f}",
            ])

        table = Table(table_data)
        table_style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 7),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ])

        # Row highlighting like the original utility
        for i, r in enumerate(records or [], 1):
            row_index = i
            if r.attendance_percentage < 65:
                table_style.add('BACKGROUND', (0, row_index), (-1, row_index), colors.lightcoral)
            elif r.attendance_percentage < 75:
                table_style.add('BACKGROUND', (0, row_index), (-1, row_index), colors.lightyellow)
            else:
                table_style.add('BACKGROUND', (0, row_index), (-1, row_index), colors.lightgreen)

        table.setStyle(table_style)
        content.append(table)
        content.append(Spacer(1, 20))
        content.append(Paragraph(
            f"Generated on: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')} | Total Records: {len(records or [])}",
            styles['Normal']
        ))
        doc.title = "Attendance Report"
        doc.build(content)
        output.seek(0)

        # Build dynamic filename
        if filter_info:
            filter_str = "_".join(str(f).replace(" ", "_").replace(":", "").replace(",", "").replace("|", "") for f in filter_info)
            filename = f"{filter_str}.pdf"
        else:
            filename = "attendance.pdf"
        
        # Sanitize filename to prevent header issues
        filename = filename.replace('"', '').replace("'", "")
        
        response = make_response(output.getvalue())
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response


