from __future__ import annotations

from typing import Any

from PySide6.QtCore import QAbstractListModel, QByteArray, QModelIndex, Qt, Signal, Slot


class RoleListModel(QAbstractListModel):
    """Small QVariant-friendly list model for QML delegates."""

    modelResetDone = Signal()

    def __init__(self, roles: list[str], rows: list[dict[str, Any]] | None = None) -> None:
        super().__init__()
        self._roles = roles
        self._role_by_number = {Qt.UserRole + i + 1: role for i, role in enumerate(roles)}
        self._role_by_name = {role: Qt.UserRole + i + 1 for i, role in enumerate(roles)}
        self._rows: list[dict[str, Any]] = rows or []

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:  # noqa: N802
        if parent.isValid():
            return 0
        return len(self._rows)

    def data(self, index: QModelIndex, role: int = Qt.DisplayRole) -> Any:
        if not index.isValid() or not (0 <= index.row() < len(self._rows)):
            return None
        role_name = self._role_by_number.get(role)
        if role_name is None:
            return None
        return self._rows[index.row()].get(role_name)

    def roleNames(self) -> dict[int, QByteArray]:  # noqa: N802
        return {role: QByteArray(name.encode("utf-8")) for role, name in self._role_by_number.items()}

    def rows(self) -> list[dict[str, Any]]:
        return [row.copy() for row in self._rows]

    def set_rows(self, rows: list[dict[str, Any]]) -> None:
        self.beginResetModel()
        self._rows = rows
        self.endResetModel()
        self.modelResetDone.emit()

    def append(self, row: dict[str, Any]) -> None:
        self.beginInsertRows(QModelIndex(), len(self._rows), len(self._rows))
        self._rows.append(row)
        self.endInsertRows()

    def prepend(self, row: dict[str, Any], max_rows: int | None = None) -> None:
        self.beginInsertRows(QModelIndex(), 0, 0)
        self._rows.insert(0, row)
        self.endInsertRows()
        if max_rows is not None and len(self._rows) > max_rows:
            self.beginRemoveRows(QModelIndex(), max_rows, len(self._rows) - 1)
            del self._rows[max_rows:]
            self.endRemoveRows()

    def update_value(self, row: int, key: str, value: Any) -> None:
        if not (0 <= row < len(self._rows)) or key not in self._role_by_name:
            return
        self._rows[row][key] = value
        model_index = self.index(row, 0)
        self.dataChanged.emit(model_index, model_index, [self._role_by_name[key]])

    @Slot(int, result="QVariantMap")
    def get(self, row: int) -> dict[str, Any]:
        if 0 <= row < len(self._rows):
            return self._rows[row].copy()
        return {}
