#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Bo tao trang web nha hang Lao Homely Restaurant - 3 ngon ngu + gio hang."""
import os, json

ROOT = os.path.dirname(os.path.abspath(__file__))

def tri(lo, en, vi, tag="span"):
    return (f'<{tag} class="lang-lo">{lo}</{tag}>'
            f'<{tag} class="lang-en">{en}</{tag}>'
            f'<{tag} class="lang-vi">{vi}</{tag}>')

SITE_NAME_LO = "ຮ້ານອາຫານລາວໂຮມລີ້"
SITE_NAME_EN = "Lao Homely Restaurant"
SITE_NAME_VI = "Nhà Hàng Lao Homely"

PHONE = "+856 20 9405 9629"
WHATSAPP_DIGITS = "8562094059629"
KITCHEN_WHATSAPP_1 = "8562094059629"   # 02094059629
KITCHEN_WHATSAPP_2 = "8562098676643"   # 02098676643
FACEBOOK = "Lao Homely Restaurant"
FACEBOOK_URL = "https://www.facebook.com/profile.php?id=61591822893556"
TIKTOK = "@laohomelyrestaurant"
TIKTOK_URL = f"https://www.tiktok.com/{TIKTOK}"
CITY = "Phonxay Village, Pakse District, Champasak Province"
ADDRESS_LO = "ບ້ານໂພນໄຊ, ເມືອງປາກເຊ, ແຂວງຈຳປາສັກ"
ADDRESS_EN = "Phonxay Village, Pakse District, Champasak Province"
ADDRESS_VI = "Bản Phonxay, huyện Pakse, tỉnh Champasak"
GMAPS_URL = "https://www.google.com/maps/place/Lao+Homely+Restaurant/@15.1215775,105.8019002,17z/data=!3m1!4b1!4m6!3m5!1s0x3114f9225608f6a1:0xa9cf81ec1215ac60!8m2!3d15.1215775!4d105.8019002!16s%2Fg%2F11mzw249ll!18m1!1e1"

# Firebase Realtime Database - dung cho he thong dat mon theo ban (QR code)
FIREBASE_CONFIG = {
    "apiKey": "AIzaSyBNP5hFGXQgzSRzK5u-qhQEQXC5u6DoFBw",
    "authDomain": "lao-homely-orders.firebaseapp.com",
    "databaseURL": "https://lao-homely-orders-default-rtdb.firebaseio.com",
    "projectId": "lao-homely-orders",
    "storageBucket": "lao-homely-orders.firebasestorage.app",
    "messagingSenderId": "468038291835",
    "appId": "1:468038291835:web:5c70d162882a3a05a8edde",
}
SITE_BASE_URL = "https://laohomelyrestaurant.github.io/lao-homely-website/"
NUM_TABLES = 10
ASSET_VERSION = "20260714f"  # bump this string whenever css/js changes, to bust browser cache

NAV = [
    ("index.html", "ໜ້າຫຼັກ", "Home", "Trang chủ"),
    ("menu.html", "ເມນູອາຫານ", "Menu", "Thực đơn"),
    ("gioi-thieu.html", "ກ່ຽວກັບພວກເຮົາ", "About Us", "Giới thiệu"),
    ("lien-he.html", "ຕິດຕໍ່", "Contact", "Liên hệ"),
]

def header(active):
    links = []
    for href, lo, en, vi in NAV:
        cls = " class=\"active\"" if href == active else ""
        links.append(f'<li><a href="{href}"{cls}>{tri(lo, en, vi)}</a></li>')
    links_html = "\n          ".join(links)
    cart_active = " class=\"active\"" if active == "gio-hang.html" else ""
    return f"""<header class="site-header">
    <div class="header-inner">
      <a class="brand" href="index.html">
        <span class="brand-mark">LHR</span>
        <span class="brand-text">
          <span class="brand-main">{tri(SITE_NAME_LO, SITE_NAME_EN, SITE_NAME_VI)}</span>
          <span class="brand-sub">{tri("ອາຫານບ້ານໆ ແບບລາວແທ້", "Authentic Lao Homestyle Food", "Ẩm thực Lào chuẩn vị gia đình")}</span>
        </span>
      </a>
      <nav class="main-nav">
        <ul>
          {links_html}
        </ul>
      </nav>
      <div class="header-actions">
        <a class="cart-link"{cart_active} href="gio-hang.html">
          <span class="cart-icon">CART</span>
          <span class="cart-badge" id="cart-badge">0</span>
        </a>
        <div class="lang-switch" role="group" aria-label="Language switch">
          <button type="button" data-set-lang="lo">LAO</button>
          <button type="button" data-set-lang="en">EN</button>
          <button type="button" data-set-lang="vi">VI</button>
        </div>
        <button class="nav-toggle" type="button" aria-label="Menu">MENU</button>
      </div>
    </div>
  </header>"""

def footer():
    return f"""<footer class="site-footer">
    <div class="footer-inner">
      <div class="footer-col">
        <div class="brand-main footer-brand">{tri(SITE_NAME_LO, SITE_NAME_EN, SITE_NAME_VI)}</div>
        <p>{tri("ອາຫານບ້ານໆ ແບບລາວແທ້ ໃຈກາງເມືອງປາກເຊ", "Authentic Lao homestyle cooking in the heart of Pakse", "Ẩm thực Lào chuẩn vị gia đình giữa lòng Pakse")}</p>
      </div>
      <div class="footer-col">
        <h4>{tri("ຕິດຕໍ່", "Contact", "Liên hệ")}</h4>
        <p><a href="{GMAPS_URL}" target="_blank" rel="noopener">{tri(ADDRESS_LO, ADDRESS_EN, ADDRESS_VI)}</a></p>
        <p>Tel: <a href="tel:{PHONE.replace(' ', '')}">{PHONE}</a></p>
        <p>WhatsApp: <a href="https://wa.me/{WHATSAPP_DIGITS}" target="_blank" rel="noopener">{PHONE}</a></p>
      </div>
      <div class="footer-col">
        <h4>{tri("ຕິດຕາມພວກເຮົາ", "Follow Us", "Theo dõi chúng tôi")}</h4>
        <p>Facebook: <a href="{FACEBOOK_URL}" target="_blank" rel="noopener">{FACEBOOK}</a></p>
        <p>TikTok: <a href="{TIKTOK_URL}" target="_blank" rel="noopener">{TIKTOK}</a></p>
      </div>
    </div>
    <div class="footer-bottom">
      <p>&copy; 2026 {SITE_NAME_EN} &middot; {tri("ສະຫງວນລິຂະສິດ", "All rights reserved", "Bảo lưu mọi quyền")}</p>
    </div>
  </footer>
  <script src="https://www.gstatic.com/firebasejs/10.13.0/firebase-app-compat.js"></script>
  <script src="https://www.gstatic.com/firebasejs/10.13.0/firebase-database-compat.js"></script>
  <script>window.HOMELY_FIREBASE_CONFIG = {json.dumps(FIREBASE_CONFIG)};</script>
  <script src="js/cart.js?v={ASSET_VERSION}"></script>
  <script src="js/main.js?v={ASSET_VERSION}"></script>"""

def page(title_lo, title_en, title_vi, active, body, extra_head=""):
    return f"""<!DOCTYPE html>
<html lang="en" data-lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title_en} | {SITE_NAME_EN}</title>
<meta name="description" content="{title_en} - {SITE_NAME_EN}, {CITY}">
<link rel="stylesheet" href="css/style.css?v={ASSET_VERSION}">
{extra_head}
</head>
<body>
  {header(active)}
  <main>
  {body}
  </main>
  {footer()}
</body>
</html>
"""

def img_placeholder(label_lo, label_en, label_vi, filename_hint, ratio="landscape"):
    cls = "img-placeholder " + ("ph-square" if ratio == "square" else "ph-landscape")
    return f"""<div class="{cls}">
      <span class="ph-icon">IMG</span>
      <span class="ph-label">{tri(label_lo, label_en, label_vi)}</span>
      <span class="ph-hint">{filename_hint}</span>
    </div>"""

# ---------------------------------------------------------------------------
# MENU DATA (id, lo, en, vi, kind, price/variants, cart_note)
# kind: simple | variant | verify
# ---------------------------------------------------------------------------
MENU = [
    ("ເຂົ້າຈານ (ອາຫານຕາມສັ່ງ)", "Rice Plates", "Cơm đĩa", [
        dict(id="pad-krapao-crispy-pork-rice", lo="ເຂົ້າຜັດກະເພົາໝູກອບ + ໄຂ່ດາວ", en="Stir-fried Crispy Pork Pad Krapao + fried egg, with rice", vi="Cơm thịt heo giòn xào lá quế + trứng ốp la", kind="simple", price=55000, note=tri("(ໄຂ່ດາວເພີ່ມ +7,000 kip)", "(extra fried egg +7,000 kip)", "(thêm trứng ốp la +7,000 kip)")),
        dict(id="pad-krapao-rice", lo="ເຂົ້າຜັດກະເພົາ (ໝູ/ໄກ່/ທະເລ) + ໄຂ່ດາວ", en="Pad Krapao pork/chicken/seafood + fried egg, with rice", vi="Cơm thịt băm xào lá quế (heo/gà/hải sản) + trứng ốp la", kind="variant",
             variants=[("ໝູ", "Pork", "Heo", 50000), ("ໄກ່", "Chicken", "Gà", 50000), ("ທະເລ", "Seafood", "Hải sản", 55000)],
             note=tri("(ໄຂ່ດາວເພີ່ມ +7,000 kip)", "(extra fried egg +7,000 kip)", "(thêm trứng ốp la +7,000 kip)")),
        dict(id="fried-rice-rice", lo="ເຂົ້າຜັດ (ທະເລ/ໝູ/ໄກ່)", en="Fried Rice (seafood / pork / chicken)", vi="Cơm chiên (hải sản/heo/gà)", kind="variant",
             variants=[("ທະເລ", "Seafood", "Hải sản", 55000), ("ໝູ", "Pork", "Heo", 50000), ("ໄກ່", "Chicken", "Gà", 50000)]),
        dict(id="curry-fried-rice", lo="ເຂົ້າຜັດຜົງກະຫລີ (ທະເລ/ໝູ/ໄກ່)", en="Curry Powder Fried Rice (seafood / pork / chicken)", vi="Cơm chiên bột cà ri (hải sản/heo/gà)", kind="variant",
             variants=[("ທະເລ", "Seafood", "Hải sản", 55000), ("ໝູ", "Pork", "Heo", 50000), ("ໄກ່", "Chicken", "Gà", 50000)]),
        dict(id="stir-fry-curry-eggplant-rice", lo="ເຂົ້າຜັດເຜັດ (ໝູ/ໄກ່) ໝາກເຂືອລາວ", en="Stir-fried Pork/Chicken with Curry Paste & Lao Eggplant, with rice", vi="Cơm thịt heo/gà xào cà ri cà tím Lào", kind="simple", price=50000),
        dict(id="beef-oyster-sauce-rice", lo="ເຂົ້າງົວຜັດນ້ຳມັນຫອຍ", en="Stir-fried Beef with Oyster Sauce, with rice", vi="Cơm bò xào dầu hào", kind="simple", price=55000),
        dict(id="green-curry", lo="ແກງຂຽວຫວານ (ໝູ/ໄກ່)", en="Green Curry (pork / chicken)", vi="Cà ri xanh (heo/gà)", kind="variant",
             variants=[("ໝູ", "Pork", "Heo", 60000), ("ໄກ່", "Chicken", "Gà", 60000)]),
        dict(id="squid-salted-egg-rice", lo="ເຂົ້າມິກຜັດໄຂ່ເຄັມ", en="Stir-fried Squid with Salted Egg, with rice", vi="Cơm mực xào trứng muối", kind="simple", price=55000),
        dict(id="kale-crispy-pork-rice", lo="ເຂົ້າກະນາໝູກອບ + ໄຂ່", en="Stir-fried Chinese Kale with Crispy Pork Belly, with rice + egg", vi="Cơm cải kale xào thịt ba chỉ giòn + trứng", kind="simple", price=55000, note=tri("(ໄຂ່ດາວເພີ່ມ +7,000 kip)", "(extra fried egg +7,000 kip)", "(thêm trứng ốp la +7,000 kip)")),
        dict(id="sweet-sour-fish-rice", lo="ເຂົ້າປົ້ຽວຫວານປາ", en="Fish with Sweet & Sour Sauce, with rice", vi="Cơm cá sốt chua ngọt", kind="simple", price=60000),
        dict(id="pork-teriyaki-rice", lo="ເຂົ້າໝູເທຣິຢະກິ", en="Pork Teriyaki, with rice", vi="Cơm thịt heo teriyaki", kind="simple", price=60000),
        dict(id="mushroom-rice", lo="ເຂົ້າຂົ້ວເຫັດ", en="Stir-fried Mushrooms, with rice", vi="Cơm nấm xào", kind="simple", price=50000),
        dict(id="mixed-veg-rice", lo="ເຂົ້າຂົ້ວຜັກລວມ", en="Stir-fried Mixed Vegetables, with rice", vi="Cơm rau củ xào thập cẩm", kind="simple", price=55000),
        dict(id="morning-glory-rice", lo="ເຂົ້າຜັກບົ້ງໄຟແດງ", en="Stir-fried Morning Glory, with rice", vi="Cơm rau muống xào", kind="simple", price=45000),
        dict(id="lao-omelette-rice", lo="ເຂົ້າໄຂ່ຈຽວ", en="Lao Omelette, with rice", vi="Cơm trứng chiên kiểu Lào", kind="simple", price=45000),
        dict(id="chicken-wings-rice", lo="ເຂົ້າທອດປີກໄກ່", en="Fried Chicken Wings, with rice", vi="Cơm cánh gà chiên", kind="simple", price=55000),
    ]),
    ("ເຝີ ແລະ ອາຫານຫວຽດນາມ", "Vietnamese Noodle Soups", "Phở & Bún Việt", [
        dict(id="pho-chicken", lo="ເຝີໄກ່ຫວຽດ", en="Vietnamese Pho with Chicken", vi="Phở gà", kind="simple", price=50000),
        dict(id="pho-beef", lo="ເຝີງົວຫວຽດ", en="Vietnamese Pho with Beef", vi="Phở bò", kind="simple", price=55000),
        dict(id="banh-canh", lo="ບັ່ນກັນ", en="Banh Canh", vi="Bánh canh", kind="simple", price=40000),
    ]),
    ("ສະປາເກັຕິ", "Spaghetti", "Mì Ý (Spaghetti)", [
        dict(id="tomato-spaghetti", lo="ສະປາເກັຕິຊອດໝາກເລັ່ນ", en="Tomato Spaghetti", vi="Spaghetti sốt cà chua", kind="simple", price=60000),
        dict(id="carbonara-spaghetti", lo="ສະປາເກັຕິ ຄາໂບນາລາ", en="Carbonara Spaghetti", vi="Spaghetti Carbonara", kind="simple", price=70000),
    ]),
    ("ເສັ້ນຜັດ", "Fried Noodles", "Mì / Bún xào", [
        dict(id="pad-thai", lo="ຜັດໄທ (ທະເລ/ໝູ/ໄກ່)", en="Pad Thai (seafood / pork / chicken)", vi="Pad Thái (hải sản/heo/gà)", kind="variant",
             variants=[("ທະເລ", "Seafood", "Hải sản", 55000), ("ໝູ", "Pork", "Heo", 50000), ("ໄກ່", "Chicken", "Gà", 50000)]),
        dict(id="pad-kee-mao", lo="ຜັດຂີ້ເມົາ Mama (ທະເລ/ໝູ/ໄກ່)", en="Mama Pad Kee Mao (seafood / pork / chicken)", vi="Mì xào cay kiểu Lào - Mama (hải sản/heo/gà)", kind="variant",
             variants=[("ທະເລ", "Seafood", "Hải sản", 70000), ("ໝູ", "Pork", "Heo", 60000), ("ໄກ່", "Chicken", "Gà", 60000)]),
        dict(id="pad-sa-iew", lo="ຜັດສະອິ້ວ (ໝູ/ໄກ່)", en="Pad Sa Iew (pork / chicken)", vi="Mì xào xì dầu (heo/gà)", kind="variant",
             variants=[("ໝູ", "Pork", "Heo", 50000), ("ໄກ່", "Chicken", "Gà", 50000)]),
    ]),
    ("ຢຳ ແລະ ສະຫຼັດລາວ", "Lao Salads", "Gỏi & Salad Lào", [
        dict(id="larb-moo", lo="ກ້ອຍໝູ", en="Lao Minced Meat Salad (Larb Moo)", vi="Gỏi thịt băm kiểu Lào (Larb)", kind="simple", price=50000),
        dict(id="mekong-fish-salad", lo="ກ້ອຍປາແມ່ນ້ຳຂອງ", en="Mekong Fish Salad", vi="Gỏi cá sông Mekong", kind="simple", price=120000),
        dict(id="grilled-eggplant-dip", lo="ປົ່ນຫມາກເຂືອ", en="Lao Grilled Eggplant Dip", vi="Chẳm cà tím nướng kiểu Lào", kind="simple", price=50000),
        dict(id="xoup-phak", lo="ຊຸບຜັກລາວ (Xoup Phak)", en="Lao Vegetable Salad (Xoup Phak)", vi="Gỏi rau kiểu Lào (Xoup Phak)", kind="simple", price=45000),
        dict(id="lao-salad", lo="ຍໍາສະຫຼັດລາວ", en="Lao Salad", vi="Gỏi Lào", kind="simple", price=75000),
        dict(id="yum-seafood", lo="ຍໍາທະເລ", en="Yum Seafood", vi="Gỏi hải sản kiểu Lào-Thái", kind="simple", price=80000),
    ]),
    ("ຂອງກິນຫຼີ້ນ ແລະ ຂອງທອດ", "Snacks & Fried Sides", "Món ăn chơi & chiên (không kèm cơm)", [
        dict(id="spring-rolls", lo="ທອດປໍເປຍ", en="Spring Rolls", vi="Chả giò (nem rán)", kind="simple", price=65000),
        dict(id="chicken-wings-side", lo="ທອດປີກໄກ່", en="Fried Chicken Wings (no rice)", vi="Cánh gà chiên (dùng riêng)", kind="simple", price=55000),
        dict(id="french-fries", lo="ທອດມັນຝຣັ່ງ", en="French Fries", vi="Khoai tây chiên", kind="simple", price=50000),
        dict(id="mushroom-side", lo="ຂົ້ວເຫັດ", en="Stir-fried Mushroom (no rice)", vi="Nấm xào (dùng riêng, không cơm)", kind="simple", price=60000),
        dict(id="mixed-veg-side", lo="ຂົ້ວຜັກລວມ", en="Stir-fried Mixed Vegetables (no rice)", vi="Rau củ xào thập cẩm (dùng riêng, không cơm)", kind="simple", price=70000),
        dict(id="morning-glory-side", lo="ຜັກບົ້ງໄຟແດງ", en="Stir-fried Morning Glory (no rice)", vi="Rau muống xào (dùng riêng, không cơm)", kind="simple", price=60000),
        dict(id="pad-krapao-side", lo="ຜັດກະເພົາ (ໝູ/ໄກ່/ທະເລ)", en="Pad Krapao pork/chicken/seafood (no rice)", vi="Thịt xào lá quế (heo/gà/hải sản, dùng riêng)", kind="variant",
             variants=[("ໝູ", "Pork", "Heo", 60000), ("ໄກ່", "Chicken", "Gà", 60000), ("ທະເລ", "Seafood", "Hải sản", 60000)]),
        dict(id="squid-salted-egg-side", lo="ມິກຜັດໄຂ່ເຄັມ", en="Stir-fried Squid with Salted Egg (no rice)", vi="Mực xào trứng muối (dùng riêng, không cơm)", kind="simple", price=80000),
        dict(id="sweet-sour-fish-side", lo="ປົ້ຽວຫວານປາ", en="Fish with Sweet & Sour Sauce (no rice)", vi="Cá sốt chua ngọt (dùng riêng, không cơm)", kind="simple", price=80000),
    ]),
    ("ອາຫານພິເສດ", "Specialties", "Đặc sản", [
        dict(id="beef-steak", lo="ສະເຕັກງົວ", en="Beef Steak", vi="Bò bít tết", kind="simple", price=100000),
        dict(id="shaking-beef", lo="ລຸກລັກງົວ", en="Shaking Beef", vi="Bò lúc lắc", kind="simple", price=80000),
        dict(id="fried-sour-fish", lo="ຈືນສົ້ມປາ", en="Fried Sour Fish", vi="Cá chua chiên giòn", kind="simple", price=70000),
    ]),
    ("ອ່ອມ ແລະ ຕົ້ມ", "Soups", "Canh & Súp", [
        dict(id="fish-maw-soup", lo="ຊຸບກະເພາະປາ", en="Fish Maw Soup", vi="Súp bong bóng cá", kind="variant",
             variants=[("ນ້ອຍ", "Small", "Nhỏ", 60000), ("ໃຫຍ່", "Big", "Lớn", 80000)]),
        dict(id="lao-style-soup", lo="ອ່ອມ (ໝູ/ໄກ່/ງົວ)", en="Lao-style Soup (pork / chicken / beef)", vi="Súp kiểu Lào (heo/gà/bò)", kind="variant",
             variants=[("ໝູ", "Pork", "Heo", 50000), ("ໄກ່", "Chicken", "Gà", 50000), ("ງົວ", "Beef", "Bò", 55000)]),
        dict(id="pork-ribs-broth", lo="ຕົ້ມແຊບກະດູກໝູ", en="Fiery Pork Ribs Broth", vi="Canh sườn heo cay kiểu Lào-Thái", kind="simple", price=60000),
        dict(id="clear-soup-tofu-pork", lo="ຕົ້ມຈືດ", en="Clear Soup with Tofu and Minced Pork", vi="Canh trong đậu hũ thịt băm", kind="simple", price=60000),
        dict(id="tom-yum-goong", lo="ຕົ້ມຍຳກຸ້ງ", en="Tom Yum Goong", vi="Tom Yum tôm", kind="simple", price=80000),
        dict(id="tom-yum-pa", lo="ຕົ້ມຍຳປານ້ຳ", en="Tom Yum Pa", vi="Tom Yum cá", kind="simple", price=120000),
        dict(id="tom-som-pa", lo="ຕົ້ມສົ້ມປາ", en="Tom Som Pa - Authentic Lao Sour Fish Soup", vi="Canh chua cá kiểu Lào (Tom Som Pa)", kind="simple", price=90000),
    ]),
    ("ເຂົ້າ / ເຂົ້າໜຽວ", "Rice", "Cơm / Xôi ăn kèm", [
        dict(id="steamed-rice", lo="ເຂົ້າຈ້າວ", en="Steamed Rice", vi="Cơm trắng", kind="simple", price=15000),
        dict(id="sticky-rice", lo="ເຂົ້າໜຽວ", en="Sticky Rice", vi="Xôi (cơm nếp)", kind="simple", price=15000),
    ]),
    ("ເຄື່ອງດື່ມ", "Drinks", "Đồ uống", [
        dict(id="cappuccino", lo="ຄາປູຊິໂນ (ຮ້ອນ/ເຢັນ)", en="Cappuccino (iced / hot)", vi="Cappuccino (đá/nóng)", kind="simple", price=35000),
        dict(id="americano", lo="ກາເຟດຳ (ຮ້ອນ/ເຢັນ)", en="Americano (iced / hot)", vi="Americano (đá/nóng)", kind="simple", price=30000),
        dict(id="latte", lo="ລາເຕ້ (ຮ້ອນ/ເຢັນ)", en="Latte (iced / hot)", vi="Latte (đá/nóng)", kind="simple", price=35000),
        dict(id="orange-juice", lo="ນ້ຳໝາກກ້ຽງສົດ", en="Fresh Orange Juice", vi="Nước cam tươi", kind="simple", price=40000),
        dict(id="avocado-smoothie", lo="ອາໂວຄາໂດປັ່ນ", en="Avocado Smoothie", vi="Sinh tố bơ", kind="simple", price=40000),
        dict(id="strawberry-yogurt", lo="ປັ່ນສະຕໍເບີຣີໂຢເກີດ", en="Strawberry Yogurt Smoothie", vi="Sinh tố dâu sữa chua", kind="simple", price=40000),
        dict(id="blueberry-yogurt", lo="ປັ່ນບູເບີຣີໂຢເກີດ", en="Blueberry Yogurt Smoothie", vi="Sinh tố việt quất sữa chua", kind="simple", price=40000),
        dict(id="matcha-latte", lo="ຊາຂຽວລາເຕ້", en="Matcha Latte", vi="Matcha Latte", kind="simple", price=40000),
        dict(id="thai-matcha", lo="ຊາໄທ", en="Thai Matcha", vi="Trà Thái matcha", kind="simple", price=35000),
    ]),
]


def fmt_price(n):
    return f"{n:,}".replace(",", ".") + " Lak"

def cart_controls_html(item):
    kind = item["kind"]
    if kind == "verify":
        return f"""<div class="cart-controls unavailable">
            <span class="verify-text">{tri('ລາຄາ: ກະລຸນາໂທຢືນຢັນ', 'price: please call to confirm', 'giá: vui lòng gọi điện xác nhận')}</span>
            <a class="btn btn-outline btn-sm" href="tel:{PHONE.replace(' ', '')}">{tri('ໂທຫາຮ້ານ', 'Call restaurant', 'Gọi cho quán')}</a>
          </div>"""
    name_attrs = f'data-name-lo="{item["lo"]}" data-name-en="{item["en"]}" data-name-vi="{item["vi"]}"'
    check_html = f"""<label class="select-check">
              <input type="checkbox" class="select-checkbox">
              <span class="select-check-box"><span class="select-check-mark">&#10003;</span></span>
              <span class="select-check-label">{tri('ເລືອກອາຫານນີ້', 'Select this dish', 'Chọn món này')}</span>
            </label>"""
    if kind == "simple":
        price = item["price"]
        return f"""<div class="cart-controls" data-id="{item['id']}" data-kind="simple" data-price="{price}" {name_attrs}>
            {check_html}
            <div class="qty-stepper">
              <button type="button" class="qty-btn" data-qty-action="dec">-</button>
              <input type="number" class="qty-input" value="1" min="1" max="20">
              <button type="button" class="qty-btn" data-qty-action="inc">+</button>
            </div>
          </div>"""
    if kind == "variant":
        options = []
        for lo_v, en_v, vi_v, price in item["variants"]:
            label = f"{lo_v} / {en_v} / {vi_v} - {fmt_price(price)}"
            options.append(f'<option value="{price}" data-label-lo="{lo_v}" data-label-en="{en_v}" data-label-vi="{vi_v}">{label}</option>')
        options_html = "\n              ".join(options)
        return f"""<div class="cart-controls" data-id="{item['id']}" data-kind="variant" {name_attrs}>
            <select class="variant-select">
              {options_html}
            </select>
            {check_html}
            <div class="qty-stepper">
              <button type="button" class="qty-btn" data-qty-action="dec">-</button>
              <input type="number" class="qty-input" value="1" min="1" max="20">
              <button type="button" class="qty-btn" data-qty-action="inc">+</button>
            </div>
          </div>"""
    return ""

def render_price_display(item):
    kind = item["kind"]
    if kind == "verify":
        return tri("(ລາຄາ: ກະລຸນາຢືນຢັນຄືນ)", "(price: to be confirmed)", "(giá: cần xác minh lại)")
    if kind == "simple":
        return fmt_price(item["price"])
    if kind == "variant":
        parts = " / ".join(fmt_price(p) for *_, p in item["variants"])
        return parts
    return ""

# ---------------------------------------------------------------------------
# INDEX PAGE
# ---------------------------------------------------------------------------
hero = f"""
  <section class="hero">
    <div class="hero-inner">
      <p class="eyebrow">{tri("ຍິນດີຕ້ອນຮັບສູ່", "Welcome to", "Chào mừng đến với")}</p>
      <h1>{tri(SITE_NAME_LO, SITE_NAME_EN, SITE_NAME_VI)}</h1>
      <p class="hero-tagline">{tri(
        "ອາຫານບ້ານໆ ແບບລາວແທ້ໆ ໃຈກາງເມືອງປາກເຊ",
        "Real Lao homestyle cooking, right in the heart of Pakse",
        "Ẩm thực Lào chuẩn vị gia đình, ngay giữa lòng thành phố Pakse")}</p>
      <div class="hero-actions">
        <a class="btn btn-primary" href="menu.html">{tri("ເບິ່ງເມນູ / ສັ່ງອາຫານ", "View Menu / Order", "Xem thực đơn / Đặt món")}</a>
        <a class="btn btn-outline" href="lien-he.html">{tri("ຕິດຕໍ່ຈອງໂຕະ", "Contact Us", "Liên hệ đặt bàn")}</a>
      </div>
    </div>
  </section>"""

intro = f"""
  <section class="section intro">
    <div class="section-inner two-col">
      <div class="col-photo">
        <img class="storefront-photo" src="images/mat-tien-quan.jpg" alt="{SITE_NAME_EN} storefront at night" loading="lazy">
      </div>
      <div class="col-text">
        <h2 class="section-title">{tri("ເລື່ອງລາວຂອງພວກເຮົາ", "Our Story", "Câu chuyện của chúng tôi")}</h2>
        <p>{tri(
          "ຮ້ານອາຫານລາວໂຮມລີ້ ຕັ້ງຢູ່ໃຈກາງເມືອງປາກເຊ ນຳສະເໜີອາຫານລາວ ແລະ ອາຫານໄທ ແບບບ້ານໆ ປຸງແຕ່ງດ້ວຍວັດຖຸດິບສົດ ບັນຍາກາດອົບອຸ່ນ ເໝາະສຳລັບຄອບຄົວ ແລະ ໝູ່ເພື່ອນ.",
          "Lao Homely Restaurant sits in the heart of Pakse, serving homestyle Lao and Thai-inspired dishes made with fresh, local ingredients. Warm, welcoming, and perfect for family meals or catching up with friends.",
          "Lao Homely Restaurant nằm ngay trung tâm thành phố Pakse, phục vụ các món ăn Lào và Thái theo phong cách gia đình, chế biến từ nguyên liệu tươi. Không gian ấm cúng, phù hợp cho bữa ăn gia đình hay gặp gỡ bạn bè.")}</p>
        <p class="note">{tri(
          "(ໝາຍເຫດ: ອານ ສາມາດປັບແກ້ຂໍ້ຄວາມນີ້ໃຫ້ກົງກັບເລື່ອງລາວແທ້ຈິງຂອງຮ້ານ)",
          "(Note: replace this text with the restaurant's real story/history.)",
          "(Ghi chú: anh có thể chỉnh sửa đoạn này cho đúng câu chuyện thật của quán.)")}</p>
      </div>
    </div>
  </section>"""

highlights = f"""
  <section class="section highlights alt-bg">
    <div class="section-inner">
      <h2 class="section-title center">{tri("ມື້ນີ້ຮ້ານແນະນຳ", "Today's Specials", "Đặc sản hôm nay")}</h2>
      <div class="grid-3">
        <div class="card">
          {img_placeholder("ບົ້ວນຶ່ງ ໄຂ່ດາວ ຂະໜົມປັງ", "Grilled Beef, Fried Eggs and Baguette Set", "Set bò nướng, trứng ốp la và bánh mì", "-> images/set-bo-nuong.jpg", "square")}
          <h3>{tri("ຊຸດອາຫານເຊົ້າໂຮມລີ້", "Homely Breakfast Set", "Set ăn sáng Homely")}</h3>
          <p>{tri("ບົ້ວນຶ່ງ, ໄຂ່ດາວ 5 ໜ່ວຍ, ຂະໜົມປັງຝຣັ່ງ 2 ອັນ", "Grilled beef, 5 fried eggs, 2 baguette loaves", "Bò nướng, 5 trứng ốp la, 2 ổ bánh mì baguette")}</p>
          <p class="price">{tri("ລາຄາ: ຕິດຕໍ່ຮ້ານ", "Price: contact restaurant", "Giá: liên hệ nhà hàng")} <span class="verify">({tri('ຕ້ອງກວດຄືນ', 'to be confirmed', 'cần xác minh lại')})</span></p>
        </div>
        <div class="card">
          {img_placeholder("ຢຳສະຫຼັດລາວ", "Lao Salad", "Gỏi Lào", "-> images/goi-lao.jpg", "square")}
          <h3>{tri("ຢຳສະຫຼັດລາວ", "Lao Salad", "Gỏi Lào")}</h3>
          <p>{tri("ອາຫານປະເພດສະຫຼັດແທ້ໆແບບລາວ", "Authentic Lao-style salad", "Món gỏi chuẩn vị Lào")}</p>
          <p class="price">75,000 Lak</p>
        </div>
        <div class="card">
          {img_placeholder("ຕົ້ມໄກ່ລາວ", "Lao Chicken Soup", "Súp gà kiểu Lào", "-> images/sup-ga-lao.jpg", "square")}
          <h3>{tri("ຕົ້ມໄກ່ລາວ", "Lao Chicken Soup", "Súp gà kiểu Lào")}</h3>
          <p>{tri("ອາຫານລາວແທ້ໆ ອົບອຸ່ນຫົວໃຈ", "Authentic comfort food from Laos", "Món ăn Lào ấm lòng")}</p>
          <p class="price">250,000 Lak</p>
        </div>
      </div>
      <div class="center"><a class="btn btn-primary" href="menu.html">{tri("ເບິ່ງເມນູທັງໝົດ", "See Full Menu", "Xem toàn bộ thực đơn")}</a></div>
    </div>
  </section>"""

gallery = f"""
  <section class="section gallery">
    <div class="section-inner">
      <h2 class="section-title center">{tri("ຮູບພາບຮ້ານ", "Gallery", "Hình ảnh quán")}</h2>
      <div class="grid-4">
        {img_placeholder("ປ້າຍຮ້ານ", "Restaurant Sign", "Bảng hiệu quán", "images/bang-hieu.jpg", "square")}
        {img_placeholder("ອາຫານເຊົ້າ", "Breakfast Plate", "Món ăn sáng", "images/mon-an-sang.jpg", "square")}
        {img_placeholder("ເມນູອາຫານ", "Menu Board", "Bảng thực đơn", "images/menu-board.jpg", "square")}
        {img_placeholder("ບັນຍາກາດຮ້ານ", "Restaurant Atmosphere", "Không gian quán", "images/khong-gian.jpg", "square")}
      </div>
    </div>
  </section>"""

index_body = hero + intro + highlights + gallery
with open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8") as f:
    f.write(page("ໜ້າຫຼັກ", "Home", "Trang chủ", "index.html", index_body))

# ---------------------------------------------------------------------------
# MENU PAGE
# ---------------------------------------------------------------------------
menu_sections_html = []
for lo_title, en_title, vi_title, items in MENU:
    rows = []
    for item in items:
        img_path = f"images/dishes/{item['id']}.jpg"
        rows.append(f"""        <div class="menu-item">
          <div class="menu-item-photo">
            <img src="{img_path}" alt="{item['en']}" loading="lazy" onerror="this.closest('.menu-item-photo').style.display='none'">
          </div>
          <div class="menu-item-body">
            <div class="menu-item-name">
              <p class="dish-lo">{item['lo']}</p>
              <p class="dish-en">{item['en']}</p>
              <p class="dish-vi">{item['vi']}</p>
              {item.get('note','')}
            </div>
            <div class="menu-item-price">{render_price_display(item)}</div>
            {cart_controls_html(item)}
          </div>
        </div>""")
    rows_html = "\n".join(rows)
    menu_sections_html.append(f"""
    <div class="menu-section">
      <h2 class="menu-section-title">{tri(lo_title, en_title, vi_title)}</h2>
      <div class="menu-list">
{rows_html}
      </div>
    </div>""")

menu_intro = f"""
  <section class="page-hero">
    <div class="section-inner">
      <p class="eyebrow">{tri(SITE_NAME_LO, SITE_NAME_EN, SITE_NAME_VI)}</p>
      <h1>{tri("ເມນູອາຫານ", "Our Menu", "Thực đơn")}</h1>
      <p>{tri(
        "ຕິກ 'ເລືອກອາຫານນີ້' ໃນແຕ່ລະລາຍການ ແລ້ວກົດ 'ໄປໜ້າສັ່ງອາຫານ' ເພື່ອສົ່ງອໍເດີໃຫ້ຫ້ອງຄົວ.",
        "Tick 'Select this dish' on each item, then go to the order page to send your order to the kitchen.",
        "Tick 'Chọn món này' ở từng món, sau đó vào trang đặt món để gửi đơn cho bếp.")}</p>
      <div id="table-banner" class="table-banner" hidden>
        <span id="table-banner-text"></span>
      </div>
      <div id="no-table-warning" class="no-table-warning" hidden>
        {tri(
          "⚠ ກະລຸນາສະແກນ QR ຢູ່ໂຕະຂອງທ່ານກ່ອນເລືອກອາຫານ",
          "⚠ Please scan the QR code at your table before ordering",
          "⚠ Vui lòng quét mã QR tại bàn của bạn trước khi chọn món")}
      </div>
    </div>
  </section>"""

menu_body = menu_intro + f"""
  <section class="section">
    <div class="section-inner">
      {''.join(menu_sections_html)}
    </div>
  </section>"""

with open(os.path.join(ROOT, "menu.html"), "w", encoding="utf-8") as f:
    f.write(page("ເມນູອາຫານ", "Menu", "Thực đơn", "menu.html", menu_body))

# ---------------------------------------------------------------------------
# ABOUT PAGE
# ---------------------------------------------------------------------------
about_body = f"""
  <section class="page-hero">
    <div class="section-inner">
      <p class="eyebrow">{tri(SITE_NAME_LO, SITE_NAME_EN, SITE_NAME_VI)}</p>
      <h1>{tri("ກ່ຽວກັບພວກເຮົາ", "About Us", "Giới thiệu")}</h1>
    </div>
  </section>

  <section class="section intro">
    <div class="section-inner two-col">
      <div class="col-text">
        <h2 class="section-title">{tri("ອາຫານບ້ານໆ, ໃຈກາງເມືອງປາກເຊ", "Homestyle food, in the heart of Pakse", "Ẩm thực gia đình, giữa lòng Pakse")}</h2>
        <p>{tri(
          "ຮ້ານອາຫານລາວໂຮມລີ້ ເປັນຮ້ານອາຫານແບບບ້ານໆ ນຳສະເໜີເມນູລາວ ແລະ ໄທ ຫຼາກຫຼາຍ ຕັ້ງແຕ່ສະຫຼັດ, ຕົ້ມ/ອ່ອມ, ອາຫານຕາມສັ່ງ ຈົນເຖິງເສັ້ນ. ວັດຖຸດິບສົດໃໝ່ທຸກມື້, ປຸງແຕ່ງດ້ວຍສູດເຄື່ອງແກງພື້ນເມືອງ.",
          "Lao Homely Restaurant is a cosy, family-run spot serving a wide range of Lao and Thai-inspired dishes, from salads and soups to made-to-order rice plates and noodles. Ingredients are sourced fresh daily and cooked with traditional local recipes.",
          "Lao Homely Restaurant là một quán ăn gia đình ấm cúng, phục vụ đa dạng món Lào và Thái, từ gỏi, canh, cơm theo yêu cầu đến các món mì xào. Nguyên liệu tươi mỗi ngày, chế biến theo công thức truyền thống địa phương.")}</p>
        <p>{tri(
          "ບໍ່ວ່າຈະເປັນຄອບຄົວ, ໝູ່ເພື່ອນ ຫຼື ນັກທ່ອງທ່ຽວຜ່ານມາ ປາກເຊ, ຮ້ານພວກເຮົາຍິນດີຕ້ອນຮັບທ່ານດ້ວຍບັນຍາກາດອົບອຸ່ນ ແລະ ບໍລິການເປັນມິດ.",
          "Whether you're a local family, a group of friends, or a traveller passing through Pakse, we welcome you with a warm atmosphere and friendly service.",
          "Dù bạn là gia đình địa phương, nhóm bạn bè hay du khách ghé qua Pakse, quán luôn chào đón bạn với không gian ấm áp và phục vụ thân thiện.")}</p>
        <p class="note">{tri(
          "(ໝາຍເຫດ: ອານ ສາມາດປັບແກ້/ຕື່ມຂໍ້ມູນປະຫວັດຮ້ານແທ້ຈິງ ໃສ່ບ່ອນນີ້)",
          "(Note: replace this section with the restaurant's real founding story if available.)",
          "(Ghi chú: anh có thể thay đoạn này bằng câu chuyện thành lập quán thật nếu có.)")}</p>
      </div>
      <div class="col-photo">
        {img_placeholder("ບັນຍາກາດພາຍໃນຮ້ານ", "Interior atmosphere photo", "Ảnh không gian bên trong quán", "-> images/khong-gian-2.jpg")}
      </div>
    </div>
  </section>

  <section class="section alt-bg">
    <div class="section-inner">
      <h2 class="section-title center">{tri("ຄຸນຄ່າຂອງພວກເຮົາ", "What We Value", "Giá trị của chúng tôi")}</h2>
      <div class="grid-3">
        <div class="card plain">
          <span class="value-icon">LEAF</span>
          <h3>{tri("ວັດຖຸດິບສົດ", "Fresh Ingredients", "Nguyên liệu tươi")}</h3>
          <p>{tri("ເລືອກຊື້ຜັກ ແລະ ຊີ້ນສົດທຸກເຊົ້າ", "Vegetables and meat sourced fresh every morning", "Rau và thịt được chọn mua tươi mỗi sáng")}</p>
        </div>
        <div class="card plain">
          <span class="value-icon">FAMILY</span>
          <h3>{tri("ບັນຍາກາດຄອບຄົວ", "Family Atmosphere", "Không khí gia đình")}</h3>
          <p>{tri("ເໝາະສຳລັບທຸກຄົນໃນຄອບຄົວ", "A welcoming space for everyone in the family", "Không gian phù hợp cho mọi thành viên gia đình")}</p>
        </div>
        <div class="card plain">
          <span class="value-icon">STAR</span>
          <h3>{tri("ບໍລິການເປັນມິດ", "Friendly Service", "Phục vụ thân thiện")}</h3>
          <p>{tri("ພະນັກງານທີ່ຍິ້ມແຍ້ມ ແລະ ເອົາໃຈໃສ່", "Staff who greet you with a smile and attentive care", "Nhân viên luôn niềm nở và chu đáo")}</p>
        </div>
      </div>
    </div>
  </section>"""

with open(os.path.join(ROOT, "gioi-thieu.html"), "w", encoding="utf-8") as f:
    f.write(page("ກ່ຽວກັບພວກເຮົາ", "About Us", "Giới thiệu", "gioi-thieu.html", about_body))

# ---------------------------------------------------------------------------
# CONTACT PAGE
# ---------------------------------------------------------------------------
contact_body = f"""
  <section class="page-hero">
    <div class="section-inner">
      <p class="eyebrow">{tri(SITE_NAME_LO, SITE_NAME_EN, SITE_NAME_VI)}</p>
      <h1>{tri("ຕິດຕໍ່ພວກເຮົາ", "Contact Us", "Liên hệ với chúng tôi")}</h1>
    </div>
  </section>

  <section class="section">
    <div class="section-inner two-col">
      <div class="col-text">
        <h2 class="section-title">{tri("ຂໍ້ມູນຕິດຕໍ່", "Contact Information", "Thông tin liên hệ")}</h2>
        <ul class="contact-list">
          <li><strong>{tri('ທີ່ຢູ່', 'Address', 'Địa chỉ')}:</strong> <a href="{GMAPS_URL}" target="_blank" rel="noopener">{tri(ADDRESS_LO, ADDRESS_EN, ADDRESS_VI)}</a></li>
          <li><strong>{tri('ໂທລະສັບ', 'Phone', 'Điện thoại')}:</strong> <a href="tel:{PHONE.replace(' ', '')}">{PHONE}</a></li>
          <li><strong>WhatsApp:</strong> <a href="https://wa.me/{WHATSAPP_DIGITS}" target="_blank" rel="noopener">{PHONE}</a></li>
          <li><strong>Facebook:</strong> <a href="{FACEBOOK_URL}" target="_blank" rel="noopener">{FACEBOOK}</a></li>
          <li><strong>TikTok:</strong> <a href="{TIKTOK_URL}" target="_blank" rel="noopener">{TIKTOK}</a></li>
          <li><strong>{tri('ໂມງເປີດ-ປິດ', 'Opening Hours', 'Giờ mở cửa')}:</strong> 10:30 - 22:00</li>
        </ul>
      </div>
      <div class="col-photo">
        <div class="map-embed-wrap">
          <iframe src="https://www.google.com/maps?q=15.1215775,105.8019002&z=17&output=embed"
            width="100%" height="100%" style="border:0;" allowfullscreen="" loading="lazy"
            referrerpolicy="no-referrer-when-downgrade" title="{tri('ແຜນທີ່ Google Maps', 'Google Maps', 'Bản đồ Google Maps')}"></iframe>
        </div>
        <a class="btn btn-outline btn-sm map-link" href="{GMAPS_URL}" target="_blank" rel="noopener">{tri("ເປີດໃນ Google Maps", "Open in Google Maps", "Mở trong Google Maps")}</a>
      </div>
    </div>
  </section>"""

with open(os.path.join(ROOT, "lien-he.html"), "w", encoding="utf-8") as f:
    f.write(page("ຕິດຕໍ່", "Contact", "Liên hệ", "lien-he.html", contact_body))

# ---------------------------------------------------------------------------
# CART / CHECKOUT PAGE
# ---------------------------------------------------------------------------
cart_body = f"""
  <section class="page-hero">
    <div class="section-inner">
      <p class="eyebrow">{tri(SITE_NAME_LO, SITE_NAME_EN, SITE_NAME_VI)}</p>
      <h1>{tri("ຢືນຢັນ ແລະ ສັ່ງອາຫານ", "Confirm &amp; Order", "Xác nhận &amp; Đặt món")}</h1>
    </div>
  </section>

  <section class="section">
    <div class="section-inner">
      <div id="table-order-banner" class="table-banner" hidden>
        <span id="table-order-banner-text"></span>
      </div>

      <div id="no-table-msg" class="no-table-warning" hidden>
        {tri(
          "⚠ ກະລຸນາສະແກນ QR ຢູ່ໂຕະຂອງທ່ານກ່ອນ ຈຶ່ງຈະສັ່ງອາຫານໄດ້",
          "⚠ Please scan the QR code at your table first before ordering",
          "⚠ Vui lòng quét mã QR tại bàn của bạn trước khi đặt món")}
        <a class="btn btn-outline btn-sm" href="menu.html">{tri("ໄປເບິ່ງເມນູ", "Go to Menu", "Xem thực đơn")}</a>
      </div>

      <div id="cart-empty-msg" class="empty-cart-msg" hidden>
        <p>{tri("ທ່ານຍັງບໍ່ໄດ້ເລືອກອາຫານ.", "You haven't selected any dishes yet.", "Bạn chưa chọn món nào.")}</p>
        <a class="btn btn-primary" href="menu.html">{tri("ໄປເລືອກອາຫານ", "Go select dishes", "Đi chọn món")}</a>
      </div>

      <div id="cart-content">
        <div class="cart-table-wrap">
          <table class="cart-table" id="cart-table">
            <thead>
              <tr>
                <th>{tri("ລາຍການ", "Item", "Món ăn")}</th>
                <th>{tri("ລາຄາ", "Price", "Đơn giá")}</th>
                <th>{tri("ຈຳນວນ", "Qty", "SL")}</th>
                <th>{tri("ລວມ", "Subtotal", "Thành tiền")}</th>
                <th></th>
              </tr>
            </thead>
            <tbody id="cart-rows"></tbody>
          </table>
        </div>
        <div class="cart-total-row">
          <span>{tri("ລວມທັງໝົດ", "Total", "Tổng cộng")}:</span>
          <span id="cart-total">0 Lak</span>
        </div>

        <div id="kitchen-order-panel" class="kitchen-order-panel">
          <h2 class="section-title">{tri("ຢືນຢັນອໍເດີ", "Confirm Order", "Xác nhận đặt món")}</h2>
          <p>{tri(
            "ກົດ 'ສັ່ງອາຫານ' ເພື່ອບັນທຶກອໍເດີ ແລະ ສົ່ງໃຫ້ຫ້ອງຄົວຜ່ານ WhatsApp. ກະລຸນາຊຳລະເງິນທີ່ເຄົາເຕີຫຼັງຈາກກິນສຳເລັດ.",
            "Tap 'Place Order' to save your order and send it to the kitchen via WhatsApp. Please pay at the counter after your meal.",
            "Bấm 'Đặt món' để lưu đơn và gửi tới bếp qua WhatsApp. Vui lòng thanh toán tại quầy sau khi dùng bữa.")}</p>
          <button type="button" id="send-kitchen-btn" class="btn btn-primary btn-lg">{tri("ສັ່ງອາຫານ", "Place Order", "Đặt món")}</button>

          <div id="kitchen-sent-msg" class="kitchen-sent-msg" hidden>
            <p>{tri("ບັນທຶກອໍເດີສຳເລັດ! ລະຫັດອໍເດີ:", "Order saved! Order code:", "Đã lưu đơn thành công! Mã đơn:")} <strong id="kitchen-order-code"></strong></p>
            <p class="note">{tri(
              "ຂັ້ນຕອນສຸດທ້າຍ: ກົດປຸ່ມລຸ່ມນີ້ 1 ຄັ້ງ ເພື່ອສົ່ງອໍເດີໃຫ້ຫ້ອງຄົວທັງ 2 ເບີຜ່ານ WhatsApp (ຕ້ອງກົດ 'ສົ່ງ' ໃນແອັບ WhatsApp ແຕ່ລະແຊັດອີກເທື່ອໜຶ່ງ)",
              "Final step: tap the button below once to send the order to the kitchen on both phone numbers via WhatsApp (you still need to tap 'Send' inside each WhatsApp chat)",
              "Bước cuối: bấm nút bên dưới 1 lần để gửi đơn cho bếp qua WhatsApp tới cả 2 số điện thoại (mỗi cuộc trò chuyện vẫn cần bấm 'Gửi' trong ứng dụng WhatsApp)")}</p>
            <a id="wa-send-both" class="btn btn-primary btn-lg" href="#" rel="noopener">{tri("ສົ່ງໃຫ້ຫ້ອງຄົວ", "Send to kitchen", "Gửi cho bếp")}</a>
            <p class="note" style="margin-top:.6rem;">{tri(
              "ຖ້າ WhatsApp ບໍ່ຂຶ້ນ ຫຼື ບໍ່ໄດ້ກົດສົ່ງ, ສາມາດກັບມາໜ້ານີ້ ແລ້ວກົດປຸ່ມຂ້າງເທິງໃໝ່ໄດ້ (ບໍ່ຕ້ອງເລືອກອາຫານຄືນ)",
              "If WhatsApp didn't open or you didn't tap Send, you can come back to this page and tap the button above again (no need to re-select dishes)",
              "Nếu WhatsApp không mở hoặc chưa bấm Gửi, anh có thể quay lại trang này và bấm lại nút trên bất cứ lúc nào (không cần chọn lại món)")}</p>
            <a id="order-more-link" class="btn btn-outline" href="menu.html">{tri("ສັ່ງເພີ່ມ", "Order more", "Gọi thêm món khác")}</a>
          </div>
        </div>
      </div>
    </div>
  </section>"""

with open(os.path.join(ROOT, "gio-hang.html"), "w", encoding="utf-8") as f:
    f.write(page("ກະຕ່າ", "Cart", "Giỏ hàng", "gio-hang.html", cart_body))

# ---------------------------------------------------------------------------
# KITCHEN BOARD (internal - bep.html) - khong danh cho khach hang
# ---------------------------------------------------------------------------
bep_html = f"""<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Bang bep - {SITE_NAME_VI}</title>
<link rel="stylesheet" href="css/bep.css?v={ASSET_VERSION}">
</head>
<body>
  <header class="bep-header">
    <h1>BANG BEP - {SITE_NAME_VI}</h1>
    <div class="bep-status" id="bep-status">Dang ket noi...</div>
  </header>
  <main class="bep-main">
    <section class="bep-section">
      <h2>DANG CHO XU LY (<span id="bep-pending-count">0</span>)</h2>
      <div id="bep-pending-list" class="bep-order-grid"></div>
      <p id="bep-pending-empty" class="bep-empty-msg" hidden>Chua co don nao.</p>
    </section>
    <section class="bep-section bep-done-section">
      <h2>DA HOAN THANH (<span id="bep-done-count">0</span>)
        <button type="button" id="bep-clear-done-btn" class="bep-clear-btn">Don dep don da xong</button>
      </h2>
      <div id="bep-done-list" class="bep-order-grid bep-done-grid"></div>
    </section>
  </main>
  <script src="https://www.gstatic.com/firebasejs/10.13.0/firebase-app-compat.js"></script>
  <script src="https://www.gstatic.com/firebasejs/10.13.0/firebase-database-compat.js"></script>
  <script>window.HOMELY_FIREBASE_CONFIG = {json.dumps(FIREBASE_CONFIG)};</script>
  <script src="js/bep.js?v={ASSET_VERSION}"></script>
</body>
</html>
"""
with open(os.path.join(ROOT, "bep.html"), "w", encoding="utf-8") as f:
    f.write(bep_html)

# ---------------------------------------------------------------------------
# QR CODE PRINT SHEET (in-qr-ban.html) - trang in 10 ma QR dan tai ban
# ---------------------------------------------------------------------------
qr_cards = []
for n in range(1, NUM_TABLES + 1):
    qr_cards.append(f"""      <div class="qr-card">
        <p class="qr-card-eyebrow">{SITE_NAME_LO}</p>
        <img class="qr-card-img" src="images/qr/ban-{n}.png?v={ASSET_VERSION}" alt="QR ໂຕະທີ {n}">
        <p class="qr-card-table">ໂຕະທີ {n}</p>
        <p class="qr-card-hint">ສະແກນ QR ເພື່ອເບິ່ງເມນູ ແລະ ສັ່ງອາຫານ<br>ກະລຸນາຊຳລະເງິນທີ່ເຄົາເຕີຫຼັງຈາກກິນສຳເລັດ</p>
      </div>""")
qr_cards_html = "\n".join(qr_cards)

qr_sheet_html = f"""<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>In ma QR dat mon theo ban - {SITE_NAME_VI}</title>
<style>
  *{{box-sizing:border-box;}}
  body{{margin:0;font-family:'Segoe UI',Arial,sans-serif;background:#f2f2f2;color:#222;}}
  .toolbar{{
    padding:1rem 1.5rem;background:#7a1f1f;color:#fff;display:flex;
    justify-content:space-between;align-items:center;flex-wrap:wrap;gap:.8rem;
  }}
  .toolbar h1{{margin:0;font-size:1.3rem;}}
  .print-btn{{
    padding:.6rem 1.4rem;border:none;border-radius:6px;background:#d4a017;
    color:#2a1500;font-weight:700;cursor:pointer;font-size:1rem;
  }}
  .qr-grid{{
    display:grid;grid-template-columns:repeat(2, 1fr);gap:1.2rem;
    padding:1.5rem;max-width:900px;margin:0 auto;
  }}
  .qr-card{{
    background:#fff;border:2px solid #7a1f1f;border-radius:14px;
    padding:1.4rem;text-align:center;break-inside:avoid;
  }}
  .qr-card-eyebrow{{margin:0 0 .3rem;font-size:.9rem;color:#7a1f1f;font-weight:700;letter-spacing:.03em;}}
  .qr-card-img{{width:100%;max-width:260px;height:auto;margin:.4rem 0;}}
  .qr-card-table{{margin:.3rem 0;font-size:1.6rem;font-weight:800;color:#7a1f1f;}}
  .qr-card-hint{{margin:0;font-size:.85rem;color:#555;line-height:1.4;}}
  @media print{{
    .toolbar{{display:none;}}
    body{{background:#fff;}}
    .qr-grid{{padding:0;max-width:100%;}}
    .qr-card:nth-child(4n+1){{page-break-before:always;}}
    .qr-card:nth-child(-n+4){{page-break-before:avoid;}}
  }}
</style>
</head>
<body>
  <div class="toolbar">
    <h1>In ma QR dat mon theo ban ({NUM_TABLES} ban)</h1>
    <button class="print-btn" type="button" onclick="window.print()">In trang nay</button>
  </div>
  <div class="qr-grid">
{qr_cards_html}
  </div>
</body>
</html>
"""
with open(os.path.join(ROOT, "in-qr-ban.html"), "w", encoding="utf-8") as f:
    f.write(qr_sheet_html)

print("HTML pages generated (with cart + kitchen board + QR print sheet).")
