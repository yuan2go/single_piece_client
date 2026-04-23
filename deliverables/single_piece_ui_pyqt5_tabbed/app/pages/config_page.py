from __future__ import annotations

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
    QMessageBox,
    QPushButton,
    QScrollArea,
    QSpinBox,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from app.widgets.common import FormFactory, inline_label, make_action_button, populate_two_col_grid, two_col_grid


class ConfigTabButton(QPushButton):
    def __init__(self, index: int, text: str, active: bool = False, parent=None):
        super().__init__(text, parent)
        self.index = index
        self.setCursor(Qt.PointingHandCursor)
        self.setCheckable(True)
        self.setFixedHeight(56)
        self.setProperty('active', active)
        self.setChecked(active)
        self.refresh_style()

    def set_active(self, active: bool) -> None:
        self.setChecked(active)
        self.setProperty('active', active)
        self.refresh_style()

    def refresh_style(self) -> None:
        self.style().unpolish(self)
        self.style().polish(self)
        self.update()


class ConfigPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.factory = FormFactory()
        self.editors = self.factory.editors
        self.time_text = '2026-04-23 16:52:13'
        self.last_validation_ok = True
        self.dirty_keys: set[str] = set()
        self.tab_buttons: list[ConfigTabButton] = []

        self.defaults = {
            'modRows': 8, 'modCols': 8, 'modL': 500.0, 'modW': 200.0,
            'separateMode': '变速模式', 'highestSpeed': 2.00, 'lowestSpeed': 0.00,
            'defaultSpeed': 0.80, 'spacing_s': 700.0, 'spacing_l': 1000.0,
            'entry_speed_thresh': 0.60, 'entry_parcel_thresh': 6, 'minBeltNum': 6,
            'defaultNumberCameras': 3, 'fenliCameraIp': '192.168.1.10', 'beltMode': '0',
            'modRows1': 8, 'modCols1': 8, 'stackTop': 2, 'stackDown': 1,
            'stackBeltNum': 3, 'stackDefSpeed': 0.80, 'stackMinSpeed': 0.40,
            'stackMaxSpeed': 1.50, 'huancunpidai_camera_ip': '192.168.1.11',
            'modRows2': 8, 'modCols2': 8, 'alignmentSpeed': 1.30,
            'supplyType': '1', 'supplySpeed': 1.00, 'supplyRecTime': 2010,
            'supplyRunTime': 1500, 'ip2D': '192.168.1.10', 'port2D': 12345,
            'ip3D': '192.168.1.11', 'port3D': 12345, 'juzhong_camera_ip': '192.168.1.1',
            'currentMode': '模式一', 'venueName': '场地名称1',
            'defaultPlcIp': '192.168.2.15', 'defaultPlcPort': 2100, 'netType': 'TCP Client',
            'bizIp': '192.168.2.15', 'bizPort': 2001,
            'saveImage': True, 'imgInterval': 5, 'imgSavePath': 'data',
            'showCacheSpeed': True, 'showRenderImage': True, 'saveStatistics': False, 'autoStart': False,
        }
        self.last_saved_data = dict(self.defaults)

        self._build_ui()
        self._connect_editors()
        self.switch_tab(0)
        self.refresh_all()

    def _build_ui(self) -> None:
        root = QVBoxLayout(self)
        root.setContentsMargins(18, 18, 18, 18)
        root.setSpacing(16)

        root.addWidget(self._build_page_header())
        root.addWidget(self._build_workspace(), 1)
        root.addWidget(self._build_bottom_bar())

    def _build_page_header(self) -> QWidget:
        card = QFrame()
        card.setObjectName('configHeaderCard')
        layout = QHBoxLayout(card)
        layout.setContentsMargins(18, 16, 18, 16)
        layout.setSpacing(14)

        left = QVBoxLayout()
        left.setContentsMargins(0, 0, 0, 0)
        left.setSpacing(6)
        title = QLabel('参数配置')
        title.setObjectName('configPageTitle')
        note = QLabel('仅在系统离线状态下允许修改并保存参数配置')
        note.setObjectName('warningNote')
        left.addWidget(title)
        left.addWidget(note)
        layout.addLayout(left)
        layout.addStretch()

        self.current_status = self._meta_chip('当前状态：', '离线', 'stateOfflineValue')
        self.template_chip = self._meta_chip('配置模板：', '默认模板')
        self.last_update_chip = self._meta_chip('最后更新时间：', self.time_text)
        layout.addWidget(self.current_status)
        layout.addWidget(self.template_chip)
        layout.addWidget(self.last_update_chip)
        return card

    def _build_workspace(self) -> QWidget:
        wrap = QWidget()
        layout = QHBoxLayout(wrap)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(14)

        layout.addWidget(self._build_directory())
        layout.addWidget(self._build_stack_area(), 1)
        return wrap

    def _build_directory(self) -> QWidget:
        card = QFrame()
        card.setObjectName('configDirectoryCard')
        card.setFixedWidth(255)
        layout = QVBoxLayout(card)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(10)

        title = QLabel('配置分区')
        title.setObjectName('configDirectoryTitle')
        layout.addWidget(title)

        items = [
            '01  分离机与进包配置',
            '02  缓存机配置',
            '03  居中机配置',
            '04  剔除机配置',
            '05  系统配置',
            '06  PLC连接与业务通讯',
            '07  存图与显示配置',
        ]
        for i, text in enumerate(items):
            btn = ConfigTabButton(i, text, active=(i == 0))
            btn.clicked.connect(lambda checked=False, idx=i: self.switch_tab(idx))
            layout.addWidget(btn)
            self.tab_buttons.append(btn)

        layout.addStretch()

        tip = QFrame()
        tip.setObjectName('configTipCard')
        tip_layout = QVBoxLayout(tip)
        tip_layout.setContentsMargins(12, 12, 12, 12)
        tip_layout.setSpacing(6)
        t1 = QLabel('提示')
        t1.setObjectName('configTipTitle')
        t2 = QLabel('修改参数后请点击右下方“保存”按钮进行保存。')
        t2.setObjectName('configTipText')
        t2.setWordWrap(True)
        tip_layout.addWidget(t1)
        tip_layout.addWidget(t2)
        layout.addWidget(tip)
        return card

    def _build_stack_area(self) -> QWidget:
        card = QFrame()
        card.setObjectName('configBodyCard')
        outer = QVBoxLayout(card)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        self.stack = QStackedWidget()
        self.stack.addWidget(self._build_page_1())
        self.stack.addWidget(self._build_page_2())
        self.stack.addWidget(self._build_page_3())
        self.stack.addWidget(self._build_page_4())
        self.stack.addWidget(self._build_page_5())
        self.stack.addWidget(self._build_page_6())
        self.stack.addWidget(self._build_page_7())
        outer.addWidget(self.stack)
        return card

    def _page_shell(self, title: str, tail: str = '') -> tuple[QWidget, QVBoxLayout, QLabel]:
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(14)

        header = QHBoxLayout()
        header.setSpacing(8)
        title_lb = QLabel(title)
        title_lb.setObjectName('tabPageTitle')
        header.addWidget(title_lb)
        header.addStretch()
        tail_lb = QLabel(tail)
        tail_lb.setObjectName('tabPageHint')
        header.addWidget(tail_lb)
        layout.addLayout(header)
        return page, layout, tail_lb

    def _build_page_1(self) -> QWidget:
        page, layout, _ = self._page_shell('01  分离机与进包配置', '排数 8 × 列数 8')
        grid = two_col_grid()
        f = self.factory
        left = [
            ('排数 (modRows)', f.integer('modRows', 8, 1, 64)),
            ('模组长度 mm (modL)', f.decimal('modL', 500.0, 0, 99999)),
            ('分离模式 (separateMode)', f.combo('separateMode', ['变速模式', '恒速模式'], self.defaults['separateMode'])),
            ('模组默认速度 m/s (defaultSpeed)', f.decimal('defaultSpeed', 0.80, 0, 100)),
            ('普通件拉包间距 mm (spacing_s)', f.decimal('spacing_s', 700.0, 0, 99999)),
            ('入口速度阈值 (entry_speed_thresh)', f.decimal('entry_speed_thresh', 0.60, 0, 9999)),
            ('算法降级最少皮带数 (minBeltNum)', f.integer('minBeltNum', 6, 0, 9999)),
            ('单件分离相机IP (fenliCameraIp)', f.text('fenliCameraIp', '192.168.1.10')),
        ]
        right = [
            ('列数 (modCols)', f.integer('modCols', 8, 1, 64)),
            ('模组宽度 mm (modW)', f.decimal('modW', 200.0, 0, 99999)),
            ('模组最高速度 m/s (highestSpeed)', f.decimal('highestSpeed', 2.00, 0, 100)),
            ('模组最低速度 m/s (lowestSpeed)', f.decimal('lowestSpeed', 0.00, 0, 100)),
            ('易滑件拉包间距 mm (spacing_l)', f.decimal('spacing_l', 1000.0, 0, 99999)),
            ('入口包裹数量阈值 (entry_parcel_thresh)', f.integer('entry_parcel_thresh', 6, 0, 9999)),
            ('默认相机数量 (defaultNumberCameras)', f.integer('defaultNumberCameras', 3, 0, 64)),
            ('皮带顺序 (beltMode)', f.combo('beltMode', ['0', '1', '2'], self.defaults['beltMode'])),
        ]
        populate_two_col_grid(grid, left, right)
        layout.addLayout(grid)
        layout.addStretch()
        return page

    def _build_page_2(self) -> QWidget:
        page, layout, _ = self._page_shell('02  缓存机配置', '排数 8 × 列数 8')
        grid = two_col_grid()
        f = self.factory
        left = [
            ('排数 (modRows1)', f.integer('modRows1', 8, 1, 64)),
            ('上层挡板 (stackTop)', f.integer('stackTop', 2, 0, 32)),
            ('皮带数量 (stackBeltNum)', f.integer('stackBeltNum', 3, 0, 64)),
            ('默认速度 (stackDefSpeed)', f.decimal('stackDefSpeed', 0.80, 0, 100)),
            ('缓存相机IP (huancunpidai_camera_ip)', f.text('huancunpidai_camera_ip', '192.168.1.11')),
        ]
        right = [
            ('列数 (modCols1)', f.integer('modCols1', 8, 1, 64)),
            ('下层挡板 (stackDown)', f.integer('stackDown', 1, 0, 32)),
            ('最低速度 (stackMinSpeed)', f.decimal('stackMinSpeed', 0.40, 0, 100)),
            ('最高速度 (stackMaxSpeed)', f.decimal('stackMaxSpeed', 1.50, 0, 100)),
        ]
        populate_two_col_grid(grid, left, right)
        layout.addLayout(grid)
        layout.addStretch()
        return page

    def _build_page_3(self) -> QWidget:
        page, layout, _ = self._page_shell('03  居中机配置', '排数 8 × 列数 8')
        grid = two_col_grid()
        f = self.factory
        left = [
            ('排数 (modRows2)', f.integer('modRows2', 8, 1, 64)),
            ('居中机速度 (alignmentSpeed)', f.decimal('alignmentSpeed', 1.30, 0, 100)),
        ]
        right = [
            ('列数 (modCols2)', f.integer('modCols2', 8, 1, 64)),
        ]
        populate_two_col_grid(grid, left, right)
        layout.addLayout(grid)
        layout.addStretch()
        return page

    def _build_page_4(self) -> QWidget:
        page, layout, _ = self._page_shell('04  剔除机配置', '供包类型 1 ｜ 供包速度 1.00')
        grid = two_col_grid()
        f = self.factory
        left = [
            ('供包类型 (supplyType)', f.combo('supplyType', ['1', '2', '3'], self.defaults['supplyType'])),
            ('接包时间 (supplyRecTime)', f.integer('supplyRecTime', 2010, 0, 999999)),
            ('2D 相机IP (ip2D)', f.text('ip2D', '192.168.1.10')),
            ('3D 相机IP (ip3D)', f.text('ip3D', '192.168.1.11')),
            ('剔除机相机IP (juzhong_camera_ip)', f.text('juzhong_camera_ip', '192.168.1.1')),
        ]
        right = [
            ('供包速度 (supplySpeed)', f.decimal('supplySpeed', 1.00, 0, 100)),
            ('运行时间 (supplyRunTime)', f.integer('supplyRunTime', 1500, 0, 999999)),
            ('2D 相机端口 (port2D)', f.integer('port2D', 12345, 1, 65535)),
            ('3D 相机端口 (port3D)', f.integer('port3D', 12345, 1, 65535)),
        ]
        populate_two_col_grid(grid, left, right)
        layout.addLayout(grid)
        layout.addStretch()
        return page

    def _build_page_5(self) -> QWidget:
        page, layout, _ = self._page_shell('05  系统配置', '默认算法 模式一')
        grid = two_col_grid()
        f = self.factory
        left = [
            ('默认启动算法 (currentMode)', f.combo('currentMode', ['模式一', '模式二'], self.defaults['currentMode'])),
        ]
        right = [
            ('场地名称 (venueName)', f.text('venueName', '场地名称1')),
        ]
        populate_two_col_grid(grid, left, right)
        layout.addLayout(grid)
        layout.addStretch()
        return page

    def _build_page_6(self) -> QWidget:
        page, layout, _ = self._page_shell('06  PLC连接与业务通讯', 'PLC IP 192.168.2.15 ｜ 端口 2100')
        grid = two_col_grid()
        f = self.factory
        left = [
            ('PLC_IP Modbus (defaultPlcIp)', f.text('defaultPlcIp', '192.168.2.15')),
            ('业务通讯客户端 (netType)', f.combo('netType', ['TCP Client', 'TCP Server', 'UDP'], self.defaults['netType'])),
            ('业务通讯端口 (bizPort)', f.integer('bizPort', 2001, 1, 65535)),
        ]
        right = [
            ('PLC_PORT Modbus (defaultPlcPort)', f.integer('defaultPlcPort', 2100, 1, 65535)),
            ('业务通讯IP (bizIp)', f.text('bizIp', '192.168.2.15')),
        ]
        populate_two_col_grid(grid, left, right)
        layout.addLayout(grid)
        layout.addStretch()
        return page

    def _build_page_7(self) -> QWidget:
        page, layout, _ = self._page_shell('07  存图与显示配置', '保存图片 开 ｜ 间隔 5s')
        f = self.factory
        row1 = QHBoxLayout()
        row1.setSpacing(18)
        row1.addWidget(f.check('saveImage', '保存图片', True))
        row1.addWidget(inline_label('间隔秒 (imgInterval)'))
        row1.addWidget(f.integer('imgInterval', 5, 1, 999, 110))
        row1.addWidget(inline_label('图片路径 (imgSavePath)'))
        row1.addWidget(f.text('imgSavePath', 'data', 220))
        row1.addStretch()

        row2 = QHBoxLayout()
        row2.setSpacing(28)
        row2.addWidget(f.check('showCacheSpeed', '显示缓存速度', True))
        row2.addWidget(f.check('showRenderImage', '显示渲染图', True))
        row2.addWidget(f.check('saveStatistics', '统计数据保存', False))
        row2.addWidget(f.check('autoStart', '开机自启动', False))
        row2.addStretch()

        layout.addLayout(row1)
        layout.addLayout(row2)
        layout.addStretch()
        return page

    def _build_bottom_bar(self) -> QWidget:
        bar = QFrame()
        bar.setObjectName('bottomBar')
        bar.setFixedHeight(82)
        layout = QHBoxLayout(bar)
        layout.setContentsMargins(18, 16, 18, 16)
        layout.setSpacing(12)
        layout.addStretch()

        self.btn_import = make_action_button('导入模板')
        self.btn_reset = make_action_button('重置')
        self.btn_save = make_action_button('保存', True)

        self.btn_import.clicked.connect(self.import_template)
        self.btn_reset.clicked.connect(self.reset_parameters)
        self.btn_save.clicked.connect(self.save_parameters)

        layout.addWidget(self.btn_import)
        layout.addWidget(self.btn_reset)
        layout.addWidget(self.btn_save)
        return bar

    def _meta_chip(self, title: str, value: str, value_object_name: str = 'metaValue') -> QWidget:
        box = QFrame()
        box.setObjectName('metaChip')
        layout = QHBoxLayout(box)
        layout.setContentsMargins(12, 8, 12, 8)
        layout.setSpacing(8)
        t = QLabel(title)
        t.setObjectName('metaTitle')
        v = QLabel(value)
        v.setObjectName(value_object_name)
        box.value_label = v
        layout.addWidget(t)
        layout.addWidget(v)
        return box

    def _connect_editors(self) -> None:
        for widget in self.editors.values():
            if isinstance(widget, QLineEdit):
                widget.textChanged.connect(self.refresh_dirty_state)
            elif isinstance(widget, QComboBox):
                widget.currentTextChanged.connect(self.refresh_dirty_state)
            elif isinstance(widget, (QSpinBox, QDoubleSpinBox)):
                widget.valueChanged.connect(self.refresh_dirty_state)
            elif isinstance(widget, QCheckBox):
                widget.stateChanged.connect(self.refresh_dirty_state)

    def switch_tab(self, index: int) -> None:
        self.stack.setCurrentIndex(index)
        for i, btn in enumerate(self.tab_buttons):
            btn.set_active(i == index)

    def set_time(self, text: str) -> None:
        self.time_text = text
        self.last_update_chip.value_label.setText(text)

    def widget_value(self, key: str):
        widget = self.editors[key]
        if isinstance(widget, QLineEdit):
            return widget.text().strip()
        if isinstance(widget, QComboBox):
            return widget.currentText()
        if isinstance(widget, QSpinBox):
            return widget.value()
        if isinstance(widget, QDoubleSpinBox):
            return round(widget.value(), 2)
        if isinstance(widget, QCheckBox):
            return widget.isChecked()
        return None

    def collect_values(self) -> dict[str, object]:
        return {k: self.widget_value(k) for k in self.editors.keys()}

    def set_values(self, data: dict[str, object]) -> None:
        for key, value in data.items():
            widget = self.editors.get(key)
            if widget is None:
                continue
            if isinstance(widget, QLineEdit):
                widget.setText(str(value))
            elif isinstance(widget, QComboBox):
                widget.setCurrentText(str(value))
            elif isinstance(widget, QSpinBox):
                widget.setValue(int(value))
            elif isinstance(widget, QDoubleSpinBox):
                widget.setValue(float(value))
            elif isinstance(widget, QCheckBox):
                widget.setChecked(bool(value))

    def refresh_dirty_state(self) -> None:
        current = self.collect_values()
        self.dirty_keys = {k for k, v in current.items() if v != self.last_saved_data.get(k)}
        self.refresh_all()

    def refresh_all(self) -> None:
        dirty = len(self.dirty_keys)
        if dirty > 0:
            self.template_chip.value_label.setText(f'默认模板 ｜ 未保存 {dirty} 项')
        else:
            self.template_chip.value_label.setText('默认模板')

    def import_template(self) -> None:
        self.set_values(self.defaults)
        self.refresh_dirty_state()
        QMessageBox.information(self, '导入模板', '已载入默认模板参数。')

    def reset_parameters(self) -> None:
        self.set_values(self.last_saved_data)
        self.refresh_dirty_state()
        QMessageBox.information(self, '重置', '已恢复到最近一次保存的参数。')

    def save_parameters(self) -> None:
        if not self.validate_parameters(show_message=False):
            QMessageBox.warning(self, '保存失败', '参数校验未通过，请先修正后再保存。')
            return
        self.last_saved_data = self.collect_values()
        self.dirty_keys.clear()
        self.refresh_all()
        QMessageBox.information(self, '保存成功', '参数已保存。')

    def validate_parameters(self, show_message: bool = True) -> bool:
        values = self.collect_values()
        errors = []
        for key in ['fenliCameraIp', 'huancunpidai_camera_ip', 'ip2D', 'ip3D', 'juzhong_camera_ip', 'defaultPlcIp', 'bizIp']:
            if not self.is_valid_ip(str(values[key])):
                errors.append(f'{key} 不是有效的 IP 地址：{values[key]}')
        for key in ['port2D', 'port3D', 'defaultPlcPort', 'bizPort']:
            if not (1 <= int(values[key]) <= 65535):
                errors.append(f'{key} 端口超出范围：{values[key]}')
        if values['lowestSpeed'] > values['highestSpeed']:
            errors.append('模组最低速度不能大于模组最高速度')
        if values['stackMinSpeed'] > values['stackMaxSpeed']:
            errors.append('缓存机最低速度不能大于最高速度')
        if not values['venueName']:
            errors.append('场地名称不能为空')
        if not values['imgSavePath']:
            errors.append('图片路径不能为空')

        self.last_validation_ok = len(errors) == 0
        if show_message:
            if errors:
                QMessageBox.warning(self, '校验失败', '发现以下问题：\n\n' + '\n'.join(errors[:12]))
            else:
                QMessageBox.information(self, '校验通过', '全部参数校验通过。')
        return len(errors) == 0

    @staticmethod
    def is_valid_ip(ip: str) -> bool:
        parts = ip.split('.')
        if len(parts) != 4:
            return False
        try:
            nums = [int(p) for p in parts]
        except ValueError:
            return False
        return all(0 <= n <= 255 for n in nums)
