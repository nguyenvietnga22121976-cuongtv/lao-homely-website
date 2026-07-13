(function () {
  var CART_KEY = "homely_cart";
  var TABLE_KEY = "homely_table";
  var PENDING_ORDER_KEY = "homely_pending_wa_order";
  var PENDING_ORDER_TTL_MS = 6 * 60 * 60 * 1000; // 6 gio - qua khoang nay coi nhu het han, khong hien lai man hinh xac nhan cu
  var KITCHEN_WHATSAPP_1 = "8562094059629";   // 02094059629
  var KITCHEN_WHATSAPP_2 = "8562098676643";   // 02098676643

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

  /* ---------------- pending WhatsApp order (survives tab reload/app-switch) ---------------- */
  function savePendingOrder(order) {
    try { localStorage.setItem(PENDING_ORDER_KEY, JSON.stringify(order)); } catch (e) {}
  }

  function getPendingOrder() {
    var raw = null;
    try { raw = localStorage.getItem(PENDING_ORDER_KEY); } catch (e) {}
    if (!raw) return null;
    var order;
    try { order = JSON.parse(raw); } catch (e) { return null; }
    if (!order || !order.ts || (Date.now() - order.ts) > PENDING_ORDER_TTL_MS) return null;
    return order;
  }

  function clearPendingOrder() {
    try { localStorage.removeItem(PENDING_ORDER_KEY); } catch (e) {}
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

    /* Neu vua gui don thanh cong o lan truoc (con han) va khach chua chon mon moi,
       khoi phuc lai man hinh xac nhan + 2 nut WhatsApp thay vi bao "chua chon mon".
       Truong hop nay xay ra khi dien thoai/trinh duyet tai lai trang gio-hang.html
       sau khi khach chuyen qua ung dung WhatsApp roi quay lai. */
    var pending = getPendingOrder();
    if (cart.length === 0 && pending && pending.table === tableNum) {
      showKitchenConfirmation(pending);
      return;
    }

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

  /* Tin nhan gui cho bep LUON LUON bang tieng Lao (dung nameLo), bat ke khach
     dang xem trang bang ngon ngu nao (Lao/Anh/Viet), vi dau bep la nguoi Lao. */
  function buildKitchenWhatsAppText(order) {
    var lines = [];
    lines.push("*ອໍເດີໃໝ່ - ໂຕະທີ " + order.table + "*");
    lines.push("ລະຫັດອໍເດີ: " + order.code);
    lines.push("");
    order.items.forEach(function (it) {
      lines.push("- " + it.nameLo + " x" + it.qty + " = " + fmtPrice(it.subtotal));
    });
    lines.push("");
    lines.push("ລວມທັງໝົດ: " + fmtPrice(order.total));
    lines.push("");
    lines.push("(ສົ່ງຈາກລະບົບສັ່ງອາຫານ QR - ຮ້ານອາຫານລາວໂຮມລີ້)");
    return lines.join("\n");
  }

  /* Hien thi man hinh xac nhan + 2 nut WhatsApp da co san href.
     Dung chung cho: (1) ngay sau khi gui don thanh cong, va (2) khoi phuc lai
     khi nguoi dung quay lai trang gio-hang.html sau khi chuyen sang app WhatsApp
     (dien thoai/trinh duyet co the tai lai trang, lam mat trang thai trong bo nho). */
  function showKitchenConfirmation(order) {
    var emptyMsg = document.getElementById("cart-empty-msg");
    var content = document.getElementById("cart-content");
    var noTableMsg = document.getElementById("no-table-msg");
    if (noTableMsg) noTableMsg.hidden = true;
    if (emptyMsg) emptyMsg.hidden = true;
    if (content) content.hidden = false;

    var btn = document.getElementById("send-kitchen-btn");
    var tableWrap = document.querySelector(".cart-table-wrap");
    var totalRow = document.querySelector(".cart-total-row");
    var sentMsg = document.getElementById("kitchen-sent-msg");
    var codeEl = document.getElementById("kitchen-order-code");
    var waBoth = document.getElementById("wa-send-both");

    if (tableWrap) tableWrap.hidden = true;
    if (totalRow) totalRow.hidden = true;
    if (btn) btn.hidden = true;
    if (codeEl) codeEl.textContent = order.code;
    if (waBoth) {
      // Luu 2 duong link WhatsApp vao data-attribute, khong dat truc tiep vao href
      // vi mot the <a> chi mo duoc 1 link - viec mo ca 2 duoc xu ly trong ham click bang tay.
      waBoth.setAttribute("data-wa1", order.wa1);
      waBoth.setAttribute("data-wa2", order.wa2);
      waBoth.setAttribute("href", order.wa1);
    }
    if (sentMsg) sentMsg.hidden = false;
  }

  /* Mo ca 2 link WhatsApp (2 so bep) tu 1 lan bam duy nhat.
     Goi window.open() 2 lan lien tiep, dong bo, ngay trong handler click
     (khong qua setTimeout/Promise) de trinh duyet khong chan popup thu 2. */
  function sendToBothKitchenPhones(wa1, wa2) {
    if (wa1) window.open(wa1, "_blank", "noopener");
    if (wa2) window.open(wa2, "_blank", "noopener");
  }

  function initKitchenOrder() {
    var btn = document.getElementById("send-kitchen-btn");
    var orderMoreLink = document.getElementById("order-more-link");
    var waBoth = document.getElementById("wa-send-both");
    if (orderMoreLink) {
      orderMoreLink.addEventListener("click", function () {
        clearPendingOrder();
      });
    }
    if (waBoth) {
      waBoth.addEventListener("click", function (e) {
        e.preventDefault();
        var wa1 = waBoth.getAttribute("data-wa1");
        var wa2 = waBoth.getAttribute("data-wa2");
        sendToBothKitchenPhones(wa1, wa2);
      });
    }
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
      var orderData = {
        table: tableNum,
        items: items,
        total: total,
        status: "moi",
        createdAt: Date.now()
      };
      btn.disabled = true;
      firebase.database().ref("orders").push(orderData)
        .then(function (ref) {
          var code = "B" + tableNum + "-" + ref.key.slice(-4).toUpperCase();
          var text = buildKitchenWhatsAppText({ table: tableNum, code: code, items: items, total: total });
          var pending = {
            code: code,
            table: tableNum,
            wa1: "https://wa.me/" + KITCHEN_WHATSAPP_1 + "?text=" + encodeURIComponent(text),
            wa2: "https://wa.me/" + KITCHEN_WHATSAPP_2 + "?text=" + encodeURIComponent(text),
            ts: Date.now()
          };
          savePendingOrder(pending);
          saveCart([]);
          showKitchenConfirmation(pending);
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
