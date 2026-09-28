from flask import Flask, render_template, session, redirect, url_for, request, flash

app = Flask(__name__)
app.secret_key = "dev-secret-key-change-me"  

PRODUCTS = [
    {"id": 1, "name": "Ноутбук Lenovo IdeaPad", "price": 54990, "category": "Электроника"},
    {"id": 2, "name": "Смартфон iphone 18",   "price": 219900, "category": "Электроника"},
    {"id": 3, "name": "Наушники airpods 3",   "price": 27990, "category": "Аудио"},
    {"id": 4, "name": "Клавиатура Logitech K380","price": 3990,  "category": "Аксессуары"},
    {"id": 5, "name": "Мышь Logitech MX Master", "price": 8990,  "category": "Аксессуары"},
    {"id": 6, "name": "Книга",      "price": 1890,  "category": "Книги"},
    {"id": 7, "name": "Кружка путин",     "price": 690,   "category": "Сувениры"},
    {"id": 8, "name": "Монитор Dell 27\"",        "price": 32990, "category": "Электроника"},
]

def find_product(product_id: int):
    return next((p for p in PRODUCTS if p["id"] == product_id), None)


def get_cart() -> dict:
    return session.get("cart", {})


def save_cart(cart: dict) -> None:
    session["cart"] = cart
    session.modified = True


def build_cart_view() -> dict:
    cart = get_cart()
    items = []
    total_sum = 0
    total_qty = 0

    for pid_str, qty in cart.items():
        product = find_product(int(pid_str))
        if not product:
            continue
        line_sum = product["price"] * qty
        items.append({
            "id": product["id"],
            "name": product["name"],
            "category": product["category"],
            "price": product["price"],
            "quantity": qty,
            "line_sum": line_sum,
        })
        total_sum += line_sum
        total_qty += qty

    return {
        "items": items,
        "total_sum": total_sum,
        "total_qty": total_qty,
        "unique_count": len(items),
    }


@app.route("/")
def index():
    return render_template("index.html", products=PRODUCTS, cart_count=sum(get_cart().values()))


@app.route("/add/<int:product_id>", methods=["POST"])
def add_to_cart(product_id: int):
    product = find_product(product_id)
    if not product:
        flash("Товар не найден", "error")
        return redirect(url_for("index"))

    cart = get_cart()
    key = str(product_id)
    cart[key] = cart.get(key, 0) + 1
    save_cart(cart)
    flash(f"«{product['name']}» добавлен в корзину", "success")
    return redirect(request.referrer or url_for("index"))


@app.route("/cart")
def cart():
    data = build_cart_view()
    return render_template("cart.html", **data)


@app.route("/remove/<int:product_id>", methods=["POST"])
def remove_from_cart(product_id: int):
    cart = get_cart()
    cart.pop(str(product_id), None)
    save_cart(cart)
    flash("Позиция удалена из корзины", "success")
    return redirect(url_for("cart"))


@app.route("/clear", methods=["POST"])
def clear_cart():
    save_cart({})
    flash("Корзина пуста", "success")
    return redirect(url_for("cart"))


@app.route("/stats")
def stats():
    data = build_cart_view()
    return render_template("stats.html", **data)


@app.template_filter("price")
def format_price(value):
    return f"{value:,.0f}".replace(",", " ") + " ₽"


if __name__ == "__main__":
    app.run(debug=True)
