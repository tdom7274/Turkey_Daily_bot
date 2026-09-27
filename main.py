import logging
import os
from urllib.parse import quote

import telebot
from telebot import types
from telebot.apihelper import ApiTelegramException


BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
if not BOT_TOKEN:
    raise RuntimeError("TELEGRAM_BOT_TOKEN is not set.")

SITE_URL = "https://www.dailytoursincappadocia.com/en/"
WHATSAPP_NUMBER = "905453216003"
PHONE_DISPLAY = "+90 545 321 60 03"
INSTAGRAM_URL = ""
GETYOURGUIDE_URL = ""
VIATOR_URL = ""
SHOW_PHOTOS = False
BRAND = "Türkiye Günlük"

bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")

TOURS = {
    "balloon": {
        "tr": (
            "Sıcak Hava Balonu Turu", "€225+", "3–4 saat (≈1 saat uçuş)",
            "Peri bacalarının üzerinde, yaklaşık 1000 m yükseklikte gün doğumu uçuşu. "
            "Kapadokya'nın imza deneyimi.",
            ["Otelden alış-bırakış", "Köpüklü şarap kutlaması", "Uçuş sertifikası"],
        ),
        "en": (
            "Hot Air Balloon Tour", "€225+", "3–4 hrs (≈1 hr flight)",
            "Sunrise flight over the fairy chimneys at about 1000 m. "
            "The signature Cappadocia experience.",
            ["Hotel pick-up & drop-off", "Sparkling wine celebration", "Flight certificate"],
        ),
    },
    "red": {
        "tr": (
            "Kırmızı Tur (biletli)", "€55", "Tam gün",
            "Zelve Açık Hava Müzesi, Paşabağ, Devrent Vadisi ve Güvercinlik Vadisi.",
            ["Profesyonel rehber", "Öğle yemeği dâhil", "Müze giriş biletleri"],
        ),
        "en": (
            "Red Tour (with tickets)", "€55", "Full day",
            "Zelve Open-Air Museum, Paşabağ, Devrent Valley and Pigeon Valley.",
            ["Professional guide", "Lunch included", "Museum entrance tickets"],
        ),
    },
    "red_lite": {
        "tr": (
            "Kırmızı Tur (biletsiz)", "€25", "Tam gün",
            "Kırmızı Tur ile aynı güzergâh; müze girişleri hariç — daha ekonomik seçenek.",
            ["Profesyonel rehber", "Ulaşım", "Öğle yemeği"],
        ),
        "en": (
            "Red Tour (no tickets)", "€25", "Full day",
            "Same route as the Red Tour, museum entrances not included — the budget option.",
            ["Professional guide", "Transport", "Lunch"],
        ),
    },
    "underground": {
        "tr": (
            "Yeraltı Şehri Turu", "€50", "Tam gün",
            "Kaymaklı Yeraltı Şehri, Soğanlı Vadisi ve Yılanlı Kilise.",
            ["Profesyonel rehber", "Ulaşım", "Giriş ücretleri"],
        ),
        "en": (
            "Underground City Tour", "€50", "Full day",
            "Kaymaklı Underground City, Soğanlı Valley and the Yılanlı Church.",
            ["Professional guide", "Transport", "Entrance fees"],
        ),
    },
    "atv": {
        "tr": (
            "ATV / Quad Gün Batımı Turu", "€30", "2 saat",
            "Gün batarken vadiler arasında sürüş.",
            ["Quad ve yakıt", "Güvenlik brifingi", "Rehber"],
        ),
        "en": (
            "ATV / Quad Sunset Tour", "€30", "2 hours",
            "Ride through the valleys as the sun goes down.",
            ["Quad bike & fuel", "Safety briefing", "Guide"],
        ),
    },
    "jeep": {
        "tr": (
            "Jeep Safari (Gün Batımı)", "€75", "2 saat",
            "Gün batımında vadilerde arazi turu (en az 2 kişi).",
            ["4x4 jeep ve sürücü", "Vadi rotası", "Fotoğraf molaları"],
        ),
        "en": (
            "Jeep Safari (Sunset)", "€75", "2 hours",
            "Off-road tour through the valleys at sunset (minimum 2 people).",
            ["4x4 jeep & driver", "Valley route", "Photo stops"],
        ),
    },
    "horse": {
        "tr": (
            "At Binme (Gün Batımı)", "€35", "2 saat",
            "Altın saatte Kapadokya manzaralarında at turu.",
            ["At ve ekipman", "Rehber", "Başlangıç seviyesine uygun"],
        ),
        "en": (
            "Horse Riding (Sunset)", "€35", "2 hours",
            "Horseback ride through Cappadocia's landscapes at golden hour.",
            ["Horse & equipment", "Guide", "Beginner friendly"],
        ),
    },
    "custom": {
        "tr": (
            "Özel Tur (size özel)", "Teklife göre", "Esnek",
            "Rotayı, süreyi ve tempoyu tamamen size göre planlıyoruz; özel rehber ve araç.",
            ["Özel rehber", "Esnek program", "Kapıdan alış-bırakış"],
        ),
        "en": (
            "Custom Tour (tailor-made)", "On request", "Flexible",
            "We plan the route, length and pace entirely around you; private guide and vehicle.",
            ["Private guide", "Flexible schedule", "Door-to-door pick-up"],
        ),
    },
}

TOUR_ORDER = ["balloon", "red", "red_lite", "underground", "atv", "jeep", "horse", "custom"]

IMAGES = {
    "balloon": "https://www.dailytoursincappadocia.com/images/balloon-hero.webp",
    "red": "https://www.dailytoursincappadocia.com/images/red-tour.webp",
    "red_lite": "https://www.dailytoursincappadocia.com/images/red-tour.webp",
    "underground": "https://www.dailytoursincappadocia.com/images/underground-city-tour.webp",
    "atv": "https://www.dailytoursincappadocia.com/images/atv-tour.webp",
    "jeep": "https://www.dailytoursincappadocia.com/images/jeep-safari.webp",
    "horse": "https://www.dailytoursincappadocia.com/images/horse-tour.webp",
    "custom": "https://www.dailytoursincappadocia.com/images/besign-your-tour-hero.webp",
}
HERO_IMAGE = "https://www.dailytoursincappadocia.com/images/fairy-chimneys-hero.webp"

T = {
    "tr": {
        "tours_btn": "Turlarımız",
        "menu_btn": "Menü",
        "site_btn": "Web sitesi",
        "faq_btn": "SSS",
        "contact_btn": "İletişim",
        "book_btn": "WhatsApp ile hemen rezervasyon",
        "chat_btn": "WhatsApp'tan yazın",
        "ig_btn": "Instagram",
        "lang_btn": "Language / Dil",
        "back_tours": "‹ Turlara dön",
        "per_person": "kişi başı",
        "included": "Dâhil olanlar:",
        "book_msg": "Merhaba! Şu turu rezerve etmek istiyorum: {title} — lütfen bilgi verin.",
        "chat_msg": "Merhaba! Turlarınız hakkında bir sorum var.",
        "start": (
            f"<b>{BRAND}</b>\n\n"
            "<i>Kapadokya'da balon uçuşları, vadi turları ve gün batımı maceraları.</i>\n\n"
            "Turlara buradan göz atın, tek dokunuşla WhatsApp'tan rezervasyon yapın."
        ),
        "tours": (
            "<b>Turlarımız</b>\n\n"
            "Ayrıntı, fiyat ve nelerin dâhil olduğunu görmek için bir tur seçin.\n\n"
            "Fiyatlar kişi başıdır; tarihe ve grup büyüklüğüne göre değişebilir."
        ),
        "menu": (
            "<b>Menü</b>\n\n"
            "• Turlarımıza fiyat ve ayrıntılarıyla göz atın.\n"
            "• Herhangi bir turu tek dokunuşla WhatsApp'tan rezerve edin.\n"
            "• Sık sorulan soruları okuyun.\n"
            "• Bize ulaşın veya web sitesini açın."
        ),
        "faq": (
            "<b>Sık sorulan sorular</b>\n\n"
            "<b>Nasıl rezervasyon yaparım?</b>\n"
            "Bir turu açıp “WhatsApp ile rezervasyon”a dokunun. Mesaj, tur adı önceden "
            "yazılmış olarak açılır — göndermeniz yeterli.\n\n"
            "<b>Otelden alış dâhil mi?</b>\n"
            "Turların çoğu Kapadokya bölgesinde otelden alış-bırakış içerir.\n\n"
            "<b>Balon uçuşu?</b>\n"
            "Hava koşullarına ve resmî uçuş iznine bağlıdır; güvenlik için ertelenebilir.\n\n"
            "<b>Hangi diller?</b>\n"
            "Rehberlik birkaç dilde mümkündür — rezervasyonda belirtin."
        ),
        "contact": (
            "<b>İletişim</b>\n\n"
            f"• WhatsApp / Telefon: {PHONE_DISPLAY}\n"
            "• Web: dailytoursincappadocia.com\n\n"
            "Turlarımız GetYourGuide ve Viator üzerinde de yer alır.\n\n"
            "FELIZ YCS TURISMO tarafından işletilir · TURSAB lisanslı acente (#12562).\n\n"
            "Size özel program da hazırlayabiliriz — bize yazmanız yeterli."
        ),
    },
    "en": {
        "tours_btn": "Our tours",
        "menu_btn": "Menu",
        "site_btn": "Website",
        "faq_btn": "FAQ",
        "contact_btn": "Contact",
        "book_btn": "Book now on WhatsApp",
        "chat_btn": "Chat on WhatsApp",
        "ig_btn": "Instagram",
        "lang_btn": "Language / Dil",
        "back_tours": "‹ Back to tours",
        "per_person": "per person",
        "included": "Included:",
        "book_msg": "Hello! I'd like to book: {title} — please send me details.",
        "chat_msg": "Hello! I have a question about your tours.",
        "start": (
            f"<b>{BRAND}</b>\n\n"
            "<i>Balloon flights, valley tours and sunset adventures in Cappadocia.</i>\n\n"
            "Browse our tours right here and book in one tap via WhatsApp."
        ),
        "tours": (
            "<b>Our tours</b>\n\n"
            "Pick a tour to see details, prices and what's included.\n\n"
            "All prices are per person and depend on date and group size."
        ),
        "menu": (
            "<b>Menu</b>\n\n"
            "• Browse our tours with prices and details.\n"
            "• Book any tour in one tap via WhatsApp.\n"
            "• Read frequently asked questions.\n"
            "• Contact us or open the website."
        ),
        "faq": (
            "<b>Frequently asked questions</b>\n\n"
            "<b>How do I book?</b>\n"
            "Open a tour and tap “Book on WhatsApp”. Your message arrives with the tour "
            "name pre-filled — just send it.\n\n"
            "<b>Are pick-ups included?</b>\n"
            "Most tours include hotel pick-up and drop-off in the Cappadocia region.\n\n"
            "<b>What about the balloon flight?</b>\n"
            "It depends on weather and official flight permissions and may be rescheduled "
            "for safety.\n\n"
            "<b>Which languages?</b>\n"
            "Guides are available in several languages — tell us when booking."
        ),
        "contact": (
            "<b>Contact</b>\n\n"
            f"• WhatsApp / Phone: {PHONE_DISPLAY}\n"
            "• Website: dailytoursincappadocia.com\n\n"
            "Our tours are also listed on GetYourGuide and Viator.\n\n"
            "Operated by FELIZ YCS TURISMO · TURSAB licensed agency (#12562).\n\n"
            "We're happy to build a custom itinerary — just message us."
        ),
    },
}


def cb(lang, action):
    return f"{lang}|{action}"


def btn(text, lang, action):
    return types.InlineKeyboardButton(text=text, callback_data=cb(lang, action))


def url_btn(text, url):
    return types.InlineKeyboardButton(text=text, url=url)


def site_btn(lang):
    return url_btn(T[lang]["site_btn"], SITE_URL)


def wa_btn(text, message):
    url = f"https://wa.me/{WHATSAPP_NUMBER}?text={quote(message)}"
    return url_btn(text, url)


def wa_chat_btn(lang):
    return wa_btn(T[lang]["chat_btn"], T[lang]["chat_msg"])


def ig_btn(lang):
    return url_btn(T[lang]["ig_btn"], INSTAGRAM_URL) if INSTAGRAM_URL else None


def lang_btn(lang):
    other = "en" if lang == "tr" else "tr"
    return types.InlineKeyboardButton(text=T[lang]["lang_btn"], callback_data=cb(other, "home"))


def make_markup(rows):
    markup = types.InlineKeyboardMarkup()
    for row in rows:
        row = [button for button in row if button is not None]
        if row:
            markup.row(*row)
    return markup


def nav_row(lang):
    return [btn(T[lang]["tours_btn"], lang, "tours"), btn(T[lang]["menu_btn"], lang, "menu")]


def tour_text(lang, key):
    title, price, duration, desc, includes = TOURS[key][lang]
    inc = "\n".join(f"• {item}" for item in includes)
    return (
        f"<b>{title}</b>\n\n{desc}\n\n"
        f"<b>{price}</b> / {T[lang]['per_person']}\n"
        f"{duration}\n\n"
        f"<b>{T[lang]['included']}</b>\n{inc}"
    )


def tour_rows(lang, key):
    title = TOURS[key][lang][0]
    booking_msg = T[lang]["book_msg"].format(title=title.strip())
    return [
        [wa_btn(T[lang]["book_btn"], booking_msg)],
        [site_btn(lang)],
        [btn(T[lang]["back_tours"], lang, "tours"), btn(T[lang]["menu_btn"], lang, "menu")],
    ]


def build_screen(lang, action):
    strings = T[lang]

    if action in ("home", "start"):
        rows = [
            [btn(strings["tours_btn"], lang, "tours")],
            [wa_chat_btn(lang)],
            [site_btn(lang), ig_btn(lang)],
            [lang_btn(lang)],
        ]
        return "photo", HERO_IMAGE, strings["start"], rows

    if action == "tours":
        rows = [[btn(TOURS[key][lang][0], lang, f"tour:{key}")] for key in TOUR_ORDER]
        rows.append([wa_chat_btn(lang)])
        rows.append([btn(strings["menu_btn"], lang, "menu")])
        return "text", None, strings["tours"], rows

    if action == "menu":
        rows = [
            [btn(strings["tours_btn"], lang, "tours")],
            [btn(strings["faq_btn"], lang, "faq"), btn(strings["contact_btn"], lang, "contact")],
            [wa_chat_btn(lang)],
            [site_btn(lang), ig_btn(lang)],
            [lang_btn(lang)],
        ]
        return "text", None, strings["menu"], rows

    if action == "faq":
        rows = [[btn(strings["tours_btn"], lang, "tours")], [btn(strings["menu_btn"], lang, "menu")]]
        return "text", None, strings["faq"], rows

    if action == "contact":
        rows = [
            [wa_btn(strings["book_btn"], strings["chat_msg"])],
            [site_btn(lang), ig_btn(lang)],
            nav_row(lang),
        ]
        return "text", None, strings["contact"], rows

    return None


def deliver(chat_id, kind, media, text, rows):
    markup = make_markup(rows)
    if SHOW_PHOTOS and kind == "photo" and media:
        try:
            bot.send_photo(chat_id, media, caption=text, reply_markup=markup)
            return
        except ApiTelegramException:
            pass
    bot.send_message(chat_id, text, reply_markup=markup)


def replace(call, kind, media, text, rows):
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
    except ApiTelegramException:
        pass
    deliver(call.message.chat.id, kind, media, text, rows)


@bot.message_handler(commands=["start"])
def start(message):
    markup = types.InlineKeyboardMarkup()
    markup.row(
        types.InlineKeyboardButton("Türkçe", callback_data=cb("tr", "home")),
        types.InlineKeyboardButton("English", callback_data=cb("en", "home")),
    )
    bot.send_message(
        message.chat.id,
        f"<b>{BRAND}</b>\n\nLütfen dil seçin / Please choose a language:",
        reply_markup=markup,
    )


@bot.callback_query_handler(func=lambda call: "|" in call.data)
def on_callback(call):
    bot.answer_callback_query(call.id)
    lang, action = call.data.split("|", 1)
    if lang not in T:
        return

    if action.startswith("tour:"):
        key = action.split(":", 1)[1]
        if key in TOURS:
            replace(call, "photo", IMAGES.get(key), tour_text(lang, key), tour_rows(lang, key))
        return

    built = build_screen(lang, action)
    if built:
        kind, media, text, rows = built
        replace(call, kind, media, text, rows)


def main():
    logging.basicConfig(
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        level=logging.INFO,
    )
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.info("%s bot is starting", BRAND)
    bot.infinity_polling(skip_pending=True)


if __name__ == "__main__":
    main()
