
import sys
from urllib.parse import quote_plus

from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QKeySequence, QShortcut
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QTabWidget,
    QLabel,
    QFrame,
    QToolButton,
    QSizePolicy,
)
from PySide6.QtWebEngineWidgets import QWebEngineView


APP_NAME = "Neon GX"
SEARCH_ENGINE = "https://www.google.com/search?q="

STYLE = """
QMainWindow, QWidget {
    background-color: #101014;
    color: #eeeeF5;
    font-family: "Segoe UI", sans-serif;
    font-size: 13px;
}
QFrame#sidebar {
    background-color: #17171e;
    border-right: 1px solid #30303b;
}
QLabel#logo {
    color: #dc72ff;
    font-size: 21px;
    font-weight: 900;
    padding: 8px;
}
QLineEdit {
    background-color: #202029;
    color: #ffffff;
    border: 1px solid #393944;
    border-radius: 10px;
    padding: 10px 14px;
    selection-background-color: #a64dff;
}
QLineEdit:focus {
    border: 1px solid #c05cff;
}
QPushButton, QToolButton {
    background-color: #22222c;
    color: #eeeeF5;
    border: 1px solid #343440;
    border-radius: 8px;
    padding: 8px;
}
QPushButton:hover, QToolButton:hover {
    background-color: #343040;
    border-color: #bc54ff;
}
QPushButton#accent {
    background-color: #8f35c9;
    border: 1px solid #c05cff;
    font-weight: bold;
}
QPushButton#accent:hover {
    background-color: #a64de0;
}
QTabWidget::pane {
    background: #101014;
    border: none;
}
QTabBar::tab {
    background: #191920;
    color: #bdbdca;
    padding: 10px 16px;
    margin-right: 3px;
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
}
QTabBar::tab:selected {
    background: #292333;
    color: #ffffff;
    border-top: 2px solid #c05cff;
}
QTabBar::tab:hover {
    background: #302a3a;
}
QLabel#status {
    color: #8d8d9b;
    padding: 5px 10px;
    font-size: 11px;
}
"""


HOME_HTML = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
* { box-sizing: border-box; }
body {
    margin: 0;
    min-height: 100vh;
    background:
      radial-gradient(ellipse at 50% 20%, #30203e 0%, transparent 50%),
      #101014;
    color: #f5f2fa;
    font-family: "Segoe UI", Arial, sans-serif;
    display: flex;
    justify-content: center;
    align-items: center;
}
main { width: min(720px, 90%); text-align: center; padding: 40px 0; }
.logo {
    font-size: clamp(40px, 8vw, 70px);
    font-weight: 900;
    letter-spacing: -3px;
    margin: 0;
}
.logo span { color: #cf65ff; }
.subtitle { color: #a5a1b1; margin: 12px 0 30px; }
form { display: flex; gap: 8px; }
input {
    flex: 1; min-width: 0;
    border: 1px solid #474052;
    background: #1c1a24; color: white;
    border-radius: 13px; padding: 16px;
    font-size: 16px; outline: none;
}
input:focus { border-color: #c05cff; }
button {
    border: 0; border-radius: 12px;
    padding: 0 22px; background: #983fce;
    color: white; font-weight: bold; cursor: pointer;
}
h3 { color: #bdb5c9; font-size: 12px; margin-top: 38px; }
.links {
    display: grid; grid-template-columns: repeat(4, 1fr);
    gap: 12px; margin-top: 16px;
}
a {
    text-decoration: none; color: #eee;
    background: #1c1b24; border: 1px solid #302b39;
    padding: 20px 5px; border-radius: 13px;
}
a:hover { border-color: #c05cff; background: #282030; }
.small { display: block; color: #a9a1b5; font-size: 11px; margin-top: 7px; }
@media(max-width: 500px) {
  .links { grid-template-columns: repeat(2, 1fr); }
  form { flex-direction: column; }
  button { padding: 14px; }
}
</style>
</head>
<body>
<main>
  <p class="logo">NEON <span>GX</span></p>
  <p class="subtitle">Your web. Your rules. Your next level.</p>
  <form action="https://www.google.com/search" method="get">
    <input name="q" placeholder="Search the web or enter a URL..." autofocus>
    <button type="submit">SEARCH ↗</button>
  </form>
  <h3>QUICK LAUNCH</h3>
  <div class="links">
    <a href="https://www.youtube.com">▶<span class="small">YouTube</span></a>
    <a href="https://www.twitch.tv">◉<span class="small">Twitch</span></a>
    <a href="https://www.reddit.com">◆<span class="small">Reddit</span></a>
    <a href="https://store.steampowered.com">🎮<span class="small">Steam</span></a>
    <a href="https://discord.com/app">◈<span class="small">Discord</span></a>
    <a href="https://open.spotify.com">♫<span class="small">Spotify</span></a>
    <a href="https://www.netflix.com">▣<span class="small">Netflix</span></a>
    <a href="https://github.com">⌘<span class="small">GitHub</span></a>
  </div>
</main>
</body>
</html>
"""


class BrowserTab(QWidget):
    def __init__(self, initial_url=None):
        super().__init__()

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.web = QWebEngineView()
        self.layout.addWidget(self.web)

        if initial_url:
            self.web.setUrl(QUrl(initial_url))
        else:
            self.show_home()

    def show_home(self):
        self.web.setHtml(HOME_HTML, QUrl("https://neongx.local/"))


class NeonGXBrowser(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle(APP_NAME)
        self.resize(1440, 900)
        self.setMinimumSize(900, 600)

        self._build_ui()
        self._setup_shortcuts()
        self.add_tab()

    def _build_ui(self):
        root = QWidget()
        self.setCentralWidget(root)

        outer = QHBoxLayout(root)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        # Sidebar
        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(68)

        side_layout = QVBoxLayout(sidebar)
        side_layout.setContentsMargins(8, 12, 8, 12)
        side_layout.setSpacing(10)

        logo = QLabel("N")
        logo.setObjectName("logo")
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        side_layout.addWidget(logo)

        side_layout.addWidget(self._side_button("⌂", "Home", self.go_home))
        side_layout.addWidget(
            self._side_button("▶", "YouTube",
                              lambda: self.navigate_to("https://youtube.com"))
        )
        side_layout.addWidget(
            self._side_button("◉", "Twitch",
                              lambda: self.navigate_to("https://twitch.tv"))
        )
        side_layout.addWidget(
            self._side_button("◈", "Discord",
                              lambda: self.navigate_to("https://discord.com/app"))
        )
        side_layout.addWidget(
            self._side_button("◆", "Reddit",
                              lambda: self.navigate_to("https://reddit.com"))
        )
        side_layout.addStretch()

        outer.addWidget(sidebar)

        # Main content
        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(10, 8, 10, 4)
        content_layout.setSpacing(7)

        toolbar = QHBoxLayout()
        toolbar.setSpacing(6)

        self.back_btn = self._tool_button("←", "Go back", self.go_back)
        self.forward_btn = self._tool_button("→", "Go forward", self.go_forward)
        self.reload_btn = self._tool_button("↻", "Reload", self.reload_page)
        self.home_btn = self._tool_button("⌂", "Home", self.go_home)

        toolbar.addWidget(self.back_btn)
        toolbar.addWidget(self.forward_btn)
        toolbar.addWidget(self.reload_btn)
        toolbar.addWidget(self.home_btn)

        self.address = QLineEdit()
        self.address.setPlaceholderText("Search Google or enter a website")
        self.address.setClearButtonEnabled(True)
        self.address.setMinimumHeight(38)
        self.address.returnPressed.connect(self.navigate_from_bar)
        toolbar.addWidget(self.address, 1)

        go_btn = QPushButton("GO ↗")
        go_btn.setObjectName("accent")
        go_btn.clicked.connect(self.navigate_from_bar)
        toolbar.addWidget(go_btn)

        new_tab_btn = self._tool_button("+", "New tab (Ctrl+T)", self.add_tab)
        toolbar.addWidget(new_tab_btn)

        content_layout.addLayout(toolbar)

        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.setMovable(True)
        self.tabs.setTabsClosable(True)
        self.tabs.tabBar().setElideMode(Qt.TextElideMode.ElideRight)
        self.tabs.setUsesScrollButtons(True)
        self.tabs.currentChanged.connect(self.on_tab_changed)
        self.tabs.tabCloseRequested.connect(self.close_tab)

        content_layout.addWidget(self.tabs, 1)

        self.status_label = QLabel("NEON GX  •  READY")
        self.status_label.setObjectName("status")
        content_layout.addWidget(self.status_label)

        outer.addWidget(content, 1)

    def _side_button(self, symbol, label, callback):
        button = QToolButton()
        button.setText(symbol)
        button.setToolTip(label)
        button.setFixedSize(48, 44)
        button.clicked.connect(callback)
        return button

    def _tool_button(self, symbol, tooltip, callback):
        button = QToolButton()
        button.setText(symbol)
        button.setToolTip(tooltip)
        button.setFixedSize(38, 36)
        button.clicked.connect(callback)
        return button

    def _setup_shortcuts(self):
        shortcuts = [
            ("Ctrl+T", self.add_tab),
            ("Ctrl+W", self.close_current_tab),
            ("Ctrl+L", self.focus_address),
            ("Ctrl+R", self.reload_page),
            ("Alt+Left", self.go_back),
            ("Alt+Right", self.go_forward),
            ("Ctrl+Shift+T", self.add_tab),
        ]

        for sequence, callback in shortcuts:
            shortcut = QShortcut(QKeySequence(sequence), self)
            shortcut.activated.connect(callback)

    def current_browser(self):
        tab = self.tabs.currentWidget()
        return tab.web if isinstance(tab, BrowserTab) else None

    def add_tab(self, url=None):
        tab = BrowserTab(url)
        index = self.tabs.addTab(tab, "New Tab")
        self.tabs.setCurrentIndex(index)

        tab.web.titleChanged.connect(
            lambda title, browser_tab=tab: self.update_tab_title(
                browser_tab, title
            )
        )
        tab.web.urlChanged.connect(
            lambda address, browser_tab=tab: self.on_url_changed(
                browser_tab, address
            )
        )
        tab.web.loadStarted.connect(
            lambda: self.status_label.setText("NEON GX  •  LOADING...")
        )
        tab.web.loadFinished.connect(self.on_load_finished)

        self.address.setFocus()
        return tab

    def update_tab_title(self, tab, title):
        index = self.tabs.indexOf(tab)
        if index >= 0:
            text = title.strip() or "New Tab"
            self.tabs.setTabText(index, text[:24])

    def on_url_changed(self, tab, url):
        if tab == self.tabs.currentWidget():
            self.address.setText(url.toString())
            self.address.setCursorPosition(0)

    def on_tab_changed(self, _index):
        browser = self.current_browser()
        if browser:
            url = browser.url().toString()
            self.address.setText(
                "" if url.startswith("about:blank") else url
            )
            self.address.setCursorPosition(0)

    def on_load_finished(self, success):
        self.status_label.setText(
            "NEON GX  •  READY" if success
            else "NEON GX  •  PAGE LOAD FAILED"
        )
        browser = self.current_browser()
        if browser:
            self.back_btn.setEnabled(browser.history().canGoBack())
            self.forward_btn.setEnabled(browser.history().canGoForward())

    def navigate_from_bar(self):
        text = self.address.text().strip()
        if not text:
            return

        if " " in text or (
            "." not in text and text.lower() not in ("localhost",)
        ):
            url = SEARCH_ENGINE + quote_plus(text)
        else:
            url = QUrl.fromUserInput(text).toString()

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
        tab = self.tabs.currentWidget()
        if isinstance(tab, BrowserTab):
            tab.show_home()
            self.address.clear()

    def close_tab(self, index):
        widget = self.tabs.widget(index)
        self.tabs.removeTab(index)
        if widget:
            widget.deleteLater()

        if self.tabs.count() == 0:
            self.add_tab()

    def close_current_tab(self):
        index = self.tabs.currentIndex()
        if index >= 0:
            self.close_tab(index)

    def focus_address(self):
        self.address.setFocus()
        self.address.selectAll()


def main():
    # Enable Qt's OpenGL sharing before creating QApplication.
    QApplication.setAttribute(
        Qt.ApplicationAttribute.AA_ShareOpenGLContexts
    )

    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    app.setOrganizationName("NeonGX")

    app.setStyleSheet(STYLE)

    window = NeonGXBrowser()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
