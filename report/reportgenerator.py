from fpdf import FPDF
import matplotlib.pyplot as plt


def draw_conso_table(pdf, fields):
    # Header
    pdf.set_font("Arial", size=11, style="B")
    pdf.cell(60, 6, txt=" Groupe", ln=0, align='L', border=True)
    pdf.cell(45, 6, txt=" Consommation", ln=1, align='L', border=True)

    pdf.set_font("Arial", size=11)
    for field in fields:
        pdf.cell(60, 6, txt=f" {field['label']}", ln=0, align='L', border=True)
        pdf.cell(45, 6, txt=f"{field['value']}   kWh ", ln=1, align='R', border=True)


def generate_report(data):

    # Draw pie graphs
    for i, table in enumerate(data["tables"]):
        values = [field["value"] for field in table["fields"] if field["pie"] and field["value"] > 0]
        labels = [field["label"] for field in table["fields"] if field["pie"] and field["value"] > 0]

        # Create a pieplot
        plt.pie(values, labels=labels, radius=1, textprops={"fontsize": 15, "fontfamily": "Arial"}, labeldistance=1.2)

        # add a circle at the center to transform it in a donut chart
        my_circle = plt.Circle((0, 0), 0.65, color='white')
        p = plt.gcf()
        p.gca().add_artist(my_circle)
        
        # plt.title(pie["title"], fontdict={"fontsize": 25, "fontfamily": "Arial", "fontweight": 600})
        
        plt.savefig(f'pie_{i}.png')
        plt.close()
        

    pdf = FPDF()

    # Add a page
    pdf.add_page()


    # Draw the title
    pdf.set_font("Arial", size=16, style="B")
    pdf.cell(0, 12, txt=f"{data['maintitle']}     {data['date']}", ln=1, align='C', border=True)
    pdf.ln()

    pdf.set_left_margin(30)


    # Draw the tables
    for i, table in enumerate(data["tables"]):
        pdf.set_font("Arial", size=13, style="B")
        pdf.cell(0, 15, txt=table["title"], ln=1, align='L')
        draw_conso_table(pdf, table["fields"])
        pdf.ln()
        pdf.image(f'pie_{i}.png', h=62) 
        

    # save the pdf with name .pdf
    pdf.output("GFG.pdf")

