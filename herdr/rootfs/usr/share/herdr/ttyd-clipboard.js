// herdr add-on: clipboard support for the ttyd web terminal.
// - OSC 52 (herdr, Claude Code, vim, ...) writes to the browser clipboard.
//   When the browser refuses without a click, a button asks for one.
// - Ctrl+V and Ctrl+Shift+V paste from the browser clipboard instead of
//   sending ^V to the terminal.
// - Ctrl+Enter and Shift+Enter are sent as Kitty keyboard sequences
//   (CSI 13;<mod> u). xterm.js would send ^J or a plain CR, so Claude Code
//   could not tell them from Ctrl+J/Enter. herdr parses the sequence and
//   re-encodes it for each pane (Kitty or modifyOtherKeys).
// - Right click opens only herdr's context menu, not the browser's on top.
//   Shift+right click still opens the browser menu.
(function () {
  "use strict";

  function decode(b64) {
    var bytes = Uint8Array.from(atob(b64), function (c) { return c.charCodeAt(0); });
    return new TextDecoder().decode(bytes);
  }

  var banner = null;

  function hideBanner() {
    if (banner) {
      banner.remove();
      banner = null;
    }
  }

  function askToCopy(text) {
    hideBanner();
    banner = document.createElement("button");
    banner.type = "button";
    banner.textContent = "📋 In die Zwischenablage kopieren (" + text.length + " Zeichen)";
    banner.style.cssText =
      "position:fixed;top:12px;right:12px;z-index:1000;padding:8px 14px;" +
      "font:14px sans-serif;color:#fff;background:#03a9f4;border:0;" +
      "border-radius:6px;box-shadow:0 2px 8px rgba(0,0,0,.4);cursor:pointer";
    banner.addEventListener("click", function () {
      navigator.clipboard.writeText(text).catch(function () {
        var area = document.createElement("textarea");
        area.value = text;
        document.body.appendChild(area);
        area.select();
        document.execCommand("copy");
        area.remove();
      });
      hideBanner();
      window.term.focus();
    });
    document.body.appendChild(banner);
    var shown = banner;
    setTimeout(function () { if (banner === shown) hideBanner(); }, 30000);
  }

  function copy(text) {
    if (navigator.clipboard && window.isSecureContext) {
      navigator.clipboard.writeText(text).catch(function () { askToCopy(text); });
    } else {
      askToCopy(text);
    }
  }

  function setup(term) {
    // OSC 52: "<targets>;<base64>", "?" asks for the clipboard (not answered)
    term.parser.registerOscHandler(52, function (data) {
      var payload = data.slice(data.indexOf(";") + 1);
      if (payload && payload !== "?") {
        try {
          copy(decode(payload));
        } catch (e) {
          console.warn("herdr: invalid OSC 52 payload", e);
        }
      }
      return true;
    });

    term.attachCustomKeyEventHandler(function (event) {
      // Let the browser handle Ctrl+V so xterm.js receives a paste event
      if (event.type === "keydown" && event.ctrlKey && !event.altKey && !event.metaKey &&
          (event.key === "v" || event.key === "V")) {
        return false;
      }
      // Modified Enter: Kitty modifier value is 1 + shift(1) + ctrl(4)
      if (event.key === "Enter" && (event.ctrlKey || event.shiftKey) &&
          !event.altKey && !event.metaKey) {
        if (event.type === "keydown") {
          var mod = 1 + (event.shiftKey ? 1 : 0) + (event.ctrlKey ? 4 : 0);
          term.input("\x1b[13;" + mod + "u", true);
        }
        event.preventDefault();
        return false;
      }
      return true;
    });
  }

  document.addEventListener("contextmenu", function (event) {
    if (!event.shiftKey) event.preventDefault();
  }, true);

  var tries = 0;
  (function waitForTerminal() {
    if (window.term && window.term.parser) {
      setup(window.term);
    } else if (tries++ < 200) {
      setTimeout(waitForTerminal, 50);
    }
  })();
})();
