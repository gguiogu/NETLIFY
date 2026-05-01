import os

with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

old_link = 'href={`https://wa.me/213562208794?text=${encodeURIComponent("مرحباً، أريد طلب هذا المنتج:\\n" + url + "\\nالمجموع: " + result.price_dzd + " د.ج")}`}'

new_link = 'href={`https://wa.me/213562208794?text=${encodeURIComponent("مرحباً متجر Kouki Shop 👋 أريد تأكيد طلب هذا المنتج من فضلك:\\n\\n📦 المنتج: " + result.title + "\\n💰 السعر: " + result.price_dzd + " دج\\n🔗 الرابط: " + url)}`}'

if old_link in content:
    content = content.replace(old_link, new_link)
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(content)
    print("WhatsApp link format updated successfully.")
else:
    print("Could not find the exact old link string. Will try a more robust search.")
