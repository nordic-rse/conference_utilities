from datetime import date
import json
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
import click


def spacing(pdf, n=1):
    for _ in range(n):
        pdf.p_markup("&nbsp;")


@click.command()
@click.option("--participant", prompt="Participants full name")
def generate_visa_invitation_letter(participant):
    with open("config.json") as f:
        config = json.load(f)
    
    sender_name = config["sender_name"]
    sender_email = config["sender_email"]
    sender_position = config["sender_position"]
    sender_organization = config["organization"]
    organization = config["organization"]
    conference_name = config["conference_name"]
    conference_dates = config["conference_dates"]
    conference_purpose = config["conference_purpose"]

    if not sender_name:
        raise ValueError("Set sender name and details in config.json")

    if not participant:
        participant = input("Enter the participant's full name: ")

    try:
        signature = Image('signature.png', 160, 40)
    except FileNotFoundError:
        raise FileNotFoundError("Please create a signature image and save it as signature.png")

    doc = SimpleDocTemplate("Invitation_Letter.pdf", pagesize=letter)
    styles = getSampleStyleSheet()
    Story = []

    Story.append(Paragraph(f"{sender_name}", styles['Normal']))
    Story.append(Spacer(1, 6))
    Story.append(Paragraph(f"{organization}", styles['Normal']))
    Story.append(Spacer(1, 6))
    Story.append(Paragraph(f"{sender_email}", styles['Normal']))
    Story.append(Spacer(1, 6))
    Story.append(Paragraph(date.today().strftime("%B %d, %Y"), styles['Normal']))
    Story.append(Spacer(1, 12))

    Story.append(Paragraph(f"Subject: Invitation Letter for {conference_name}", styles['Heading2']))
    Story.append(Spacer(1, 12))

    Story.append(Paragraph(f"Dear {participant},", styles['Normal']))
    Story.append(Spacer(1, 6))
    Story.append(Paragraph(f"On behalf of {organization}, I am delighted to extend an invitation for you to attend the {conference_name}, which will take place on {conference_dates}.", styles['Normal']))
    Story.append(Spacer(1, 6))
    Story.append(Paragraph(f"The purpose of this conference is {conference_purpose}.", styles['Normal']))
    Story.append(Spacer(1, 6))
    Story.append(Paragraph("Kind Regards,", styles['Normal']))
    Story.append(Spacer(1, 6))
    signature = Image('signature.png', 160, 40)
    signature.hAlign = 'LEFT'
    Story.append(signature)
    Story.append(Paragraph(f"{sender_name}", styles['Normal']))
    Story.append(Spacer(1, 6))
    Story.append(Paragraph(f"{sender_position}", styles['Normal']))
    Story.append(Spacer(1, 6))
    Story.append(Paragraph(f"{sender_organization}", styles['Normal']))

    doc.build(Story)



if __name__ == "__main__":
    generate_visa_invitation_letter()