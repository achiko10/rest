import qrcode

# ეს არის მისამართი, რომელსაც QR კოდი "დამალავს"
# როცა საიტს ინტერნეტში გაუშვებ (მაგ. Render.com-ზე), აქ იმ ლინკს ჩაწერ
link = "http://192.168.100.4" 

# QR კოდის პარამეტრების გამართვა
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)

qr.add_data(link)
qr.make(fit=True)

# სურათის შექმნა
img = qr.make_image(fill_color="black", back_color="white")

# შენახვა ფაილად
img.save("restaurant_review_qr.png")

print("✅ QR კოდი წარმატებით შეიქმნა! ნახე ფაილი: restaurant_review_qr.png")