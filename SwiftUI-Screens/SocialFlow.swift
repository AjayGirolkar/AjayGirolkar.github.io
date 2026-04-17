import SwiftUI

// ─────────────────────────────────────────────────────────────────
//  SOCIALFLOW — Social Media App (Instagram style)
//  6 screens, white + purple-pink gradient theme
// ─────────────────────────────────────────────────────────────────

private extension Color {
    static let sfBG     = Color.white
    static let sfPink   = Color(hex: "E1306C")
    static let sfPurple = Color(hex: "833AB4")
    static let sfOrange = Color(hex: "F56040")
    static let sfBlue   = Color(hex: "405DE6")
    static let sfGray   = Color(hex: "8E8E8E")
    static let sfLine   = Color(hex: "DBDBDB")
}

private let sfGradient = LinearGradient(
    colors: [.sfOrange, .sfPink, .sfPurple, .sfBlue],
    startPoint: .topLeading, endPoint: .bottomTrailing
)

// MARK: - Reusable Story Bubble
private struct StoryBubble: View {
    var name: String
    var color: Color
    var isAdd: Bool = false
    var body: some View {
        VStack(spacing: 4) {
            ZStack {
                Circle().fill(LinearGradient(colors: [.sfOrange,.sfPink,.sfPurple], startPoint:.topLeading, endPoint:.bottomTrailing))
                    .frame(width: 60, height: 60)
                Circle().fill(Color.sfBG).frame(width: 54, height: 54)
                Circle().fill(color.opacity(0.3)).frame(width: 50, height: 50)
                if isAdd {
                    Image(systemName: "plus").font(.system(size: 20, weight: .medium)).foregroundColor(.sfBlue)
                } else {
                    Text(String(name.prefix(1))).font(.system(size: 20, weight: .semibold)).foregroundColor(color)
                }
            }
            Text(isAdd ? "Your Story" : name).font(.system(size: 11)).foregroundColor(.black)
                .lineLimit(1).frame(width: 60)
        }
    }
}

// MARK: - Post Card
private struct PostCard: View {
    var username: String
    var subtitle: String
    var color: Color
    var likes: String
    var comments: String
    var caption: String
    var body: some View {
        VStack(alignment: .leading, spacing: 0) {
            // Header
            HStack(spacing: 10) {
                Circle().fill(color.opacity(0.3)).frame(width: 32, height: 32)
                    .overlay(Text(String(username.prefix(1))).font(.system(size: 13, weight: .semibold)).foregroundColor(color))
                VStack(alignment: .leading, spacing: 1) {
                    Text(username).font(.system(size: 13, weight: .semibold)).foregroundColor(.black)
                    Text(subtitle).font(.system(size: 11)).foregroundColor(.sfGray)
                }
                Spacer()
                Image(systemName: "ellipsis").font(.system(size: 16)).foregroundColor(.black)
            }
            .padding(.horizontal, 12).padding(.vertical, 8)

            // Image area
            Rectangle().fill(color.opacity(0.18)).frame(height: 300)
                .overlay(Image(systemName: "photo").font(.system(size: 36)).foregroundColor(color.opacity(0.4)))

            // Actions
            HStack(spacing: 16) {
                Image(systemName: "heart").font(.system(size: 22)).foregroundColor(.black)
                Image(systemName: "bubble.right").font(.system(size: 21)).foregroundColor(.black)
                Image(systemName: "paperplane").font(.system(size: 20)).foregroundColor(.black)
                Spacer()
                Image(systemName: "bookmark").font(.system(size: 21)).foregroundColor(.black)
            }
            .padding(.horizontal, 12).padding(.vertical, 8)

            Text("\(likes) likes").font(.system(size: 13, weight: .semibold)).foregroundColor(.black)
                .padding(.horizontal, 12)
            Text(caption).font(.system(size: 13)).foregroundColor(.black).lineLimit(2)
                .padding(.horizontal, 12).padding(.vertical, 3)
            Text("View all \(comments) comments").font(.system(size: 13)).foregroundColor(.sfGray)
                .padding(.horizontal, 12).padding(.bottom, 8)
        }
    }
}

// MARK: - Screen 1: Feed
struct SF_Feed: View {
    let stories: [(String, Color)] = [
        ("Alex",.sfBlue),("Priya",.sfPink),("Rohit",.sfPurple),("Sara",.sfOrange),("Dev",Color(hex:"2ECC71"))
    ]
    var body: some View {
        ZStack { Color.sfBG.ignoresSafeArea()
            VStack(spacing: 0) {
                IOSStatusBar(dark: false)
                // Nav
                HStack {
                    Text("SocialFlow").font(.system(size: 22, weight: .bold, design: .serif)).foregroundColor(.black)
                    Spacer()
                    Image(systemName: "heart").font(.system(size: 22)).foregroundColor(.black)
                    Image(systemName: "paperplane").font(.system(size: 22)).foregroundColor(.black).padding(.leading, 16)
                }
                .padding(.horizontal, 16).padding(.bottom, 8)
                Divider()

                ScrollView(showsIndicators: false) {
                    // Stories
                    ScrollView(.horizontal, showsIndicators: false) {
                        HStack(spacing: 12) {
                            StoryBubble(name: "You", color: .sfBlue, isAdd: true)
                            ForEach(stories, id:\.0) { s in StoryBubble(name: s.0, color: s.1) }
                        }.padding(.horizontal, 12).padding(.vertical, 8)
                    }
                    Divider()
                    PostCard(username:"priya.designs",subtitle:"Mumbai",color:.sfPink,likes:"4,821",comments:"48","✨ Golden hour never disappoints 🌇")
                    Divider()
                    PostCard(username:"rohit.travels",subtitle:"Ladakh",color:.sfBlue,likes:"12,340",comments:"203","The mountains are calling 🏔️ #Travel")
                }
                Divider()
                TabBar(icons:["house.fill","magnifyingglass","plus.app","heart","person.circle"],
                       labels:["Home","Search","Create","Likes","Profile"],
                       activeIndex:0, activeColor:.black, background:.white)
            }
        }.frame(width:393, height:852)
    }
}

// MARK: - Screen 2: Stories Viewer
struct SF_Stories: View {
    var body: some View {
        ZStack { Color.black.ignoresSafeArea()
            VStack(spacing: 0) {
                // Progress bars
                HStack(spacing: 4) {
                    ForEach(0..<5, id:\.self) { i in
                        Capsule()
                            .fill(i == 1 ? Color.white : Color.white.opacity(0.4))
                            .frame(height: 2)
                    }
                }.padding(.horizontal, 12).padding(.top, 54)

                HStack(spacing: 10) {
                    Circle().fill(Color.sfPink.opacity(0.4)).frame(width:32,height:32)
                        .overlay(Text("P").font(.system(size:13,weight:.bold)).foregroundColor(.white))
                    Text("priya.designs").font(.system(size:13,weight:.semibold)).foregroundColor(.white)
                    Text("2h ago").font(.system(size:12)).foregroundColor(.white.opacity(0.6))
                    Spacer()
                    Image(systemName:"xmark").font(.system(size:18)).foregroundColor(.white)
                    Image(systemName:"ellipsis").font(.system(size:16)).foregroundColor(.white).padding(.leading,8)
                }.padding(.horizontal,12).padding(.top,8)

                ZStack {
                    LinearGradient(colors:[Color(hex:"FF6B35"),Color(hex:"F7C59F"),Color(hex:"EFEFD0")],
                                   startPoint:.top,endPoint:.bottom)
                        .cornerRadius(0)
                    VStack(spacing: 16) {
                        Image(systemName:"sun.max.fill").font(.system(size:60)).foregroundColor(.sfOrange)
                        Text("Golden Hour 🌅").font(.system(size:24,weight:.bold)).foregroundColor(.white)
                        Text("Mumbai, India").font(.system(size:15)).foregroundColor(.white.opacity(0.8))
                    }
                }
                .frame(maxWidth:.infinity).frame(height:520).padding(.horizontal,0).padding(.top,8)
                .cornerRadius(16)
                .padding(.horizontal, 10)

                Spacer()
                HStack(spacing: 12) {
                    HStack(spacing: 8) {
                        Circle().fill(Color.white.opacity(0.2)).frame(width:32,height:32)
                        Text("Reply to priya.designs...").font(.system(size:14)).foregroundColor(.white.opacity(0.8))
                        Spacer()
                    }
                    .padding(.horizontal,14).padding(.vertical,8)
                    .background(Color.white.opacity(0.15)).cornerRadius(24)
                    Image(systemName:"paperplane.fill").font(.system(size:20)).foregroundColor(.white)
                    Image(systemName:"heart").font(.system(size:22)).foregroundColor(.white)
                }.padding(.horizontal,12).padding(.bottom,40)
            }
        }.frame(width:393, height:852)
    }
}

// MARK: - Screen 3: Reels
struct SF_Reels: View {
    var body: some View {
        ZStack { Color.black.ignoresSafeArea()
            // Video bg
            LinearGradient(colors:[Color(hex:"1A1A2E"),Color(hex:"16213E"),Color(hex:"0F3460")],
                           startPoint:.top,endPoint:.bottom).ignoresSafeArea()
            Image(systemName:"play.fill").font(.system(size:40)).foregroundColor(.white.opacity(0.3))

            // Overlay
            VStack {
                HStack {
                    Text("Reels").font(.system(size:18,weight:.bold)).foregroundColor(.white)
                    Spacer()
                    Image(systemName:"camera").font(.system(size:20)).foregroundColor(.white)
                }
                .padding(.horizontal,16).padding(.top,54)
                Spacer()

                HStack(alignment:.bottom) {
                    // Caption + audio
                    VStack(alignment:.leading, spacing:8) {
                        HStack(spacing: 8) {
                            Circle().fill(Color.sfPurple.opacity(0.4)).frame(width:32,height:32)
                                .overlay(Text("D").font(.system(size:13,weight:.bold)).foregroundColor(.white))
                            Text("dev.codes").font(.system(size:14,weight:.semibold)).foregroundColor(.white)
                            Capsule().fill(Color.white.opacity(0.2)).frame(width:60,height:24)
                                .overlay(Text("Follow").font(.system(size:11,weight:.medium)).foregroundColor(.white))
                        }
                        Text("SwiftUI animations 🚀 #iOS #SwiftUI #developer")
                            .font(.system(size:13)).foregroundColor(.white).lineLimit(2)
                        HStack(spacing:6) {
                            Image(systemName:"music.note").font(.system(size:12)).foregroundColor(.white)
                            Text("Original Audio - dev.codes").font(.system(size:12)).foregroundColor(.white)
                        }
                    }
                    Spacer()
                    // Action buttons
                    VStack(spacing:20) {
                        VStack(spacing:4) {
                            Image(systemName:"heart.fill").font(.system(size:26)).foregroundColor(.white)
                            Text("48.2K").font(.system(size:12)).foregroundColor(.white)
                        }
                        VStack(spacing:4) {
                            Image(systemName:"bubble.right.fill").font(.system(size:24)).foregroundColor(.white)
                            Text("1,204").font(.system(size:12)).foregroundColor(.white)
                        }
                        VStack(spacing:4) {
                            Image(systemName:"paperplane.fill").font(.system(size:24)).foregroundColor(.white)
                            Text("Share").font(.system(size:12)).foregroundColor(.white)
                        }
                        VStack(spacing:4) {
                            Image(systemName:"ellipsis").font(.system(size:24)).foregroundColor(.white)
                        }
                        ZStack {
                            RoundedRectangle(cornerRadius:6).fill(Color.sfPurple.opacity(0.4)).frame(width:34,height:34)
                            Image(systemName:"music.note").font(.system(size:14)).foregroundColor(.white)
                        }
                    }
                }
                .padding(.horizontal,16).padding(.bottom,80)
            }
            VStack {
                Spacer()
                TabBar(icons:["house","magnifyingglass","plus.app","film","person.circle"],
                       labels:["Home","Search","Create","Reels","Profile"],
                       activeIndex:3, activeColor:.white,
                       background:Color.black.opacity(0.6))
            }
        }.frame(width:393, height:852)
    }
}

// MARK: - Screen 4: Explore
struct SF_Explore: View {
    let topics = ["Travel ✈️","Food 🍕","Fashion 👗","Tech 💻","Fitness 💪","Art 🎨"]
    let colors: [Color] = [.sfBlue,.sfOrange,.sfPink,.sfPurple,Color(hex:"2ECC71"),Color(hex:"F39C12")]
    var body: some View {
        ZStack { Color.sfBG.ignoresSafeArea()
            VStack(spacing: 0) {
                IOSStatusBar(dark: false)
                HStack(spacing: 12) {
                    HStack(spacing: 8) {
                        Image(systemName:"magnifyingglass").foregroundColor(.sfGray)
                        Text("Search").foregroundColor(.sfGray).font(.system(size:15))
                    }
                    .frame(maxWidth:.infinity).padding(.vertical,9)
                    .background(Color(hex:"EFEFEF")).cornerRadius(10)
                }.padding(.horizontal,14).padding(.bottom,10)

                ScrollView(.horizontal, showsIndicators:false) {
                    HStack(spacing: 8) {
                        ForEach(topics, id:\.self) { t in
                            Text(t).font(.system(size:13,weight:.medium))
                                .padding(.horizontal,14).padding(.vertical,7)
                                .background(Color(hex:"EFEFEF")).cornerRadius(20)
                        }
                    }.padding(.horizontal,14)
                }.padding(.bottom,8)

                ScrollView(showsIndicators:false) {
                    // Masonry-style grid
                    HStack(alignment:.top, spacing:2) {
                        // Left column
                        VStack(spacing:2) {
                            ForEach([300,180,240,160] as [CGFloat], id:\.self) { h in
                                Rectangle().fill(colors.randomElement()!.opacity(0.25)).frame(height:h)
                                    .overlay(Image(systemName:"photo").font(.system(size:24)).foregroundColor(colors.randomElement()!.opacity(0.5)))
                            }
                        }.frame(maxWidth:.infinity)
                        // Right column
                        VStack(spacing:2) {
                            ForEach([180,300,160,240] as [CGFloat], id:\.self) { h in
                                Rectangle().fill(colors.randomElement()!.opacity(0.25)).frame(height:h)
                                    .overlay(Image(systemName:"photo").font(.system(size:24)).foregroundColor(colors.randomElement()!.opacity(0.5)))
                            }
                        }.frame(maxWidth:.infinity)
                    }
                }

                TabBar(icons:["house","magnifyingglass","plus.app","film","person.circle"],
                       labels:["Home","Search","Create","Reels","Profile"],
                       activeIndex:1, activeColor:.black, background:.white)
            }
        }.frame(width:393, height:852)
    }
}

// MARK: - Screen 5: Post Detail
struct SF_PostDetail: View {
    var body: some View {
        ZStack { Color.sfBG.ignoresSafeArea()
            VStack(spacing: 0) {
                IOSStatusBar(dark: false)
                HStack {
                    Image(systemName:"chevron.left").font(.system(size:18,weight:.semibold)).foregroundColor(.black)
                    Spacer()
                    Text("Post").font(.system(size:16,weight:.semibold)).foregroundColor(.black)
                    Spacer()
                    Image(systemName:"ellipsis").font(.system(size:16)).foregroundColor(.black)
                }.padding(.horizontal,16).padding(.bottom,8)

                ScrollView(showsIndicators:false) {
                    VStack(alignment:.leading, spacing:0) {
                        HStack(spacing:10) {
                            Circle().fill(Color.sfPink.opacity(0.3)).frame(width:36,height:36)
                                .overlay(Text("P").font(.system(size:14,weight:.bold)).foregroundColor(.sfPink))
                            VStack(alignment:.leading,spacing:1) {
                                Text("priya.designs").font(.system(size:13,weight:.semibold)).foregroundColor(.black)
                                Text("Mumbai, India").font(.system(size:11)).foregroundColor(.sfGray)
                            }
                            Spacer()
                            Image(systemName:"ellipsis").foregroundColor(.black)
                        }.padding(.horizontal,14).padding(.vertical,8)

                        Rectangle().fill(LinearGradient(colors:[Color(hex:"FF6B35"),Color(hex:"F7C59F")],startPoint:.top,endPoint:.bottom))
                            .frame(maxWidth:.infinity).frame(height:340)
                            .overlay(Image(systemName:"sun.max.fill").font(.system(size:60)).foregroundColor(.white.opacity(0.6)))

                        HStack(spacing:16) {
                            Image(systemName:"heart.fill").font(.system(size:24)).foregroundColor(.sfPink)
                            Image(systemName:"bubble.right").font(.system(size:22)).foregroundColor(.black)
                            Image(systemName:"paperplane").font(.system(size:22)).foregroundColor(.black)
                            Spacer()
                            Image(systemName:"bookmark").font(.system(size:22)).foregroundColor(.black)
                        }.padding(.horizontal,14).padding(.vertical,10)

                        Text("4,821 likes").font(.system(size:13,weight:.semibold)).foregroundColor(.black).padding(.horizontal,14)
                        Text("✨ Golden hour never disappoints 🌇 #photography #mumbai #sunset").font(.system(size:13)).foregroundColor(.black).padding(.horizontal,14).padding(.top,2)

                        Divider().padding(.vertical, 10)
                        ForEach([("alex.photo","Stunning composition! 📸",Color.sfBlue),
                                 ("rohit.t","This is gorgeous 🌟",Color.sfPurple),
                                 ("sara_k","Where exactly in Mumbai?",Color.sfOrange)],id:\.0) { c in
                            HStack(alignment:.top,spacing:10) {
                                Circle().fill(c.2.opacity(0.3)).frame(width:30,height:30)
                                    .overlay(Text(String(c.0.prefix(1))).font(.system(size:11,weight:.bold)).foregroundColor(c.2))
                                VStack(alignment:.leading,spacing:2) {
                                    Text(c.0).font(.system(size:12,weight:.semibold)).foregroundColor(.black)
                                    Text(c.1).font(.system(size:13)).foregroundColor(.black)
                                }
                                Spacer()
                                Image(systemName:"heart").font(.system(size:12)).foregroundColor(.sfGray)
                            }.padding(.horizontal,14).padding(.vertical,6)
                        }
                    }
                }

                HStack(spacing:10) {
                    Circle().fill(Color.sfBlue.opacity(0.2)).frame(width:30,height:30)
                        .overlay(Text("A").font(.system(size:11,weight:.bold)).foregroundColor(.sfBlue))
                    Text("Add a comment...").font(.system(size:13)).foregroundColor(.sfGray)
                    Spacer()
                    Image(systemName:"paperplane.fill").foregroundColor(.sfPink)
                }.padding(.horizontal,14).padding(.vertical,10)
                .background(Color.sfBG)
                .overlay(Divider(),alignment:.top)
            }
        }.frame(width:393, height:852)
    }
}

// MARK: - Screen 6: Profile
struct SF_Profile: View {
    var body: some View {
        ZStack { Color.sfBG.ignoresSafeArea()
            VStack(spacing: 0) {
                IOSStatusBar(dark: false)
                HStack {
                    Image(systemName:"chevron.left").font(.system(size:18,weight:.semibold)).foregroundColor(.black)
                    Spacer()
                    Text("ajay.ios").font(.system(size:16,weight:.semibold)).foregroundColor(.black)
                    Spacer()
                    Image(systemName:"line.3.horizontal").font(.system(size:20)).foregroundColor(.black)
                }.padding(.horizontal,16).padding(.bottom,12)

                VStack(spacing: 12) {
                    HStack(spacing: 20) {
                        ZStack {
                            Circle().fill(sfGradient).frame(width:86,height:86)
                            Circle().fill(Color.sfBG).frame(width:80,height:80)
                            Circle().fill(Color.sfBlue.opacity(0.2)).frame(width:76,height:76)
                                .overlay(Text("AJ").font(.system(size:26,weight:.bold)).foregroundColor(.sfBlue))
                        }
                        ForEach([("284","Posts"),("14.2K","Followers"),("312","Following")],id:\.0) { s in
                            VStack(spacing:4) {
                                Text(s.0).font(.system(size:18,weight:.bold)).foregroundColor(.black)
                                Text(s.1).font(.system(size:12)).foregroundColor(.sfGray)
                            }.frame(maxWidth:.infinity)
                        }
                    }.padding(.horizontal,16)

                    VStack(alignment:.leading,spacing:3) {
                        Text("Ajay Girolkar").font(.system(size:14,weight:.semibold)).foregroundColor(.black)
                        Text("📱 Senior iOS Developer").font(.system(size:13)).foregroundColor(.black)
                        Text("Swift • SwiftUI • UIKit").font(.system(size:13)).foregroundColor(.black)
                        Text("ajaygirolkar.dev").font(.system(size:13)).foregroundColor(.sfBlue)
                    }.frame(maxWidth:.infinity,alignment:.leading).padding(.horizontal,16)

                    HStack(spacing:8) {
                        Text("Edit Profile").font(.system(size:13,weight:.semibold)).foregroundColor(.black)
                            .frame(maxWidth:.infinity).padding(.vertical,7)
                            .background(Color(hex:"EFEFEF")).cornerRadius(8)
                        Text("Share Profile").font(.system(size:13,weight:.semibold)).foregroundColor(.black)
                            .frame(maxWidth:.infinity).padding(.vertical,7)
                            .background(Color(hex:"EFEFEF")).cornerRadius(8)
                        Image(systemName:"person.badge.plus").font(.system(size:14)).foregroundColor(.black)
                            .padding(.vertical,7).padding(.horizontal,12)
                            .background(Color(hex:"EFEFEF")).cornerRadius(8)
                    }.padding(.horizontal,16)
                }.padding(.bottom,8)

                Divider()
                // Grid
                LazyVGrid(columns:[GridItem(.flexible()),GridItem(.flexible()),GridItem(.flexible())],spacing:2) {
                    ForEach(0..<12, id:\.self) { i in
                        let colors: [Color] = [.sfPink,.sfBlue,.sfPurple,.sfOrange,Color(hex:"2ECC71"),Color(hex:"F39C12")]
                        Rectangle().fill(colors[i%colors.count].opacity(0.2))
                            .frame(height:130)
                            .overlay(Image(systemName:"photo").font(.system(size:22)).foregroundColor(colors[i%colors.count].opacity(0.5)))
                    }
                }

                TabBar(icons:["house","magnifyingglass","plus.app","film","person.circle"],
                       labels:["Home","Search","Create","Reels","Profile"],
                       activeIndex:4, activeColor:.black, background:.white)
            }
        }.frame(width:393, height:852)
    }
}

#Preview("1 Feed")        { SF_Feed() }
#Preview("2 Stories")     { SF_Stories() }
#Preview("3 Reels")       { SF_Reels() }
#Preview("4 Explore")     { SF_Explore() }
#Preview("5 Post Detail") { SF_PostDetail() }
#Preview("6 Profile")     { SF_Profile() }
