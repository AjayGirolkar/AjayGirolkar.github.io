import SwiftUI

// ─────────────────────────────────────────────────────────────────
//  APPMARKET — App Store style app (Apple App Store)
//  6 screens, white + blue accent, Apple minimal
// ─────────────────────────────────────────────────────────────────

private extension Color {
    static let amBG    = Color.white
    static let amBlue  = Color(hex: "007AFF")
    static let amGray  = Color(hex: "8E8E93")
    static let amCard  = Color(hex: "F2F2F7")
    static let amLine  = Color(hex: "E5E5EA")
}

private let categoryData: [(String, String, [Color])] = [
    ("Games",       "gamecontroller.fill",   [Color(hex:"FF3B30"), Color(hex:"FF6B35")]),
    ("Productivity","bolt.fill",             [Color(hex:"007AFF"), Color(hex:"5AC8FA")]),
    ("Finance",     "dollarsign.circle.fill",[Color(hex:"34C759"), Color(hex:"30D158")]),
    ("Health",      "heart.fill",            [Color(hex:"FF2D55"), Color(hex:"FF6B8A")]),
    ("Education",   "book.fill",             [Color(hex:"FFCC00"), Color(hex:"FFD60A")]),
    ("Photo",       "camera.fill",           [Color(hex:"AF52DE"), Color(hex:"BF5AF2")]),
    ("Travel",      "airplane",              [Color(hex:"FF9500"), Color(hex:"FFB340")]),
    ("Social",      "person.2.fill",         [Color(hex:"007AFF"), Color(hex:"32ADE6")]),
    ("Music",       "music.note",            [Color(hex:"FF3B30"), Color(hex:"FF6961")]),
    ("News",        "newspaper.fill",        [Color(hex:"8E8E93"), Color(hex:"636366")]),
    ("Shopping",    "bag.fill",              [Color(hex:"34C759"), Color(hex:"30D158")]),
    ("Utilities",   "gearshape.fill",        [Color(hex:"8E8E93"), Color(hex:"636366")]),
]

// MARK: - App Row
private struct AppRow: View {
    var icon: String; var iconColor: Color; var name: String; var sub: String
    var rating: Double; var price: String
    var body: some View {
        HStack(spacing:14) {
            RoundedRectangle(cornerRadius:14).fill(iconColor.opacity(0.2)).frame(width:60,height:60)
                .overlay(Image(systemName:icon).font(.system(size:24)).foregroundColor(iconColor))
                .overlay(RoundedRectangle(cornerRadius:14).stroke(Color.amLine,lineWidth:0.5))
            VStack(alignment:.leading,spacing:3) {
                Text(name).font(.system(size:16,weight:.medium)).foregroundColor(.black).lineLimit(1)
                Text(sub).font(.system(size:13)).foregroundColor(.amGray).lineLimit(1)
                HStack(spacing:2) {
                    ForEach(0..<5,id:\.self) { i in
                        Image(systemName: Double(i) < rating ? "star.fill" : "star")
                            .font(.system(size:9)).foregroundColor(.amGray)
                    }
                    Text("(\(Int.random(in:100...9999)))").font(.system(size:10)).foregroundColor(.amGray)
                }
            }
            Spacer()
            Text(price).font(.system(size:15,weight:.semibold)).foregroundColor(.amBlue)
                .padding(.horizontal,16).padding(.vertical,6)
                .background(Color.amCard).clipShape(Capsule())
        }
        .padding(.vertical,6)
    }
}

// MARK: - Screen 1: Today / Featured
struct AM_Today: View {
    var body: some View {
        ZStack { Color.amBG.ignoresSafeArea()
            VStack(alignment:.leading,spacing:0) {
                IOSStatusBar(dark:false)
                HStack {
                    VStack(alignment:.leading,spacing:2) {
                        Text("WEDNESDAY, DECEMBER 18").font(.system(size:12,weight:.semibold)).foregroundColor(.amGray)
                        Text("Today").font(.system(size:32,weight:.bold)).foregroundColor(.black)
                    }
                    Spacer()
                    Circle().fill(Color.amBlue.opacity(0.15)).frame(width:36,height:36)
                        .overlay(Text("AJ").font(.system(size:12,weight:.semibold)).foregroundColor(.amBlue))
                }.padding(.horizontal,20).padding(.bottom,14)

                ScrollView(showsIndicators:false) {
                    VStack(spacing:16) {
                        // Hero card
                        ZStack(alignment:.bottomLeading) {
                            LinearGradient(colors:[Color(hex:"1C1C3A"),Color(hex:"3A0066")],startPoint:.topLeading,endPoint:.bottomTrailing)
                                .cornerRadius(18)
                            VStack(alignment:.leading,spacing:8) {
                                Text("APP OF THE DAY").font(.system(size:11,weight:.semibold)).foregroundColor(.white.opacity(0.7)).kerning(1.2)
                                HStack(spacing:14) {
                                    RoundedRectangle(cornerRadius:14).fill(Color.white.opacity(0.15)).frame(width:60,height:60)
                                        .overlay(Image(systemName:"brain.head.profile").font(.system(size:26)).foregroundColor(.white))
                                    VStack(alignment:.leading,spacing:4) {
                                        Text("MindSpace AI").font(.system(size:20,weight:.bold)).foregroundColor(.white)
                                        Text("Your AI-powered focus companion").font(.system(size:13)).foregroundColor(.white.opacity(0.75))
                                    }
                                }
                            }.padding(20)
                        }
                        .frame(maxWidth:.infinity).frame(height:200).padding(.horizontal,20)

                        // 2-col editorial
                        HStack(spacing:12) {
                            ForEach([
                                ("Top Charts","chart.bar.fill",Color(hex:"FF6B35")),
                                ("New & Noteworthy","sparkles",Color(hex:"007AFF"))],id:\.0) { card in
                                ZStack(alignment:.bottomLeading) {
                                    LinearGradient(colors:[card.2.opacity(0.8),card.2],startPoint:.top,endPoint:.bottom)
                                        .cornerRadius(14)
                                    VStack(alignment:.leading,spacing:6) {
                                        Image(systemName:card.1).font(.system(size:24)).foregroundColor(.white)
                                        Text(card.0).font(.system(size:14,weight:.bold)).foregroundColor(.white)
                                    }.padding(14)
                                }.frame(height:130)
                            }
                        }.padding(.horizontal,20)

                        // App list section
                        VStack(alignment:.leading,spacing:0) {
                            Text("Essential Apps").font(.system(size:20,weight:.bold)).foregroundColor(.black)
                                .padding(.horizontal,20).padding(.vertical,10)
                            ForEach([
                                ("bolt.fill",Color(hex:"007AFF"),"Focusplan","Productivity · Editors' Choice",4.8,"Free"),
                                ("camera.filters",Color(hex:"AF52DE"),"Luminate","Photo & Video",4.6,"₹199"),
                                ("music.note",Color(hex:"FF3B30"),"SoundWave","Music",4.9,"Free"),
                            ],id:\.2) { a in
                                AppRow(icon:a.0,iconColor:a.1,name:a.2,sub:a.3,rating:a.4,price:a.5)
                                    .padding(.horizontal,20)
                                if a.2 != "SoundWave" { Divider().padding(.horizontal,20) }
                            }
                        }.background(Color.amBG)
                    }.padding(.bottom,20)
                }

                TabBar(icons:["doc.richtext","magnifyingglass","checklist","gamecontroller","person.circle"],
                       labels:["Today","Search","Apps","Arcade","Account"],
                       activeIndex:0,activeColor:.amBlue,background:.white)
            }
        }.frame(width:393,height:852)
    }
}

// MARK: - Screen 2: Categories
struct AM_Categories: View {
    var body: some View {
        ZStack { Color.amBG.ignoresSafeArea()
            VStack(spacing:0) {
                IOSStatusBar(dark:false)
                Text("Categories").font(.system(size:32,weight:.bold)).foregroundColor(.black)
                    .frame(maxWidth:.infinity,alignment:.leading).padding(.horizontal,20).padding(.bottom,14)
                ScrollView(showsIndicators:false) {
                    LazyVGrid(columns:[GridItem(.flexible()),GridItem(.flexible()),GridItem(.flexible())],spacing:14) {
                        ForEach(categoryData,id:\.0) { cat in
                            VStack(spacing:8) {
                                ZStack {
                                    RoundedRectangle(cornerRadius:16)
                                        .fill(LinearGradient(colors:cat.2,startPoint:.topLeading,endPoint:.bottomTrailing))
                                        .frame(width:70,height:70)
                                    Image(systemName:cat.1).font(.system(size:28)).foregroundColor(.white)
                                }
                                Text(cat.0).font(.system(size:12,weight:.medium)).foregroundColor(.black).multilineTextAlignment(.center)
                            }
                        }
                    }.padding(.horizontal,20)
                }
                TabBar(icons:["doc.richtext","magnifyingglass","checklist","gamecontroller","person.circle"],
                       labels:["Today","Search","Apps","Arcade","Account"],
                       activeIndex:2,activeColor:.amBlue,background:.white)
            }
        }.frame(width:393,height:852)
    }
}

// MARK: - Screen 3: Search
struct AM_Search: View {
    let results = [
        ("bolt.fill",Color(hex:"007AFF"),"Focusplan","Productivity · #1 in Productivity",4.8,"Free"),
        ("camera.filters",Color(hex:"AF52DE"),"Luminate","Photo & Video",4.6,"₹199"),
        ("dollarsign.circle.fill",Color(hex:"34C759"),"MoneyMap","Finance · Personal Finance",4.7,"Free"),
        ("music.note",Color(hex:"FF3B30"),"SoundWave","Music",4.9,"Free"),
        ("brain.head.profile",Color(hex:"5AC8FA"),"MindSpace","Health & Fitness",4.5,"₹149"),
        ("map.fill",Color(hex:"FF9500"),"Wanderlust","Travel",4.4,"Free"),
    ]
    var body: some View {
        ZStack { Color.amBG.ignoresSafeArea()
            VStack(spacing:0) {
                IOSStatusBar(dark:false)
                Text("Search").font(.system(size:32,weight:.bold)).foregroundColor(.black)
                    .frame(maxWidth:.infinity,alignment:.leading).padding(.horizontal,20).padding(.bottom,8)
                HStack(spacing:10) {
                    HStack(spacing:8) {
                        Image(systemName:"magnifyingglass").foregroundColor(.amGray)
                        Text("Games, Apps, Stories, More").font(.system(size:15)).foregroundColor(.amGray)
                        Spacer()
                        Image(systemName:"mic.fill").foregroundColor(.amGray)
                    }.padding(10).background(Color.amCard).cornerRadius(12)
                }.padding(.horizontal,20).padding(.bottom,14)

                ScrollView(showsIndicators:false) {
                    VStack(alignment:.leading,spacing:0) {
                        Text("Top Results").font(.system(size:20,weight:.bold)).foregroundColor(.black)
                            .padding(.horizontal,20).padding(.bottom,8)
                        ForEach(results,id:\.2) { a in
                            AppRow(icon:a.0,iconColor:a.1,name:a.2,sub:a.3,rating:a.4,price:a.5)
                                .padding(.horizontal,20)
                            if a.2 != results.last?.2 { Divider().padding(.horizontal,20) }
                        }
                    }.padding(.bottom,20)
                }
                TabBar(icons:["doc.richtext","magnifyingglass","checklist","gamecontroller","person.circle"],
                       labels:["Today","Search","Apps","Arcade","Account"],
                       activeIndex:1,activeColor:.amBlue,background:.white)
            }
        }.frame(width:393,height:852)
    }
}

// MARK: - Screen 4: App Detail
struct AM_AppDetail: View {
    var body: some View {
        ZStack { Color.amBG.ignoresSafeArea()
            VStack(spacing:0) {
                IOSStatusBar(dark:false)
                HStack {
                    Image(systemName:"chevron.left").font(.system(size:17,weight:.semibold)).foregroundColor(.amBlue)
                    Text("Productivity").font(.system(size:15)).foregroundColor(.amBlue)
                    Spacer()
                    Image(systemName:"square.and.arrow.up").font(.system(size:17)).foregroundColor(.amBlue)
                }.padding(.horizontal,16).padding(.bottom,14)

                ScrollView(showsIndicators:false) {
                    VStack(alignment:.leading,spacing:0) {
                        HStack(alignment:.top,spacing:14) {
                            RoundedRectangle(cornerRadius:22)
                                .fill(LinearGradient(colors:[Color(hex:"007AFF"),Color(hex:"5AC8FA")],startPoint:.topLeading,endPoint:.bottomTrailing))
                                .frame(width:110,height:110)
                                .overlay(Image(systemName:"bolt.fill").font(.system(size:44)).foregroundColor(.white))
                                .overlay(RoundedRectangle(cornerRadius:22).stroke(Color.amLine,lineWidth:0.5))
                            VStack(alignment:.leading,spacing:6) {
                                Text("Focusplan").font(.system(size:22,weight:.bold)).foregroundColor(.black)
                                Text("Deep work timer & planner").font(.system(size:14)).foregroundColor(.amGray)
                                Text("GET").font(.system(size:15,weight:.bold)).foregroundColor(.amBlue)
                                    .padding(.horizontal,22).padding(.vertical,7)
                                    .background(Color.amCard).clipShape(Capsule())
                                Text("In-App Purchases").font(.system(size:11)).foregroundColor(.amGray)
                            }
                        }.padding(.horizontal,20).padding(.bottom,14)

                        HStack(spacing:0) {
                            ForEach([("4.8","Rating"),("18.3K","Reviews"),("#1","Productivity"),("4+","Age")],id:\.0) { m in
                                VStack(spacing:4) {
                                    Text(m.0).font(.system(size:18,weight:.bold)).foregroundColor(.black)
                                    Text(m.1).font(.system(size:11)).foregroundColor(.amGray)
                                }.frame(maxWidth:.infinity)
                                if m.0 != "4+" { Divider().frame(height:32).background(Color.amLine) }
                            }
                        }.padding(.vertical,12).background(Color.amCard).cornerRadius(14).padding(.horizontal,20).padding(.bottom,14)

                        ScrollView(.horizontal,showsIndicators:false) {
                            HStack(spacing:10) {
                                ForEach([Color(hex:"007AFF"),Color(hex:"5856D6"),Color(hex:"34C759")],id:\.self) { c in
                                    RoundedRectangle(cornerRadius:12).fill(c.opacity(0.15)).frame(width:170,height:300)
                                        .overlay(Image(systemName:"bolt.fill").font(.system(size:40)).foregroundColor(c.opacity(0.5)))
                                        .overlay(RoundedRectangle(cornerRadius:12).stroke(Color.amLine,lineWidth:0.5))
                                }
                            }.padding(.horizontal,20)
                        }.padding(.bottom,14)

                        Text("About this app").font(.system(size:18,weight:.bold)).foregroundColor(.black).padding(.horizontal,20).padding(.bottom,6)
                        Text("Focusplan helps you achieve deep work sessions using the proven Pomodoro technique. Track your productivity, set goals, and eliminate distractions with smart blocking. Trusted by 500K+ professionals worldwide.")
                            .font(.system(size:14)).foregroundColor(.black).padding(.horizontal,20).lineLimit(3)
                        Text("more").font(.system(size:14)).foregroundColor(.amBlue).padding(.horizontal,20).padding(.top,2)
                    }.padding(.bottom,20)
                }
                TabBar(icons:["doc.richtext","magnifyingglass","checklist","gamecontroller","person.circle"],
                       labels:["Today","Search","Apps","Arcade","Account"],
                       activeIndex:1,activeColor:.amBlue,background:.white)
            }
        }.frame(width:393,height:852)
    }
}

// MARK: - Screen 5: Ratings
struct AM_Ratings: View {
    let distribution: [(Int,Double)] = [(5,0.78),(4,0.12),(3,0.05),(2,0.03),(1,0.02)]
    var body: some View {
        ZStack { Color.amBG.ignoresSafeArea()
            VStack(spacing:0) {
                IOSStatusBar(dark:false)
                HStack {
                    Image(systemName:"chevron.left").font(.system(size:17,weight:.semibold)).foregroundColor(.amBlue)
                    Text("Ratings & Reviews").font(.system(size:16,weight:.semibold)).foregroundColor(.black)
                    Spacer()
                    Text("Write a Review").font(.system(size:14)).foregroundColor(.amBlue)
                }.padding(.horizontal,16).padding(.bottom,14)

                ScrollView(showsIndicators:false) {
                    VStack(spacing:14) {
                        HStack(alignment:.center,spacing:20) {
                            VStack(spacing:6) {
                                Text("4.8").font(.system(size:56,weight:.bold)).foregroundColor(.black)
                                HStack(spacing:3) {
                                    ForEach(0..<5,id:\.self) { _ in Image(systemName:"star.fill").font(.system(size:14)).foregroundColor(.amGray) }
                                }
                                Text("out of 5").font(.system(size:13)).foregroundColor(.amGray)
                            }
                            VStack(spacing:5) {
                                ForEach(distribution,id:\.0) { d in
                                    HStack(spacing:8) {
                                        Text("\(d.0)").font(.system(size:12)).foregroundColor(.amGray).frame(width:12)
                                        GeometryReader { geo in
                                            ZStack(alignment:.leading) {
                                                Capsule().fill(Color.amCard).frame(height:4)
                                                Capsule().fill(Color.amGray).frame(width:geo.size.width*CGFloat(d.1),height:4)
                                            }
                                        }.frame(height:4)
                                    }
                                }
                            }.frame(maxWidth:.infinity)
                        }.padding(.horizontal,20)

                        Divider().padding(.horizontal,20)

                        ForEach([
                            ("alex_photo","December 14","★★★★★","Life-changing app!","This app completely transformed my work routine. The focus sessions are incredibly effective and the analytics give real insights."),
                            ("dev_builds","December 10","★★★★★","Best focus app","Been using for 6 months. Clean UI, works flawlessly, worth every penny."),
                            ("sara_k","December 8","★★★★☆","Almost perfect","Great app, just wish the widget had more customisation. Otherwise 10/10"),
                        ],id:\.0) { r in
                            VStack(alignment:.leading,spacing:6) {
                                HStack {
                                    Circle().fill(Color.amBlue.opacity(0.2)).frame(width:30,height:30)
                                        .overlay(Text(String(r.0.prefix(1)).uppercased()).font(.system(size:12,weight:.bold)).foregroundColor(.amBlue))
                                    Text(r.0).font(.system(size:14,weight:.semibold)).foregroundColor(.black)
                                    Spacer()
                                    Text(r.1).font(.system(size:12)).foregroundColor(.amGray)
                                }
                                Text(r.2).font(.system(size:12)).foregroundColor(Color(hex:"FF9500"))
                                Text(r.3).font(.system(size:14,weight:.semibold)).foregroundColor(.black)
                                Text(r.4).font(.system(size:13)).foregroundColor(.black).lineLimit(3)
                            }.padding(.horizontal,20)
                            Divider().padding(.horizontal,20)
                        }
                    }.padding(.bottom,20)
                }
                TabBar(icons:["doc.richtext","magnifyingglass","checklist","gamecontroller","person.circle"],
                       labels:["Today","Search","Apps","Arcade","Account"],
                       activeIndex:1,activeColor:.amBlue,background:.white)
            }
        }.frame(width:393,height:852)
    }
}

// MARK: - Screen 6: Updates
struct AM_Updates: View {
    let apps = [
        ("bolt.fill",Color(hex:"007AFF"),"Focusplan","6.2.1","42 MB","Bug fixes and performance improvements for iOS 17."),
        ("camera.filters",Color(hex:"AF52DE"),"Luminate","3.8.0","156 MB","New AI filters, improved RAW processing speed."),
        ("dollarsign.circle.fill",Color(hex:"34C759"),"MoneyMap","2.4.2","28 MB","Added UPI auto-pay support and dark mode refresh."),
        ("music.note",Color(hex:"FF3B30"),"SoundWave","5.1.0","88 MB","Spatial Audio support, new EQ presets."),
        ("map.fill",Color(hex:"FF9500"),"Wanderlust","1.9.3","64 MB","Offline map downloads now 60% smaller."),
    ]
    var body: some View {
        ZStack { Color.amBG.ignoresSafeArea()
            VStack(spacing:0) {
                IOSStatusBar(dark:false)
                HStack {
                    Text("Updates").font(.system(size:32,weight:.bold)).foregroundColor(.black)
                    Spacer()
                    Text("Update All").font(.system(size:15,weight:.semibold)).foregroundColor(.amBlue)
                }.padding(.horizontal,20).padding(.bottom,6)
                Text("Updated Recently").font(.system(size:20,weight:.bold)).foregroundColor(.black)
                    .frame(maxWidth:.infinity,alignment:.leading).padding(.horizontal,20).padding(.bottom,10)

                ScrollView(showsIndicators:false) {
                    VStack(spacing:0) {
                        ForEach(apps,id:\.2) { a in
                            HStack(alignment:.top,spacing:14) {
                                RoundedRectangle(cornerRadius:14).fill(a.1.opacity(0.15)).frame(width:60,height:60)
                                    .overlay(Image(systemName:a.0).font(.system(size:24)).foregroundColor(a.1))
                                    .overlay(RoundedRectangle(cornerRadius:14).stroke(Color.amLine,lineWidth:0.5))
                                VStack(alignment:.leading,spacing:3) {
                                    HStack {
                                        Text(a.2).font(.system(size:16,weight:.medium)).foregroundColor(.black)
                                        Spacer()
                                        Text("UPDATE").font(.system(size:13,weight:.bold)).foregroundColor(.amBlue)
                                            .padding(.horizontal,16).padding(.vertical,6)
                                            .background(Color.amCard).clipShape(Capsule())
                                    }
                                    Text("Version \(a.3) · \(a.4)").font(.system(size:12)).foregroundColor(.amGray)
                                    Text(a.5).font(.system(size:12)).foregroundColor(.amGray).lineLimit(2)
                                }
                            }.padding(.horizontal,20).padding(.vertical,12)
                            Divider().padding(.horizontal,20)
                        }
                    }
                }
                TabBar(icons:["doc.richtext","magnifyingglass","checklist","gamecontroller","person.circle"],
                       labels:["Today","Search","Apps","Arcade","Account"],
                       activeIndex:4,activeColor:.amBlue,background:.white)
            }
        }.frame(width:393,height:852)
    }
}

#Preview("1 Today")      { AM_Today() }
#Preview("2 Categories") { AM_Categories() }
#Preview("3 Search")     { AM_Search() }
#Preview("4 App Detail") { AM_AppDetail() }
#Preview("5 Ratings")    { AM_Ratings() }
#Preview("6 Updates")    { AM_Updates() }
