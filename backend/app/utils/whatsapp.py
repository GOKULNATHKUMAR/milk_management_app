import urllib.parse

def build_whatsapp_message(summary: dict):
    msg = f"""
🥛 Milk Business Daily Summary
📅 Date: {summary['date']}

📥 Intake: {summary['total_intake_qty']} L
📤 Sold: {summary['total_sold_qty']} L
⚖ Balance: {summary['balance_qty']} L

💰 Intake Amount: ₹{summary['total_intake_amount']}
💵 Sales Amount: ₹{summary['total_sales_amount']}

📈 Profit: ₹{summary['profit']}
"""
    return urllib.parse.quote(msg.strip())


def generate_whatsapp_link(mobile: str, message: str):
    return f"https://wa.me/91{mobile}?text={message}"
