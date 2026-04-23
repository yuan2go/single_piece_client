from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDoubleSpinBox,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QSpinBox,
    QToolButton,
    QVBoxLayout,
)


class InfoCard(QFrame):
    def __init__(self, title: str, value: str, desc: str = '', value_object: str = 'overviewValue', parent=None):
        super().__init__(parent)
        self.setObjectName('overviewCard')
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 14, 16, 14)
        layout.setSpacing(4)

        title_label = QLabel(title)
        title_label.setObjectName('overviewTitle')
        self.value_label = QLabel(value)
        self.value_label.setObjectName(value_object)
        desc_label = QLabel(desc)
        desc_label.setObjectName('overviewDesc')
        desc_label.setWordWrap(True)

        layout.addWidget(title_label)
        layout.addWidget(self.value_label)
        layout.addWidget(desc_label)


class SummaryCard(QFrame):
    def __init__(self, title: str, value: str, lines: list[str], accent: str = 'info', parent=None):
        super().__init__(parent)
        self.setObjectName('summaryCard')
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(8)

        title_label = QLabel(title)
        title_label.setObjectName('summaryTitle')
        self.value_label = QLabel(value)
        self.value_label.setObjectName(
            'summaryValueOk' if accent == 'ok' else 'summaryValueWarn' if accent == 'warning' else 'summaryValueInfo'
        )

        layout.addWidget(title_label)
        layout.addWidget(self.value_label)
        self.detail_labels = []
        for line in lines:
            lb = QLabel(line)
            lb.setObjectName('summaryText')
            lb.setWordWrap(True)
            layout.addWidget(lb)
            self.detail_labels.append(lb)


class CollapsibleSection(QFrame):
    def __init__(self, number: int, title: str, param_count: int, summary: str, expanded=False, parent=None):
        super().__init__(parent)
        self.expanded = expanded
        self.setObjectName('sectionCard')

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        self.header = QFrame()
        self.header.setObjectName('sectionHeader')
        h = QHBoxLayout(self.header)
        h.setContentsMargins(18, 14, 18, 14)
        h.setSpacing(12)

        num = QLabel(str(number))
        num.setObjectName('sectionNumber')
        title_label = QLabel(title)
        title_label.setObjectName('sectionTitle')
        self.ok_chip = QLabel('已配置')
        self.ok_chip.setObjectName('okChip')
        count_label = QLabel(f'{param_count}项参数')
        count_label.setObjectName('sectionMeta')
        self.summary_label = QLabel(summary)
        self.summary_label.setObjectName('sectionSummary')

        self.toggle_btn = QToolButton()
        self.toggle_btn.setObjectName('toggleButton')
        self.toggle_btn.setText('▾' if expanded else '▸')
        self.toggle_btn.clicked.connect(self.toggle)

        h.addWidget(num)
        h.addWidget(title_label)
        h.addWidget(self.ok_chip)
        h.addWidget(count_label)
        h.addWidget(self.summary_label, 1)
        h.addWidget(self.toggle_btn)

        self.content = QFrame()
        self.content.setObjectName('sectionContent')
        self.content_layout = QVBoxLayout(self.content)
        self.content_layout.setContentsMargins(20, 8, 20, 20)
        self.content_layout.setSpacing(14)
        self.content.setVisible(expanded)

        root.addWidget(self.header)
        root.addWidget(self.content)

        self.header.mousePressEvent = self._clicked

    def _clicked(self, event):
        self.toggle()
        super().mousePressEvent(event)

    def toggle(self):
        self.expanded = not self.expanded
        self.content.setVisible(self.expanded)
        self.toggle_btn.setText('▾' if self.expanded else '▸')

    def set_summary(self, text: str):
        self.summary_label.setText(text)


class FormFactory:
    def __init__(self):
        self.editors = {}

    def register(self, key: str, widget):
        self.editors[key] = widget
        return widget

    def text(self, key: str, value: str, width=None):
        w = QLineEdit(str(value))
        if width:
            w.setFixedWidth(width)
        return self.register(key, w)

    def combo(self, key: str, items: list[str], current: str):
        w = QComboBox()
        w.addItems(items)
        w.setCurrentText(str(current))
        return self.register(key, w)

    def integer(self, key: str, value: int, minimum: int, maximum: int, width=None):
        w = QSpinBox()
        w.setRange(minimum, maximum)
        w.setValue(int(value))
        if width:
            w.setFixedWidth(width)
        return self.register(key, w)

    def decimal(self, key: str, value: float, minimum: float, maximum: float, width=None):
        w = QDoubleSpinBox()
        w.setDecimals(2)
        w.setSingleStep(0.10)
        w.setRange(minimum, maximum)
        w.setValue(float(value))
        if width:
            w.setFixedWidth(width)
        return self.register(key, w)

    def check(self, key: str, text: str, checked: bool):
        w = QCheckBox(text)
        w.setChecked(bool(checked))
        return self.register(key, w)


def make_action_button(text: str, primary: bool = False) -> QPushButton:
    btn = QPushButton(text)
    btn.setCursor(Qt.PointingHandCursor)
    btn.setFixedHeight(46)
    btn.setMinimumWidth(126)
    btn.setObjectName('primaryButton' if primary else 'secondaryButton')
    return btn


def field_label(text: str) -> QLabel:
    label = QLabel(text)
    label.setObjectName('fieldLabel')
    return label


def two_col_grid() -> QGridLayout:
    grid = QGridLayout()
    grid.setHorizontalSpacing(22)
    grid.setVerticalSpacing(12)
    grid.setColumnStretch(1, 1)
    grid.setColumnStretch(3, 1)
    return grid


def populate_two_col_grid(grid: QGridLayout, left_items: list[tuple[str, object]], right_items: list[tuple[str, object]]):
    max_rows = max(len(left_items), len(right_items))
    for i in range(max_rows):
        if i < len(left_items):
            text, editor = left_items[i]
            grid.addWidget(field_label(text), i, 0)
            grid.addWidget(editor, i, 1)
        if i < len(right_items):
            text, editor = right_items[i]
            grid.addWidget(field_label(text), i, 2)
            grid.addWidget(editor, i, 3)


def inline_label(text: str) -> QLabel:
    lb = QLabel(text)
    lb.setObjectName('inlineLabel')
    return lb


def metric_tile(title: str, value: str, unit: str = '', color_object='monitorMetricValue') -> QFrame:
    frame = QFrame()
    frame.setObjectName('metricTile')
    layout = QVBoxLayout(frame)
    layout.setContentsMargins(16, 16, 16, 16)
    layout.setSpacing(6)

    title_label = QLabel(title)
    title_label.setObjectName('metricTitle')
    value_wrap = QHBoxLayout()
    value_wrap.setSpacing(6)
    value_label = QLabel(value)
    value_label.setObjectName(color_object)
    unit_label = QLabel(unit)
    unit_label.setObjectName('metricUnit')
    value_wrap.addWidget(value_label)
    value_wrap.addWidget(unit_label)
    value_wrap.addStretch()

    layout.addWidget(title_label)
    layout.addLayout(value_wrap)
    return frame


def block_card(title: str) -> tuple[QFrame, QVBoxLayout]:
    card = QFrame()
    card.setObjectName('monitorBlock')
    layout = QVBoxLayout(card)
    layout.setContentsMargins(16, 14, 16, 14)
    layout.setSpacing(12)

    title_label = QLabel(title)
    title_label.setObjectName('blockTitle')
    layout.addWidget(title_label)
    return card, layout
