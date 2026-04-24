from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFrame, QGridLayout, QHBoxLayout, QLabel, QVBoxLayout, QWidget


class ProcessStage(QFrame):
    def __init__(
        self,
        name: str,
        speed: str,
        parcel_color: str = '#D8A24B',
        status_color: str = '#39d353',
        icon_text: str = '▣',
        parent=None,
    ):
        super().__init__(parent)
        self.setObjectName('processStage')
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        label_panel = QFrame()
        label_panel.setObjectName('stageLabelPanel')
        label_panel.setFixedWidth(150)
        label_layout = QHBoxLayout(label_panel)
        label_layout.setContentsMargins(12, 10, 12, 10)
        label_layout.setSpacing(8)

        dot = QLabel('●')
        dot.setObjectName('stageStatusDot')
        dot.setStyleSheet(f'color:{status_color};')

        name_label = QLabel(name)
        name_label.setObjectName('stageName')

        label_layout.addWidget(dot)
        label_layout.addWidget(name_label)
        label_layout.addStretch()

        belt = QFrame()
        belt.setObjectName('beltBox')
        belt_layout = QHBoxLayout(belt)
        belt_layout.setContentsMargins(18, 7, 18, 7)
        belt_layout.setSpacing(0)
        belt_layout.addStretch()

        if icon_text:
            parcel = QLabel(icon_text)
            parcel.setObjectName('parcelBox')
            parcel.setStyleSheet(f'background:{parcel_color}; color:#111;')
            parcel.setAlignment(Qt.AlignCenter)
            parcel.setFixedSize(30, 24)
            belt_layout.addWidget(parcel)
        belt_layout.addStretch()

        speed_label = QLabel(speed)
        speed_label.setObjectName('stageSpeed')
        speed_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        speed_label.setFixedWidth(70)

        layout.addWidget(label_panel)
        layout.addWidget(belt, 1)
        layout.addWidget(speed_label)


class ArrowDown(QLabel):
    def __init__(self, parent=None):
        super().__init__('↓', parent)
        self.setObjectName('flowArrow')
        self.setAlignment(Qt.AlignCenter)
        self.setFixedHeight(22)


class CacheGrid(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName('cacheGridCard')
        self.setMinimumHeight(270)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(14)

        left_panel = QFrame()
        left_panel.setObjectName('cacheLeftPanel')
        left_panel.setFixedWidth(98)
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(10, 10, 10, 10)
        left_layout.setSpacing(0)
        left_title = QLabel('缓存存格\n阵列\n（居中区）')
        left_title.setObjectName('cacheLeftTitle')
        left_title.setAlignment(Qt.AlignCenter)
        left_layout.addStretch()
        left_layout.addWidget(left_title)
        left_layout.addStretch()
        layout.addWidget(left_panel)

        center = QWidget()
        center_layout = QVBoxLayout(center)
        center_layout.setContentsMargins(0, 0, 0, 0)
        center_layout.setSpacing(8)

        header = QHBoxLayout()
        header.setSpacing(6)
        header.addSpacing(24)
        for col in range(1, 13):
            lb = QLabel(f'{col:02d}')
            lb.setObjectName('gridHeaderLabel')
            lb.setFixedWidth(26)
            lb.setAlignment(Qt.AlignCenter)
            header.addWidget(lb)
        header.addStretch()
        center_layout.addLayout(header)

        matrix = QFrame()
        matrix.setObjectName('cacheMatrixFrame')
        grid = QGridLayout(matrix)
        grid.setContentsMargins(0, 0, 0, 0)
        grid.setHorizontalSpacing(6)
        grid.setVerticalSpacing(6)

        for row in range(1, 6):
            row_lb = QLabel(f'{row:02d}')
            row_lb.setObjectName('gridHeaderLabel')
            row_lb.setAlignment(Qt.AlignCenter)
            row_lb.setFixedWidth(22)
            grid.addWidget(row_lb, row - 1, 0)
            for col in range(1, 13):
                cell = QLabel('●')
                cell.setAlignment(Qt.AlignCenter)
                cell.setObjectName('gridCell')
                if (row, col) == (3, 5):
                    cell.setText('▣')
                    cell.setObjectName('gridCellActiveGreen')
                elif (row, col) == (4, 9):
                    cell.setText('▣')
                    cell.setObjectName('gridCellActiveYellow')
                grid.addWidget(cell, row - 1, col)
        center_layout.addWidget(matrix)
        layout.addWidget(center, 1)

        right_panel = QFrame()
        right_panel.setObjectName('cacheRightPanel')
        right_panel.setFixedWidth(70)
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(4, 10, 4, 10)
        right_layout.setSpacing(4)
        right_layout.addStretch()
        title = QLabel('在库\n数量')
        title.setObjectName('cacheCountTitle')
        title.setAlignment(Qt.AlignCenter)
        value = QLabel('2')
        value.setObjectName('cacheCountValue')
        value.setAlignment(Qt.AlignCenter)
        unit = QLabel('件')
        unit.setObjectName('cacheCountUnit')
        unit.setAlignment(Qt.AlignCenter)
        right_layout.addWidget(title)
        right_layout.addWidget(value)
        right_layout.addWidget(unit)
        right_layout.addStretch()
        layout.addWidget(right_panel)


class LegendRow(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName('legendRow')
        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setSpacing(16)
        items = [
            ('●', '设备运行', '#39d353'),
            ('●', '设备待机', '#3398ff'),
            ('●', '告警', '#ff5f57'),
            ('●', '光电遮挡', '#f5b83d'),
            ('●', '离线', '#8fa3b9'),
        ]
        for icon, text, color in items:
            icon_lb = QLabel(icon)
            icon_lb.setStyleSheet(f'color:{color}; font-size:18px; font-weight:800;')
            text_lb = QLabel(text)
            text_lb.setObjectName('legendText')
            wrap = QHBoxLayout()
            wrap.setSpacing(6)
            wrap.addWidget(icon_lb)
            wrap.addWidget(text_lb)
            holder = QWidget()
            holder.setLayout(wrap)
            layout.addWidget(holder)
        layout.addStretch()
