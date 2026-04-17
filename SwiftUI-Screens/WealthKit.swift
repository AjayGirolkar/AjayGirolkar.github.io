import SwiftUI

// ─────────────────────────────────────────────────────────────────
//  WEALTHKIT — Finance & Investment App (INDMoney / Zerodha style)
//  6 screens, all use dark navy + emerald green theme
//  Screenshot each #Preview from Xcode Canvas
// ─────────────────────────────────────────────────────────────────

// MARK: - Brand Colors
private extension Color {
    static let wkBG     = Color(hex: "0A1628")
    static let wkCard   = Color(hex: "112240")
    static let wkCard2  = Color(hex: "1A3158")
    static let wkGreen  = Color(hex: "22D88F")
    static let wkRed    = Color(hex: "F74F4F")
    static let wkBlue   = Color(hex: "3A8EFF")
    static let wkGold   = Color(hex: "FFD166")
    static let wkText   = Color.white
    static let wkMuted  = Color.white.opacity(0.5)
}

// MARK: - Screen 1: Dashboard
struct WK_Dashboard: View {
    let segments: [(value: Double, color: Color)] = [
        (0.35, .wkBlue), (0.25, .wkGreen), (0.22, Color(hex: "9B6DFF")), (0.18, .wkGold)
    ]
    let holdings = [
        ("AAPL", "14 shares", "₹2,41,840", "+2.3%", true,  Color(hex: "147EFB")),
        ("NVDA", "8 shares",  "₹1,87,320", "+4.1%", true,  Color(hex: "76B900")),
        ("MSFT", "11 shares", "₹1,65,910", "+1.7%", true,  Color(hex: "00A4EF")),
        ("TSLA", "5 shares",  "₹82,140",   "-1.4%", false, Color(hex: "CC0000")),
    ]

    var body: some View {
        ZStack(alignment: .bottom) {
            Color.wkBG.ignoresSafeArea()
            VStack(spacing: 0) {
                IOSStatusBar(dark: true)
                // Header
                HStack {
                    VStack(alignment: .leading, spacing: 2) {
                        Text("PORTFOLIO VALUE")
                            .font(.system(size: 11, weight: .medium))
                            .foregroundColor(.wkMuted)
                            .kerning(1)
                        Text("₹8,47,293")
                            .font(.system(size: 34, weight: .bold, design: .rounded))
                            .foregroundColor(.wkText)
                    }
                    Spacer()
                    HStack(spacing: 4) {
                        Image(systemName: "arrow.up.right")
                            .font(.system(size: 11, weight: .bold))
                        Text("+1.49%")
                            .font(.system(size: 13, weight: .semibold))
                    }
                    .foregroundColor(.wkGreen)
                    .padding(.horizontal, 10).padding(.vertical, 5)
                    .background(Color.wkGreen.opacity(0.15))
                    .clipShape(Capsule())
                }
                .padding(.horizontal, 20).padding(.top, 4).padding(.bottom, 20)

                // Donut Chart
                ZStack {
                    ForEach(0..<segments.count, id: \.self) { i in
                        let start = segments[0..<i].reduce(0) { $0 + $1.value }
                        let end   = start + segments[i].value
                        Circle()
                            .trim(from: CGFloat(start), to: CGFloat(end))
                            .stroke(segments[i].color, style: StrokeStyle(lineWidth: 30, lineCap: .butt))
                            .rotationEffect(.degrees(-90))
                            .padding(4)
                    }
                    VStack(spacing: 2) {
                        Text("Total").font(.system(size: 11)).foregroundColor(.wkMuted)
                        Text("₹8.47L").font(.system(size: 18, weight: .bold)).foregroundColor(.white)
                        Text("4 stocks").font(.system(size: 11)).foregroundColor(.wkMuted)
                    }
                }
                .frame(width: 164, height: 164)
                .padding(.bottom, 8)

                // Legend row
                HStack(spacing: 16) {
                    ForEach(["AAPL","NVDA","MSFT","TSLA"], id: \.self) { s in
                        HStack(spacing: 4) {
                            Circle().fill(holdings.first(where: { $0.0 == s })?.5 ?? .gray).frame(width: 7, height: 7)
                            Text(s).font(.system(size: 10)).foregroundColor(.wkMuted)
                        }
                    }
                }
                .padding(.bottom, 16)

                // Holdings
                VStack(spacing: 0) {
                    HStack {
                        Text("Holdings").font(.system(size: 15, weight: .semibold)).foregroundColor(.wkText)
                        Spacer()
                        Text("See all").font(.system(size: 13)).foregroundColor(.wkBlue)
                    }
                    .padding(.horizontal, 20).padding(.bottom, 8)

                    ForEach(holdings, id: \.0) { h in
                        HStack {
                            ZStack {
                                Circle().fill(h.5).frame(width: 38, height: 38)
                                Text(String(h.0.prefix(1))).font(.system(size: 14, weight: .bold)).foregroundColor(.white)
                            }
                            VStack(alignment: .leading, spacing: 2) {
                                Text(h.0).font(.system(size: 14, weight: .semibold)).foregroundColor(.wkText)
                                Text(h.1).font(.system(size: 11)).foregroundColor(.wkMuted)
                            }
                            Spacer()
                            Sparkline(points: h.4 ? [40,45,42,50,55,52,60,65] : [65,60,58,55,50,48,44,40], color: h.4 ? .wkGreen : .wkRed)
                                .frame(width: 50, height: 24)
                            VStack(alignment: .trailing, spacing: 2) {
                                Text(h.2).font(.system(size: 13, weight: .semibold)).foregroundColor(.wkText)
                                Text(h.3).font(.system(size: 12, weight: .medium)).foregroundColor(h.4 ? .wkGreen : .wkRed)
                            }
                            .frame(width: 70)
                        }
                        .padding(.horizontal, 20).padding(.vertical, 10)
                        Divider().background(Color.white.opacity(0.07)).padding(.horizontal, 20)
                    }
                }
                Spacer()
                TabBar(icons: ["chart.bar.fill","briefcase","arrow.left.arrow.right.circle","bell","person.circle"],
                       labels: ["Home","Portfolio","Trade","Alerts","Profile"],
                       activeIndex: 0, activeColor: .wkGreen, background: Color.wkCard)
            }
        }
        .frame(width: 393, height: 852)
    }
}

// MARK: - Screen 2: Portfolio
struct WK_Portfolio: View {
    let stocks = [
        ("AAPL","Apple Inc.","₹2,41,840","+₹5,480","+2.3%",true, Color(hex:"147EFB"), [40.0,44,42,50,55,52,60,65]),
        ("NVDA","NVIDIA Corp","₹1,87,320","+₹7,430","+4.1%",true, Color(hex:"76B900"), [30.0,35,40,38,50,60,58,72]),
        ("MSFT","Microsoft","₹1,65,910","+₹2,760","+1.7%",true, Color(hex:"00A4EF"), [55.0,58,56,60,64,62,66,70]),
        ("TSLA","Tesla Inc.","₹82,140","-₹1,180","-1.4%",false,Color(hex:"CC0000"), [70.0,65,68,60,55,58,50,48]),
        ("BRK","Berkshire H.","₹63,280","+₹980", "+1.1%",true, Color(hex:"6B4226"), [45.0,47,46,50,52,51,55,58]),
        ("AMZN","Amazon","₹58,970","+₹1,340","+2.3%",true, Color(hex:"FF9900"), [38.0,40,44,48,46,52,55,60]),
    ]
    var body: some View {
        ZStack {
            Color.wkBG.ignoresSafeArea()
            VStack(spacing: 0) {
                IOSStatusBar(dark: true)
                HStack {
                    Text("Portfolio").font(.system(size: 22, weight: .bold)).foregroundColor(.white)
                    Spacer()
                    Image(systemName: "arrow.up.arrow.down").font(.system(size: 16)).foregroundColor(.wkMuted)
                    Image(systemName: "slider.horizontal.3").font(.system(size: 16)).foregroundColor(.wkMuted).padding(.leading, 12)
                }
                .padding(.horizontal, 20).padding(.bottom, 12)

                // Summary strip
                HStack(spacing: 0) {
                    ForEach([("Invested","₹7,12,430"),("Current","₹8,47,293"),("P&L","₹1,34,863")], id: \.0) { item in
                        VStack(spacing: 2) {
                            Text(item.0).font(.system(size: 10)).foregroundColor(.wkMuted)
                            Text(item.1).font(.system(size: 13, weight: .semibold)).foregroundColor(item.0 == "P&L" ? .wkGreen : .white)
                        }
                        .frame(maxWidth: .infinity)
                        if item.0 != "P&L" { Divider().frame(height: 28).background(Color.white.opacity(0.12)) }
                    }
                }
                .padding(.vertical, 12)
                .background(Color.wkCard).cornerRadius(12).padding(.horizontal, 20).padding(.bottom, 12)

                ScrollView(showsIndicators: false) {
                    VStack(spacing: 0) {
                        ForEach(stocks, id: \.0) { s in
                            HStack(spacing: 12) {
                                ZStack {
                                    RoundedRectangle(cornerRadius: 10).fill(s.6).frame(width: 42, height: 42)
                                    Text(String(s.0.prefix(1))).font(.system(size: 16, weight: .bold)).foregroundColor(.white)
                                }
                                VStack(alignment: .leading, spacing: 3) {
                                    Text(s.0).font(.system(size: 14, weight: .semibold)).foregroundColor(.white)
                                    Text(s.1).font(.system(size: 11)).foregroundColor(.wkMuted)
                                }
                                Spacer()
                                Sparkline(points: s.7, color: s.5 ? .wkGreen : .wkRed).frame(width: 54, height: 28)
                                VStack(alignment: .trailing, spacing: 3) {
                                    Text(s.2).font(.system(size: 13, weight: .semibold)).foregroundColor(.white)
                                    Text(s.4).font(.system(size: 12)).foregroundColor(s.5 ? .wkGreen : .wkRed)
                                }
                            }
                            .padding(.horizontal, 20).padding(.vertical, 12)
                            Divider().background(Color.white.opacity(0.07)).padding(.horizontal, 20)
                        }
                    }
                }
                TabBar(icons:["chart.bar.fill","briefcase","arrow.left.arrow.right.circle","bell","person.circle"],
                       labels:["Home","Portfolio","Trade","Alerts","Profile"],
                       activeIndex:1, activeColor:.wkGreen, background:Color.wkCard)
            }
        }
        .frame(width: 393, height: 852)
    }
}

// MARK: - Screen 3: Mutual Funds
struct WK_MutualFunds: View {
    let funds = [
        ("Equity","Large Cap","₹1,240 Cr","18.4%",Color(hex:"3A8EFF")),
        ("Debt","Liquid Fund","₹820 Cr","7.2%",Color(hex:"22D88F")),
        ("Hybrid","Balanced","₹560 Cr","12.8%",Color(hex:"9B6DFF")),
        ("Index","Nifty 50","₹2,100 Cr","16.1%",Color(hex:"FFD166")),
        ("ELSS","Tax Saver","₹430 Cr","21.3%",Color(hex:"F74F4F")),
        ("International","US Tech","₹380 Cr","14.7%",Color(hex:"FF6B35")),
    ]
    let filters = ["All","Equity","Debt","Hybrid","Index"]
    var body: some View {
        ZStack { Color.wkBG.ignoresSafeArea()
            VStack(spacing: 0) {
                IOSStatusBar(dark: true)
                Text("Mutual Funds").font(.system(size: 22, weight: .bold)).foregroundColor(.white)
                    .frame(maxWidth:.infinity, alignment:.leading).padding(.horizontal,20).padding(.bottom,12)
                ScrollView(.horizontal, showsIndicators: false) {
                    HStack(spacing: 8) {
                        ForEach(filters, id:\.self) { f in
                            Text(f).font(.system(size: 13, weight: .medium))
                                .foregroundColor(f == "All" ? .wkBG : .wkMuted)
                                .padding(.horizontal, 16).padding(.vertical, 7)
                                .background(f == "All" ? Color.wkGreen : Color.wkCard)
                                .clipShape(Capsule())
                        }
                    }.padding(.horizontal, 20)
                }.padding(.bottom, 16)

                LazyVGrid(columns: [GridItem(.flexible()), GridItem(.flexible())], spacing: 12) {
                    ForEach(funds, id:\.0) { f in
                        VStack(alignment:.leading, spacing: 8) {
                            ZStack {
                                RoundedRectangle(cornerRadius: 10).fill(f.4.opacity(0.2)).frame(height: 44)
                                Image(systemName: "chart.line.uptrend.xyaxis").font(.system(size: 22)).foregroundColor(f.4)
                            }
                            Text(f.0).font(.system(size: 13, weight: .semibold)).foregroundColor(.white)
                            Text(f.1).font(.system(size: 11)).foregroundColor(.wkMuted)
                            HStack {
                                Text(f.3).font(.system(size: 13, weight: .bold)).foregroundColor(.wkGreen)
                                Text("1Y returns").font(.system(size: 10)).foregroundColor(.wkMuted)
                            }
                            Text("Invest").font(.system(size: 12, weight: .semibold)).foregroundColor(.wkBG)
                                .frame(maxWidth:.infinity).padding(.vertical, 6)
                                .background(Color.wkGreen).cornerRadius(8)
                        }
                        .padding(14).background(Color.wkCard).cornerRadius(14)
                    }
                }.padding(.horizontal, 20)
                Spacer()
                TabBar(icons:["chart.bar.fill","briefcase","arrow.left.arrow.right.circle","bell","person.circle"],
                       labels:["Home","Portfolio","Trade","Alerts","Profile"],
                       activeIndex:2, activeColor:.wkGreen, background:Color.wkCard)
            }
        }.frame(width:393, height:852)
    }
}

// MARK: - Screen 4: Transactions
struct WK_Transactions: View {
    let txns = [
        ("Buy AAPL","Today 10:24 AM","−₹12,340","buy",Color(hex:"147EFB")),
        ("SIP - Nifty 50","Today 09:00 AM","−₹5,000","repeat",Color(hex:"22D88F")),
        ("Sell TSLA","Yesterday 3:45 PM","+₹8,720","arrow.up.right",Color(hex:"F74F4F")),
        ("Dividend MSFT","Dec 14","Received ₹430","indianrupeesign.circle",Color(hex:"FFD166")),
        ("Buy NVDA","Dec 12","−₹23,800","buy",Color(hex:"76B900")),
        ("SIP - ELSS","Dec 10","−₹3,000","repeat",Color(hex:"9B6DFF")),
        ("Sell BRK.B","Dec 8","+₹6,150","arrow.up.right",Color(hex:"6B4226")),
    ]
    var body: some View {
        ZStack { Color.wkBG.ignoresSafeArea()
            VStack(spacing: 0) {
                IOSStatusBar(dark: true)
                HStack {
                    Text("Transactions").font(.system(size: 22, weight: .bold)).foregroundColor(.white)
                    Spacer()
                    Image(systemName: "calendar").font(.system(size: 16)).foregroundColor(.wkMuted)
                }
                .padding(.horizontal, 20).padding(.bottom, 16)

                ScrollView(showsIndicators: false) {
                    VStack(spacing: 0) {
                        Text("Today").font(.system(size: 12, weight: .semibold)).foregroundColor(.wkMuted)
                            .frame(maxWidth:.infinity,alignment:.leading).padding(.horizontal,20).padding(.vertical,6)
                        ForEach(txns.prefix(2), id:\.0) { t in txnRow(t) }
                        Text("Yesterday").font(.system(size: 12, weight: .semibold)).foregroundColor(.wkMuted)
                            .frame(maxWidth:.infinity,alignment:.leading).padding(.horizontal,20).padding(.vertical,6)
                        txnRow(txns[2])
                        Text("December 2024").font(.system(size: 12, weight: .semibold)).foregroundColor(.wkMuted)
                            .frame(maxWidth:.infinity,alignment:.leading).padding(.horizontal,20).padding(.vertical,6)
                        ForEach(txns.dropFirst(3), id:\.0) { t in txnRow(t) }
                    }
                }
                TabBar(icons:["chart.bar.fill","briefcase","arrow.left.arrow.right.circle","bell","person.circle"],
                       labels:["Home","Portfolio","Trade","Alerts","Profile"],
                       activeIndex:0, activeColor:.wkGreen, background:Color.wkCard)
            }
        }.frame(width:393, height:852)
    }
    func txnRow(_ t: (String,String,String,String,Color)) -> some View {
        HStack(spacing: 12) {
            ZStack { Circle().fill(t.4.opacity(0.2)).frame(width:40,height:40)
                Image(systemName: t.3).font(.system(size:14)).foregroundColor(t.4) }
            VStack(alignment:.leading,spacing:3) {
                Text(t.0).font(.system(size:14,weight:.medium)).foregroundColor(.white)
                Text(t.1).font(.system(size:11)).foregroundColor(.wkMuted)
            }
            Spacer()
            Text(t.2).font(.system(size:13,weight:.semibold))
                .foregroundColor(t.2.hasPrefix("+") ? .wkGreen : .white)
        }
        .padding(.horizontal,20).padding(.vertical,10)
        Divider().background(Color.white.opacity(0.07)).padding(.horizontal,20)
    }
}

// MARK: - Screen 5: Goals
struct WK_Goals: View {
    let goals: [(String,String,Double,Color,String,String)] = [
        ("Emergency Fund","Safety net for 6 months",0.72,.wkGreen,"₹3,60,000","₹5,00,000"),
        ("Retirement","Corpus by age 55",0.34,Color(hex:"9B6DFF"),"₹8,47,293","₹25,00,000"),
        ("Europe Trip","2025 summer vacation",0.58,.wkGold,"₹1,16,000","₹2,00,000"),
    ]
    var body: some View {
        ZStack { Color.wkBG.ignoresSafeArea()
            VStack(spacing: 0) {
                IOSStatusBar(dark: true)
                HStack {
                    Text("My Goals").font(.system(size: 22, weight: .bold)).foregroundColor(.white)
                    Spacer()
                    Image(systemName: "plus.circle.fill").font(.system(size: 22)).foregroundColor(.wkGreen)
                }.padding(.horizontal,20).padding(.bottom,16)

                ScrollView(showsIndicators: false) {
                    VStack(spacing: 14) {
                        ForEach(goals, id: \.0) { g in
                            VStack(alignment: .leading, spacing: 14) {
                                HStack {
                                    VStack(alignment:.leading,spacing:3) {
                                        Text(g.0).font(.system(size:16,weight:.semibold)).foregroundColor(.white)
                                        Text(g.1).font(.system(size:12)).foregroundColor(.wkMuted)
                                    }
                                    Spacer()
                                    ZStack {
                                        Circle().stroke(g.3.opacity(0.2), lineWidth: 5)
                                        Circle().trim(from:0, to:CGFloat(g.2)).stroke(g.3, style:StrokeStyle(lineWidth:5,lineCap:.round))
                                            .rotationEffect(.degrees(-90))
                                        Text("\(Int(g.2*100))%").font(.system(size:12,weight:.bold)).foregroundColor(g.3)
                                    }.frame(width:52,height:52)
                                }
                                ProgressView(value: g.2).tint(g.3).background(Color.white.opacity(0.1)).cornerRadius(4)
                                HStack {
                                    Text(g.5).font(.system(size:11)).foregroundColor(.wkMuted)
                                    Spacer()
                                    Text("\(g.4) saved").font(.system(size:11,weight:.medium)).foregroundColor(g.3)
                                }
                            }
                            .padding(16).background(Color.wkCard).cornerRadius(16)
                            .padding(.horizontal, 20)
                        }
                    }.padding(.top, 4).padding(.bottom, 20)
                }
                TabBar(icons:["chart.bar.fill","briefcase","arrow.left.arrow.right.circle","bell","person.circle"],
                       labels:["Home","Portfolio","Trade","Alerts","Profile"],
                       activeIndex:0, activeColor:.wkGreen, background:Color.wkCard)
            }
        }.frame(width:393, height:852)
    }
}

// MARK: - Screen 6: Profile
struct WK_Profile: View {
    var body: some View {
        ZStack { Color.wkBG.ignoresSafeArea()
            VStack(spacing: 0) {
                IOSStatusBar(dark: true)
                Text("Profile").font(.system(size: 22, weight: .bold)).foregroundColor(.white)
                    .frame(maxWidth:.infinity,alignment:.leading).padding(.horizontal,20).padding(.bottom,16)

                VStack(spacing: 12) {
                    // Avatar
                    ZStack(alignment:.bottomTrailing) {
                        Circle().fill(Color.wkBlue.opacity(0.3)).frame(width:76,height:76)
                            .overlay(Text("AJ").font(.system(size:28,weight:.bold)).foregroundColor(.wkBlue))
                        Circle().fill(Color.wkGreen).frame(width:22,height:22)
                            .overlay(Image(systemName:"checkmark").font(.system(size:10,weight:.bold)).foregroundColor(.black))
                    }
                    Text("Ajay Girolkar").font(.system(size:18,weight:.bold)).foregroundColor(.white)
                    Text("ajay@wealthkit.io").font(.system(size:13)).foregroundColor(.wkMuted)
                    HStack(spacing: 20) {
                        ForEach([("KYC","Verified"),("PAN","Linked"),("2FA","Active")],id:\.0) { badge in
                            VStack(spacing:3) {
                                Text(badge.0).font(.system(size:10)).foregroundColor(.wkMuted)
                                Text(badge.1).font(.system(size:11,weight:.semibold)).foregroundColor(.wkGreen)
                            }
                        }
                    }
                    .padding(.vertical,8).padding(.horizontal,20)
                    .background(Color.wkCard).cornerRadius(10)
                }
                .padding(.bottom, 20)

                VStack(spacing: 0) {
                    ForEach([
                        ("Linked Accounts","building.columns","3 banks",Color.wkBlue),
                        ("UPI IDs","indianrupeesign.circle","2 active",Color.wkGreen),
                        ("Nominees","person.2","1 added",Color(hex:"9B6DFF")),
                        ("Notifications","bell","All enabled",Color.wkGold),
                        ("Security","lock.shield","Face ID on",Color(hex:"F74F4F")),
                        ("Tax Reports","doc.text","FY 2023-24",Color(hex:"FF6B35")),
                    ],id:\.0) { row in
                        HStack(spacing:14) {
                            ZStack { RoundedRectangle(cornerRadius:8).fill(row.3.opacity(0.15)).frame(width:36,height:36)
                                Image(systemName:row.1).font(.system(size:14)).foregroundColor(row.3) }
                            Text(row.0).font(.system(size:14)).foregroundColor(.white)
                            Spacer()
                            Text(row.2).font(.system(size:12)).foregroundColor(.wkMuted)
                            Image(systemName:"chevron.right").font(.system(size:12)).foregroundColor(.wkMuted)
                        }.padding(.horizontal,20).padding(.vertical,12)
                        Divider().background(Color.white.opacity(0.07)).padding(.horizontal,20)
                    }
                }.background(Color.wkCard).cornerRadius(14).padding(.horizontal,20)

                Spacer()
                TabBar(icons:["chart.bar.fill","briefcase","arrow.left.arrow.right.circle","bell","person.circle"],
                       labels:["Home","Portfolio","Trade","Alerts","Profile"],
                       activeIndex:4, activeColor:.wkGreen, background:Color.wkCard)
            }
        }.frame(width:393, height:852)
    }
}

// MARK: - Previews
#Preview("1 Dashboard")   { WK_Dashboard().preferredColorScheme(.dark) }
#Preview("2 Portfolio")   { WK_Portfolio().preferredColorScheme(.dark) }
#Preview("3 MutualFunds") { WK_MutualFunds().preferredColorScheme(.dark) }
#Preview("4 Transactions"){ WK_Transactions().preferredColorScheme(.dark) }
#Preview("5 Goals")       { WK_Goals().preferredColorScheme(.dark) }
#Preview("6 Profile")     { WK_Profile().preferredColorScheme(.dark) }
