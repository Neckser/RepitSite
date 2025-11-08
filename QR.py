import qrcode
import wifi_qrcode_generator.generator
import io

def generate_qr_link(link_url):
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
    qr.add_data(link_url)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='White')
    with io.BytesIO() as output:
        img.save(output, format='PNG')
        return output.getvalue()
    
print("Hello World")