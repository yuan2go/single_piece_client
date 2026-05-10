import QtQuick
import "../styles"

Canvas {
    id: root
    property var points: []

    onPaint: {
        var ctx = getContext("2d")
        ctx.reset()
        var left = 42
        var top = 12
        var right = 10
        var bottom = 28
        var chartWidth = width - left - right
        var chartHeight = height - top - bottom

        ctx.strokeStyle = "#263a4c"
        ctx.fillStyle = "#7f91a3"
        ctx.font = "11px sans-serif"

        for (var i = 0; i <= 4; i++) {
            var gridY = top + chartHeight * i / 4
            ctx.beginPath()
            ctx.moveTo(left, gridY)
            ctx.lineTo(width - right, gridY)
            ctx.stroke()
            ctx.fillText(1600 - 400 * i, 2, gridY + 4)
        }

        if (!points || points.length < 2) return

        function x(index) { return left + chartWidth * index / (points.length - 1) }
        function y(value) { return top + chartHeight * (1 - Math.min(1600, Math.max(0, value)) / 1600) }

        var keys = ["main", "supply", "manual", "cycle"]
        var colors = [Theme.accent, Theme.success, Theme.warning, "#9d6dff"]

        for (var series = 0; series < keys.length; series++) {
            ctx.strokeStyle = colors[series]
            ctx.lineWidth = 2
            ctx.beginPath()
            for (var p = 0; p < points.length; p++) {
                var xx = x(p)
                var yy = y(points[p][keys[series]])
                if (p === 0) ctx.moveTo(xx, yy)
                else ctx.lineTo(xx, yy)
            }
            ctx.stroke()
        }
    }

    onPointsChanged: requestPaint()
    Component.onCompleted: requestPaint()
}
