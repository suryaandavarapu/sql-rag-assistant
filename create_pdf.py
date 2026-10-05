from fpdf import FPDF

pdf = FPDF()
pdf.set_auto_page_break(auto=True, margin=15)
pdf.add_page()

# Title
pdf.set_font("Helvetica", "B", 20)
pdf.cell(0, 15, "SuperStore Business Policy Document", new_x="LMARGIN", new_y="NEXT", align="C")
pdf.set_font("Helvetica", "I", 11)
pdf.cell(0, 10, "Internal Reference Guide - FY 2024", new_x="LMARGIN", new_y="NEXT", align="C")
pdf.ln(5)

sections = [
    ("1. Discount Policy", [
        "Standard discount for Consumer segment is capped at 20% on all product categories.",
        "Corporate segment customers are eligible for discounts up to 30% on bulk orders above $500.",
        "Home Office segment receives a flat 15% discount on Office Supplies and Technology products.",
        "Discounts exceeding 40% require written approval from regional manager.",
        "Furniture category discounts are strictly limited to 20% due to high shipping costs.",
        "Seasonal discounts apply only in Q4 (October to December) and must not exceed 35%.",
        "Any discount above 50% is prohibited and will result in automatic order cancellation.",
    ]),
    ("2. Shipping and Delivery Policy", [
        "Standard Class shipping is the default mode for all orders below $200.",
        "First Class shipping is available for orders above $500 at no additional cost.",
        "Same Day delivery is available only in West and East regions for Technology products.",
        "Furniture orders require a minimum of 5 business days for delivery regardless of ship mode.",
        "Corporate customers receive free Second Class shipping on all orders.",
        "Orders above $1000 automatically qualify for First Class shipping.",
        "Shipping costs are absorbed by the company for Home Office segment in South region.",
    ]),
    ("3. Regional Sales Strategy", [
        "West region is the primary revenue driver and accounts for 32% of total company sales.",
        "East region focuses on Corporate and Consumer segments with emphasis on Technology products.",
        "Central region has shown consistent losses in Furniture category due to high discount rates.",
        "South region is an emerging market with focus on expanding Home Office segment.",
        "Regional managers are responsible for maintaining profit margins above 10% in their territory.",
        "West region has a dedicated key accounts team for Corporate customers above $50000 annual spend.",
        "Central region discount approvals are subject to stricter controls due to historical profit losses.",
    ]),
    ("4. Product Category Guidelines", [
        "Technology products carry the highest profit margin at an average of 17% net margin.",
        "Furniture category is the lowest margin category at an average of 6% net margin.",
        "Office Supplies are high volume low margin products with average margin of 12%.",
        "Sub-category Tables within Furniture has been flagged for review due to consistent losses.",
        "Copiers and Phones are the top performing sub-categories within Technology.",
        "Bookcases and Chairs are recommended for promotional focus in Q1 and Q2.",
        "Binders and Paper are the highest volume products in Office Supplies category.",
    ]),
    ("5. Customer Segment Policy", [
        "Consumer segment represents 52% of total orders and is the largest customer base.",
        "Corporate segment generates highest average order value at $850 per order.",
        "Home Office segment has shown 18% growth in FY2023 and is a priority for FY2024.",
        "Consumer segment customers are eligible for loyalty discounts after 5 repeat purchases.",
        "Corporate accounts with annual spend above $10000 are assigned a dedicated account manager.",
        "All segment complaints must be resolved within 48 hours as per customer satisfaction policy.",
        "Home Office customers receive quarterly business reviews from their assigned sales representative.",
    ]),
    ("6. Profit and Loss Guidelines", [
        "Any order resulting in a loss above $500 must be reported to the finance team immediately.",
        "Products with consistent negative profit over 3 consecutive quarters are flagged for discontinuation.",
        "Regional profit targets for FY2024 are set at 15% growth over FY2023 actuals.",
        "Loss making orders due to excessive discounts are charged back to the sales representative.",
        "Finance team conducts monthly profit audits across all regions and product categories.",
        "Orders with discount above 40% and negative profit are automatically escalated for review.",
        "Annual profit target for the company is $350000 with West region contributing 35% of that target.",
    ]),
]

for title, points in sections:
    pdf.set_font("Helvetica", "B", 14)
    pdf.set_fill_color(230, 230, 230)
    pdf.cell(0, 10, title, new_x="LMARGIN", new_y="NEXT", fill=True)
    pdf.ln(2)
    pdf.set_font("Helvetica", "", 11)
    for point in points:
        pdf.multi_cell(0, 8, f"  - {point}")
        pdf.ln(1)
    pdf.ln(5)

pdf.output("data/report.pdf")
print("PDF created: data/report.pdf")