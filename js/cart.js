(function () {
  var CART_KEY = "homely_cart";
  var TABLE_KEY = "homely_table";
  var WHATSAPP_DIGITS = "8562094059629";

  function getLang() {
    return document.documentElement.getAttribute("data-lang") || "en";
  }

  /* ---------------- table (QR order) handling ---------------- */
  function getTableNumber() {
    var v = null;
    try { v = localStorage.getItem(TABLE_KEY); } catch (e) {}
    return v ? parseInt(v, 10) : null;
  }

  function setTableNumber(n) {
    try { localStorage.setItem(TABLE_KEY, String(n)); } catch (e) {}
  }

  function initTableFromUrl() {
    try {
      var params = new URLSearchParams(window.location.search);
      var t = parseInt(params.get("table"), 10);
      if (t && t > 0) setTableNumber(t);
    } catch (e) {}
  }

  function tableBannerHtml(n) {
    return '<span class="lang-lo">ໂຕະທີ ' + n + '</span>' +
           '<span class="lang-en">Table ' + n + '</span>' +
           '<span class="lang-vi">Bàn số ' + n + '</span>';
  }

  function renderTableBanners() {
    var n = getTableNumber();
    var menuBanner = document.getElementById("table-banner");
    var menuText = document.getElementById("table-banner-text");
    if (menuBanner && menuText) {
      if (n) {
        menuText.innerHTML = tableBannerHtml(n);
        menuBanner.hidden = false;
      } else {
        menuBanner.hidden = true;
      }
    }
    var cartBanner = document.getElementById("table-order-banner");
    var cartText = document.getElementById("table-order-banner-text");
    if (cartBanner && cartText) {
      if (n) {
        cartText.innerHTML = tableBannerHtml(n);
        cartBanner.hidden = false;
      } else {
        cartBanner.hidden = true;
      }
    }
  }

  /* ---------------- firebase (kitchen board backend) ---------------- */
  function initFirebaseApp() {
    try {
      if (typeof firebase !== "undefined" && window.HOMELY_FIREBASE_CONFIG && !firebase.apps.length) {
        firebase.initializeApp(window.HOMELY_FIREBASE_CONFIG);
      }
    } catch (e) {}
  }

  function getCart() {
    try {
      return JSON.parse(localStorage.getItem(CART_KEY)) || [];
    } catch (e) {
      return [];
    }
  }

  function saveCart(cart) {
    try { localStorage.setItem(CART_KEY, JSON.stringify(cart)); } catch (e) {}
    updateBadge();
  }

  function cartCount() {
    return getCart().reduce(function (sum, l) { return sum + l.qty; }, 0);
  }

  function updateBadge() {
    var badge = document.getElementById("cart-badge");
    if (badge) {
      var count = cartCount();
      badge.textContent = count;
      badge.style.display = count > 0 ? "inline-flex" : "none";
    }
  }

  function fmtPrice(n) {
    return n.toLocaleString("en-US").replace(/,/g, ".") + " Lak";
  }

  function addLine(line) {
    var cart = getCart();
    var existing = cart.find(function (l) {
      return l.id === line.id && l.variantLabelEn === line.variantLabelEn;
    });
    if (existing) {
      existing.qty += line.qty;
    } else {
      cart.push(line);
    }
    saveCart(cart);
  }

  function removeLine(index) {
    var cart = getCart();
    cart.splice(index, 1);
    saveCart(cart);
    renderCartPage();
  }

  function setQty(index, qty) {
    var cart = getCart();
    if (!cart[index]) return;
    qty = Math.max(1, Math.min(50, qty));
    cart[index].qty = qty;
    saveCart(cart);
    renderCartPage();
  }

  /* ---------------- menu page: add-to-cart controls ---------------- */
  function initMenuControls() {
    var controlsList = document.querySelectorAll(".cart-controls[data-id]");
    controlsList.forEach(function (el) {
      var qtyInput = el.querySelector(".qty-input");
      var decBtn = el.querySelector('[data-qty-action="dec"]');
      var incBtn = el.querySelector('[data-qty-action="inc"]');
      if (decBtn) decBtn.addEventListener("click", function () {
        qtyInput.value = Math.max(1, parseInt(qtyInput.value || "1", 10) - 1);
      });
      if (incBtn) incBtn.addEventListener("click", function () {
        qtyInput.value = Math.min(50, parseInt(qtyInput.value || "1", 10) + 1);
      });
      var addBtn = el.querySelector(".add-to-cart-btn");
      if (!addBtn) return;
      addBtn.addEventListener("click", function () {
        var id = el.getAttribute("data-id");
        var kind = el.getAttribute("data-kind");
        var qty = Math.max(1, parseInt(qtyInput.value || "1", 10));
        var nameLo = el.getAttribute("data-name-lo");
        var nameEn = el.getAttribute("data-name-en");
        var nameVi = el.getAttribute("data-name-vi");
        var unitPrice, variantLabelLo = "", variantLabelEn = "", variantLabelVi = "";
        if (kind === "variant") {
          var select = el.querySelector(".variant-select");
          var opt = select.options[select.selectedIndex];
          unitPrice = parseInt(opt.value, 10);
          variantLabelLo = opt.getAttribute("data-label-lo");
          variantLabelEn = opt.getAttribute("data-label-en");
          variantLabelVi = opt.getAttribute("data-label-vi");
        } else {
          unitPrice = parseInt(el.getAttribute("data-price"), 10);
        }
        addLine({
          id: id, qty: qty, unitPrice: unitPrice,
          nameLo: nameLo, nameEn: nameEn, nameVi: nameVi,
          variantLabelLo: variantLabelLo, variantLabelEn: variantLabelEn, variantLabelVi: variantLabelVi
        });
        addBtn.textContent = "OK";
        setTimeout(function () {
          addBtn.innerHTML = el.querySelector(".add-to-cart-btn") ? addBtn.innerHTML : "";
        }, 900);
        flashBadge();
      });
    });
  }

  function flashBadge() {
    var badge = document.getElementById("cart-badge");
    if (!badge) return;
    badge.classList.add("bump");
    setTimeout(function () { badge.classList.remove("bump"); }, 300);
  }

  /* ---------------- cart / checkout page ---------------- */
  function lineName(line) {
    var lo = line.nameLo, en = line.nameEn, vi = line.nameVi;
    if (line.variantLabelEn) {
      lo += " (" + line.variantLabelLo + ")";
      en += " (" + line.variantLabelEn + ")";
      vi += " (" + line.variantLabelVi + ")";
    }
    return { lo: lo, en: en, vi: vi };
  }

  function renderCartPage() {
    var rowsBody = document.getElementById("cart-rows");
    if (!rowsBody) return; // not the cart page
    var cart = getCart();
    var emptyMsg = document.getElementById("cart-empty-msg");
    var content = document.getElementById("cart-content");
    var paymentStep = document.getElementById("payment-step");
    var onlineSection = document.getElementById("online-order-section");
    var kitchenPanel = document.getElementById("kitchen-order-panel");
    var tableNum = getTableNumber();

    renderTableBanners();

    if (cart.length === 0) {
      if (emptyMsg) emptyMsg.hidden = false;
      if (content) content.hidden = true;
      if (paymentStep) paymentStep.hidden = true;
      return;
    }
    if (emptyMsg) emptyMsg.hidden = true;
    if (content) content.hidden = false;

    if (tableNum) {
      if (onlineSection) onlineSection.hidden = true;
      if (paymentStep) paymentStep.hidden = true;
      if (kitchenPanel) kitchenPanel.hidden = false;
      var sentMsg = document.getElementById("kitchen-sent-msg");
      var sendBtn = document.getElementById("send-kitchen-btn");
      var tableWrap = document.querySelector(".cart-table-wrap");
      var totalRow = document.querySelector(".cart-total-row");
      if (sentMsg) sentMsg.hidden = true;
      if (sendBtn) { sendBtn.hidden = false; sendBtn.disabled = false; }
      if (tableWrap) tableWrap.hidden = false;
      if (totalRow) totalRow.hidden = false;
    } else {
      if (onlineSection) onlineSection.hidden = false;
      if (kitchenPanel) kitchenPanel.hidden = true;
    }

    rowsBody.innerHTML = "";
    var total = 0;
    cart.forEach(function (line, idx) {
      var subtotal = line.unitPrice * line.qty;
      total += subtotal;
      var names = lineName(line);
      var tr = document.createElement("tr");
      tr.innerHTML =
        '<td>' +
          '<p class="dish-lo">' + names.lo + '</p>' +
          '<p class="dish-en">' + names.en + '</p>' +
          '<p class="dish-vi">' + names.vi + '</p>' +
        '</td>' +
        '<td>' + fmtPrice(line.unitPrice) + '</td>' +
        '<td><input type="number" class="qty-input cart-qty-input" min="1" max="50" value="' + line.qty + '" data-index="' + idx + '"></td>' +
        '<td>' + fmtPrice(subtotal) + '</td>' +
        '<td><button type="button" class="remove-line-btn" data-index="' + idx + '">&times;</button></td>';
      rowsBody.appendChild(tr);
    });

    document.getElementById("cart-total").textContent = fmtPrice(total);

    rowsBody.querySelectorAll(".cart-qty-input").forEach(function (input) {
      input.addEventListener("change", function () {
        setQty(parseInt(input.getAttribute("data-index"), 10), parseInt(input.value, 10) || 1);
      });
    });
    rowsBody.querySelectorAll(".remove-line-btn").forEach(function (btn) {
      btn.addEventListener("click", function () {
        removeLine(parseInt(btn.getAttribute("data-index"), 10));
      });
    });
  }

  /* ---------------- kitchen order (table QR flow) ---------------- */
  function buildKitchenOrderItems(cart) {
    return cart.map(function (line) {
      var names = lineName(line);
      return {
        nameLo: names.lo, nameEn: names.en, nameVi: names.vi,
        qty: line.qty, unitPrice: line.unitPrice,
        subtotal: line.unitPrice * line.qty
      };
    });
  }

function initKitchenOrder() {
    var btn = document.getElementById("send-kitchen-btn");
    if (!btn) return;
    btn.addEventListener("click", function () {
      var cart = getCart();
      var tableNum = getTableNumber();
      if (!cart.length || !tableNum) return;
      if (typeof firebase === "undefined" || !firebase.apps || !firebase.apps.length) {
        alert("Khong ket noi duoc voi he thong bep (kiem tra mang). Vui long thu lai.");
        return;
      }
      var total = cart.reduce(function (sum, l) { return sum + l.unitPrice * l.qty; }, 0);
      var order = {
        table: tableNum,
        items: buildKitchenOrderItems(cart),
        total: total,
        status: "moi",
        createdAt: Date.now()
      };
      btn.disabled = true;
      firebase.database().ref("orders").push(order)
        .then(function (ref) {
          var code = "B" + tableNum + "-" + ref.key.slice(-4).toUpperCase();
          saveCart([]);
          var tableWrap = document.querySelector(".cart-table-wrap");
          var totalRow = document.querySelector(".cart-total-row");
          if (tableWrap) tableWrap.hidden = true;
          if (totalRow) totalRow.hidden = true;
          btn.hidden = true;
          var sentMsg = document.getElementById("kitchen-sent-msg");
          var codeEl = document.getElementById("kitchen-order-code");
          if (codeEl) codeEl.textContent = code;
          if (sentMsg) sentMsg.hidden = false;
        })
        .catch(function (err) {
          btn.disabled = false;
          alert("Gui don khong thanh cong, vui long thu lai. Loi: " + (err && err.message ? err.message : err));
        });
    });
  }

  function initDeliveryToggle() {
    var radios = document.querySelectorAll('input[name="cf-delivery"]');
    var addressWrap = document.getElementById("cf-address-wrap");
    if (!radios.length || !addressWrap) return;
    radios.forEach(function (r) {
      r.addEventListener("change", function () {
        addressWrap.hidden = (r.value === "pickup" && r.checked) || document.querySelector('input[name="cf-delivery"]:checked').value === "pickup";
      });
    });
  }

  function buildWhatsAppMessage(order) {
    var lines = [];
    lines.push("*DON HANG - LAO HOMELY RESTAURANT*");
    lines.push("Ma don: " + order.code);
    lines.push("");
    order.cart.forEach(function (line) {
      var names = lineName(line);
      lines.push("- " + names.vi + " x" + line.qty + " = " + fmtPrice(line.unitPrice * line.qty));
    });
    lines.push("");
    lines.push("Tong cong: " + fmtPrice(order.total));
    lines.push("");
    lines.push("Ten khach: " + order.name);
    lines.push("SDT: " + order.phone);
    lines.push("Hinh thuc: " + (order.delivery === "delivery" ? "Giao hang" : "Tu den lay tai quan"));
    if (order.delivery === "delivery" && order.address) {
      lines.push("Dia chi: " + order.address);
    }
    if (order.note) {
      lines.push("Ghi chu: " + order.note);
    }
    lines.push("");
    lines.push("(Da/se chuyen khoan - se gui anh chuyen khoan qua WhatsApp)");
    return lines.join("\n");
  }

  function initCheckoutForm() {
    var form = document.getElementById("checkout-form");
    if (!form) return;
    initDeliveryToggle();

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var cart = getCart();
      if (cart.length === 0) return;

      var name = document.getElementById("cf-name").value.trim();
      var phone = document.getElementById("cf-phone").value.trim();
      var delivery = document.querySelector('input[name="cf-delivery"]:checked').value;
      var address = document.getElementById("cf-address").value.trim();
      var note = document.getElementById("cf-note").value.trim();
      if (!name || !phone) return;
      if (delivery === "delivery" && !address) {
        document.getElementById("cf-address").focus();
        return;
      }

      var total = cart.reduce(function (sum, l) { return sum + l.unitPrice * l.qty; }, 0);
      var code = "HL" + Date.now().toString().slice(-8);

      document.getElementById("payment-amount").textContent = fmtPrice(total);
      document.getElementById("order-code").textContent = code;
      var paymentStep = document.getElementById("payment-step");
      paymentStep.hidden = false;
      paymentStep.scrollIntoView({ behavior: "smooth" });

      var message = buildWhatsAppMessage({
        code: code, cart: cart, total: total, name: name, phone: phone,
        delivery: delivery, address: address, note: note
      });
      var waLink = "https://wa.me/" + WHATSAPP_DIGITS + "?text=" + encodeURIComponent(message);
      document.getElementById("whatsapp-send-btn").setAttribute("href", waLink);
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    initFirebaseApp();
    initTableFromUrl();
    renderTableBanners();
    updateBadge();
    initMenuControls();
    renderCartPage();
    initCheckoutForm();
    initKitchenOrder();
  });
})();
