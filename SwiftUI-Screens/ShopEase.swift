import SwiftUI

// ─────────────────────────────────────────────────────────────────
//  SHOPEASY — E-Commerce App (Amazon / Meesho style)
//  6 screens, vibrant orange + white
// ─────────────────────────────────────────────────────────────────

private extension Color {
    static let seBG     = Color.white
    static let seOrange = Color(hex: "FF6200")
    static let seCard   = Color(hex: "F5F5F5")
    static let seGray   = Color(hex: "757575")
    static let seGreen  = Color(hex: "2ECC71")
    static let seLine   = Color(hex: "E0E0E0")
}

// MARK: - Product Card
private struct ProductCard: View {
    var icon: String; var color: Color; var name: String; var price: String; var originalPrice: String; var rating: String
    var body: some View {
        VStack(alignment:.leading,spacing:0) {
            ZStack {
                RoundedRectangle(cornerRadius:0).fill(color.opacity(0.1)).frame(height:160)
                Image(systemName:icon).font(.system(size:40)).foregroundColor(color.opacity(0.5))
                VStack { HStack { Spacer()
                    Text("20% OFF").font(.system(size:10,weight:.bold)).foregroundColor(.white)
                        .padding(.horizontal,7).padding(.vertical,3).background(Color.seOrange)
                    }.padding(.top,8).padding(.trailing,8)
                    Spacer() }
            }
            VStack(alignment:.leading,spacing:4) {
                Text(name).font(.system(size:13,weight:.medium)).foregroundColor(.black).lineLimit(2).padding(.horizontal,8).padding(.top,8)
                HStack(spacing:4) {
                    HStack(spacing:2) {
                        Image(systemName:"star.fill").font(.system(size:10)).foregroundColor(Color(hex:"FF9500"))
                        Text(rating).font(.system(size:11,weight:.semibold)).foregroundColor(.black)
                    }
                    Text("(2.4k)").font(.system(size:10)).foregroundColor(.seGray)
                }.padding(.horizontal,8)
                HStack(alignment:.firstTextBaseline,spacing:4) {
                    Text(price).font(.system(size:15,weight:.bold)).foregroundColor(.black)
                    Text(originalPrice).font(.system(size:12)).foregroundColor(.seGray).strikethrough()
                }.padding(.horizontal,8).padding(.bottom,8)
            }
        }.background(Color.white).cornerRadius(8).shadow(color:.black.opacity(0.06),radius:4,x:0,y:2)
    }
}

// MARK: - Screen 1: Home
struct SE_Home: View {
    let categories: [(String,String,Color)] = [
        ("Electronics","laptopcomputer",Color(hex:"3498DB")),
        ("Fashion","tshirt",Color(hex:"E74C3C")),
        ("Grocery","basket",Color(hex:"27AE60")),
        ("Beauty","sparkles",Color(hex:"9B59B6")),
        ("Sports","figure.run",Color(hex:"F39C12")),
        ("Home","house",Color(hex:"16A085")),
    ]
    var body: some View {
        ZStack { Color.seCard.ignoresSafeArea()
            VStack(spacing:0) {
                // Orange header
                VStack(spacing:0) {
                    IOSStatusBar(dark:false)
                    HStack(spacing:10) {
                        HStack(spacing:8) {
                            Image(systemName:"magnifyingglass").foregroundColor(.seGray)
                            Text("Search products...").foregroundColor(.seGray).font(.system(size:14))
                            Spacer()
                            Image(systemName:"mic.fill").foregroundColor(.seOrange)
                        }.padding(10).background(Color.white).cornerRadius(8)
                        Image(systemName:"cart.badge.plus").font(.system(size:20)).foregroundColor(.black)
                    }.padding(.horizontal,14).padding(.bottom,10)
                }.background(LinearGradient(colors:[Color(hex:"FF8C00"),Color(hex:"FF6200")],startPoint:.top,endPoint:.bottom))

                ScrollView(showsIndicators:false) {
                    VStack(spacing:12) {
                        // Banner
                        ZStack {
                            LinearGradient(colors:[Color(hex:"667EEA"),Color(hex:"764BA2")],startPoint:.topLeading,endPoint:.bottomTrailing)
                                .cornerRadius(12)
                            HStack {
                                VStack(alignment:.leading,spacing:6) {
                                    Text("MEGA SALE").font(.system(size:11,weight:.bold)).foregroundColor(.white.opacity(0.8)).kerning(2)
                                    Text("Up to 70% OFF").font(.system(size:22,weight:.bold)).foregroundColor(.white)
                                    Text("Shop Now →").font(.system(size:13,weight:.semibold)).foregroundColor(.white)
                                        .padding(.horizontal,14).padding(.vertical,7).background(Color.white.opacity(0.2)).cornerRadius(20)
                                }.padding(18)
                                Spacer()
                                Image(systemName:"bag.fill").font(.system(size:54)).foregroundColor(.white.opacity(0.3)).padding(.trailing,18)
                            }
                        }.frame(height:130).padding(.horizontal,14)

                        // Categories
                        VStack(alignment:.leading,spacing:10) {
                            Text("Shop by Category").font(.system(size:16,weight:.bold)).foregroundColor(.black).padding(.horizontal,14)
                            ScrollView(.horizontal,showsIndicators:false) {
                                HStack(spacing:16) {
                                    ForEach(categories,id:\.0) { cat in
                                        VStack(spacing:6) {
                                            ZStack { Circle().fill(cat.2.opacity(0.15)).frame(width:56,height:56)
                                                Image(systemName:cat.1).font(.system(size:22)).foregroundColor(cat.2) }
                                            Text(cat.0).font(.system(size:11)).foregroundColor(.black)
                                        }
                                    }
                                }.padding(.horizontal,14)
                            }
                        }

                        // Products
                        VStack(alignment:.leading,spacing:10) {
                            Text("Today's Deals").font(.system(size:16,weight:.bold)).foregroundColor(.black).padding(.horizontal,14)
                            LazyVGrid(columns:[GridItem(.flexible()),GridItem(.flexible())],spacing:10) {
                                ProductCard(icon:"laptopcomputer",color:Color(hex:"3498DB"),name:"Wireless Earbuds Pro",price:"₹1,299",originalPrice:"₹2,499",rating:"4.4")
                                ProductCard(icon:"tshirt",color:Color(hex:"E74C3C"),name:"Premium Cotton T-Shirt",price:"₹499",originalPrice:"₹999",rating:"4.2")
                                ProductCard(icon:"sparkles",color:Color(hex:"9B59B6"),name:"Face Serum Glow Kit",price:"₹849",originalPrice:"₹1,500",rating:"4.6")
                                ProductCard(icon:"figure.run",color:Color(hex:"F39C12"),name:"Running Shoes Lite",price:"₹1,799",originalPrice:"₹3,500",rating:"4.3")
                            }.padding(.horizontal,14)
                        }
                    }.padding(.vertical,10)
                }
                TabBar(icons:["house.fill","magnifyingglass","heart","bag","person.circle"],
                       labels:["Home","Search","Wishlist","Cart","Profile"],
                       activeIndex:0,activeColor:.seOrange,background:.white)
            }
        }.frame(width:393,height:852)
    }
}

// MARK: - Screen 2: Product Listing
struct SE_Listing: View {
    let products: [(String,Color,String,String,String,String)] = [
        ("laptopcomputer",Color(hex:"3498DB"),"Wireless Earbuds Pro Max","₹1,299","₹2,499","4.4"),
        ("tshirt",Color(hex:"E74C3C"),"Classic Cotton Polo Shirt","₹599","₹1,200","4.1"),
        ("sparkles",Color(hex:"9B59B6"),"Vitamin C Glow Face Serum","₹849","₹1,500","4.6"),
        ("figure.run",Color(hex:"F39C12"),"CloudStep Running Shoes","₹1,799","₹3,500","4.3"),
        ("iphone",Color(hex:"2C3E50"),"Phone Stand Adjustable","₹299","₹699","4.5"),
        ("house",Color(hex:"16A085"),"Smart LED Strip Lights","₹649","₹1,299","4.7"),
    ]
    var body: some View {
        ZStack { Color.seCard.ignoresSafeArea()
            VStack(spacing:0) {
                VStack(spacing:8) {
                    IOSStatusBar(dark:false)
                    HStack(spacing:10) {
                        HStack(spacing:8) {
                            Image(systemName:"magnifyingglass").foregroundColor(.seGray)
                            Text("Earbuds").font(.system(size:14,weight:.medium)).foregroundColor(.black)
                            Spacer()
                            Image(systemName:"xmark").foregroundColor(.seGray)
                        }.padding(10).background(Color.white).cornerRadius(8)
                    }.padding(.horizontal,14)
                    ScrollView(.horizontal,showsIndicators:false) {
                        HStack(spacing:8) {
                            ForEach(["All","Under ₹1K","4★ & above","Prime","New Arrivals"],id:\.self) { f in
                                Text(f).font(.system(size:12,weight:.medium))
                                    .foregroundColor(f=="All" ? .white : .seOrange)
                                    .padding(.horizontal,14).padding(.vertical,7)
                                    .background(f=="All" ? Color.seOrange : Color.white)
                                    .overlay(RoundedRectangle(cornerRadius:20).stroke(f=="All" ? Color.clear : Color.seOrange,lineWidth:1))
                                    .cornerRadius(20)
                            }
                        }.padding(.horizontal,14)
                    }.padding(.bottom,8)
                }.background(Color.white)

                ScrollView(showsIndicators:false) {
                    LazyVGrid(columns:[GridItem(.flexible()),GridItem(.flexible())],spacing:10) {
                        ForEach(products,id:\.2) { p in
                            ProductCard(icon:p.0,color:p.1,name:p.2,price:p.3,originalPrice:p.4,rating:p.5)
                        }
                    }.padding(14)
                }
                TabBar(icons:["house.fill","magnifyingglass","heart","bag","person.circle"],
                       labels:["Home","Search","Wishlist","Cart","Profile"],
                       activeIndex:1,activeColor:.seOrange,background:.white)
            }
        }.frame(width:393,height:852)
    }
}

// MARK: - Screen 3: Product Detail
struct SE_Detail: View {
    var body: some View {
        ZStack { Color.seBG.ignoresSafeArea()
            VStack(spacing:0) {
                IOSStatusBar(dark:false)
                HStack {
                    Image(systemName:"chevron.left").font(.system(size:17,weight:.semibold)).foregroundColor(.black)
                    Spacer()
                    Image(systemName:"magnifyingglass").font(.system(size:18)).foregroundColor(.black)
                    Image(systemName:"heart").font(.system(size:18)).foregroundColor(.black).padding(.leading,16)
                    Image(systemName:"bag").font(.system(size:18)).foregroundColor(.black).padding(.leading,16)
                }.padding(.horizontal,16).padding(.bottom,8)

                ScrollView(showsIndicators:false) {
                    VStack(alignment:.leading,spacing:0) {
                        ZStack {
                            Color(hex:"3498DB").opacity(0.08).frame(height:280)
                            Image(systemName:"laptopcomputer").font(.system(size:80)).foregroundColor(Color(hex:"3498DB").opacity(0.6))
                            VStack { HStack { Spacer()
                                Image(systemName:"heart").font(.system(size:22)).foregroundColor(.seGray).padding(12)
                            }.padding(.top,8); Spacer() }
                        }

                        HStack(spacing:8) {
                            ForEach(0..<4,id:\.self) { i in
                                RoundedRectangle(cornerRadius:6).fill(Color(hex:"3498DB").opacity(0.1)).frame(width:60,height:60)
                                    .overlay(Image(systemName:"laptopcomputer").font(.system(size:22)).foregroundColor(Color(hex:"3498DB").opacity(0.5)))
                                    .overlay(RoundedRectangle(cornerRadius:6).stroke(i==0 ? Color.seOrange : Color.seLine,lineWidth:1.5))
                            }
                        }.padding(.horizontal,16).padding(.top,12)

                        VStack(alignment:.leading,spacing:8) {
                            Text("Wireless Earbuds Pro Max").font(.system(size:18,weight:.semibold)).foregroundColor(.black)
                            HStack(spacing:6) {
                                HStack(spacing:3) {
                                    ForEach(0..<4,id:\.self) { _ in Image(systemName:"star.fill").font(.system(size:12)).foregroundColor(Color(hex:"FF9500")) }
                                    Image(systemName:"star.leadinghalf.filled").font(.system(size:12)).foregroundColor(Color(hex:"FF9500"))
                                }
                                Text("4.4").font(.system(size:13,weight:.semibold)).foregroundColor(.black)
                                Text("(2,418 ratings)").font(.system(size:12)).foregroundColor(.seGray)
                            }
                            HStack(alignment:.firstTextBaseline,spacing:8) {
                                Text("₹1,299").font(.system(size:24,weight:.bold)).foregroundColor(.black)
                                Text("₹2,499").font(.system(size:15)).foregroundColor(.seGray).strikethrough()
                                Text("48% off").font(.system(size:13,weight:.semibold)).foregroundColor(Color(hex:"B12704"))
                            }
                            HStack {
                                Image(systemName:"checkmark.circle.fill").foregroundColor(.seGreen).font(.system(size:14))
                                Text("In Stock").font(.system(size:13,weight:.medium)).foregroundColor(.seGreen)
                                Text("· Free delivery by Tomorrow").font(.system(size:13)).foregroundColor(.seGray)
                            }
                        }.padding(.horizontal,16).padding(.vertical,12)

                        Divider().padding(.horizontal,16)
                        Text("Select Variant").font(.system(size:14,weight:.semibold)).foregroundColor(.black).padding(.horizontal,16).padding(.vertical,10)
                        HStack(spacing:10) {
                            ForEach(["Black","White","Navy"],id:\.self) { c in
                                Text(c).font(.system(size:13))
                                    .foregroundColor(c == "Black" ? .white : .black)
                                    .padding(.horizontal,18).padding(.vertical,8)
                                    .background(c == "Black" ? Color.black : Color.seLine)
                                    .cornerRadius(20)
                            }
                        }.padding(.horizontal,16).padding(.bottom,16)
                    }
                }

                HStack(spacing:10) {
                    Text("Add to Cart").font(.system(size:15,weight:.semibold)).foregroundColor(.seOrange)
                        .frame(maxWidth:.infinity).padding(.vertical,14)
                        .background(Color.seOrange.opacity(0.1))
                        .overlay(RoundedRectangle(cornerRadius:8).stroke(Color.seOrange,lineWidth:1.5))
                        .cornerRadius(8)
                    Text("Buy Now").font(.system(size:15,weight:.bold)).foregroundColor(.white)
                        .frame(maxWidth:.infinity).padding(.vertical,14)
                        .background(Color.seOrange).cornerRadius(8)
                }.padding(.horizontal,16).padding(.vertical,12)
                .background(Color.white).shadow(color:.black.opacity(0.06),radius:8,x:0,y:-4)
            }
        }.frame(width:393,height:852)
    }
}

// MARK: - Screen 4: Cart
struct SE_Cart: View {
    var body: some View {
        ZStack { Color.seCard.ignoresSafeArea()
            VStack(spacing:0) {
                VStack {
                    IOSStatusBar(dark:false)
                    Text("Cart (3 items)").font(.system(size:20,weight:.bold)).foregroundColor(.black)
                        .frame(maxWidth:.infinity,alignment:.leading).padding(.horizontal,16)
                }.background(Color.white).padding(.bottom,10)

                ScrollView(showsIndicators:false) {
                    VStack(spacing:10) {
                        ForEach([
                            ("laptopcomputer",Color(hex:"3498DB"),"Wireless Earbuds Pro Max","Black","₹1,299"),
                            ("tshirt",Color(hex:"E74C3C"),"Classic Cotton Polo","L / Navy","₹599"),
                            ("sparkles",Color(hex:"9B59B6"),"Vitamin C Face Serum","50ml","₹849"),
                        ],id:\.2) { item in
                            HStack(alignment:.top,spacing:12) {
                                RoundedRectangle(cornerRadius:8).fill(item.1.opacity(0.1)).frame(width:80,height:80)
                                    .overlay(Image(systemName:item.0).font(.system(size:30)).foregroundColor(item.1.opacity(0.6)))
                                VStack(alignment:.leading,spacing:6) {
                                    Text(item.2).font(.system(size:14,weight:.medium)).foregroundColor(.black).lineLimit(2)
                                    Text(item.3).font(.system(size:12)).foregroundColor(.seGray)
                                    HStack(spacing:12) {
                                        HStack(spacing:0) {
                                            ForEach(["-","1","+"],id:\.self) { btn in
                                                Text(btn).font(.system(size:15,weight: btn=="1" ? .regular : .bold))
                                                    .foregroundColor(btn=="1" ? .black : .seOrange)
                                                    .frame(width:30,height:28)
                                            }
                                        }
                                        .overlay(RoundedRectangle(cornerRadius:4).stroke(Color.seLine,lineWidth:1))
                                        Text(item.4).font(.system(size:15,weight:.bold)).foregroundColor(.black)
                                    }
                                    HStack(spacing:16) {
                                        Button(action:{}) { Text("Remove").font(.system(size:12)).foregroundColor(.seGray) }
                                        Button(action:{}) { Text("Save for Later").font(.system(size:12)).foregroundColor(.seOrange) }
                                    }
                                }
                            }.padding(12).background(Color.white).cornerRadius(8)
                        }.padding(.horizontal,14)

                        // Promo
                        HStack(spacing:10) {
                            Image(systemName:"tag.fill").foregroundColor(.seOrange)
                            Text("Apply coupon code").font(.system(size:14)).foregroundColor(.seGray)
                            Spacer()
                            Image(systemName:"chevron.right").font(.system(size:13)).foregroundColor(.seGray)
                        }.padding(14).background(Color.white).cornerRadius(8).padding(.horizontal,14)

                        // Summary
                        VStack(spacing:0) {
                            Text("Price Details").font(.system(size:16,weight:.bold)).foregroundColor(.black)
                                .frame(maxWidth:.infinity,alignment:.leading).padding(14)
                            ForEach([("Price (3 items)","₹2,747"),("Discount","−₹648"),("Delivery","Free")],id:\.0) { r in
                                HStack {
                                    Text(r.0).font(.system(size:14)).foregroundColor(r.0=="Discount" ? Color(hex:"B12704") : .black)
                                    Spacer()
                                    Text(r.1).font(.system(size:14)).foregroundColor(r.0=="Discount" ? Color(hex:"B12704") : .black)
                                }.padding(.horizontal,14).padding(.vertical,6)
                            }
                            Divider().padding(.horizontal,14)
                            HStack {
                                Text("Total Amount").font(.system(size:15,weight:.bold)).foregroundColor(.black)
                                Spacer()
                                Text("₹2,099").font(.system(size:15,weight:.bold)).foregroundColor(.black)
                            }.padding(14)
                        }.background(Color.white).cornerRadius(8).padding(.horizontal,14)
                    }.padding(.vertical,4)
                }

                VStack(spacing:0) {
                    Divider()
                    HStack {
                        VStack(alignment:.leading,spacing:2) {
                            Text("₹2,099").font(.system(size:18,weight:.bold)).foregroundColor(.black)
                            Text("You save ₹648").font(.system(size:12)).foregroundColor(Color(hex:"B12704"))
                        }
                        Spacer()
                        Text("Proceed to Checkout").font(.system(size:15,weight:.bold)).foregroundColor(.white)
                            .padding(.horizontal,20).padding(.vertical,12).background(Color.seOrange).cornerRadius(8)
                    }.padding(.horizontal,16).padding(.vertical,12).background(Color.white)
                }
            }
        }.frame(width:393,height:852)
    }
}

// MARK: - Screen 5: Checkout
struct SE_Checkout: View {
    var body: some View {
        ZStack { Color.seCard.ignoresSafeArea()
            VStack(spacing:0) {
                VStack(spacing:10) {
                    IOSStatusBar(dark:false)
                    HStack {
                        Image(systemName:"chevron.left").font(.system(size:17,weight:.semibold)).foregroundColor(.black)
                        Text("Checkout").font(.system(size:18,weight:.semibold)).foregroundColor(.black)
                        Spacer()
                    }.padding(.horizontal,16)
                    HStack(spacing:0) {
                        ForEach(["Address","Payment","Review"],id:\.self) { step in
                            Text(step).font(.system(size:12,weight: step == "Payment" ? .bold : .regular))
                                .foregroundColor(step == "Payment" ? .white : Color(step == "Address" ? .seGreen : .seGray))
                                .frame(maxWidth:.infinity).padding(.vertical,8)
                                .background(step == "Payment" ? Color.seOrange : Color.clear)
                        }
                    }.background(Color.seLine).cornerRadius(8).padding(.horizontal,16).padding(.bottom,8)
                }.background(Color.white)

                ScrollView(showsIndicators:false) {
                    VStack(spacing:10) {
                        // Address
                        VStack(alignment:.leading,spacing:8) {
                            HStack {
                                Text("Deliver to").font(.system(size:15,weight:.bold)).foregroundColor(.black)
                                Spacer()
                                Text("Change").font(.system(size:13)).foregroundColor(.seOrange)
                            }
                            HStack(alignment:.top,spacing:10) {
                                Image(systemName:"location.fill").foregroundColor(.seOrange)
                                VStack(alignment:.leading,spacing:2) {
                                    Text("Ajay Girolkar  •  Home").font(.system(size:14,weight:.medium)).foregroundColor(.black)
                                    Text("123, Palm Grove Society, Bandra West, Mumbai 400050").font(.system(size:13)).foregroundColor(.seGray)
                                }
                            }
                        }.padding(14).background(Color.white).cornerRadius(8).padding(.horizontal,14)

                        // Payment methods
                        VStack(alignment:.leading,spacing:10) {
                            Text("Select Payment").font(.system(size:15,weight:.bold)).foregroundColor(.black).padding(.horizontal,14)
                            ForEach([
                                ("creditcard","UPI / Net Banking","Pay via UPI or Bank","checkmark.circle.fill"),
                                ("creditcard.fill","Credit / Debit Card","Visa, Mastercard, RuPay","circle"),
                                ("wallet.pass","ShopEase Wallet","Balance: ₹240","circle"),
                                ("bag","Cash on Delivery","Available","circle"),
                            ],id:\.0) { pm in
                                HStack(spacing:14) {
                                    Image(systemName:pm.0).font(.system(size:18)).foregroundColor(.seOrange).frame(width:26)
                                    VStack(alignment:.leading,spacing:2) {
                                        Text(pm.1).font(.system(size:14,weight:.medium)).foregroundColor(.black)
                                        Text(pm.2).font(.system(size:12)).foregroundColor(.seGray)
                                    }
                                    Spacer()
                                    Image(systemName:pm.3).font(.system(size:20))
                                        .foregroundColor(pm.3.contains("fill") ? .seOrange : .seLine)
                                }.padding(14).background(Color.white).cornerRadius(8)
                                .overlay(RoundedRectangle(cornerRadius:8).stroke(pm.3.contains("fill") ? Color.seOrange : Color.clear, lineWidth:1.5))
                                .padding(.horizontal,14)
                            }
                        }

                        // Summary
                        HStack {
                            Text("Total: ₹2,099").font(.system(size:15,weight:.bold)).foregroundColor(.black)
                            Spacer()
                            Text("(3 items)").font(.system(size:13)).foregroundColor(.seGray)
                        }.padding(14).background(Color.white).cornerRadius(8).padding(.horizontal,14)
                    }.padding(.vertical,10)
                }

                Button(action:{}) {
                    Text("Place Order • ₹2,099").font(.system(size:16,weight:.bold)).foregroundColor(.white)
                        .frame(maxWidth:.infinity).padding(.vertical,15)
                        .background(Color.seOrange).cornerRadius(8)
                }.padding(.horizontal,16).padding(.vertical,12).background(Color.white)
                .shadow(color:.black.opacity(0.06),radius:8,x:0,y:-4)
            }
        }.frame(width:393,height:852)
    }
}

// MARK: - Screen 6: Order Tracking
struct SE_Tracking: View {
    let steps: [(String,String,Bool,String)] = [
        ("Order Placed","Dec 18, 10:45 AM",true,"checkmark.circle.fill"),
        ("Order Confirmed","Dec 18, 11:02 AM",true,"checkmark.circle.fill"),
        ("Shipped","Dec 18, 3:30 PM — On the way",true,"shippingbox.fill"),
        ("Out for Delivery","Expected Today by 8 PM",false,"scooter"),
        ("Delivered","Expected Today",false,"house.fill"),
    ]
    var body: some View {
        ZStack { Color.seCard.ignoresSafeArea()
            VStack(spacing:0) {
                VStack(spacing:8) {
                    IOSStatusBar(dark:false)
                    HStack {
                        Image(systemName:"chevron.left").font(.system(size:17,weight:.semibold)).foregroundColor(.black)
                        Text("Track Order").font(.system(size:18,weight:.semibold)).foregroundColor(.black)
                        Spacer()
                        Text("Help").font(.system(size:15)).foregroundColor(.seOrange)
                    }.padding(.horizontal,16)
                }.background(Color.white).padding(.bottom,10)

                ScrollView(showsIndicators:false) {
                    VStack(spacing:10) {
                        // ETA card
                        HStack(spacing:14) {
                            Image(systemName:"clock.fill").font(.system(size:26)).foregroundColor(.seOrange)
                            VStack(alignment:.leading,spacing:4) {
                                Text("Expected Delivery").font(.system(size:12)).foregroundColor(.seGray)
                                Text("Today by 8:00 PM").font(.system(size:18,weight:.bold)).foregroundColor(.black)
                                Text("Shipped via BlueDart · DL2834901").font(.system(size:12)).foregroundColor(.seGray)
                            }
                            Spacer()
                        }.padding(16).background(Color.white).cornerRadius(12).padding(.horizontal,14)

                        // Items
                        VStack(alignment:.leading,spacing:10) {
                            Text("3 items in this shipment").font(.system(size:14,weight:.semibold)).foregroundColor(.black)
                            ScrollView(.horizontal,showsIndicators:false) {
                                HStack(spacing:10) {
                                    ForEach([("laptopcomputer",Color(hex:"3498DB")),("tshirt",Color(hex:"E74C3C")),("sparkles",Color(hex:"9B59B6"))],id:\.0) { item in
                                        RoundedRectangle(cornerRadius:8).fill(item.1.opacity(0.1)).frame(width:60,height:60)
                                            .overlay(Image(systemName:item.0).font(.system(size:22)).foregroundColor(item.1.opacity(0.6)))
                                    }
                                }.padding(.horizontal,16)
                            }
                        }.padding(.vertical,14).background(Color.white).cornerRadius(12).padding(.horizontal,14)

                        // Timeline
                        VStack(alignment:.leading,spacing:0) {
                            Text("Order Timeline").font(.system(size:15,weight:.bold)).foregroundColor(.black).padding(.horizontal,16).padding(.top,14).padding(.bottom,8)
                            ForEach(Array(steps.enumerated()),id:\.offset) { idx, step in
                                HStack(alignment:.top,spacing:14) {
                                    VStack(spacing:0) {
                                        Image(systemName:step.2 ? step.3 : "circle").font(.system(size:22))
                                            .foregroundColor(step.2 ? .seOrange : idx == 3 ? .seOrange : Color.seLine)
                                        if idx < steps.count-1 {
                                            Rectangle().fill(step.2 ? Color.seOrange : Color.seLine).frame(width:2).frame(minHeight:30)
                                        }
                                    }.frame(width:30)
                                    VStack(alignment:.leading,spacing:4) {
                                        Text(step.0).font(.system(size:14,weight: step.2 || idx==3 ? .semibold : .regular))
                                            .foregroundColor(step.2 || idx==3 ? .black : .seGray)
                                        Text(step.1).font(.system(size:12)).foregroundColor(.seGray)
                                    }.padding(.bottom,16)
                                }.padding(.horizontal,16)
                            }
                        }.background(Color.white).cornerRadius(12).padding(.horizontal,14).padding(.bottom,10)
                    }.padding(.vertical,4)
                }
            }
        }.frame(width:393,height:852)
    }
}

#Preview("1 Home")     { SE_Home() }
#Preview("2 Listing")  { SE_Listing() }
#Preview("3 Detail")   { SE_Detail() }
#Preview("4 Cart")     { SE_Cart() }
#Preview("5 Checkout") { SE_Checkout() }
#Preview("6 Tracking") { SE_Tracking() }
