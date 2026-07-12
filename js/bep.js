(function () {
  function initFirebaseApp() {
    try {
      if (typeof firebase !== "undefined" && window.HOMELY_FIREBASE_CONFIG && !firebase.apps.length) {
        firebase.initializeApp(window.HOMELY_FIREBASE_CONFIG);
      }
    } catch (e) {}
  }

  function fmtPrice(n) {
    return (n || 0).toLocaleString("en-US").replace(/,/g, ".") + " Lak";
  }

  function pad2(n) {
    return (n < 10 ? "0" : "") + n;
  }

  function fmtTime(ts) {
    var d = new Date(ts || Date.now());
    return pad2(d.getHours()) + ":" + pad2(d.getMinutes());
  }

  function orderCode(key, table) {
    return "B" + table + "-" + String(key).slice(-4).toUpperCase();
  }

  function renderOrderCard(key, order) {
    var card = document.createElement("div");
    card.className = "bep-card" + (order.status === "xong" ? " bep-card-done" : "");
    var itemsHtml = (order.items || []).map(function (it) {
      var name = it.nameVi || it.nameEn || it.nameLo || "";
      return '<li><span class="bep-item-qty">x' + it.qty + '</span> <span class="bep-item-name">' + name + '</span></li>';
    }).join("");
    card.innerHTML =
      '<div class="bep-card-head">' +
        '<span class="bep-card-table">BAN ' + order.table + '</span>' +
        '<span class="bep-card-time">' + fmtTime(order.createdAt) + '</span>' +
      '</div>' +
      '<div class="bep-card-code">Ma: ' + orderCode(key, order.table) + '</div>' +
      '<ul class="bep-card-items">' + itemsHtml + '</ul>' +
      '<div class="bep-card-total">Tong: ' + fmtPrice(order.total) + '</div>' +
      (order.status === "xong"
        ? '<div class="bep-card-done-label">Da xong</div>'
        : '<button type="button" class="bep-done-btn" data-key="' + key + '">Da xong</button>');
    return card;
  }

  function attachDoneHandlers(container, ordersRef) {
    container.querySelectorAll(".bep-done-btn").forEach(function (btn) {
      btn.addEventListener("click", function () {
        var key = btn.getAttribute("data-key");
        btn.disabled = true;
        ordersRef.child(key).update({ status: "xong", doneAt: Date.now() });
      });
    });
  }

  function initKitchenBoard() {
    initFirebaseApp();
    var statusEl = document.getElementById("bep-status");
    if (typeof firebase === "undefined" || !firebase.apps.length) {
      if (statusEl) statusEl.textContent = "Loi ket noi Firebase";
      return;
    }
    var ordersRef = firebase.database().ref("orders");

    var pendingList = document.getElementById("bep-pending-list");
    var doneList = document.getElementById("bep-done-list");
    var pendingCount = document.getElementById("bep-pending-count");
    var doneCount = document.getElementById("bep-done-count");
    var pendingEmpty = document.getElementById("bep-pending-empty");

    ordersRef.on("value", function (snapshot) {
      if (statusEl) statusEl.textContent = "Da ket noi - cap nhat theo thoi gian thuc";
      var val = snapshot.val() || {};
      var pending = [];
      var done = [];
      Object.keys(val).forEach(function (key) {
        var order = val[key];
        if (order.status === "xong") done.push([key, order]);
        else pending.push([key, order]);
      });
      pending.sort(function (a, b) { return (a[1].createdAt || 0) - (b[1].createdAt || 0); });
      done.sort(function (a, b) { return (b[1].doneAt || b[1].createdAt || 0) - (a[1].doneAt || a[1].createdAt || 0); });

      pendingList.innerHTML = "";
      pending.forEach(function (pair) {
        pendingList.appendChild(renderOrderCard(pair[0], pair[1]));
      });
      attachDoneHandlers(pendingList, ordersRef);
      if (pendingEmpty) pendingEmpty.hidden = pending.length > 0;
      if (pendingCount) pendingCount.textContent = pending.length;

      doneList.innerHTML = "";
      done.slice(0, 20).forEach(function (pair) {
        doneList.appendChild(renderOrderCard(pair[0], pair[1]));
      });
      if (doneCount) doneCount.textContent = done.length;
    }, function (err) {
      if (statusEl) statusEl.textContent = "Loi doc du lieu: " + (err && err.message ? err.message : err);
    });

    var clearBtn = document.getElementById("bep-clear-done-btn");
    if (clearBtn) {
      clearBtn.addEventListener("click", function () {
        if (!window.confirm("Xoa tat ca don da hoan thanh?")) return;
        ordersRef.once("value").then(function (snapshot) {
          var val = snapshot.val() || {};
          var updates = {};
          Object.keys(val).forEach(function (key) {
            if (val[key].status === "xong") updates[key] = null;
          });
          ordersRef.update(updates);
        });
      });
    }
  }

  document.addEventListener("DOMContentLoaded", initKitchenBoard);
})();
