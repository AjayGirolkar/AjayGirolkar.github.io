import SwiftUI

// ─────────────────────────────────────────────────────────────────
//  PAYSWIFT — Payments & Wallet App (Paytm / PhonePe style)
//  6 screens, deep navy + gold theme
// ─────────────────────────────────────────────────────────────────

private extension Color {
    static let psBG     = Color(hex: "060E1F")
    static let psCard   = Color(hex: "0E1F3D")
    static let psCard2  = Color(hex: "162848")
    static let psGold   = Color(hex: "FFD166")
    static let psBlue   = Color(hex: "3D8EFF")
    static let psGreen  = Color(hex: "06D6A0")
    static let psRed    = Color(hex: "FF4757")
    static let psMuted  = Color.white.opacity(0.45)
}

// MARK: - Quick Action Button
private struct QuickAction: View {
    var icon: String; var label: String; var color: Color
    var body: some View {
        VStack(spacing:6) {
            ZStack {
                Circle().fill(color.opacity(0.15)).frame(width:54,height:54)
                Image(systemName:icon).font(.system(size:22)).foregroundColor(color)
            }
            Text(label).font(.system(size:11,weight:.medium)).foregroundColor(.white)
        }
    }
}

// MARK: - Screen 1: Wallet Home
struct PS_Wallet: View {
    let txns = [
        ("Zomato","Food & Drink","-₹348",false,Color(hex:"E23744")),
        ("Received","From Rohit","+₹2,000",true,Color.psGreen),
        ("Amazon Pay","Shopping","-₹1,299",false,Color(hex:"FF9900")),
        ("Electricity","Utility Bill","-₹1,847",false,Color(hex:"FFD166")),
    ]
    var body: some View {
        ZStack { Color.psBG.ignoresSafeArea()
            VStack(spacing:0) {
                IOSStatusBar(dark:true)
                HStack {
                    VStack(alignment:.leading,spacing:2) {
                        Text("Good morning").font(.system(size:13)).foregroundColor(.psMuted)
                        Text("Ajay 👋").font(.system(size:20,weight:.bold)).foregroundColor(.white)
                    }
                    Spacer()
                    ZStack(alignment:.topTrailing) {
                        Circle().fill(Color.psCard).frame(width:38,height:38)
                            .overlay(Image(systemName:"bell").font(.system(size:16)).foregroundColor(.white))
                        Circle().fill(Color.psRed).frame(width:10,height:10).offset(x:2,y:-2)
                    }
                }.padding(.horizontal,20).padding(.bottom,16)

                // Balance card
                ZStack {
                    RoundedRectangle(cornerRadius:20)
                        .fill(LinearGradient(colors:[Color(hex:"1A3A6B"),Color(hex:"0A1F4A")],startPoint:.topLeading,endPoint:.bottomTrailing))
                    VStack(spacing:6) {
                        Text("Total Balance").font(.system(size:12)).foregroundColor(.psMuted)
                        Text("₹12,847.50").font(.system(size:34,weight:.bold,design:.rounded)).foregroundColor(.white)
                        HStack(spacing:16) {
                            HStack(spacing:4) { Image(systemName:"arrow.down.circle.fill").foregroundColor(.psGreen)
                                Text("+₹5,200 this week").font(.system(size:12)).foregroundColor(.psGreen) }
                        }
                        Divider().background(Color.white.opacity(0.12)).padding(.horizontal,8)
                        HStack {
                            VStack(spacing:2) {
                                Text("Wallet").font(.system(size:11)).foregroundColor(.psMuted)
                                Text("₹4,847").font(.system(size:14,weight:.semibold)).foregroundColor(.white)
                            }.frame(maxWidth:.infinity)
                            Divider().frame(height:28).background(Color.white.opacity(0.12))
                            VStack(spacing:2) {
                                Text("Bank").font(.system(size:11)).foregroundColor(.psMuted)
                                Text("₹8,000").font(.system(size:14,weight:.semibold)).foregroundColor(.white)
                            }.frame(maxWidth:.infinity)
                        }
                    }.padding(20)
                }.padding(.horizontal,20).padding(.bottom,20)

                // Quick actions
                HStack(spacing:0) {
                    ForEach([("Send Money","arrow.up.circle.fill",Color.psBlue),
                             ("Add Money","plus.circle.fill",Color.psGreen),
                             ("Pay","qrcode.viewfinder",Color.psGold),
                             ("More","ellipsis.circle.fill",Color.psMuted)],id:\.0) { a in
                        Spacer()
                        QuickAction(icon:a.1,label:a.0,color:a.2)
                        Spacer()
                    }
                }.padding(.bottom,20)

                // Transactions
                VStack(spacing:0) {
                    HStack {
                        Text("Recent Transactions").font(.system(size:15,weight:.semibold)).foregroundColor(.white)
                        Spacer()
                        Text("See all").font(.system(size:13)).foregroundColor(.psBlue)
                    }.padding(.horizontal,20).padding(.bottom,8)

                    ForEach(txns,id:\.0) { t in
                        HStack(spacing:12) {
                            ZStack { Circle().fill(t.4.opacity(0.15)).frame(width:40,height:40)
                                Image(systemName:t.2.hasPrefix("+") ? "arrow.down" : "arrow.up").font(.system(size:14,weight:.semibold)).foregroundColor(t.4) }
                            VStack(alignment:.leading,spacing:2) {
                                Text(t.0).font(.system(size:14,weight:.medium)).foregroundColor(.white)
                                Text(t.1).font(.system(size:11)).foregroundColor(.psMuted)
                            }
                            Spacer()
                            Text(t.2).font(.system(size:14,weight:.semibold)).foregroundColor(t.3 ? .psGreen : .white)
                        }.padding(.horizontal,20).padding(.vertical,10)
                        Divider().background(Color.white.opacity(0.07)).padding(.horizontal,20)
                    }
                }
                Spacer()
                TabBar(icons:["house.fill","qrcode","arrow.left.arrow.right","creditcard","person.circle"],
                       labels:["Home","Scan","Transfer","Cards","Profile"],
                       activeIndex:0,activeColor:.psGold,background:Color.psCard)
            }
        }.frame(width:393,height:852)
    }
}

// MARK: - Screen 2: Send Money
struct PS_SendMoney: View {
    let contacts = [
        ("Priya S.","₹500 · 2 days ago",Color(hex:"E91E8C")),
        ("Rohit M.","₹2,000 · 1 week ago",Color.psBlue),
        ("Mom","₹1,000 · 3 days ago",Color.psGreen),
        ("Dev K.","₹350 · 2 weeks ago",Color(hex:"9B6DFF")),
        ("Sara J.","₹750 · 1 month ago",Color(hex:"FF6B35")),
    ]
    var body: some View {
        ZStack { Color.psBG.ignoresSafeArea()
            VStack(spacing:0) {
                IOSStatusBar(dark:true)
                HStack {
                    Image(systemName:"chevron.left").font(.system(size:18,weight:.semibold)).foregroundColor(.white)
                    Text("Send Money").font(.system(size:18,weight:.semibold)).foregroundColor(.white)
                    Spacer()
                }.padding(.horizontal,20).padding(.bottom,16)

                // Search
                HStack(spacing:10) {
                    Image(systemName:"magnifyingglass").foregroundColor(.psMuted)
                    Text("Search name, phone, UPI ID").font(.system(size:14)).foregroundColor(.psMuted)
                    Spacer()
                }.padding(12).background(Color.psCard).cornerRadius(12).padding(.horizontal,20).padding(.bottom,16)

                Text("Frequent Contacts").font(.system(size:13,weight:.medium)).foregroundColor(.psMuted)
                    .frame(maxWidth:.infinity,alignment:.leading).padding(.horizontal,20).padding(.bottom,10)

                VStack(spacing:0) {
                    ForEach(contacts,id:\.0) { c in
                        HStack(spacing:14) {
                            Circle().fill(c.2.opacity(0.2)).frame(width:46,height:46)
                                .overlay(Text(String(c.0.prefix(1))).font(.system(size:18,weight:.bold)).foregroundColor(c.2))
                            VStack(alignment:.leading,spacing:3) {
                                Text(c.0).font(.system(size:15,weight:.medium)).foregroundColor(.white)
                                Text(c.1).font(.system(size:12)).foregroundColor(.psMuted)
                            }
                            Spacer()
                            Image(systemName:"chevron.right").font(.system(size:13)).foregroundColor(.psMuted)
                        }.padding(.horizontal,20).padding(.vertical,12)
                        Divider().background(Color.white.opacity(0.07)).padding(.horizontal,20)
                    }
                }

                Spacer()

                // Amount pad
                VStack(spacing: 8) {
                    Text("Enter Amount").font(.system(size:13)).foregroundColor(.psMuted)
                    Text("₹ 0").font(.system(size:36,weight:.bold,design:.rounded)).foregroundColor(.psGold)
                    LazyVGrid(columns:[GridItem(.flexible()),GridItem(.flexible()),GridItem(.flexible())],spacing:0) {
                        ForEach(["1","2","3","4","5","6","7","8","9","⌫","0","→"],id:\.self) { k in
                            Text(k).font(.system(size:k=="→" ? 16 : 22,weight:.medium))
                                .foregroundColor(k=="→" ? .psBG : .white)
                                .frame(maxWidth:.infinity).frame(height:52)
                                .background(k=="→" ? Color.psGold : Color.clear)
                        }
                    }
                }.background(Color.psCard).cornerRadius(20,antialiased:true).padding(.horizontal,20)
                .padding(.bottom, 30)
            }
        }.frame(width:393,height:852)
    }
}

// MARK: - Screen 3: QR Scanner
struct PS_QRScan: View {
    var body: some View {
        ZStack { Color.black.ignoresSafeArea()
            VStack(spacing:0) {
                HStack {
                    Image(systemName:"xmark").font(.system(size:18,weight:.semibold)).foregroundColor(.white)
                    Spacer()
                    Text("Scan & Pay").font(.system(size:16,weight:.semibold)).foregroundColor(.white)
                    Spacer()
                    Image(systemName:"bolt.fill").font(.system(size:18)).foregroundColor(.psGold)
                }.padding(.horizontal,20).padding(.top,54)

                Spacer()
                ZStack {
                    RoundedRectangle(cornerRadius:4).fill(Color.white.opacity(0.08)).frame(width:240,height:240)
                    // Corner brackets
                    ForEach([(0.0,0.0),(1.0,0.0),(0.0,1.0),(1.0,1.0)],id:\.0) { corner in
                        let xSign: CGFloat = corner.0 == 0 ? 1 : -1
                        let ySign: CGFloat = corner.1 == 0 ? 1 : -1
                        Path { path in
                            path.move(to: CGPoint(x: 120 + xSign*120, y: 120 + ySign*84))
                            path.addLine(to: CGPoint(x: 120 + xSign*120, y: 120 + ySign*120))
                            path.addLine(to: CGPoint(x: 120 + xSign*84, y: 120 + ySign*120))
                        }
                        .stroke(Color.psGold, style: StrokeStyle(lineWidth:4,lineCap:.round,lineJoin:.round))
                        .frame(width:240,height:240)
                    }
                    // Scan line
                    Rectangle().fill(LinearGradient(colors:[Color.psGold.opacity(0),Color.psGold,Color.psGold.opacity(0)],startPoint:.leading,endPoint:.trailing))
                        .frame(width:220,height:2).offset(y:20)
                }
                Text("Point camera at QR code").font(.system(size:14)).foregroundColor(.white.opacity(0.7))
                    .padding(.top,16)
                Spacer()

                // Merchant card at bottom
                VStack(spacing:14) {
                    HStack(spacing:14) {
                        ZStack { RoundedRectangle(cornerRadius:10).fill(Color(hex:"E23744").opacity(0.2)).frame(width:44,height:44)
                            Image(systemName:"fork.knife").font(.system(size:18)).foregroundColor(Color(hex:"E23744")) }
                        VStack(alignment:.leading,spacing:2) {
                            Text("Zomato - Payment").font(.system(size:15,weight:.semibold)).foregroundColor(.white)
                            Text("zomato@upi").font(.system(size:12)).foregroundColor(.psMuted)
                        }
                        Spacer()
                        Image(systemName:"checkmark.seal.fill").font(.system(size:20)).foregroundColor(.psGold)
                    }
                    HStack(spacing: 12) {
                        Text("Enter Amount").font(.system(size:14)).foregroundColor(.psMuted).frame(maxWidth:.infinity).padding(.vertical,12)
                            .background(Color.psCard2).cornerRadius(10)
                        Text("Pay Now").font(.system(size:14,weight:.semibold)).foregroundColor(.psBG).frame(maxWidth:.infinity).padding(.vertical,12)
                            .background(Color.psGold).cornerRadius(10)
                    }
                }.padding(20).background(Color.psCard).cornerRadius(20,antialiased:true)
                .padding(.horizontal,16).padding(.bottom,34)
            }
        }.frame(width:393,height:852)
    }
}

// MARK: - Screen 4: Transaction History
struct PS_History: View {
    let sections = [
        ("Today",[
            ("Zomato","Food","−₹348",false,Color(hex:"E23744"),"fork.knife"),
            ("Ajay sent you","Transfer","+₹2,000",true,.psGreen,"arrow.down"),
        ]),
        ("Yesterday",[
            ("Amazon Pay","Shopping","−₹1,299",false,Color(hex:"FF9900"),"cart"),
            ("Electricity Bill","Utility","−₹1,847",false,Color.psGold,"bolt"),
        ]),
        ("December 12",[
            ("Netflix","Entertainment","−₹649",false,Color(hex:"E50914"),"tv"),
            ("Swiggy","Food","−₹284",false,Color(hex:"FC8019"),"bag"),
            ("Salary","Credit","+₹85,000",true,.psGreen,"briefcase"),
        ]),
    ]
    var body: some View {
        ZStack { Color.psBG.ignoresSafeArea()
            VStack(spacing:0) {
                IOSStatusBar(dark:true)
                HStack {
                    Text("Transactions").font(.system(size:22,weight:.bold)).foregroundColor(.white)
                    Spacer()
                    Image(systemName:"slider.horizontal.3").font(.system(size:16)).foregroundColor(.psMuted)
                }.padding(.horizontal,20).padding(.bottom,14)
                ScrollView(showsIndicators:false) {
                    VStack(spacing:0) {
                        ForEach(sections,id:\.0) { section in
                            Text(section.0).font(.system(size:12,weight:.semibold)).foregroundColor(.psMuted)
                                .frame(maxWidth:.infinity,alignment:.leading).padding(.horizontal,20).padding(.vertical,6)
                            ForEach(section.1,id:\.0) { t in
                                HStack(spacing:12) {
                                    ZStack { Circle().fill(t.4.opacity(0.15)).frame(width:42,height:42)
                                        Image(systemName:t.5).font(.system(size:14)).foregroundColor(t.4) }
                                    VStack(alignment:.leading,spacing:2) {
                                        Text(t.0).font(.system(size:14,weight:.medium)).foregroundColor(.white)
                                        Text(t.1).font(.system(size:11)).foregroundColor(.psMuted)
                                    }
                                    Spacer()
                                    Text(t.2).font(.system(size:14,weight:.semibold)).foregroundColor(t.3 ? .psGreen : .white)
                                }.padding(.horizontal,20).padding(.vertical,10)
                                Divider().background(Color.white.opacity(0.07)).padding(.horizontal,20)
                            }
                        }
                    }
                }
                TabBar(icons:["house.fill","qrcode","arrow.left.arrow.right","creditcard","person.circle"],
                       labels:["Home","Scan","Transfer","Cards","Profile"],
                       activeIndex:2,activeColor:.psGold,background:Color.psCard)
            }
        }.frame(width:393,height:852)
    }
}

// MARK: - Screen 5: Offers
struct PS_Offers: View {
    let offers = [
        ("Zomato","50% off on food",Color(hex:"E23744"),"fork.knife"),
        ("Amazon","10% cashback",Color(hex:"FF9900"),"cart"),
        ("Swiggy","Free delivery",Color(hex:"FC8019"),"scooter"),
        ("BookMyShow","₹100 off",Color(hex:"C0392B"),"film"),
        ("Uber","Flat ₹50 off",Color(hex:"141414"),"car"),
        ("BigBazaar","5% on groceries",Color(hex:"0087C8"),"bag"),
    ]
    var body: some View {
        ZStack { Color.psBG.ignoresSafeArea()
            VStack(spacing:0) {
                IOSStatusBar(dark:true)
                Text("Offers & Cashback").font(.system(size:22,weight:.bold)).foregroundColor(.white)
                    .frame(maxWidth:.infinity,alignment:.leading).padding(.horizontal,20).padding(.bottom,14)

                ScrollView(showsIndicators:false) {
                    LazyVGrid(columns:[GridItem(.flexible()),GridItem(.flexible())],spacing:12) {
                        ForEach(offers,id:\.0) { o in
                            VStack(alignment:.leading,spacing:10) {
                                HStack {
                                    ZStack { RoundedRectangle(cornerRadius:8).fill(o.2.opacity(0.2)).frame(width:40,height:40)
                                        Image(systemName:o.3).font(.system(size:16)).foregroundColor(o.2) }
                                    Spacer()
                                    Text("NEW").font(.system(size:9,weight:.bold)).foregroundColor(.psBG)
                                        .padding(.horizontal,6).padding(.vertical,3).background(Color.psGold).cornerRadius(4)
                                }
                                Text(o.0).font(.system(size:14,weight:.semibold)).foregroundColor(.white)
                                Text(o.1).font(.system(size:12)).foregroundColor(.psMuted)
                                Text("Claim").font(.system(size:12,weight:.semibold)).foregroundColor(.psBG)
                                    .frame(maxWidth:.infinity).padding(.vertical,7)
                                    .background(Color.psGold).cornerRadius(8)
                            }.padding(14).background(Color.psCard).cornerRadius(14)
                        }
                    }.padding(.horizontal,20)
                }
                TabBar(icons:["house.fill","qrcode","arrow.left.arrow.right","creditcard","person.circle"],
                       labels:["Home","Scan","Transfer","Cards","Profile"],
                       activeIndex:0,activeColor:.psGold,background:Color.psCard)
            }
        }.frame(width:393,height:852)
    }
}

// MARK: - Screen 6: Profile
struct PS_Profile: View {
    var body: some View {
        ZStack { Color.psBG.ignoresSafeArea()
            VStack(spacing:0) {
                IOSStatusBar(dark:true)
                Text("My Account").font(.system(size:22,weight:.bold)).foregroundColor(.white)
                    .frame(maxWidth:.infinity,alignment:.leading).padding(.horizontal,20).padding(.bottom,14)

                VStack(spacing:10) {
                    ZStack(alignment:.bottomTrailing) {
                        Circle().fill(Color.psCard).frame(width:72,height:72)
                            .overlay(Text("AJ").font(.system(size:24,weight:.bold)).foregroundColor(.psGold))
                        Circle().fill(Color.psGreen).frame(width:20,height:20)
                            .overlay(Image(systemName:"checkmark").font(.system(size:9,weight:.bold)).foregroundColor(.white))
                    }
                    Text("Ajay Girolkar").font(.system(size:18,weight:.bold)).foregroundColor(.white)
                    Text("+91 98765 43210").font(.system(size:13)).foregroundColor(.psMuted)
                    HStack(spacing:20) {
                        ForEach([("UPI Active","checkmark.circle",Color.psGreen),("KYC Done","person.badge.checkmark",Color.psGold),("Secure","lock.shield",Color.psBlue)],id:\.0) { b in
                            HStack(spacing:4) {
                                Image(systemName:b.1).font(.system(size:12)).foregroundColor(b.2)
                                Text(b.0).font(.system(size:11)).foregroundColor(b.2)
                            }
                        }
                    }.padding(.vertical,8).padding(.horizontal,16).background(Color.psCard).cornerRadius(10)
                }.padding(.bottom,16)

                VStack(spacing:0) {
                    ForEach([
                        ("Bank Accounts","building.columns","2 linked",Color.psBlue),
                        ("UPI IDs","indianrupeesign.circle","3 active",Color.psGreen),
                        ("Cards","creditcard","1 card",Color.psGold),
                        ("Transaction Limit","arrow.up.circle","₹1L/day",Color(hex:"9B6DFF")),
                        ("Help & Support","questionmark.circle","24×7",Color(hex:"FF6B35")),
                        ("Security","lock.shield","Face ID",Color.psRed),
                    ],id:\.0) { row in
                        HStack(spacing:14) {
                            ZStack { RoundedRectangle(cornerRadius:8).fill(row.3.opacity(0.15)).frame(width:36,height:36)
                                Image(systemName:row.1).font(.system(size:14)).foregroundColor(row.3) }
                            Text(row.0).font(.system(size:14)).foregroundColor(.white)
                            Spacer()
                            Text(row.2).font(.system(size:12)).foregroundColor(.psMuted)
                            Image(systemName:"chevron.right").font(.system(size:12)).foregroundColor(.psMuted)
                        }.padding(.horizontal,20).padding(.vertical,12)
                        Divider().background(Color.white.opacity(0.07)).padding(.horizontal,20)
                    }
                }.background(Color.psCard).cornerRadius(14).padding(.horizontal,20)
                Spacer()
                TabBar(icons:["house.fill","qrcode","arrow.left.arrow.right","creditcard","person.circle"],
                       labels:["Home","Scan","Transfer","Cards","Profile"],
                       activeIndex:4,activeColor:.psGold,background:Color.psCard)
            }
        }.frame(width:393,height:852)
    }
}

#Preview("1 Wallet")  { PS_Wallet() }
#Preview("2 Send")    { PS_SendMoney() }
#Preview("3 QR Scan") { PS_QRScan() }
#Preview("4 History") { PS_History() }
#Preview("5 Offers")  { PS_Offers() }
#Preview("6 Profile") { PS_Profile() }
