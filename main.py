import sys
from urllib.parse import quote_plus

from PySide6.QtCore import Qt, QUrl, QSettings, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QKeySequence, QShortcut, QAction
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QTabWidget, QLabel, QFrame, QToolButton,
    QSizePolicy, QProgressBar, QMenu, QMessageBox, QFileDialog,
    QInputDialog, QStatusBar
)
from PySide6.QtWebEngineCore import QWebEngineProfile, QWebEngineSettings, QWebEnginePage
from PySide6.QtWebEngineWidgets import QWebEngineView


APP_NAME = "Neon GX"
SEARCH_ENGINE = "https://www.google.com/search?q="
ACCENT = "#a855f7"

STYLE = """
* { font-family: "Segoe UI", "Arial", sans-serif; font-size: 13px; }
QMainWindow, QWidget { background: #0a0b10; color: #e9eaf4; }
QFrame#sidebar { background: #0d0f17; border-right: 1px solid #252638; }
QLabel#logo { color: #d9a4ff; font-size: 22px; font-weight: 900; padding: 7px; }
QLabel#brand { color: #f4edff; font-size: 14px; font-weight: 800; letter-spacing: 2px; }
QLabel#status { color: #9295ad; padding: 4px 9px; font-size: 11px; }
QLabel#section { color: #777b96; font-size: 10px; font-weight: 800; padding: 8px 4px 2px; }
QLineEdit {
    background: #131521; color: #f5f4ff; border: 1px solid #2b2e43;
    border-radius: 11px; padding: 10px 14px; selection-background-color: #7840b8;
}
QLineEdit:focus { border: 1px solid #b66bff; background: #171827; }
QPushButton, QToolButton {
    background: #171927; color: #dfe0f0; border: 1px solid #292d42;
    border-radius: 9px; padding: 8px 10px;
}
QPushButton:hover, QToolButton:hover { background: #252039; border-color: #9958e8; color: white; }
QPushButton:pressed, QToolButton:pressed { background: #38244c; }
QPushButton:disabled, QToolButton:disabled { color: #4f5267; border-color: #202232; }
QPushButton#accent {
    background: #8b42d7; border: 1px solid #bb7aff; color: white;
    font-weight: 800; padding-left: 15px; padding-right: 15px;
}
QPushButton#accent:hover { background: #a254ef; }
QPushButton#side { font-size: 18px; padding: 0; }
QTabWidget::pane { border: 1px solid #202337; border-radius: 9px; background: #0a0b10; top: -1px; }
QTabBar::tab {
    background: #11131e; color: #8e91a9; padding: 10px 15px;
    margin-right: 4px; border: 1px solid #22253a;
    border-top-left-radius: 9px; border-top-right-radius: 9px; min-width: 75px;
}
QTabBar::tab:selected { background: #1a1929; color: #f6eaff; border-color: #58377a; border-bottom: 2px solid #bd72ff; }
QTabBar::tab:hover:!selected { background: #1b1d2b; color: #d9c9f0; }
QProgressBar { background: #171927; border: none; border-radius: 2px; max-height: 3px; }
QProgressBar::chunk { background: #c084fc; border-radius: 2px; }
QMenu { background: #151724; color: #e9eaf4; border: 1px solid #30334a; padding: 5px; }
QMenu::item { padding: 7px 24px; border-radius: 5px; }
QMenu::item:selected { background: #38264c; }
QStatusBar { background: #0d0f17; color: #8589a2; border-top: 1px solid #22253a; }
"""

HOME_HTML = r"""
<!doctype html><html><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
*{box-sizing:border-box} :root{color-scheme:dark}
body{margin:0;min-height:100vh;background:radial-gradient(ellipse at 50% 18%,#302044 0%,#171322 24%,transparent 58%),#0a0b10;color:#f5f1ff;font-family:Segoe UI,Arial,sans-serif;display:flex;align-items:center;justify-content:center;overflow-x:hidden}
body:before{content:"";position:fixed;inset:0;pointer-events:none;background-image:linear-gradient(#ffffff05 1px,transparent 1px),linear-gradient(90deg,#ffffff05 1px,transparent 1px);background-size:46px 46px;mask-image:linear-gradient(to bottom,#000,transparent 80%)}
main{position:relative;width:min(820px,90%);padding:58px 0;text-align:center}
.eyebrow{color:#c084fc;font-size:11px;letter-spacing:5px;font-weight:800}
.logo{font-size:clamp(48px,9vw,86px);font-weight:900;letter-spacing:-5px;margin:10px 0 0;line-height:1.1;text-shadow:0 0 48px #b15cff30}
.logo span{background:linear-gradient(110deg,#e9b7ff,#a855f7 55%,#76d5ff);-webkit-background-clip:text;background-clip:text;color:transparent}
.subtitle{color:#9a9ab4;margin:14px 0 34px;font-size:14px;letter-spacing:.5px}
form{display:flex;gap:10px;padding:7px;background:#121421;border:1px solid #383049;border-radius:16px;box-shadow:0 15px 65px #0007}
input{flex:1;min-width:0;background:transparent;border:0;outline:0;color:white;padding:13px 14px;font-size:15px}
button{border:1px solid #c084fc;border-radius:11px;padding:0 22px;background:linear-gradient(120deg,#8b42d7,#6d3eb3);color:white;font-weight:800;cursor:pointer;transition:transform .18s,filter .18s}
button:hover{filter:brightness(1.2);transform:translateY(-1px)}
h3{font-size:10px;letter-spacing:3px;color:#777b98;margin:42px 0 16px}
.links{display:grid;grid-template-columns:repeat(4,1fr);gap:11px}
a{display:block;text-decoration:none;color:#eae8f6;background:#121420;border:1px solid #292b40;border-radius:13px;padding:19px 7px;transition:transform .2s,border-color .2s,background .2s}
a:hover{transform:translateY(-3px);border-color:#a855f7;background:#1c192a}
.symbol{font-size:21px;color:#d4a5ff}.small{display:block;color:#9a9db6;font-size:11px;margin-top:8px}
.footer{color:#545970;font-size:10px;letter-spacing:2px;margin-top:38px}
@media(max-width:520px){.links{grid-template-columns:repeat(2,1fr)}form{flex-direction:column}button{padding:14px}.logo{letter-spacing:-3px}}
</style></head><body><main>
<div class="eyebrow">PERSONAL BROWSING ENVIRONMENT</div>
<p class="logo">NEON <span>GX</span></p>
<p class="subtitle">A cleaner portal to everything online.</p>
<form action="https://www.google.com/search" method="get">
<input name="q" placeholder="Search the web or enter a URL..." autofocus autocomplete="off">
<button type="submit">SEARCH ↗</button></form>
<h3>QUICK LAUNCH</h3><div class="links">
<a href="https://www.youtube.com"><span class="symbol">▶</span><span class="small">YouTube</span></a>
<a href="https://www.twitch.tv"><span class="symbol">◉</span><span class="small">Twitch</span></a>
<a href="https://www.reddit.com"><span class="symbol">◆</span><span class="small">Reddit</span></a>
<a href="https://store.steampowered.com"><span class="symbol">◈</span><span class="small">Steam</span></a>
<a href="https://discord.com/app"><span class="symbol">✳</span><span class="small">Discord</span></a>
<a href="https://open.spotify.com"><span class="symbol">♫</span><span class="small">Spotify</span></a>
<a href="https://www.netflix.com"><span class="symbol">▣</span><span class="small">Netflix</span></a>
<a href="https://github.com"><span class="symbol">⌘</span><span class="small">GitHub</span></a>
</div><div class="footer">NEON GX &nbsp; / &nbsp; DESIGNED FOR FLOW</div>
</main></body></html>
"""


class BrowserTab(QWidget):
    def __init__(self, profile, initial_url=None, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.web = QWebEngineView(self)
        self.web.setPage(QWebEnginePage(profile, self.web))
        settings = self.web.settings()
        settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptCanOpenWindows, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.FullScreenSupportEnabled, True)
        layout.addWidget(self.web)
        if initial_url:
            self.web.setUrl(QUrl(initial_url))
        else:
            self.show_home()

    def show_home(self):
        self.web.setHtml(HOME_HTML, QUrl("https://neongx.local/"))


class NeonGXBrowser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.settings_store = QSettings("NeonGX", "NeonGXBrowser")
        self.closed_tabs = []
        self.bookmarks = self.settings_store.value("bookmarks", [], type=list)
        self.setWindowTitle(APP_NAME)
        self.resize(1440, 900)
        self.setMinimumSize(900, 600)
        self.profile = QWebEngineProfile.defaultProfile()
        self.profile.downloadRequested.connect(self.handle_download)
        self._build_ui()
        self._setup_shortcuts()
        self.add_tab()
        self.apply_saved_geometry()

    def _build_ui(self):
        root = QWidget()
        self.setCentralWidget(root)
        outer = QHBoxLayout(root)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(76)
        side = QVBoxLayout(sidebar)
        side.setContentsMargins(9, 14, 9, 14)
        side.setSpacing(9)
        logo = QLabel("N")
        logo.setObjectName("logo")
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        side.addWidget(logo)
        side.addWidget(self._side_button("⌂", "Home", self.go_home))
        side.addWidget(self._side_button("＋", "New tab", self.add_tab))
        side.addWidget(self._side_button("★", "Bookmark this page", self.add_bookmark))
        side.addWidget(self._side_button("▤", "Bookmarks", self.show_bookmarks))
        side.addWidget(self._side_button("◷", "History", self.show_history))
        side.addStretch()
        side.addWidget(self._side_button("↓", "Downloads", self.show_downloads))
        outer.addWidget(sidebar)

        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(12, 10, 12, 6)
        content_layout.setSpacing(7)

        brandrow = QHBoxLayout()
        brand = QLabel("NEON GX")
        brand.setObjectName("brand")
        brandrow.addWidget(brand)
        brandrow.addWidget(QLabel(" /  HYPERSPACE WEB"))
        brandrow.addStretch()
        self.private_hint = QLabel("●  STANDARD SESSION")
        self.private_hint.setStyleSheet("color:#8bdaa9;font-size:10px;font-weight:700;letter-spacing:1px;")
        brandrow.addWidget(self.private_hint)
        content_layout.addLayout(brandrow)

        toolbar = QHBoxLayout()
        toolbar.setSpacing(6)
        self.back_btn = self._tool_button("←", "Go back (Alt+Left)", self.go_back)
        self.forward_btn = self._tool_button("→", "Go forward (Alt+Right)", self.go_forward)
        self.reload_btn = self._tool_button("↻", "Reload (Ctrl+R)", self.reload_page)
        self.home_btn = self._tool_button("⌂", "Home", self.go_home)
        for button in (self.back_btn, self.forward_btn, self.reload_btn, self.home_btn):
            toolbar.addWidget(button)

        self.address = QLineEdit()
        self.address.setPlaceholderText("Search Google or enter a website address…")
        self.address.setClearButtonEnabled(True)
        self.address.setMinimumHeight(40)
        self.address.returnPressed.connect(self.navigate_from_bar)
        toolbar.addWidget(self.address, 1)
        go_btn = QPushButton("GO ↗")
        go_btn.setObjectName("accent")
        go_btn.clicked.connect(self.navigate_from_bar)
        toolbar.addWidget(go_btn)

        self.bookmark_btn = self._tool_button("☆", "Bookmark current page", self.add_bookmark)
        toolbar.addWidget(self.bookmark_btn)
        self.menu_btn = self._tool_button("⋯", "Browser menu", self.open_browser_menu)
        toolbar.addWidget(self.menu_btn)
        content_layout.addLayout(toolbar)

        self.progress = QProgressBar()
        self.progress.setTextVisible(False)
        self.progress.setRange(0, 100)
        self.progress.setValue(0)
        self.progress.hide()
        content_layout.addWidget(self.progress)

        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.setMovable(True)
        self.tabs.setTabsClosable(True)
        self.tabs.setElideMode(Qt.TextElideMode.ElideRight)
        self.tabs.setUsesScrollButtons(True)
        self.tabs.currentChanged.connect(self.on_tab_changed)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        content_layout.addWidget(self.tabs, 1)

        self.status_label = QLabel("READY  •  NEON GX")
        self.status_label.setObjectName("status")
        content_layout.addWidget(self.status_label)
        outer.addWidget(content, 1)

        self.setStatusBar(QStatusBar())
        self.statusBar().showMessage("Welcome to Neon GX", 3500)

    def _side_button(self, symbol, label, callback):
        button = QToolButton()
        button.setObjectName("side")
        button.setText(symbol)
        button.setToolTip(label)
        button.setFixedSize(54, 46)
        button.clicked.connect(callback)
        return button

    def _tool_button(self, symbol, tooltip, callback):
        button = QToolButton()
        button.setText(symbol)
        button.setToolTip(tooltip)
        button.setFixedSize(39, 38)
        button.clicked.connect(callback)
        return button

    def _setup_shortcuts(self):
        shortcuts = [
            ("Ctrl+T", self.add_tab), ("Ctrl+W", self.close_current_tab),
            ("Ctrl+L", self.focus_address), ("Ctrl+R", self.reload_page),
            ("Ctrl+F", self.find_on_page), ("Ctrl+D", self.add_bookmark),
            ("Ctrl+Shift+T", self.reopen_closed_tab), ("Ctrl+H", self.show_history),
            ("Ctrl+J", self.show_downloads), ("Ctrl+Tab", self.next_tab),
            ("Ctrl+Shift+Tab", self.previous_tab),
            ("Alt+Left", self.go_back), ("Alt+Right", self.go_forward),
            ("Ctrl+Plus", lambda: self.zoom_page(0.1)),
            ("Ctrl+Minus", lambda: self.zoom_page(-0.1)),
            ("Ctrl+0", lambda: self.zoom_page(0, reset=True)),
        ]
        for sequence, callback in shortcuts:
            shortcut = QShortcut(QKeySequence(sequence), self)
            shortcut.activated.connect(callback)

    def current_tab(self):
        tab = self.tabs.currentWidget()
        return tab if isinstance(tab, BrowserTab) else None

    def current_browser(self):
        tab = self.current_tab()
        return tab.web if tab else None

    def add_tab(self, url=None):
        tab = BrowserTab(self.profile, url)
        index = self.tabs.addTab(tab, "New Tab")
        self.tabs.setCurrentIndex(index)
        tab.web.titleChanged.connect(lambda title, t=tab: self.update_tab_title(t, title))
        tab.web.urlChanged.connect(lambda address, t=tab: self.on_url_changed(t, address))
        tab.web.loadStarted.connect(lambda t=tab: self.on_load_started(t))
        tab.web.loadProgress.connect(lambda value, t=tab: self.on_load_progress(t, value))
        tab.web.loadFinished.connect(lambda success, t=tab: self.on_load_finished(t, success))
        tab.web.iconChanged.connect(lambda icon, t=tab: self.update_tab_icon(t, icon))
        tab.web.urlChanged.connect(lambda url, t=tab: self.record_history(t, url))
        self.address.setFocus()
        return tab

    def update_tab_title(self, tab, title):
        index = self.tabs.indexOf(tab)
        if index >= 0:
            title = title.strip() or "New Tab"
            self.tabs.setTabText(index, title[:22])
            tab.setToolTip(title)

    def update_tab_icon(self, tab, icon):
        index = self.tabs.indexOf(tab)
        if index >= 0 and not icon.isNull():
            self.tabs.setTabIcon(index, icon)

    def on_url_changed(self, tab, url):
        if tab == self.current_tab():
            self.address.setText("" if url.toString().startswith("https://neongx.local") else url.toString())
            self.address.setCursorPosition(0)
            self.bookmark_btn.setText("★" if url.toString() in self.bookmarks else "☆")

    def on_tab_changed(self, _index):
        browser = self.current_browser()
        if browser:
            url = browser.url().toString()
            self.address.setText("" if url.startswith(("about:blank", "https://neongx.local")) else url)
            self.address.setCursorPosition(0)
            self.refresh_navigation_buttons()
            self.bookmark_btn.setText("★" if url in self.bookmarks else "☆")

    def on_load_started(self, tab):
        if tab == self.current_tab():
            self.progress.show()
            self.progress.setValue(0)
            self.status_label.setText("CONNECTING  •  ESTABLISHING SECURE ROUTE…")

    def on_load_progress(self, tab, value):
        if tab == self.current_tab():
            self.progress.setValue(value)

    def on_load_finished(self, tab, success):
        if tab == self.current_tab():
            self.progress.hide()
            self.status_label.setText("READY  •  PAGE LOADED" if success else "NOTICE  •  PAGE COULD NOT LOAD")
            self.refresh_navigation_buttons()
        if success:
            self.statusBar().showMessage("Page loaded", 1800)

    def refresh_navigation_buttons(self):
        browser = self.current_browser()
        if browser:
            self.back_btn.setEnabled(browser.history().canGoBack())
            self.forward_btn.setEnabled(browser.history().canGoForward())

    def navigate_from_bar(self):
        text = self.address.text().strip()
        if not text:
            return
        if " " in text or ("." not in text and text.lower() not in ("localhost",)):
            url = SEARCH_ENGINE + quote_plus(text)
        else:
            url = QUrl.fromUserInput(text).toString()
            if QUrl(url).scheme().lower() not in ("http", "https", "file", "about"):
                url = "https://" + text
        browser = self.current_browser()
        if browser:
            browser.setUrl(QUrl(url))

    def navigate_to(self, url):
        browser = self.current_browser()
        if browser:
            browser.setUrl(QUrl(url))

    def go_back(self):
        browser = self.current_browser()
        if browser:
            browser.back()

    def go_forward(self):
        browser = self.current_browser()
        if browser:
            browser.forward()

    def reload_page(self):
        browser = self.current_browser()
        if browser:
            browser.reload()

    def go_home(self):
        tab = self.current_tab()
        if tab:
            tab.show_home()
            self.address.clear()

    def close_tab(self, index):
        if self.tabs.count() <= 1:
            self.go_home()
            return
        widget = self.tabs.widget(index)
        if isinstance(widget, BrowserTab):
            url = widget.web.url().toString()
            if url and not url.startswith("https://neongx.local"):
                self.closed_tabs.append(url)
                self.closed_tabs = self.closed_tabs[-10:]
        self.tabs.removeTab(index)
        if widget:
            widget.deleteLater()

    def close_current_tab(self):
        index = self.tabs.currentIndex()
        if index >= 0:
            self.close_tab(index)

    def reopen_closed_tab(self):
        if self.closed_tabs:
            self.add_tab(self.closed_tabs.pop())
        else:
            self.add_tab()

    def next_tab(self):
        if self.tabs.count():
            self.tabs.setCurrentIndex((self.tabs.currentIndex() + 1) % self.tabs.count())

    def previous_tab(self):
        if self.tabs.count():
            self.tabs.setCurrentIndex((self.tabs.currentIndex() - 1) % self.tabs.count())

    def focus_address(self):
        self.address.setFocus()
        self.address.selectAll()

    def add_bookmark(self):
        browser = self.current_browser()
        if not browser:
            return
        url = browser.url().toString()
        if not url or url.startswith("https://neongx.local"):
            self.statusBar().showMessage("Open a website before bookmarking it", 2500)
            return
        if url in self.bookmarks:
            self.bookmarks.remove(url)
            self.statusBar().showMessage("Bookmark removed", 2000)
        else:
            self.bookmarks.append(url)
            self.statusBar().showMessage("Bookmark saved", 2000)
        self.settings_store.setValue("bookmarks", self.bookmarks)
        self.bookmark_btn.setText("★" if url in self.bookmarks else "☆")

    def show_bookmarks(self):
        menu = QMenu(self)
        if not self.bookmarks:
            action = menu.addAction("No bookmarks yet")
            action.setEnabled(False)
        else:
            for url in self.bookmarks:
                action = menu.addAction(url[:70])
                action.triggered.connect(lambda checked=False, u=url: self.navigate_to(u))
            menu.addSeparator()
            menu.addAction("Clear bookmarks…", self.clear_bookmarks)
        menu.exec(self.mapToGlobal(self.rect().topLeft() + self.rect().center()))

    def clear_bookmarks(self):
        answer = QMessageBox.question(self, "Clear bookmarks", "Remove all saved bookmarks?")
        if answer == QMessageBox.StandardButton.Yes:
            self.bookmarks.clear()
            self.settings_store.setValue("bookmarks", self.bookmarks)
            self.bookmark_btn.setText("☆")

    def record_history(self, tab, url):
        value = url.toString()
        if not value or value.startswith(("https://neongx.local", "about:blank")):
            return
        history = self.settings_store.value("history", [], type=list)
        entry = {"title": tab.web.title() or value, "url": value}
        history = [item for item in history if item.get("url") != value]
        history.insert(0, entry)
        self.settings_store.setValue("history", history[:200])

    def show_history(self):
        history = self.settings_store.value("history", [], type=list)
        dialog = QMessageBox(self)
        dialog.setWindowTitle("Browsing history")
        dialog.setText("Recent pages are stored locally in this app's settings.")
        dialog.setInformativeText("\n".join(f"{item.get('title', 'Page')[:38]} — {item.get('url', '')[:70]}" for item in history[:12]) or "No history yet.")
        dialog.setStandardButtons(QMessageBox.StandardButton.Close)
        clear_btn = dialog.addButton("Clear history", QMessageBox.ButtonRole.DestructiveRole)
        dialog.exec()
        if dialog.clickedButton() == clear_btn:
            self.settings_store.setValue("history", [])
            self.statusBar().showMessage("Browsing history cleared", 2000)

    def show_downloads(self):
        QMessageBox.information(self, "Downloads", "When a website starts a download, Neon GX will ask where to save it.\n\nUse your system's Downloads folder to view completed files.")

    def handle_download(self, download):
        suggested = download.downloadFileName() or "download"
        path, _ = QFileDialog.getSaveFileName(self, "Save download", suggested)
        if not path:
            download.cancel()
            return
        from pathlib import Path
        download.setDownloadDirectory(str(Path(path).parent))
        download.setDownloadFileName(Path(path).name)
        download.accept()
        self.statusBar().showMessage(f"Downloading {Path(path).name}…", 5000)
        download.isFinishedChanged.connect(lambda: self.statusBar().showMessage("Download finished" if download.isFinished() else "Download stopped", 4000))

    def find_on_page(self):
        browser = self.current_browser()
        if not browser:
            return
        text, ok = QInputDialog.getText(self, "Find on page", "Search this page:")
        if ok and text:
            browser.findText(text)

    def zoom_page(self, amount, reset=False):
        browser = self.current_browser()
        if browser:
            browser.setZoomFactor(1.0 if reset else max(0.5, min(2.5, browser.zoomFactor() + amount)))

    def open_browser_menu(self):
        menu = QMenu(self)
        menu.addAction("New tab", self.add_tab, QKeySequence("Ctrl+T"))
        menu.addAction("Reopen closed tab", self.reopen_closed_tab, QKeySequence("Ctrl+Shift+T"))
        menu.addSeparator()
        menu.addAction("Bookmark this page", self.add_bookmark, QKeySequence("Ctrl+D"))
        menu.addAction("Bookmarks", self.show_bookmarks)
        menu.addAction("History", self.show_history, QKeySequence("Ctrl+H"))
        menu.addAction("Downloads", self.show_downloads, QKeySequence("Ctrl+J"))
        menu.addSeparator()
        menu.addAction("Find on page", self.find_on_page, QKeySequence("Ctrl+F"))
        menu.addAction("Zoom in", lambda: self.zoom_page(0.1))
        menu.addAction("Zoom out", lambda: self.zoom_page(-0.1))
        menu.addAction("Reset zoom", lambda: self.zoom_page(0, reset=True))
        menu.addSeparator()
        menu.addAction("Clear browsing history", self.clear_history)
        menu.exec(self.menu_btn.mapToGlobal(self.menu_btn.rect().bottomLeft()))

    def clear_history(self):
        answer = QMessageBox.question(self, "Clear browsing history", "Clear locally saved recent pages?")
        if answer == QMessageBox.StandardButton.Yes:
            self.settings_store.setValue("history", [])
            self.statusBar().showMessage("History cleared", 2000)

    def apply_saved_geometry(self):
        geometry = self.settings_store.value("geometry")
        if geometry:
            self.restoreGeometry(geometry)

    def closeEvent(self, event):
        self.settings_store.setValue("geometry", self.saveGeometry())
        super().closeEvent(event)


def main():
    QApplication.setAttribute(Qt.ApplicationAttribute.AA_ShareOpenGLContexts)
    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    app.setOrganizationName("NeonGX")
    app.setStyle("Fusion")
    app.setStyleSheet(STYLE)
    window = NeonGXBrowser()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
