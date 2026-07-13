(function () {
  var CART_KEY = "homely_cart";
  var TABLE_KEY = "homely_table";
  var KITCHEN_WHATSAPP_1 = "8562094059629";   // 02094059629
  var KITCHEN_WHATSAPP_2 = "8562099316688";   // 02099316688

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
    var menuWarning = document.getElementById("no-table-warning");
    if (menuBanner && menuText) {
      if (n) {
        menuText.innerHTML = tableBannerHtml(n);
        menuBanner.hidden = false;
        if (menuWarning) menuWarning.hidden = true;
      } else {
        menuBanner.hidden = true;
        if (menuWarning) menuWarning.hidden = false;
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

  /* setLine: upsert (qty>0) or remove (qty<=0) a single line, matched by dish id */
  function setLine(id, unitPrice, nameLo, nameEn, nameVi, variantLabelLo, variantLabelEn, variantLabelVi, qty) {
    var cart = getCart();
    var idx = cart.findIndex(function (l) { return l.id === id; });
    if (!qty || qty <= 0) {
      if (idx !== -1) cart.splice(idx, 1);
    } else {
      var line = {
        id: id, qty: qty, unitPrice: unitPrice,
        nameLo: nameLo, nameEn: nameEn, nameVi: nameVi,
        variantLabelLo: variantLabelLo || "", variantLabelEn: variantLabelEn || "", variantLabelVi: variantLabelVi || ""
      };
      if (idx !== -1) cart[idx] = line; else cart.push(line);
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

  /* ---------------- menu page: tick-to-select controls ---------------- */
  function initMenuControls() {
    var controlsList = document.querySelectorAll(".cart-controls[data-id]");
    if (!controlsList.length) return;
    var cart = getCart();
    var hasTable = !!getTableNumber();

    controlsList.forEach(function (el) {
      var id = el.getAttribute("data-id");
      var kind = el.getAttribute("data-kind");
      var checkbox = el.querySelector(".select-checkbox");
      var qtyInput = el.querySelector(".qty-input");
      var decBtn = el.querySelector('[data-qty-action="dec"]');
      var incBtn = el.querySelector('[data-qty-action="inc"]');
      var variantSelect = el.querySelector(".variant-select");
      var nameLo = el.getAttribute("data-name-lo");
      var nameEn = el.getAttribute("data-name-en");
      var nameVi = el.getAttribute("data-name-vi");
      if (!checkbox) return;

      function currentUnitPrice() {
        if (kind === "variant" && variantSelect) {
          return parseInt(variantSelect.options[variantSelect.selectedIndex].value, 10);
        }
        return parseInt(el.getAttribute("data-price"), 10);
      }
      function currentVariantLabels() {
        if (kind === "variant" && variantSelect) {
          var opt = variantSelect.options[variantSelect.selectedIndex];
          return {
            lo: opt.getAttribute("data-label-lo"),
            en: opt.getAttribute("data-label-en"),
            vi: opt.getAttribute("data-label-vi")
          };
        }
        return { lo: "", en: "", vi: "" };
      }
      function syncLine() {
        if (!checkbox.checked) {
          setLine(id, 0);
          el.classList.remove("selected");
          return;
        }
        var qty = Math.max(1, parseInt(qtyInput.value || "1", 10));
        var vl = currentVariantLabels();
        setLine(id, currentUnitPrice(), nameLo, nameEn, nameVi, vl.lo, vl.en, vl.vi, qty);
        el.classList.add("selected");
      }

      /* restore state from existing cart (e.g. navigating back from order page) */
      var existing = cart.find(function (l) { return l.id === id; });
      if (existing) {
        checkbox.checked = true;
        qtyInput.value = existing.qty;
        el.classList.add("selected");
        if (kind === "variant" && variantSelect && existing.variantLabelEn) {
          for (var i = 0; i < variantSelect.options.length; i++) {
            if (variantSelect.options[i].getAttribute("data-label-en") === existing.variantLabelEn) {
              variantSelect.selectedIndex = i;
              break;
            }
          }
        }
      }

      if (!hasTable) {
        checkbox.disabled = true;
        qtyInput.disabled = true;
        if (decBtn) decBtn.disabled = true;
        if (incBtn) incBtn.disabled = true;
        if (variantSelect) variantSelect.disabled = true;
      }

      checkbox.addEventListener("change", function () {
        syncLine();
        flashBadge();
      });
      if (decBtn) decBtn.addEventListener("click", function () {
        qtyInput.value = Math.max(1, parseInt(qtyInput.value || "1", 10) - 1);
        if (checkbox.checked) syncLine();
      });
      if (incBtn) incBtn.addEventListener("click", function () {
        qtyInput.value = Math.min(20, parseInt(qtyInput.value || "1", 10) + 1);
        if (checkbox.checked) syncLine();
      });
      qtyInput.addEventListener("change", function () {
        qtyInput.value = Math.max(1, Math.min(20, parseInt(qtyInput.value || "1", 10) || 1));
        if (checkbox.checked) syncLine();
      });
      if (variantSelect) {
        variantSelect.addEventListener("change", function () {
          if (checkbox.checked) syncLine();
        });
      }
    });
  }

  function flashBadge() {
    var badge = document.getElementById("cart-badge");
    if (!badge) return;
    badge.classList.add("bump");
    setTimeout(function () { badge.classList.remove("bump"); }, 300);
  }

  /* ---------------- order page ---------------- */
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
    if (!rowsBody) return; // not the order page
    var cart = getCart();
    var emptyMsg = document.getElementById("cart-empty-msg");
    var content = document.getElementById("cart-content");
    var noTableMsg = document.getElementById("no-table-msg");
    var tableNum = getTableNumber();

    renderTableBanners();

    if (!tableNum) {
      if (noTableMsg) noTableMsg.hidden = false;
      if (emptyMsg) emptyMsg.hidden = true;
      if (content) content.hidden = true;
      return;
    }
    if (noTableMsg) noTableMsg.hidden = true;

    if (cart.length === 0) {
      if (emptyMsg) emptyMsg.hidden = false;
      if (content) content.hidden = true;
      return;
    }
    if (emptyMsg) emptyMsg.hidden = true;
    if (content) content.hidden = false;

    var sentMsg = document.getElementById("kitchen-sent-msg");
    var sendBtn = document.getElementById("send-kitchen-btn");
    var tableWrap = document.querySelector(".cart-table-wrap");
    var totalRow = document.querySelector(".cart-total-row");
    if (sentMsg) sentMsg.hidden = true;
    if (sendBtn) { sendBtn.hidden = false; sendBtn.disabled = false; }
    if (tableWrap) tableWrap.hidden = false;
    if (totalRow) totalRow.hidden = false;

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

  /* ---------------- kitchen order (send to Firebase + WhatsApp x2) ---------------- */
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

  function buildKitchenWhatsAppText(order) {
    var lines = [];
    lines.push("*DON DAT MON - BAN SO " + order.table + "*");
    lines.push("Ma don: " + order.code);
    lines.push("");
    order.items.forEach(function (it) {
      lines.push("- " + it.nameVi + " x" + it.qty + " = " + fmtPrice(it.subtotal));
    });
    lines.push("");
    lines.push("Tong cong: " + fmtPrice(order.total));
    lines.push("");
    lines.push("(Gui tu he thong dat mon QR - Lao Homely Restaurant)");
    return lines.join("\n");
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
      var items = buildKitchenOrderItems(cart);
      var order = {
        table: tableNum,
        items: items,
        total: total,
        status: "moi",
        createdAt: Date.now()
      };
      btn.disabled = true;
      firebase.database().ref("orders").push(order)
        .then(function (ref) {
          var code = "B" + tableNum + "-" + ref.key.slice(-4).toUpperCase();
          var text = buildKitchenWhatsAppText({ table: tableNum, code: code, items: items, total: total });
          var wa1 = document.getElementById("wa-send-1");
          var wa2 = document.getElementById("wa-send-2");
          if (wa1) wa1.setAttribute("href", "https://wa.me/" + KITCHEN_WHATSAPP_1 + "?text=" + encodeURIComponent(text));
          if (wa2) wa2.setAttribute("href", "https://wa.me/" + KITCHEN_WHATSAPP_2 + "?text=" + encodeURIComponent(text));

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

  document.addEventListener("DOMContentLoaded", function () {
    initFirebaseApp();
    initTableFromUrl();
    renderTableBanners();
    updateBadge();
    initMenuControls();
    renderCartPage();
    initKitchenOrder();
  });
})();
