import qrcode


def generate_qr():
    vcard = """BEGIN:VCARD
                    VERSION:3.0
                    N:Pheerunggee;Mahmad
                    FN:Mahmad Pheerunggee
                    ORG:Formation Électro Inc.
                    TITLE:Formateur
                    TEL;TYPE=WORK,VOICE:5146054275
                    EMAIL:info@formationelectro.com
                    ADR;TYPE=WORK:;;4030 Bd de la Côte Vertu;Saint-Laurent;QC;H4R 1V4;Canada
                    URL:http://www.formationelectro.com
                END:VCARD
            """

    # Create a QRCode instance
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    # Add the vCard data
    qr.add_data(vcard)
    qr.make(fit=True)

    # Generate the QR code image
    img = qr.make_image(fill='black', back_color='white')

    # Save the image
    img.save("formation_electro_vcard_qr.png")


if __name__ == "__main__":
    generate_qr()
