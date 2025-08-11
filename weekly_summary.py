# file: weekly_summary.py
from flask import Flask, request, jsonify
import openai
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os
from dotenv import load_dotenv
load_dotenv(dotenv_path="api.env")

openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

def generate_gpt_insight(sales_summary):
    prompt = f"""
    You are a sales analyst. Here is the data for this week:

    Total Sales: ${sales_summary['Weekly_Sales']}

    Write a concise paragraph (3-4 sentences) giving insights and recommendations.
    """

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return response.choices[0].message["content"].strip()

def create_pdf_report(sales_summary, insights):
    filename = f"weekly_sales_{datetime.now().strftime('%Y%m%d')}.pdf"
    filepath = os.path.join("reports", filename)
    os.makedirs("reports", exist_ok=True)

    c = canvas.Canvas(filepath, pagesize=letter)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, 750, "Weekly Sales Report")

    c.setFont("Helvetica", 12)
    c.drawString(100, 720, f"Total Weekly Sales: ${sales_summary['Weekly_Sales']}")

    c.setFont("Helvetica-Bold", 14)
    c.drawString(100, 640, "Insights:")
    c.setFont("Helvetica", 12)
    text_object = c.beginText(100, 620)
    for line in insights.split("\n"):
        text_object.textLine(line)
    c.drawText(text_object)

    c.save()
    return filepath

@app.route("/generate_insight", methods=["POST"])
def generate_insight():
    data = request.json
    insights = generate_gpt_insight(data)
    pdf_path = create_pdf_report(data, insights)
    return jsonify({"insight": insights, "pdf_path": pdf_path})

if __name__ == "__main__":
    app.run(port=5000, debug=True)




from dotenv import load_dotenv
load_dotenv()
