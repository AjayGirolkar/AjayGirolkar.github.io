import SwiftUI

// MARK: - Color from Hex
extension Color {
    init(hex: String) {
        let hex = hex.trimmingCharacters(in: CharacterSet.alphanumerics.inverted)
        var int: UInt64 = 0
        Scanner(string: hex).scanHexInt64(&int)
        let a, r, g, b: UInt64
        switch hex.count {
        case 3: (a, r, g, b) = (255, (int >> 8) * 17, (int >> 4 & 0xF) * 17, (int & 0xF) * 17)
        case 6: (a, r, g, b) = (255, int >> 16, int >> 8 & 0xFF, int & 0xFF)
        case 8: (a, r, g, b) = (int >> 24, int >> 16 & 0xFF, int >> 8 & 0xFF, int & 0xFF)
        default: (a, r, g, b) = (255, 0, 0, 0)
        }
        self.init(.sRGB, red: Double(r)/255, green: Double(g)/255, blue: Double(b)/255, opacity: Double(a)/255)
    }
}

// MARK: - iOS Status Bar
struct IOSStatusBar: View {
    var dark: Bool = false
    var body: some View {
        HStack {
            Text("9:41")
                .font(.system(size: 15, weight: .semibold))
                .foregroundColor(dark ? .white : .black)
            Spacer()
            HStack(spacing: 6) {
                Image(systemName: "cellularbars")
                Image(systemName: "wifi")
                Image(systemName: "battery.75")
            }
            .font(.system(size: 13, weight: .medium))
            .foregroundColor(dark ? .white : .black)
        }
        .padding(.horizontal, 20)
        .padding(.top, 54)
        .padding(.bottom, 10)
    }
}

// MARK: - iOS Bottom Tab Bar
struct TabBar: View {
    var icons: [String]
    var labels: [String]
    var activeIndex: Int = 0
    var activeColor: Color = .blue
    var background: Color = Color(.systemBackground)

    var body: some View {
        HStack(spacing: 0) {
            ForEach(0..<icons.count, id: \.self) { i in
                Spacer()
                VStack(spacing: 4) {
                    Image(systemName: icons[i])
                        .font(.system(size: 22))
                    Text(labels[i])
                        .font(.system(size: 10))
                }
                .foregroundColor(i == activeIndex ? activeColor : Color(.systemGray3))
                Spacer()
            }
        }
        .padding(.vertical, 10)
        .padding(.bottom, 24)
        .background(background)
    }
}

// MARK: - Sparkline
struct Sparkline: View {
    var points: [CGFloat]
    var color: Color = .green
    var body: some View {
        GeometryReader { geo in
            let w = geo.size.width
            let h = geo.size.height
            let max = points.max() ?? 1
            let min = points.min() ?? 0
            let range = max - min == 0 ? 1 : max - min
            Path { path in
                for (i, point) in points.enumerated() {
                    let x = CGFloat(i) / CGFloat(points.count - 1) * w
                    let y = h - ((point - min) / range) * h
                    if i == 0 { path.move(to: CGPoint(x: x, y: y)) }
                    else { path.addLine(to: CGPoint(x: x, y: y)) }
                }
            }
            .stroke(color, style: StrokeStyle(lineWidth: 1.5, lineCap: .round, lineJoin: .round))
        }
    }
}

// MARK: - Card Background
struct CardBG: ViewModifier {
    var color: Color = Color(.secondarySystemBackground)
    var radius: CGFloat = 16
    func body(content: Content) -> some View {
        content
            .background(color)
            .cornerRadius(radius)
    }
}
extension View {
    func cardBG(_ color: Color = Color(.secondarySystemBackground), radius: CGFloat = 16) -> some View {
        modifier(CardBG(color: color, radius: radius))
    }
}
