import hashlib, json, os, re, secrets, threading, time
from datetime import datetime, timedelta
import flet as ft

# ================= THEME =================
PRIMARY, DARK, MUTED, BORDER, BG = "#2563eb", "#0f172a", "#64748b", "#e2e8f0", "#f8fafc"
INDIGO, GREEN, AMBER, RED = "#4f46e5", "#16a34a", "#f59e0b", "#ef4444"
SUPPORT_PHONE = "+91 9561560448"      
SUPPORT_EMAIL = "support@gadgethub.in"  
WHATSAPP_URL = "https://wa.me/919561560448"  

U = lambda i: f"https://images.unsplash.com/{i}?auto=format&fit=crop&w=800&q=80"
S, L, A, G, W_, X = "Smartphones", "Laptops", "Audio", "Gaming", "Wearables", "Accessories"

# (id, name, category, price, old price, rating, reviews, badge, image URL, description)
RAW = [
    (1, "Samsung Galaxy S25", S, 74999, 79999, 4.8, 245, "BEST SELLER", "https://images.samsung.com/is/image/samsung/p6pim/in/feature/165835044/in-feature-galaxy-s25-s931-544962134?$FB_TYPE_A_MO_JPG$", "Premium flagship smartphone with powerful performance and an advanced camera."),
    (2, "iPhone 16 Pro", S, 119999, 124999, 4.9, 512, "PREMIUM", "https://rukminim3.flixcart.com/image/480/640/xif0q/mobile/o/o/9/-resized-original-imahggev6y5zhbjz.jpeg?q=90", "Premium smartphone with a powerful processor, pro camera system and stunning display."),
    (100, "Nothing Phone 3a Pro", S, 34000, 38000, 4.9, 512, "PREMIUM", "https://m.media-amazon.com/images/I/71vGgiknBQL._AC_UF1000,1000_QL80_.jpg", "Premium smartphone with a powerful processor, pro camera system and stunning display."),
    (3, "OnePlus 13", S, 69999, 74999, 4.7, 186, "TRENDING", "https://m.media-amazon.com/images/I/71vRZZ+FCiL._AC_UF1000,1000_QL80_.jpg", "High-performance 5G smartphone with fast charging and a premium design."),
    (4, "Google Pixel 11 Pro", S, 79999, 84999, 4.6, 143, "NEW", "https://media-ik.croma.com/Croma%20Assets/Communication/Mobiles/Images/325392_0_fI1oSY8Vf.png?updatedAt=1786601024435", "Smart Android phone with excellent computational photography and clean software."),
    (5, "Nothing Phone 4a Pro", S, 44999, 49999, 4.5, 97, "HOT", "https://m.media-amazon.com/images/I/31IpyH9EWuL._AC_UF1000,1000_QL80_.jpg", "Stylish smartphone with a unique design and smooth everyday performance."),
    (101, "vivo X300 FE", S, 84999, 96999, 4.5, 97, "HOT", "https://in-exstatic-vivofs.vivo.com/gdHFRinHEMrj3yPG/product/1786608927064/zip/img/wap/vivo-x300-fe.png", "Stylish smartphone with a unique design and smooth everyday performance."),
    (102, "Vivo X300 Ultra", S, 109999, 119999, 4.6, 143, "SUPER", "https://m.media-amazon.com/images/I/71ioZCO-biL._AC_UF1000,1000_QL80_.jpg", "Smart Android phone with excellent computational photography."),
   
    (103, "Xiaomi 15 Ultra", S, 109999, 119999, 4.6, 143, "SUPER", "https://fdn2.gsmarena.com/vv/bigpic/xiaomi-15-ultra.jpg", "16GB/512GB, 200 MP Leica quad camera, Snapdragon 8 Elite, WQHD+ AMOLED, Hyper AI."),
    (6, "ASUS Vivobook 16", L, 64999, 69999, 4.7, 184, "POPULAR", "https://m.media-amazon.com/images/I/71oGM-26fZL._SY450_.jpg", "Large-screen laptop for study, office work, coding and entertainment."),
    (7, "MacBook Air M5", L, 139490, 149900, 4.9, 325, "PREMIUM", "https://store.storeimages.cdn-apple.com/1/as-images.apple.com/is/mba13-midnight-select-202503?wid=904&hei=840&fmt=jpeg&qlt=90&.v=1741885366392", "Thin and powerful laptop for productivity, creative work and everyday computing."),
    (8, "HP Pavilion 15", L, 75794, 84999, 4.5, 156, "SALE", "https://rukminim2.flixcart.com/image/767/767/xif0q/computer/8/p/b/-original-imahg4utjwvr6bxs.jpeg?q=90", "Reliable everyday laptop for office work, education and multimedia."),
    (9, "Lenovo IdeaPad Plus", L, 184000, 189999, 4.6, 121, "NEW", "https://m.media-amazon.com/images/I/81Ev2S5nrVL.jpg", "Modern performance laptop with a premium design and strong multitasking."),
    (10, "Acer Nitro Gaming", L, 82999, 89999, 4.8, 209, "GAMING", "https://m.media-amazon.com/images/I/71Y00S6FsWL._AC_UF1000,1000_QL80_.jpg", "Gaming laptop built for demanding games and high-performance multitasking."),
    (104, "Acer Aspire 5", L, 73990, 99999, 4.6, 121, "NEW", "https://media-ik.croma.com/Croma%20Assets/Computers%20Peripherals/Laptop/Images/323615_0_uEVNRr5R8Y.png?updatedAt=1783326915036&tr=w-360", "Modern performance laptop with a premium design and strong multitasking."),
    (11, "Sony WH-1000XM5", A, 29999, 34999, 4.9, 421, "BEST SELLER", "photo-1505740420928-5e560c06d30e", "Premium wireless headphones with powerful sound and noise cancellation."),
    (12, "Apple AirPods Pro", A, 24999, 26999, 4.8, 389, "POPULAR", "photo-1600294037681-c80b4cb5b434", "Premium wireless earbuds with active noise cancellation and immersive sound."),
    (13, "JBL Tune 770NC", A, 5999, 7999, 4.6, 287, "VALUE", "photo-1484704849700-f032a568e944", "Comfortable wireless headphones with noise cancellation and long battery life."),
    (14, "Boat Airdopes Elite", A, 2499, 3499, 4.4, 632, "HOT", "photo-1590658268037-6bf12165a8df", "Affordable true wireless earbuds for music, calls and entertainment."),
    (15, "Bose SoundLink Speaker", A, 14999, 16999, 4.7, 178, "PREMIUM", "photo-1608043152269-423dbba4e7e1", "Portable Bluetooth speaker with rich, powerful audio."),
    (16, "PlayStation 5", G, 54999, 59999, 4.9, 516, "BEST SELLER", "photo-1606813907291-d86efa9b94db", "Next-generation console for immersive gaming and high-quality graphics."),
    (17, "Xbox Series X", G, 52999, 57999, 4.8, 321, "POPULAR", "photo-1621259182978-fbf93132d53d", "Powerful console with fast performance and high-quality gaming."),
    (18, "Gaming RGB Keyboard", G, 3499, 4999, 4.6, 215, "SALE", "photo-1587829741301-dc798b83add3", "Mechanical gaming keyboard with RGB lighting and responsive keys."),
    (19, "Pro Gaming Mouse", G, 2499, 3299, 4.7, 194, "HOT", "photo-1527814050087-3793815479db", "High-precision gaming mouse with an ergonomic design."),
    (20, "Gaming Headset RGB", G, 3999, 4999, 4.5, 143, "GAMING", "photo-1599669454699-248893623440", "Gaming headset with immersive audio, microphone and RGB lighting."),
    (21, "Apple Watch Series 11", W_, 46999, 49999, 4.8, 278, "PREMIUM", "https://m.media-amazon.com/images/I/71roT3lDUvL._AC_UF894,1000_QL80_.jpg", "Premium smartwatch with notifications, fitness features and modern design."),
    (22, "Samsung Galaxy Watch", W_, 29999, 34999, 4.7, 196, "POPULAR", "https://assets.myntassets.com/h_1440,q_75,w_1080/v1/assets/images/24435058/2023/8/14/5e0fb72d-aa26-4de7-999a-199e01ed1df21691985473864SamsungGalaxyWatch6LTE44mmSilverCompatiblewithAndroidonly1.jpg", "Smartwatch with health tracking, fitness features and stylish design."),
    (23, "Fitbit Charge", W_, 11999, 14999, 4.5, 157, "FITNESS", "https://m.media-amazon.com/images/I/51KJ3Pe2w5L.jpg", "Fitness tracker for activity monitoring, workouts and health goals."),
    (24, "Amazfit Active", W_, 8999, 10999, 4.4, 143, "VALUE", "https://m.media-amazon.com/images/I/61eLhGc40TL._AC_UF1000,1000_QL80_.jpg", "Affordable smartwatch with fitness tracking and smart features."),
    (25, "Smart Fitness Band", W_, 1999, 2999, 4.3, 412, "SALE", "https://m.media-amazon.com/images/I/61KpySHjUYL._AC_UF1000,1000_QL80_.jpg", "Lightweight fitness band for steps, activity and daily notifications."),
    (26, "65W Fast Charger", X, 1499, 1999, 4.6, 523, "VALUE", "https://m.media-amazon.com/images/I/51Lb0lChR3L._SL1500_.jpg", "Compact fast charger for smartphones, tablets and compatible devices."),
    (27, "USB-C Hub 7-in-1", X, 2299, 2999, 4.5, 187, "POPULAR", "https://m.media-amazon.com/images/I/61tPYsj5cGL._SX522_.jpg", "Multi-port USB-C hub for laptops and modern devices."),
    (28, "Wireless Power Bank", X, 2999, 3999, 4.4, 231, "HOT", "https://www.ugreenindia.com/cdn/shop/files/51_L-fiALcL._AC_SL1500.jpg?v=1763828011&width=1125", "Portable power bank for convenient wireless and wired charging."),
    (29, "Premium Phone Case", X, 799, 1299, 4.3, 648, "SALE", "https://millioncases.com/cdn/shop/files/Untitled_Instagram_Post_45_1.jpg?v=1774600640&width=1200", "Premium protective phone case with a stylish design."),
   
    (30, "4K Action Camera", X, 15999, 18999, 4.6, 119, "NEW", "photo-1502920917128-1aa500764cbd", "Compact 4K action camera for travel, adventure and video recording."),
]
KEYS = ("id", "name", "category", "price", "old", "rating", "reviews", "badge", "img", "desc")
PRODUCTS = [dict(zip(KEYS, r)) for r in RAW]
BY = {p["id"]: p for p in PRODUCTS}

#
ALT = {
    103: ["photo-1511707171634-5f897ff02aa9"],
    4: ["https://fdn2.gsmarena.com/vv/bigpic/google-pixel-10-pro.jpg"],
    30: ["https://static1.industrybuying.com/products/security/cctv-cameras/wifi-camera/SEC.WIF.724089633_1703760821062.webp"],
}

CATS = [(S, "📱", "Latest phones"), (L, "💻", "Powerful computing"), (A, "🎧", "Headphones & buds"),
        (G, "🎮", "Level up"), (W_, "⌚", "Smart lifestyle"), (X, "🔌", "Everyday essentials")]
CAT_ICON = {c[0]: c[1] for c in CATS}
BRANDS = ["Samsung", "Apple", "Sony", "OnePlus", "Google", "Nothing", "vivo", "Xiaomi", "JBL", "Bose", "HP", "Acer", "Lenovo", "ASUS"]
TRENDING = ["iPhone", "Sony", "Gaming", "Laptop", "Watch", "Earbuds"]

# code: (kind, value, min order, description)
COUPONS = {
    "GADGET10": ("pct", 10, 0, "10% off on every order"),
    "FESTIVE5": ("pct", 5, 5000, "Extra 5% off above ₹5,000"),
    "FLAT500": ("flat", 500, 20000, "₹500 off above ₹20,000"),
}

REVIEWS = [
    ("Rahul Sharma", "Delhi", "Delivery bahut fast thi aur product 100% original mila. Price bhi market se kam!"),
    ("Priya Verma", "Mumbai", "Easy returns aur great support. Mera naya phone ekdum sealed aaya. Highly recommended."),
    ("Aman Gupta", "Bengaluru", "Best deals on gaming gear. Checkout smooth tha aur packaging premium thi."),
]

DATA_FILE = os.path.join(os.getenv("FLET_APP_STORAGE_DATA") or ".", "gadgethub.json")
SHADOW = ft.BoxShadow(blur_radius=16, color=ft.Colors.with_opacity(0.08, "black"), offset=ft.Offset(0, 4))
STRIKE = ft.TextStyle(decoration=ft.TextDecoration.LINE_THROUGH)


# ================= HELPERS =================
def inr(n):
    s = str(int(round(n)))
    if len(s) > 3:
        s = re.sub(r"(\d)(?=(\d\d)+$)", r"\1,", s[:-3]) + "," + s[-3:]
    return "₹" + s


def pct(p):
    return round((1 - p["price"] / p["old"]) * 100)


def hash_pw(pw, salt=None):
    salt = salt or secrets.token_hex(8)
    return salt + ":" + hashlib.pbkdf2_hmac("sha256", pw.encode(), salt.encode(), 100000).hex()


def check_pw(pw, stored):
    return hash_pw(pw, stored.split(":")[0]) == stored


def load():
    try:
        with open(DATA_FILE, encoding="utf-8") as f:
            d = json.load(f)
    except Exception:
        d = {}
    return {"users": d.get("users", {}), "user": d.get("user"), "wish": d.get("wish", []),
            "cart": d.get("cart", {}), "orders": d.get("orders", {}), "recent": d.get("recent", [])}


def save(db):
    try:
        os.makedirs(os.path.dirname(os.path.abspath(DATA_FILE)), exist_ok=True)
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(db, f)
    except Exception:
        pass


def luhn_ok(d):
    s, alt = 0, False
    for ch in reversed(d):
        n = int(ch)
        if alt:
            n = n * 2 - 9 if n * 2 > 9 else n * 2
        s += n
        alt = not alt
    return len(d) > 0 and s % 10 == 0


def card_network(d):
    if d.startswith(("34", "37")):
        return "American Express"
    if d.startswith("4"):
        return "Visa"
    if re.match(r"^(5[1-5]|2[2-7])", d):
        return "Mastercard"
    if re.match(r"^(60|65|81|82|508)", d):
        return "RuPay"
    return ""


def end_of_day():
    return (datetime.now() + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)


# ================= APP =================
def main(page: ft.Page):
    page.title = "Gadget Hub"
    page.padding = 0
    page.bgcolor = BG
    page.theme_mode = ft.ThemeMode.LIGHT
    db = load()
    view = {"cat": None, "q": "", "sort": "default", "wish": False, "title": "All Products"}
    cur = {"dlg": None, "coupon": None, "after": None, "slide": 0, "auth": "login"}
    width = lambda: page.width or 400

    # ---------- small UI helpers ----------
    def T(v, size=14, bold=False, color=DARK, **k):
        return ft.Text(v, size=size, color=color, weight=ft.FontWeight.BOLD if bold else None, **k)

    def toast(m):
        page.open(ft.SnackBar(T(m, color="white"), bgcolor=DARK))

    def btn(label, fn, primary=True):
        st = ft.ButtonStyle(bgcolor=PRIMARY if primary else "white", color="white" if primary else DARK,
                            shape=ft.RoundedRectangleBorder(radius=10),
                            side=None if primary else ft.BorderSide(1, BORDER))
        return ft.ElevatedButton(label, on_click=fn, style=st)

    def wide(label, fn):
        b = btn(label, fn)
        b.expand = True
        return ft.Row([b])

    def field(label, **k):
        return ft.TextField(label=label, border_radius=10, dense=True, **k)

    def pad(c, v=8):
        return ft.Container(c, padding=ft.padding.symmetric(horizontal=14, vertical=v))

    def placeholder(p, w=None, h=None):
        return ft.Container(
            ft.Column([T(CAT_ICON.get(p["category"], "📷"), 34), T(p["name"], 10, color=MUTED, text_align=ft.TextAlign.CENTER,
                                                                     max_lines=2, overflow=ft.TextOverflow.ELLIPSIS)],
                      horizontal_alignment=ft.CrossAxisAlignment.CENTER, alignment=ft.MainAxisAlignment.CENTER, spacing=4),
            alignment=ft.alignment.center, bgcolor="#f1f5f9", width=w, height=h, padding=8)

    def src_of(s):
        return U(s) if s.startswith("photo-") else s

    def img(p, w=None, h=None):
        # main image -> backup images -> placeholder (chain)
        srcs = [src_of(s) for s in [p.get("img")] + ALT.get(p["id"], []) if s]
        node = placeholder(p, w, h)
        for s in reversed(srcs):
            fit = ft.ImageFit.COVER if "unsplash.com" in s else ft.ImageFit.CONTAIN
            node = ft.Image(src=s, width=w, height=h, fit=fit, error_content=node)
        return node

    def close():
        if cur["dlg"]:
            page.close(cur["dlg"])
            cur["dlg"] = None

    def popup(controls, title=None):
        close()
        d = ft.AlertDialog(
            scrollable=True, shape=ft.RoundedRectangleBorder(radius=18),
            title=T(title, 20, True) if title else None,
            content=ft.Container(ft.Column(controls, tight=True, spacing=10), width=min(width() - 60, 460)),
            inset_padding=ft.padding.symmetric(horizontal=12, vertical=20),
            on_dismiss=lambda e: cur.update(dlg=None))
        cur["dlg"] = d
        page.open(d)

    def chip(label, fn, selected=False):
        return ft.Container(T(label, 12, True, "white" if selected else DARK),
                            bgcolor=PRIMARY if selected else "white", border=ft.border.all(1, PRIMARY if selected else BORDER),
                            border_radius=20, padding=ft.padding.symmetric(horizontal=14, vertical=8), on_click=fn)

    def hlist(controls, height):
        return ft.ListView(controls, horizontal=True, spacing=12, height=height,
                           padding=ft.padding.symmetric(horizontal=14))

    def section_head(title, sub=None, action=None):
        left = ft.Column([T(title, 20, True)] + ([T(sub, 12, color=MUTED)] if sub else []), spacing=0, expand=True)
        row = [left]
        if action:
            row.append(ft.TextButton("View all →", on_click=action))
        return pad(ft.Row(row, vertical_alignment=ft.CrossAxisAlignment.CENTER), 4)

    # ---------- cart math ----------
    def cart_total():
        return sum(BY[int(k)]["price"] * q for k, q in db["cart"].items())

    def coupon_discount(sub):
        c = COUPONS.get(cur["coupon"])
        if not c or sub < c[2]:
            return 0
        return round(sub * c[1] / 100) if c[0] == "pct" else c[1]

    def totals():
        sub = cart_total()
        disc = coupon_discount(sub)
        ship = 0 if (sub >= 999 or sub == 0) else 49
        return sub, disc, ship, max(0, sub - disc + ship)

    # ---------- header ----------
    wl_btn = ft.IconButton(ft.Icons.FAVORITE_BORDER, on_click=lambda e: show_wishlist())
    cart_btn = ft.IconButton(ft.Icons.SHOPPING_CART_OUTLINED, on_click=lambda e: open_cart())
    user_btn = ft.IconButton(ft.Icons.PERSON_OUTLINE, on_click=lambda e: open_account())

    def refresh_badges():
        n, w = sum(db["cart"].values()), len(db["wish"])
        cart_btn.badge = ft.Badge(text=str(n)) if n else None
        wl_btn.badge = ft.Badge(text=str(w)) if w else None
        user_btn.icon = ft.Icons.PERSON if db["user"] else ft.Icons.PERSON_OUTLINE
        user_btn.icon_color = PRIMARY if db["user"] else DARK

    search = ft.TextField(hint_text="Search phones, laptops, audio...", prefix_icon=ft.Icons.SEARCH, border_radius=14,
                          dense=True, filled=True, bgcolor="#f1f5f9", border_color="transparent",
                          on_change=lambda e: on_search(e, False), on_submit=lambda e: on_search(e, True))

    logo = ft.Container(
        ft.Row([ft.Container(T("G", 18, True, "white"), width=36, height=36, border_radius=10, alignment=ft.alignment.center,
                             gradient=ft.LinearGradient(begin=ft.alignment.top_left, end=ft.alignment.bottom_right,
                                                        colors=[PRIMARY, INDIGO])),
                T("Gadget", 21, True), T("Hub", 21, True, PRIMARY)], spacing=2),
        on_click=lambda e: show_home())

    header = ft.Container(
        ft.Column([ft.Row([logo, ft.Row([wl_btn, cart_btn, user_btn], spacing=0)],
                          alignment=ft.MainAxisAlignment.SPACE_BETWEEN), search], spacing=4),
        bgcolor="white", padding=ft.padding.only(left=14, right=14, top=6, bottom=10), shadow=SHADOW)

    announce = ft.Container(
        T("🚚 Free delivery above ₹999  •  Use code GADGET10 for 10% OFF", 11, True, "white", text_align=ft.TextAlign.CENTER),
        gradient=ft.LinearGradient(colors=[DARK, "#1e3a8a"]), padding=ft.padding.symmetric(horizontal=10, vertical=7),
        alignment=ft.alignment.center)

    # ---------- hero carousel ----------
    SLIDES = [
        ("FESTIVE SALE 🎉", "Up to 30% off on\ntop gadgets", "Phones, laptops, audio & more", "Shop Now", None, "📱", ["#2563eb", "#4f46e5"]),
        ("GAMING ZONE", "PS5, Xbox & pro\naccessories", "Level up your setup today", "Explore Gaming", G, "🎮", ["#7c3aed", "#db2777"]),
        ("PREMIUM AUDIO", "Noise cancelling\nheadphones", "Starting at just ₹2,499", "Shop Audio", A, "🎧", ["#0f172a", "#1d4ed8"]),
        ("SMART LIVING", "Watches & fitness\nbands", "Track every step in style", "Shop Wearables", W_, "⌚", ["#0d9488", "#059669"]),
    ]

    def slide_ui(i):
        tag, title, sub, cta, cat, emoji, cols = SLIDES[i]
        go = (lambda e: show_all()) if cat is None else (lambda e, c=cat: show_cat(c))
        cta_btn = ft.ElevatedButton(cta, on_click=go, style=ft.ButtonStyle(
            bgcolor="white", color=DARK, shape=ft.RoundedRectangleBorder(radius=10)))
        return ft.Container(
            ft.Row([ft.Column([
                ft.Container(T(tag, 10, True, "white"), bgcolor=ft.Colors.with_opacity(0.22, "white"), border_radius=20,
                             padding=ft.padding.symmetric(horizontal=10, vertical=4)),
                T(title, 24, True, "white"), T(sub, 12, color=ft.Colors.with_opacity(0.85, "white")), cta_btn],
                spacing=8, expand=True, alignment=ft.MainAxisAlignment.CENTER),
                T(emoji, 64)], vertical_alignment=ft.CrossAxisAlignment.CENTER),
            height=210, border_radius=22, padding=22, shadow=SHADOW,
            gradient=ft.LinearGradient(begin=ft.alignment.top_left, end=ft.alignment.bottom_right, colors=cols))

    hero_box = ft.AnimatedSwitcher(slide_ui(0), transition=ft.AnimatedSwitcherTransition.FADE, duration=600,
                                   reverse_duration=300)
    dots = ft.Row(alignment=ft.MainAxisAlignment.CENTER, spacing=6)

    def build_dots():
        dots.controls = [ft.Container(width=22 if i == cur["slide"] else 8, height=8, border_radius=4,
                                      bgcolor=PRIMARY if i == cur["slide"] else "#cbd5e1",
                                      animate=ft.Animation(300), on_click=lambda e, i=i: set_slide(i))
                         for i in range(len(SLIDES))]

    def set_slide(i):
        cur["slide"] = i % len(SLIDES)
        hero_box.content = slide_ui(cur["slide"])
        build_dots()
        try:
            hero_box.update()
            dots.update()
        except Exception:
            pass

    build_dots()

    # ---------- flash sale countdown ----------
    hh, mm, ss = T("00", 14, True, "white"), T("00", 14, True, "white"), T("00", 14, True, "white")

    def tbox(t):
        return ft.Container(t, bgcolor=DARK, border_radius=8, padding=ft.padding.symmetric(horizontal=8, vertical=5))

    timer_row = ft.Row([tbox(hh), T(":", 16, True), tbox(mm), T(":", 16, True), tbox(ss)], spacing=4)

    def tick_values():
        s = max(0, int((end_of_day() - datetime.now()).total_seconds()))
        hh.value, mm.value, ss.value = f"{s // 3600:02d}", f"{s % 3600 // 60:02d}", f"{s % 60:02d}"

    tick_values()

    def ticker():
        n = 0
        while True:
            time.sleep(1)
            n += 1
            try:
                tick_values()
                timer_row.update()
                if n % 5 == 0:
                    set_slide(cur["slide"] + 1)
            except Exception:
                break

    # ---------- product cards ----------
    def mini(p, w=164):
        top = ft.Stack([
            ft.Container(img(p, None, 118), left=0, right=0, top=0, bottom=0, bgcolor="white",
                         alignment=ft.alignment.center, padding=6),
            ft.Container(T(f"{pct(p)}% OFF", 9, True, "white"), bgcolor=GREEN, border_radius=6, left=8, top=8,
                         padding=ft.padding.symmetric(horizontal=6, vertical=3)),
        ], height=118)
        body = ft.Container(ft.Column([
            ft.Container(T(p["name"], 12, True, max_lines=2, overflow=ft.TextOverflow.ELLIPSIS), height=32),
            T(f"★ {p['rating']}  ({p['reviews']})", 10, color=AMBER),
            T(inr(p["price"]), 14, True),
            T(inr(p["old"]), 10, color="#94a3b8", style=STRIKE),
        ], spacing=2), padding=10)
        return ft.Container(ft.Column([top, body], spacing=0), width=w, bgcolor="white", border=ft.border.all(1, BORDER),
                            border_radius=16, clip_behavior=ft.ClipBehavior.ANTI_ALIAS, on_click=lambda e, p=p: quick(p))

    def card(p):
        liked = p["id"] in db["wish"]
        top = ft.Stack([
            ft.Container(img(p, None, 188), left=0, right=0, top=0, bottom=0, bgcolor="white",
                         alignment=ft.alignment.center, padding=8, on_click=lambda e, p=p: quick(p)),
            ft.Container(T(p["badge"], 9, True, "white"), bgcolor=DARK, border_radius=6, left=8, top=8,
                         padding=ft.padding.symmetric(horizontal=7, vertical=4)),
            ft.Container(T(f"{pct(p)}% OFF", 9, True, "white"), bgcolor=GREEN, border_radius=6, left=8, bottom=8,
                         padding=ft.padding.symmetric(horizontal=7, vertical=4)),
            ft.IconButton(ft.Icons.FAVORITE if liked else ft.Icons.FAVORITE_BORDER, icon_size=18, right=2, top=2,
                          icon_color=RED if liked else MUTED, bgcolor="white", on_click=lambda e, i=p["id"]: toggle_wish(i)),
        ], height=200)
        add = ft.ElevatedButton("Add to Cart", expand=True, on_click=lambda e, i=p["id"]: add_cart(i),
                                style=ft.ButtonStyle(bgcolor=DARK, color="white", shape=ft.RoundedRectangleBorder(radius=10)))
        body = ft.Container(ft.Column([
            T(p["category"].upper(), 9, True, MUTED),
            T(p["name"], 14, True, max_lines=2, overflow=ft.TextOverflow.ELLIPSIS),
            ft.Row([ft.Container(T(f"★ {p['rating']}", 10, True, "white"), bgcolor=GREEN, border_radius=6,
                                 padding=ft.padding.symmetric(horizontal=6, vertical=2)),
                    T(f"({p['reviews']})", 11, color=MUTED)], spacing=6),
            ft.Row([T(inr(p["price"]), 16, True), T(inr(p["old"]), 11, color="#94a3b8", style=STRIKE)], wrap=True, spacing=6),
            ft.Row([add, ft.IconButton(ft.Icons.VISIBILITY_OUTLINED, icon_color=PRIMARY, bgcolor="#eff6ff",
                                       on_click=lambda e, p=p: quick(p))], spacing=4),
        ], spacing=4), padding=12)
        return ft.Container(ft.Column([top, body], spacing=0, horizontal_alignment=ft.CrossAxisAlignment.STRETCH),
                            bgcolor="white", border=ft.border.all(1, BORDER), border_radius=16, shadow=SHADOW,
                            clip_behavior=ft.ClipBehavior.ANTI_ALIAS, col={"xs": 6, "sm": 4, "md": 3})

    # ---------- listing (all products grid) ----------
    title_txt = T("All Products", 22, True)
    count_txt = T("", 12, color=MUTED)
    grid = ft.ResponsiveRow(spacing=10, run_spacing=10)
    cat_chips = ft.ListView(horizontal=True, spacing=8, height=42)
    sort_dd = ft.Dropdown(value="default", dense=True, width=170, border_radius=10, text_size=12,
                          options=[ft.dropdown.Option("default", "Featured"), ft.dropdown.Option("low", "Price: Low to High"),
                                   ft.dropdown.Option("high", "Price: High to Low"), ft.dropdown.Option("rating", "Top Rated")],
                          on_change=lambda e: (view.update(sort=sort_dd.value), render()))
    recent_box = ft.Column(spacing=0, visible=False)

    def current():
        items = PRODUCTS
        if view["wish"]:
            items = [p for p in items if p["id"] in db["wish"]]
        if view["cat"]:
            items = [p for p in items if p["category"] == view["cat"]]
        q = view["q"].strip().lower()
        if q:
            items = [p for p in items if q in (p["name"] + " " + p["category"] + " " + p["desc"]).lower()]
        s = view["sort"]
        if s == "low":
            items = sorted(items, key=lambda p: p["price"])
        elif s == "high":
            items = sorted(items, key=lambda p: -p["price"])
        elif s == "rating":
            items = sorted(items, key=lambda p: -p["rating"])
        return items

    def refresh_recent():
        ids = [i for i in db["recent"] if i in BY]
        recent_box.visible = bool(ids)
        recent_box.controls = ([section_head("Recently Viewed", "Pick up where you left off"),
                                hlist([mini(BY[i]) for i in ids], 232)] if ids else [])

    def render():
        items = current()
        title_txt.value = view["title"]
        count_txt.value = f"{len(items)} products"
        grid.controls = [card(p) for p in items] or [ft.Container(
            ft.Column([T("🔍", 50), T("No products found", 18, True), T("Try another search or category.", color=MUTED)],
                      horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=40, alignment=ft.alignment.center, col=12)]
        cat_chips.controls = [chip("All", lambda e: show_all(), view["cat"] is None and not view["wish"] and not view["q"])] + [
            chip(f"{ic} {c}", lambda e, c=c: show_cat(c, False), view["cat"] == c) for c, ic, _ in CATS]
        refresh_recent()
        refresh_badges()
        page.update()

    def go_products():
        main_col.scroll_to(key="products", duration=500)

    def set_view(cat=None, q="", wish=False, title="All Products"):
        view.update(cat=cat, q=q, wish=wish, title=title)
        search.value = q
        render()

    def show_home():
        sort_dd.value = view["sort"] = "default"
        set_view()
        main_col.scroll_to(offset=0, duration=500)

    def show_cat(c, scroll=True):
        set_view(cat=c, title=c)
        if scroll:
            go_products()

    def show_all():
        set_view()
        go_products()

    def show_wishlist():
        set_view(wish=True, title="My Wishlist")
        go_products()

    def search_for(q):
        set_view(q=q, title=f"Results for “{q}”")
        go_products()

    def on_search(e, scroll):
        q = search.value or ""
        set_view(q=q, title="Search Results" if q.strip() else "All Products")
        if scroll and q.strip():
            go_products()

    def toggle_wish(i):
        if i in db["wish"]:
            db["wish"].remove(i)
            toast("Removed from wishlist")
        else:
            db["wish"].append(i)
            toast("Added to wishlist ❤️")
        save(db)
        render()

    def add_cart(i, n=1, silent=False):
        k = str(i)
        db["cart"][k] = min(10, db["cart"].get(k, 0) + n)
        save(db)
        refresh_badges()
        page.update()
        if not silent:
            toast("Added to cart 🛒")

    def quick(p):
        db["recent"] = [p["id"]] + [i for i in db["recent"] if i != p["id"]][:7]
        save(db)
        eta = (datetime.now() + timedelta(days=3)).strftime("%a, %d %b")

        def buy_now(e, i=p["id"]):
            add_cart(i, silent=True)
            open_cart()

        popup([
            ft.Container(img(p, min(width() - 92, 428), 230), border_radius=14, bgcolor="white",
                         clip_behavior=ft.ClipBehavior.ANTI_ALIAS),
            ft.Row([ft.Container(T(p["badge"], 9, True, "white"), bgcolor=DARK, border_radius=6,
                                 padding=ft.padding.symmetric(horizontal=8, vertical=4)),
                    T(p["category"].upper(), 10, True, MUTED)], spacing=8),
            T(f"★ {p['rating']}  ({p['reviews']} reviews)", 12, color=AMBER),
            T(p["desc"], color=MUTED),
            ft.Row([T(inr(p["price"]), 26, True), T(inr(p["old"]), 13, color="#94a3b8", style=STRIKE),
                    T(f"{pct(p)}% off", 13, True, GREEN)], wrap=True, spacing=8),
            ft.Container(ft.Column([T(f"🚚 Free delivery by {eta}", 12), T("✅ 100% genuine  •  🔄 7-day easy returns", 12)],
                                   spacing=4), bgcolor="#f0fdf4", border_radius=10, padding=10),
            ft.Row([btn("Add to Cart", lambda e, i=p["id"]: add_cart(i)), btn("Buy Now", buy_now),
                    btn("♡ Wishlist", lambda e, i=p["id"]: (close(), toggle_wish(i)), False)], wrap=True),
        ], p["name"])
        refresh_recent()
        page.update()

    # ---------- cart ----------
    cart_col = ft.Column(tight=True, spacing=8)
    coupon_tf = field("Coupon code", expand=True, text_size=13)

    def change(k, d):
        q = db["cart"].get(k, 0) + d
        if q <= 0:
            db["cart"].pop(k, None)
        else:
            db["cart"][k] = min(10, q)
        save(db)
        refresh_cart()

    def apply_coupon(e):
        code = (coupon_tf.value or "").strip().upper()
        c = COUPONS.get(code)
        if not c:
            toast("Invalid coupon code")
        elif cart_total() < c[2]:
            toast(f"Minimum order {inr(c[2])} required")
        else:
            cur["coupon"] = code
            toast(f"{code} applied 🎉")
        refresh_cart()

    def remove_coupon(e):
        cur["coupon"] = None
        refresh_cart()

    def line(label, value, bold=False, color=DARK):
        return ft.Row([T(label, 15 if bold else 13, bold, color), T(value, 15 if bold else 13, bold, color)],
                      alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

    def refresh_cart():
        if not db["cart"]:
            cart_col.controls = [ft.Column([T("🛒", 44), T("Your cart is empty", 16, True),
                                            T("Add some gadgets to get started.", color=MUTED)],
                                           horizontal_alignment=ft.CrossAxisAlignment.CENTER)]
        else:
            rows = []
            for k, q in db["cart"].items():
                p = BY[int(k)]
                rows.append(ft.Row([
                    ft.Container(img(p, 64, 64), width=64, height=64, border_radius=10, bgcolor="white",
                                 clip_behavior=ft.ClipBehavior.ANTI_ALIAS, border=ft.border.all(1, BORDER)),
                    ft.Column([T(p["name"], 13, True, max_lines=2, overflow=ft.TextOverflow.ELLIPSIS),
                               T(inr(p["price"]), 12, color=MUTED),
                               ft.Row([ft.IconButton(ft.Icons.REMOVE, icon_size=16, on_click=lambda e, k=k: change(k, -1)),
                                       T(str(q), 14, True),
                                       ft.IconButton(ft.Icons.ADD, icon_size=16, on_click=lambda e, k=k: change(k, 1)),
                                       ft.IconButton(ft.Icons.DELETE_OUTLINE, icon_size=18, icon_color="#dc2626",
                                                     on_click=lambda e, k=k: change(k, -99))], spacing=0)],
                              spacing=0, expand=True)], vertical_alignment=ft.CrossAxisAlignment.START))
            sub, disc, ship, total = totals()
            if cur["coupon"] and disc:
                coupon_ui = ft.Row([T(f"🎟️ {cur['coupon']} applied", 12, True, GREEN),
                                    ft.TextButton("Remove", on_click=remove_coupon)],
                                   alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
            else:
                cur["coupon"] = None
                coupon_ui = ft.Row([coupon_tf, btn("Apply", apply_coupon, False)], spacing=6)
            summary = [line("Subtotal", inr(sub))]
            if disc:
                summary.append(line("Coupon discount", "-" + inr(disc), color=GREEN))
            summary.append(line("Delivery", "FREE" if ship == 0 else inr(ship), color=GREEN if ship == 0 else DARK))
            cart_col.controls = rows + [ft.Divider(height=1, color=BORDER), coupon_ui] + summary + [
                ft.Divider(height=1, color=BORDER), line("Total", inr(total), True),
                wide("Proceed to Checkout", lambda e: checkout())]
        refresh_badges()
        page.update()

    def open_cart():
        popup([cart_col], "Your Cart")
        refresh_cart()

    # ---------- account ----------
    def open_account(after=None):
        if after:
            cur["after"] = after
        if db["user"]:
            u = db["users"].get(db["user"], {})
            orders = db["orders"].get(db["user"], [])
            ctrls = [ft.Container(ft.Row([
                ft.Container(T((u.get("name", "U")[:1] or "U").upper(), 20, True, "white"), width=48, height=48, border_radius=24,
                             bgcolor=PRIMARY, alignment=ft.alignment.center),
                ft.Column([T(u.get("name", ""), 16, True), T(db["user"], 12, color=MUTED)], spacing=0)], spacing=12),
                bgcolor="#eff6ff", border_radius=12, padding=12), T("My Orders", 15, True)]
            if not orders:
                ctrls.append(T("No orders yet.", color=MUTED))
            for o in orders[:5]:
                ctrls.append(ft.Container(ft.Column([
                    ft.Row([T(o["id"], 12, True), T("✅ " + o["status"], 11, True, GREEN)],
                           alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    T(o["date"] + "  •  " + o["pay"], 11, color=MUTED),
                    T(", ".join(f"{n} ×{q}" for n, q, _ in o["items"]), 12, max_lines=2, overflow=ft.TextOverflow.ELLIPSIS),
                    T(inr(o["total"]), 14, True)], spacing=3), border=ft.border.all(1, BORDER), border_radius=12, padding=10))
            ctrls.append(btn("Logout", lambda e: logout(), False))
            popup(ctrls, "My Account")
        else:
            auth_view()

    def auth_view():
        signup = cur["auth"] == "signup"
        name = field("Full name")
        email = field("Email", keyboard_type=ft.KeyboardType.EMAIL)
        pw = field("Password", password=True, can_reveal_password=True)

        def submit(e):
            em, pwd = (email.value or "").strip().lower(), pw.value or ""
            if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", em):
                return toast("Enter a valid email")
            if signup:
                if not (name.value or "").strip():
                    return toast("Enter your name")
                if len(pwd) < 6:
                    return toast("Password must be at least 6 characters")
                if em in db["users"]:
                    return toast("Account already exists. Please login.")
                db["users"][em] = {"name": name.value.strip(), "pw": hash_pw(pwd)}
            else:
                u = db["users"].get(em)
                if not u or not check_pw(pwd, u["pw"]):
                    return toast("Wrong email or password")
            db["user"] = em
            save(db)
            refresh_badges()
            close()
            page.update()
            toast("Welcome, " + db["users"][em]["name"] + " 👋")
            nxt, cur["after"] = cur["after"], None
            if nxt == "checkout":
                checkout()

        def flip(e):
            cur["auth"] = "login" if signup else "signup"
            auth_view()

        popup(([name] if signup else []) + [email, pw, wide("Create Account" if signup else "Login", submit),
              ft.TextButton("Already have an account? Login" if signup else "New here? Create an account", on_click=flip)],
              "Sign Up" if signup else "Welcome Back")

    def logout():
        db["user"] = None
        save(db)
        close()
        refresh_badges()
        page.update()
        toast("Logged out")

    # ---------- checkout ----------
    def checkout():
        if not db["cart"]:
            return toast("Your cart is empty")
        if not db["user"]:
            toast("Please login to continue")
            return open_account("checkout")
        u = db["users"].get(db["user"], {})
        nm = field("Full name", value=u.get("name", ""))
        ph_ = field("Mobile number", keyboard_type=ft.KeyboardType.PHONE, max_length=10, prefix_text="+91 ")
        addr = field("Full address", multiline=True, min_lines=2, max_lines=3)
        pin = field("Pincode", keyboard_type=ft.KeyboardType.NUMBER, max_length=6)
        sub, disc, ship, total = totals()

        # ----- payment detail fields (UPI / Card) -----
        upi_id = field("UPI ID (e.g. name@okhdfcbank)", keyboard_type=ft.KeyboardType.EMAIL, prefix_icon=ft.Icons.QR_CODE_2)
        card_no = field("Card number", keyboard_type=ft.KeyboardType.NUMBER, max_length=19, prefix_icon=ft.Icons.CREDIT_CARD)
        card_name = field("Name on card", capitalization=ft.TextCapitalization.WORDS)
        card_exp = field("Expiry (MM/YY)", keyboard_type=ft.KeyboardType.NUMBER, max_length=5, expand=True)
        card_cvv = field("CVV", password=True, keyboard_type=ft.KeyboardType.NUMBER, max_length=4, expand=True)

        def fmt_card(e):
            d = re.sub(r"\D", "", card_no.value or "")[:16]
            card_no.value = " ".join(d[i:i + 4] for i in range(0, len(d), 4))
            net = card_network(d)
            card_no.helper_text = net if net else None
            card_no.update()

        def fmt_exp(e):
            d = re.sub(r"\D", "", card_exp.value or "")[:4]
            card_exp.value = d if len(d) <= 2 else d[:2] + "/" + d[2:]
            card_exp.update()

        def only_digits(e):
            card_cvv.value = re.sub(r"\D", "", card_cvv.value or "")[:4]
            card_cvv.update()

        card_no.on_change, card_exp.on_change, card_cvv.on_change = fmt_card, fmt_exp, only_digits

        upi_box = ft.Container(ft.Column([upi_id, T("🔒 We never ask for your UPI PIN.", 11, color=MUTED)], spacing=6),
                               visible=False, bgcolor="#f8fafc", border=ft.border.all(1, BORDER), border_radius=12, padding=10)
        card_box = ft.Container(ft.Column([card_no, card_name, ft.Row([card_exp, card_cvv], spacing=8),
                                           T("🔒 Card details are used only to verify this order and are never saved.", 11, color=MUTED)],
                                          spacing=8),
                                visible=False, bgcolor="#f8fafc", border=ft.border.all(1, BORDER), border_radius=12, padding=10)

        def on_pay_change(e):
            upi_box.visible = pay.value == "UPI"
            card_box.visible = pay.value == "Card"
            page.update()

        pay = ft.RadioGroup(value="Cash on Delivery", on_change=on_pay_change, content=ft.Column([
            ft.Radio(value="Cash on Delivery", label="💵 Cash on Delivery"),
            ft.Radio(value="UPI", label="📲 UPI (GPay / PhonePe / Paytm)"),
            ft.Radio(value="Card", label="💳 Credit / Debit Card")], spacing=0))

        def pay_error():
            """Returns an error message if payment details are invalid, else None."""
            if pay.value == "UPI":
                if not re.fullmatch(r"[A-Za-z0-9._-]{2,64}@[A-Za-z]{2,32}", (upi_id.value or "").strip()):
                    return "Enter a valid UPI ID (like name@okhdfcbank)"
            elif pay.value == "Card":
                digits = re.sub(r"\D", "", card_no.value or "")
                if not (13 <= len(digits) <= 19) or not luhn_ok(digits):
                    return "Enter a valid card number"
                if len((card_name.value or "").strip()) < 3:
                    return "Enter the name on your card"
                m = re.fullmatch(r"(\d{2})/(\d{2})", card_exp.value or "")
                if not m or not 1 <= int(m.group(1)) <= 12:
                    return "Enter expiry as MM/YY"
                now = datetime.now()
                if (2000 + int(m.group(2)), int(m.group(1))) < (now.year, now.month):
                    return "This card has expired"
                need = 4 if card_network(digits) == "American Express" else 3
                if not re.fullmatch(rf"\d{{{need}}}", card_cvv.value or ""):
                    return f"Enter the {need}-digit CVV"
            return None

        def pay_label():
            if pay.value == "UPI":
                uid = upi_id.value.strip()
                return f"UPI ({uid[:2]}***@{uid.split('@')[-1]})"
            if pay.value == "Card":
                return "Card •••• " + re.sub(r"\D", "", card_no.value)[-4:]
            return pay.value

        def place(e):
            if not (nm.value or "").strip():
                return toast("Enter your name")
            if not re.fullmatch(r"[6-9]\d{9}", ph_.value or ""):
                return toast("Enter a valid 10-digit mobile number")
            if len((addr.value or "").strip()) < 8:
                return toast("Enter your full address")
            if not re.fullmatch(r"\d{6}", pin.value or ""):
                return toast("Enter a valid 6-digit pincode")
            err = pay_error()
            if err:
                return toast(err)
            label = pay_label()  # only a masked label is stored; card number/CVV/expiry are never saved
            oid = "GH" + datetime.now().strftime("%y%m%d%H%M%S")
            order = {"id": oid, "date": datetime.now().strftime("%d %b %Y, %I:%M %p"), "pay": label, "status": "Confirmed",
                     "total": total, "items": [[BY[int(k)]["name"], q, BY[int(k)]["price"]] for k, q in db["cart"].items()],
                     "address": f"{addr.value.strip()} - {pin.value}", "name": nm.value.strip(), "phone": ph_.value}
            db["orders"].setdefault(db["user"], []).insert(0, order)
            db["cart"] = {}
            cur["coupon"] = None
            save(db)
            refresh_badges()
            eta = (datetime.now() + timedelta(days=3)).strftime("%a, %d %b")
            popup([ft.Column([T("🎉", 56), T("Order placed!", 22, True),
                              T(f"Order ID: {oid}", 13, True, PRIMARY), T(f"{'Pay on delivery' if label == 'Cash on Delivery' else 'Total paid'}: {inr(total)}  •  {label}", 12, color=MUTED),
                              T(f"Estimated delivery: {eta}", 12, color=MUTED)],
                             horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=6),
                   wide("Continue Shopping", lambda e: close())])
            page.update()

        summary = [line("Subtotal", inr(sub))]
        if disc:
            summary.append(line("Coupon discount", "-" + inr(disc), color=GREEN))
        summary.append(line("Delivery", "FREE" if ship == 0 else inr(ship)))
        popup([T("Delivery details", 14, True), nm, ph_, addr, pin, T("Payment method", 14, True), pay, upi_box, card_box,
               ft.Divider(height=1, color=BORDER)] + summary + [line("Total", inr(total), True),
               wide(f"Place Order • {inr(total)}", place)], "Checkout")

    # ---------- help / support ----------
    def open_help(e=None):
        popup([T("We are here to help You 😊", 13, color=MUTED),
               ft.ListTile(leading=ft.Icon(ft.Icons.CHAT, color="#22c55e"), title=T("Chat on WhatsApp", 14, True),
                           on_click=lambda e: page.launch_url(WHATSAPP_URL)),
               ft.ListTile(leading=ft.Icon(ft.Icons.CALL, color=PRIMARY), title=T(SUPPORT_PHONE, 14, True),
                           subtitle=T("Mon–Sat, 9am – 8pm", 11, color=MUTED), on_click=lambda e: page.launch_url("tel:" + SUPPORT_PHONE.replace(" ", ""))),
               ft.ListTile(leading=ft.Icon(ft.Icons.MAIL_OUTLINE, color=PRIMARY), title=T(SUPPORT_EMAIL, 14, True),
                           on_click=lambda e: page.launch_url("mailto:" + SUPPORT_EMAIL))], "Help & Support")

    # ---------- homepage sections ----------
    def trust_strip():
        items = [("🚚", "Free Delivery", "On orders ₹999+"), ("🔄", "7-Day Returns", "Easy & hassle-free"),
                 ("✅", "100% Genuine", "Brand warranty"), ("🔒", "Secure Payment", "UPI, Cards, COD")]
        return pad(ft.ResponsiveRow([ft.Container(ft.Row([T(ic, 26), ft.Column([T(t, 12, True), T(s, 10, color=MUTED)], spacing=0, expand=True)],
                                                         spacing=10), bgcolor="white", border=ft.border.all(1, BORDER), border_radius=14,
                                                  padding=12, col={"xs": 6, "md": 3}) for ic, t, s in items], spacing=8, run_spacing=8))

    def category_row():
        cards = [ft.Container(ft.Column([
            ft.Container(T(ic, 28), width=62, height=62, border_radius=31, bgcolor="#eff6ff", alignment=ft.alignment.center),
            T(c, 11, True, text_align=ft.TextAlign.CENTER)], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=6),
            width=92, on_click=lambda e, c=c: show_cat(c)) for c, ic, _ in CATS]
        return ft.Container(ft.Column([section_head("Shop by Category", "Find exactly what you need"), hlist(cards, 112)], spacing=0),
                            key="cats")

    def trending_row():
        return ft.Container(hlist([ft.Row([T("🔥 Trending:", 12, True, MUTED)])] +
                                  [chip(t, lambda e, t=t: search_for(t)) for t in TRENDING], 42))

    def flash_sale():
        items = sorted(PRODUCTS, key=lambda p: -pct(p))[:8]
        head = pad(ft.Row([ft.Column([T("⚡ Flash Sale", 20, True, "white"), T("Hurry! Offers end tonight", 12, color=ft.Colors.with_opacity(0.8, "white"))],
                                     spacing=0, expand=True),
                           ft.Column([T("Ends in", 10, color=ft.Colors.with_opacity(0.8, "white")), timer_row], spacing=2,
                                     horizontal_alignment=ft.CrossAxisAlignment.END)],
                          vertical_alignment=ft.CrossAxisAlignment.CENTER), 14)
        return pad(ft.Container(ft.Column([head, hlist([mini(p) for p in items], 232),
                                           ft.Container(height=10)], spacing=0), border_radius=22, shadow=SHADOW,
                                gradient=ft.LinearGradient(begin=ft.alignment.top_left, end=ft.alignment.bottom_right,
                                                           colors=["#dc2626", "#ea580c"])), 6)

    def offers_row():
        cards = []
        for code, (kind, val, mn, desc) in COUPONS.items():
            cards.append(ft.Container(ft.Column([
                ft.Row([T("🎟️", 18), T(code, 15, True, PRIMARY)], spacing=6), T(desc, 11, color=MUTED),
                ft.TextButton("Copy code", on_click=lambda e, c=code: (page.set_clipboard(c), toast(f"{c} copied!")))],
                spacing=2), width=210, bgcolor="white", border=ft.border.all(1.5, "#bfdbfe"), border_radius=14, padding=12))
        return ft.Column([section_head("Exclusive Offers", "Apply at checkout"), hlist(cards, 118)], spacing=0)

    def brands_row():
        cards = [ft.Container(T(b, 13, True, "#334155"), bgcolor="white", border=ft.border.all(1, BORDER), border_radius=12,
                              padding=ft.padding.symmetric(horizontal=18, vertical=12), on_click=lambda e, b=b: search_for(b))
                 for b in BRANDS]
        return ft.Column([section_head("Top Brands", "Shop your favourites"), hlist(cards, 56)], spacing=0)

    def product_row(title, sub, items):
        return ft.Column([section_head(title, sub, lambda e: show_all()), hlist([mini(p) for p in items], 232)], spacing=0)

    def reviews_section():
        cards = [ft.Container(ft.Column([T("★★★★★", 14, color=AMBER), T(f"“{txt}”", 12, color="#334155"),
                                         ft.Row([ft.Container(T(n[:1], 13, True, "white"), width=32, height=32, border_radius=16, bgcolor=PRIMARY,
                                                              alignment=ft.alignment.center),
                                                 ft.Column([T(n, 12, True), T(c, 10, color=MUTED)], spacing=0)], spacing=8)], spacing=8),
                              bgcolor="white", border=ft.border.all(1, BORDER), border_radius=16, padding=14, col={"xs": 12, "md": 4})
                 for n, c, txt in REVIEWS]
        return ft.Column([section_head("What our customers say", "Trusted by thousands of happy shoppers"),
                          pad(ft.ResponsiveRow(cards, spacing=10, run_spacing=10))], spacing=0)

    def newsletter():
        em = field("Enter your email", expand=True, text_size=13, bgcolor="white")

        def sub(e):
            if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", em.value or ""):
                return toast("Enter a valid email")
            em.value = ""
            page.update()
            toast("Subscribed! Use code GADGET10 for 10% off 🎁")

        return pad(ft.Container(ft.Column([T("📩 Get 10% off your first order", 18, True, "white"),
                                           T("Subscribe for exclusive deals, launches & offers.", 12, color=ft.Colors.with_opacity(0.85, "white")),
                                           ft.Row([em, ft.ElevatedButton("Subscribe", on_click=sub, style=ft.ButtonStyle(
                                               bgcolor=DARK, color="white", shape=ft.RoundedRectangleBorder(radius=10)))], spacing=8)], spacing=8),
                                border_radius=22, padding=20,
                                gradient=ft.LinearGradient(begin=ft.alignment.top_left, end=ft.alignment.bottom_right, colors=[PRIMARY, INDIGO])), 10)

    def footer():
        def col(title, links):
            return ft.Column([T(title, 13, True, "white")] + [
                ft.Container(T(t, 12, color="#94a3b8"), on_click=fn) for t, fn in links], spacing=6, col={"xs": 6, "sm": 3})

        return ft.Container(ft.Column([
            ft.Row([T("Gadget", 20, True, "white"), T("Hub", 20, True, "#60a5fa")], spacing=2),
            T("Your one-stop shop for the latest smartphones, laptops, audio, gaming and smart accessories.", 12, color="#94a3b8"),
            ft.ResponsiveRow([
                col("Shop", [(c, lambda e, c=c: show_cat(c)) for c, _, _ in CATS[:4]]),
                col("Support", [("Help Center", open_help), ("Returns & Refunds", open_help), ("Track Order", lambda e: open_account())]),
                col("Contact", [(SUPPORT_PHONE, open_help), (SUPPORT_EMAIL, open_help), ("Mon–Sat, 9am–8pm", None)]),
                col("Company", [("About Us", None), ("Privacy Policy", None), ("Terms of Use", None)])], run_spacing=14),
            ft.Row([ft.Icon(ic, color="#94a3b8", size=20) for ic in (ft.Icons.FACEBOOK, ft.Icons.CAMERA_ALT_OUTLINED,
                                                                      ft.Icons.ALTERNATE_EMAIL, ft.Icons.PLAY_CIRCLE_OUTLINE)], spacing=14),
            ft.Divider(height=1, color="#1e293b"),
            T(f"© {datetime.now().year} Gadget Hub. All rights reserved. Made with ❤️ in India", 11, color="#64748b",
              text_align=ft.TextAlign.CENTER),
            T("crafted by Datta Joldapke", 9, color="#334155", text_align=ft.TextAlign.CENTER, italic=True),
        ], spacing=14), bgcolor=DARK, padding=ft.padding.only(left=20, right=20, top=26, bottom=90))

    # ---------- assemble page ----------
    best = sorted(PRODUCTS, key=lambda p: -p["reviews"])[:8]
    new = [p for p in PRODUCTS if p["badge"] in ("NEW", "TRENDING", "SUPER")][:8]
    top = sorted(PRODUCTS, key=lambda p: (-p["rating"], -p["reviews"]))[:8]
    under = sorted([p for p in PRODUCTS if p["price"] <= 10000], key=lambda p: p["price"])[:8]

    listing = ft.Container(ft.Column([
        pad(ft.Row([ft.Column([title_txt, count_txt], spacing=0, expand=True), sort_dd],
                   vertical_alignment=ft.CrossAxisAlignment.CENTER), 4),
        cat_chips, pad(grid, 8)], spacing=4), key="products")

    main_col = ft.Column([
        trending_row(),
        pad(ft.Column([hero_box, dots], spacing=8), 4),
        trust_strip(),
        category_row(),
        flash_sale(),
        offers_row(),
        product_row("Best Sellers", "Most loved by our customers", best),
        product_row("New Arrivals", "Fresh drops & trending now", new),
        brands_row(),
        product_row("Top Rated", "Highest rated picks", top),
        product_row("Deals under ₹10,000", "Smart buys on a budget", under),
        recent_box,
        listing,
        reviews_section(),
        newsletter(),
        footer(),
    ], scroll=ft.ScrollMode.AUTO, expand=True, spacing=6)

    def nav_change(e):
        i = nav.selected_index
        nav.selected_index = 0
        if i == 0:
            show_home()
        elif i == 1:
            main_col.scroll_to(key="cats", duration=500)
        elif i == 2:
            show_wishlist()
        elif i == 3:
            open_cart()
        else:
            open_account()
        page.update()

    nav = ft.NavigationBar(selected_index=0, on_change=nav_change, bgcolor="white", destinations=[
        ft.NavigationBarDestination(icon=ft.Icons.HOME_OUTLINED, selected_icon=ft.Icons.HOME, label="Home"),
        ft.NavigationBarDestination(icon=ft.Icons.GRID_VIEW_OUTLINED, selected_icon=ft.Icons.GRID_VIEW, label="Categories"),
        ft.NavigationBarDestination(icon=ft.Icons.FAVORITE_BORDER, selected_icon=ft.Icons.FAVORITE, label="Wishlist"),
        ft.NavigationBarDestination(icon=ft.Icons.SHOPPING_CART_OUTLINED, selected_icon=ft.Icons.SHOPPING_CART, label="Cart"),
        ft.NavigationBarDestination(icon=ft.Icons.PERSON_OUTLINE, selected_icon=ft.Icons.PERSON, label="Account")])
    page.navigation_bar = nav
    page.floating_action_button = ft.FloatingActionButton(icon=ft.Icons.SUPPORT_AGENT, bgcolor="#22c55e",
                                                          foreground_color="white", on_click=open_help)

    page.add(ft.SafeArea(ft.Column([announce, header, main_col], spacing=0, expand=True), expand=True))
    render()
    threading.Thread(target=ticker, daemon=True).start()


ft.app(target=main)
