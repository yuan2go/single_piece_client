import QtQuick

Item {
    id: root
    property string direction: "down"
    property color lineColor: "#2F80ED"
    width: 42
    height: 28

    Canvas {
        anchors.fill: parent
        onPaint: {
            const ctx = getContext("2d")
            ctx.reset()
            ctx.strokeStyle = root.lineColor
            ctx.fillStyle = root.lineColor
            ctx.lineWidth = 2
            ctx.globalAlpha = 0.75

            if (root.direction === "down") {
                const cx = width / 2
                ctx.beginPath()
                ctx.moveTo(cx, 2)
                ctx.lineTo(cx, height - 8)
                ctx.stroke()
                ctx.beginPath()
                ctx.moveTo(cx - 6, height - 10)
                ctx.lineTo(cx, height - 2)
                ctx.lineTo(cx + 6, height - 10)
                ctx.closePath()
                ctx.fill()
            } else {
                const cy = height / 2
                ctx.beginPath()
                ctx.moveTo(2, cy)
                ctx.lineTo(width - 8, cy)
                ctx.stroke()
                ctx.beginPath()
                ctx.moveTo(width - 10, cy - 6)
                ctx.lineTo(width - 2, cy)
                ctx.lineTo(width - 10, cy + 6)
                ctx.closePath()
                ctx.fill()
            }
        }
    }
}
