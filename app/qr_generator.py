import qrcode
from qrcode.constants import ERROR_CORRECT_M

vcard = """BEGIN:VCARD
VERSION:3.0
N:Pheerunggee;Mahmad
FN:Mahmad Pheerunggee
ORG:Formation Électro Inc.
TITLE:Formateur
TEL;TYPE=WORK,VOICE:5146054275
EMAIL:info@formationelectro.com
ADR;TYPE=WORK:;;4030 Bd de la Côte Vertu #104;Saint-Laurent;QC;H4R 1V4;Canada
URL:http://www.formationelectro.com
END:VCARD
"""

def normalize_vcard(text: str) -> str:
    # vCard QR works best with CRLF line endings and no extra indentation
    lines = [line.strip() for line in text.strip().splitlines() if line.strip()]
    return "\r\n".join(lines) + "\r\n"

def make_qr(data: str, out_path: str = "vcard_qr.png") -> None:
    qr = qrcode.QRCode(
        version=None,                  # auto-fit
        error_correction=ERROR_CORRECT_M,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save(out_path)
    print(f"Saved: {out_path}")

if __name__ == "__main__":
    make_qr(normalize_vcard(vcard), "formation_electro_vcard_qr.png")
