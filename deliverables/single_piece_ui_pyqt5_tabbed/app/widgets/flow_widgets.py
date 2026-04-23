from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFrame, QGridLayout, QHBoxLayout, QLabel, QVBoxLayout, QWidget


class ProcessStage(QFrame):
    def __init__(self, name: str, speed: str, parcel_color: str = '#D8A24B', status_color: str = '#39d353', icon_text: str = '▣', parent=None):
        super().__init__(parent)
        self.setObjectName('processStage')
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 8, 10, 8)
        layout.setSpacing(12)

        dot = QLabel('●')
        dot.setObjectName('stageStatusDot')
        dot.setStyleSheet(f'color:{status_color};')

        name_label = QLabel(name)
        name_label.setObjectName('stageName')
        name_label.setFixedWidth(92)

        belt = QFrame()
        belt.setObjectName('beltBox')
        belt_layout = QHBoxLayout(belt)
        belt_layout.setContentsMargins(14, 6, 14, 6)
        belt_layout.setSpacing(0)
        belt_layout.addStretch()

        parcel = QLabel(icon_text)
        parcel.setObjectName('parcelBox')
        parcel.setStyleSheet(f'background:{parcel_color}; color:#111;')
        parcel.setAlignment(Qt.AlignCenter)
        parcel.setFixedSize(28, 22)
        belt_layout.addWidget(parcel)
        belt_layout.addStretch()

        speed_label = QLabel(speed)
        speed_label.setObjectName('stageSpeed')
        speed_label.setFixedWidth(64)

        layout.addWidget(dot)
        layout.addWidget(name_label)
        layout.addWidget(belt, 1)
        layout.addWidget(speed_label)


class ArrowDown(QLabel):
    def __init__(self, parent=None):
        super().__init__('↓', parent)
        self.setObjectName('flowArrow')
        self.setAlignment(Qt.AlignCenter)


class CacheGrid(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName('cacheGridCard')
        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(14)

        left_title = QLabel('缓存存格\n阵列\n(居中区)')
        left_title.setObjectName('cacheLeftTitle')
        left_title.setAlignment(Qt.AlignCenter)
        left_title.setFixedWidth(76)
        layout.addWidget(left_title)

        center = QWidget()
        center_layout = QVBoxLayout(center)
        center_layout.setContentsMargins(0, 0, 0, 0)
        center_layout.setSpacing(6)

        header = QHBoxLayout()
        header.setSpacing(6)
        header.addSpacing(20)
        for col in range(1, 13):
            lb = QLabel(f'{col:02d}')
            lb.setObjectName('gridHeaderLabel')
            lb.setFixedWidth(24)
            lb.setAlignment(Qt.AlignCenter)
            header.addWidget(lb)
        center_layout.addLayout(header)

        grid = QGridLayout()
        grid.setHorizontalSpacing(6)
        grid.setVerticalSpacing(6)

        for row in range(1, 6):
            row_lb = QLabel(f'{row:02d}')
            row_lb.setObjectName('gridHeaderLabel')
            row_lb.setAlignment(Qt.AlignCenter)
            row_lb.setFixedWidth(20)
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
        center_layout.addLayout(grid)
        layout.addWidget(center, 1)

        right_wrap = QVBoxLayout()
        right_wrap.setSpacing(6)
        title = QLabel('在库\n数量')
        title.setObjectName('cacheCountTitle')
        title.setAlignment(Qt.AlignCenter)
        value = QLabel('2')
        value.setObjectName('cacheCountValue')
        value.setAlignment(Qt.AlignCenter)
        unit = QLabel('件')
        unit.setObjectName('cacheCountUnit')
        unit.setAlignment(Qt.AlignCenter)
        right_wrap.addStretch()
        right_wrap.addWidget(title)
        right_wrap.addWidget(value)
        right_wrap.addWidget(unit)
        right_wrap.addStretch()
        layout.addLayout(right_wrap)


class LegendRow(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName('legendRow')
        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setSpacing(18)
        items = [
            ('■', '设备运行', '#39d353'),
            ('■', '设备待机', '#3398ff'),
            ('■', '告警', '#ff5f57'),
            ('■', '光电遮挡', '#f5b83d'),
            ('■', '离线', '#8fa3b9'),
        ]
        for icon, text, color in items:
            icon_lb = QLabel(icon)
            icon_lb.setStyleSheet(f'color:{color}; font-size:16px;')
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
