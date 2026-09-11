"""
Content data for the /<service>-company-<location> location pages
(see aligarh-onsite-seo.md). One dict entry per URL slug — each entry
carries its own intro, FAQ, and framing so pages don't read as a single
template with the city name swapped (the checklist explicitly warns
against that pattern, and Google treats it as near-duplicate content).

Nexa Solutions' Aligarh office is founder-led and genuinely local; the
nearby-town pages are framed honestly as served *from* that Aligarh
office rather than claiming a separate local presence in each town.
"""

SERVICES = {
    "web-development": {
        "label": "Web Development Company",
        "short": "web development",
        "image": "images/services/web-dev.webp",
        "route_name": "web_development",
        "breakdown": [
            (
                "Custom Websites & Web Apps",
                "From business websites to e-commerce stores and custom web applications, "
                "we design and build sites that load fast, work properly on mobile, and are "
                "actually built to bring in enquiries, not just look good in a screenshot.",
            ),
            (
                "Our Process",
                "We start by understanding your business and customers, then design and build "
                "in stages you can see and approve, and hand over a site you can actually "
                "manage, not one that locks you into us for every small change.",
            ),
            (
                "Technology We Use",
                "WordPress and Shopify for businesses that want to manage content themselves, "
                "or a fully custom build in React, Next.js, or Python/Flask when the project "
                "needs more than a template can offer.",
            ),
        ],
    },
    "software-development": {
        "label": "Software Development Company",
        "short": "software development",
        "image": "images/services/software-development.webp",
        "route_name": "software_development_company",
        "breakdown": [
            (
                "Custom Business Software",
                "Inventory systems, billing and invoicing tools, internal dashboards, and "
                "workflow software built around how your business actually operates, not a "
                "generic package you have to bend your process around.",
            ),
            (
                "Our Process",
                "We map out what the software actually needs to do before we design anything, "
                "build it in stages so you can see progress, and document it properly so it's "
                "not a black box only we can maintain.",
            ),
            (
                "Technology We Use",
                "Python, Flask, and PostgreSQL for reliable backend systems, with clean "
                "dashboards built in React where your team needs to see and manage data.",
            ),
        ],
    },
    "app-development": {
        "label": "App Development Company",
        "short": "app development",
        "image": "images/stock/photo-1512941937669-90a1b58e7e9c.webp",
        "route_name": "app_development",
        "breakdown": [
            (
                "Android, iOS & Cross-Platform Apps",
                "Customer-facing apps, staff/delivery apps, and internal business apps, built "
                "for Android, iOS, or both, depending on where your actual customers are.",
            ),
            (
                "Our Process",
                "We start with what the app needs to do for your business and your users, "
                "design the screens first so you can react before any code is written, then "
                "build and test on real devices before it ever reaches an app store.",
            ),
            (
                "Technology We Use",
                "React Native and Flutter for most cross-platform apps, native Android/iOS "
                "development when a project genuinely needs it, with Flask or Node.js APIs "
                "behind the scenes.",
            ),
        ],
    },
}

# Real nearby-Aligarh towns we don't have a dedicated page for, but still
# genuinely serve (remotely, from the Aligarh office). Used to broaden the
# `areaServed` schema on every location page and for a single natural
# mention on the Aligarh flagship pages and the /locations hub — not
# repeated verbatim across every page, to avoid it reading as stuffing.
EXTENDED_AREAS = ["Gabhana", "Akrabad", "Jawan", "Chandaus", "Tappal", "Beswan"]

# location key -> display data
LOCATIONS = {
    "aligarh": {
        "name": "Aligarh",
        "is_hq": True,
        "district_note": "Aligarh",
        "context": (
            "Aligarh is home to a strong base of manufacturing and trading businesses, from "
            "the city's well-known lock and hardware industry to retail, education, and "
            "logistics tied to its position on NH91"
        ),
        "nearby": "Hathras, Khair, Atrauli, and the wider Aligarh district",
    },
    "delhi": {
        "name": "Delhi",
        "is_hq": False,
        "district_note": "Delhi",
        "context": (
            "Delhi's business landscape spans everything from government-adjacent enterprises "
            "to corporate offices and fast-growing startups, and competition for customer "
            "attention online is intense across nearly every industry"
        ),
        "nearby": "Noida, Gurugram, and the wider National Capital Region",
        "aligarh_relation": "Aligarh",
        "office_line": (
            "We're based in Aligarh, a few hours' drive from Delhi — the project itself runs "
            "remotely for the large majority of clients, and we travel in for meetings when a "
            "project genuinely calls for it."
        ),
    },
    "noida": {
        "name": "Noida",
        "is_hq": False,
        "district_note": "Gautam Buddh Nagar",
        "context": (
            "Noida's economy is built heavily around IT companies, startups, and media and "
            "production businesses, which means most local companies already expect a strong "
            "digital presence from anyone they work with, including their own vendors"
        ),
        "nearby": "Delhi, Greater Noida, Ghaziabad, and the wider NCR",
        "aligarh_relation": "Aligarh",
        "office_line": (
            "We're based in Aligarh, a few hours from Noida — most projects run fully "
            "remotely, and we're available to meet in person for the ones where it makes a "
            "real difference."
        ),
    },
    "hathras": {
        "name": "Hathras",
        "is_hq": False,
        "district_note": "Hathras",
        "context": (
            "Hathras' economy is built around manufacturing (including hosiery and metal "
            "goods) and agriculture-linked trade, with a growing number of local businesses "
            "needing a proper online presence to reach customers beyond the district"
        ),
        "nearby": "Aligarh, Sasni, Sikandra Rao, and the surrounding district",
        "aligarh_relation": "nearby Aligarh",
    },
    "khair": {
        "name": "Khair",
        "is_hq": False,
        "district_note": "Aligarh",
        "context": (
            "Khair's economy is largely agriculture and local trade, and businesses here are "
            "increasingly competing with ones based in Aligarh city itself for the same "
            "customers online"
        ),
        "nearby": "Aligarh city, Chandaus, Tappal, and the wider Khair tehsil",
        "aligarh_relation": "nearby Aligarh",
    },
    "atrauli": {
        "name": "Atrauli",
        "is_hq": False,
        "district_note": "Aligarh",
        "context": (
            "Atrauli's businesses are mostly agriculture, trade, and small manufacturing "
            "based, and most don't yet have a real website, which means real advantage for "
            "the ones that do"
        ),
        "nearby": "Aligarh city, Gangiri, and the wider Atrauli tehsil",
        "aligarh_relation": "nearby Aligarh",
    },
    "gurugram": {
        "name": "Gurugram",
        "is_hq": False,
        "district_note": "Gurugram",
        "context": (
            "Gurugram is one of India's biggest corporate and startup hubs, home to everything "
            "from MNC headquarters to SaaS companies and consulting firms, which makes it one "
            "of the most competitive markets in the country for any digital service"
        ),
        "nearby": "Delhi, Noida, Faridabad, and the wider NCR",
        "aligarh_relation": "Aligarh",
        "office_line": (
            "We're based in Aligarh, roughly a half-day's drive from Gurugram — the project "
            "itself is handled remotely for most clients, with in-person meetings arranged for "
            "larger engagements."
        ),
    },
}

FAQ_BY_LOCATION_SERVICE = {
    ("aligarh", "web-development"): [
        ("Do you work with Aligarh-based businesses remotely, or in person?", "Both. Our office is in Aligarh, so we meet in person when it helps, and work remotely for everything that doesn't need a face-to-face visit — most of the project runs smoothly either way."),
        ("How much does a website cost for a business in Aligarh?", "It depends on what you need — a simple business website costs far less than an e-commerce store or a custom web app. Tell us what you're trying to achieve and we'll give you a straight number, not a vague range."),
        ("How long does it take to build a website?", "A standard business website typically takes 2-4 weeks. E-commerce stores and custom builds take longer depending on scope — we'll give you a realistic timeline before starting, not an optimistic one."),
        ("Can you help with an existing website that needs fixing or redesigning?", "Yes — we take on redesigns and fixes for existing sites, not just new builds from scratch."),
    ],
    ("aligarh", "software-development"): [
        ("Can a small or mid-sized Aligarh business actually afford custom software?", "Custom software doesn't have to mean an enterprise-scale project — we build focused tools (a billing system, an inventory tracker) sized to what your business actually needs, not an oversized system you'll never fully use."),
        ("We already use spreadsheets — why switch to custom software?", "Spreadsheets work until multiple people need to update the same data, or you need reports you can't easily build by hand. If that's where you are, custom software usually pays for itself in saved time within months."),
        ("Do you provide support after the software is delivered?", "Yes — we stay available for fixes, small changes, and questions after launch, not just during the build."),
        ("Is our business data kept private and secure?", "Yes — access controls, secure hosting, and data-handling practices are part of every build, not an optional add-on."),
    ],
    ("aligarh", "app-development"): [
        ("Do I need a separate app if I already have a website?", "Not always — for many Aligarh businesses a mobile-friendly website covers it. An app makes sense when you need offline access, push notifications, or a tool your staff/delivery team use daily. We'll tell you honestly which one fits."),
        ("Android, iOS, or both?", "Depends on your actual customers and team — for most local businesses in India, Android-first (or Android-only) is the practical choice, and we'll recommend based on your real usage, not by default."),
        ("How much does an app cost to build?", "It depends heavily on features — a simple app costs far less than one with real-time tracking, payments, or complex logic. We'll scope it honestly before quoting."),
        ("Will the app be listed on the Play Store / App Store?", "Yes, we handle store listing and submission as part of the build."),
    ],
    ("hathras", "web-development"): [
        ("Do you have an office in Hathras, or work remotely?", "We're based in Aligarh and serve Hathras remotely — most website projects don't need in-person meetings, and we're close enough to visit when it genuinely helps."),
        ("Can you build a website in Hindi or bilingual (Hindi/English)?", "Yes — we build bilingual sites regularly for businesses in this region, where customers search and browse in both languages."),
        ("How much does a website cost for a Hathras business?", "It depends on scope — tell us what you're trying to achieve and we'll give a clear number rather than a vague estimate."),
        ("How long does a typical project take?", "A standard business website usually takes 2-4 weeks from kickoff to launch."),
    ],
    ("hathras", "software-development"): [
        ("Is custom software worth it for a smaller Hathras business?", "If you're currently managing inventory, billing, or orders manually or across spreadsheets, a focused custom tool often pays for itself quickly in time saved — it doesn't need to be a big enterprise system."),
        ("Do you support the software after it's delivered?", "Yes — ongoing support and small fixes are part of how we work, not a one-time handoff."),
        ("Can the software work with limited or unreliable internet?", "We can design for that where needed — offline-capable features and lightweight interfaces are something we account for when it matters for your location."),
        ("How do we get started?", "Tell us what's currently slow, manual, or spreadsheet-based, and we'll recommend the right approach — no obligation."),
    ],
    ("hathras", "app-development"): [
        ("Do Hathras businesses actually need a mobile app?", "Not always — many are better served by a mobile-friendly website first. We'll give you an honest recommendation instead of upselling an app you don't need."),
        ("What kind of apps do you build for businesses in this region?", "Customer ordering apps, staff/delivery apps, and internal tools are the most common — built for Android first, since that's where most local users are."),
        ("How much does app development cost?", "It depends on features — we'll scope it honestly and give you a real number before you commit."),
        ("Can you maintain the app after launch?", "Yes, ongoing maintenance and updates are available after the initial build."),
    ],
    ("khair", "web-development"): [
        ("Do you work with businesses in Khair even though your office is in Aligarh?", "Yes — Khair is close enough that in-person meetings are easy when needed, and most of the project runs remotely regardless."),
        ("What does a basic business website cost?", "It depends on what pages and features you need — we'll give you a clear quote once we understand your goals, not a generic package price."),
        ("Can you help us compete with businesses already online in Aligarh city?", "That's exactly the gap we help close — a proper website puts a Khair business on equal footing in search results and first impressions."),
        ("How soon can we launch?", "A standard business website typically takes 2-4 weeks from our first call to going live."),
    ],
    ("khair", "software-development"): [
        ("Do you build software for small Khair-based businesses, or only large companies?", "We size the software to the business — a focused tool for a small operation, a larger system if you need it. No project is too small to be worth doing properly."),
        ("What if we're not sure exactly what we need yet?", "That's normal — describe what's slow or manual today and we'll recommend the right scope, rather than you having to spec it yourself."),
        ("Is support available after delivery?", "Yes, we remain available for fixes and changes after the software goes live."),
        ("How do you handle our business data?", "With proper access control and secure hosting — data handling is built into the project, not bolted on afterward."),
    ],
    ("khair", "app-development"): [
        ("Should a Khair business start with a website or an app?", "Almost always a website first — apps make sense once you have a specific need like staff coordination or repeat-customer ordering. We'll tell you honestly which applies."),
        ("What's the typical cost for a business app?", "It depends on the features — we'll scope it properly and quote honestly rather than guessing."),
        ("Do you build apps for both Android and iOS?", "Yes, though for most businesses in this region we usually recommend starting Android-first based on where the actual users are."),
        ("Can we start with something small and expand later?", "Yes — building a focused first version and expanding it later is often the smarter approach than trying to build everything at once."),
    ],
    ("atrauli", "web-development"): [
        ("We're a small Atrauli business — is a website worth it for us?", "If your competitors aren't online yet, a simple, well-built website is one of the highest-leverage things you can do — you don't need a large budget to get meaningful results."),
        ("Do you meet in person, or is everything remote?", "We're based in Aligarh and happy to meet when useful — most of the actual project work happens remotely either way."),
        ("How much does a basic business website cost?", "It depends on your goals and pages needed — we'll quote clearly once we understand what you're trying to achieve."),
        ("How long does it take?", "Typically 2-4 weeks for a standard business website."),
    ],
    ("atrauli", "software-development"): [
        ("Is custom software realistic for a business our size in Atrauli?", "Yes — we build focused tools sized to what you actually need, not oversized enterprise systems. A simple billing or inventory tool is often enough to make a real difference."),
        ("What if our current process is mostly manual or on paper?", "That's a common starting point — we design around your current process and digitize it in stages, rather than asking you to change everything at once."),
        ("Do you provide support after launch?", "Yes, ongoing support and fixes are part of the engagement."),
        ("How do we start?", "Describe what's slow or manual today, and we'll recommend the right first step."),
    ],
    ("atrauli", "app-development"): [
        ("Does a business in Atrauli really need a mobile app?", "Usually not as a first step — a website covers most needs. An app makes sense for specific cases like staff coordination or repeat ordering, and we'll tell you honestly if that's you."),
        ("What's the cost range for a simple business app?", "It depends on features — we scope and quote honestly rather than guessing upfront."),
        ("Android or iOS first?", "For most businesses in this region, Android-first is the practical choice based on where users actually are."),
        ("Can you support the app after it launches?", "Yes, ongoing maintenance is available after the initial build."),
    ],
    ("delhi", "web-development"): [
        ("There are hundreds of web development agencies in Delhi — why choose a team based in Aligarh?", "Because you get the same senior-level work without big-agency overhead — direct access to the person actually building your site, competitive pricing, and full attention on your project instead of being one of fifty accounts."),
        ("Do you work with Delhi businesses remotely, or do we need to meet in person?", "Almost all of our Delhi projects run fully remotely — video calls, shared documents, and regular updates cover it. We're happy to travel in for a kickoff or a major milestone if that's useful."),
        ("How much does a website cost for a Delhi-based business?", "It depends entirely on scope — a business site costs far less than a custom web app or e-commerce platform. We'll give you a clear number once we understand what you actually need, not a generic Delhi-market rate."),
        ("How long does a typical project take?", "A standard business website usually takes 2-4 weeks. More complex builds take longer — we'll give you a realistic timeline before starting."),
    ],
    ("delhi", "software-development"): [
        ("Can a smaller or newer Delhi business actually get quality custom software without enterprise pricing?", "Yes — we size the software to your actual needs. A focused internal tool costs a fraction of an enterprise system, and it's often all a growing business actually needs."),
        ("We already work with a Delhi-based dev shop — why consider you?", "If it's working, stick with it. If you're not getting real attention or the pricing doesn't match the value, a smaller, founder-led team is often a better fit for a mid-sized project."),
        ("Is our data secure with a team based outside Delhi?", "Yes — access control, secure hosting, and proper data-handling practices are part of every build regardless of where we're based."),
        ("Do you provide support after delivery?", "Yes, ongoing support and fixes are part of how we work, not a one-time handoff."),
    ],
    ("delhi", "app-development"): [
        ("How do you compare to Delhi-based app development agencies on cost?", "Being based in Aligarh means lower overhead, which usually means more competitive pricing for the same quality of work — we're not paying Delhi office rents."),
        ("Android, iOS, or both?", "Depends on your actual users — for most businesses we'll recommend based on real usage data, not a default answer."),
        ("What's a realistic budget for a business app?", "It depends heavily on features — we'll scope honestly and give you a real number before you commit to anything."),
        ("Can you maintain the app after it's live?", "Yes, ongoing maintenance and updates are available after the initial build."),
    ],
    ("noida", "web-development"): [
        ("Noida has a huge number of IT companies already building websites — what's different about you?", "We're not trying to out-market big Noida agencies — we compete on direct access, honest pricing, and actually caring about a mid-sized project the way a bigger shop often can't."),
        ("Do you understand what a Noida-based tech or media company actually needs from a website?", "Yes — professional, fast, credible, and built to convert visitors into leads or clients, which is what most Noida businesses are actually optimizing for."),
        ("What does a business website cost?", "It depends on scope — we'll quote clearly once we understand your goals."),
        ("How long does a project take?", "Typically 2-4 weeks for a standard business site; longer for custom builds."),
    ],
    ("noida", "software-development"): [
        ("Do you build software for Noida startups, or only established businesses?", "Both — we size the project to where the business actually is, whether that's an early-stage tool or something more established."),
        ("How do you handle a fast-moving startup timeline?", "We build in stages so you see real progress quickly, rather than waiting months for a single big reveal."),
        ("Can the software integrate with tools we already use?", "Yes — connecting to your existing CRM, payment systems, or other software is a normal part of the build."),
        ("What happens after launch?", "We stay available for fixes, changes, and support — not a one-time handoff."),
    ],
    ("noida", "app-development"): [
        ("Do you build apps for Noida-based IT and media companies?", "Yes — customer-facing apps, internal tools, and staff apps are all things we build regularly."),
        ("React Native, Flutter, or native?", "Depends on the project — we'll recommend based on what genuinely fits your timeline and requirements, not a one-size-fits-all default."),
        ("What's the typical cost range?", "It depends heavily on features — we scope and quote honestly before you commit."),
        ("Do you handle app store submission?", "Yes, store listing and submission are part of the build."),
    ],
    ("gurugram", "web-development"): [
        ("Gurugram is full of corporate agencies — why would we go with a team based in Aligarh?", "Lower overhead means more competitive pricing for comparable quality, plus direct access to the people actually doing the work instead of being routed through account managers."),
        ("Can you handle a corporate-level website, not just a small business site?", "Yes — we build sites for businesses of varying scale; what matters is understanding your actual requirements, not the size of our own office."),
        ("What's the cost for a professional business website?", "It depends on scope and features — we'll give you a clear number once we understand your goals."),
        ("How long does a project take?", "Typically 2-4 weeks for a standard site, longer for custom or enterprise-level builds."),
    ],
    ("gurugram", "software-development"): [
        ("Do you work with Gurugram-based corporates and MNCs, or only smaller businesses?", "We work with businesses of various sizes — what matters is whether the project is a genuine fit, not the size of the company logo."),
        ("How do you ensure quality without a large local team?", "Focused, senior-level attention on fewer projects at a time, rather than spreading a large team thin across dozens of accounts."),
        ("Is support available after the software goes live?", "Yes, ongoing support and fixes are part of the engagement."),
        ("How do we get started?", "Tell us what's slow or manual today, and we'll recommend a realistic approach and cost."),
    ],
    ("gurugram", "app-development"): [
        ("Can a team based in Aligarh really deliver for a Gurugram corporate client?", "Yes — the work itself doesn't depend on office location; what matters is the process and the people doing it, and we're happy to prove that with a small pilot project first if that helps."),
        ("What's a realistic app development budget?", "It depends heavily on features and complexity — we'll scope it honestly and give a real number, not an inflated corporate estimate."),
        ("Do you build for enterprise-scale apps?", "We take on projects where we can genuinely deliver quality — for very large enterprise-scale apps, we'll be upfront if it's outside a good fit."),
        ("Can you support the app after launch?", "Yes, ongoing maintenance is available after the initial build."),
    ],
}


DEEP_DIVE = {
    ("aligarh", "web-development"): (
        "Aligarh's lock and hardware manufacturers have traditionally sold through distributor "
        "networks and word-of-mouth, but that's changing fast — buyers now search online before "
        "ever picking up the phone, whether they're a local retailer or a bulk buyer three states "
        "away. A business without a real website is invisible to that search, no matter how good "
        "the product is. For Aligarh's trading and manufacturing businesses specifically, a "
        "website that shows your catalogue, your minimum order quantities, your certifications, "
        "and a clear way to get in touch does more selling before a call ever happens than a "
        "brochure ever could. AMU also brings a steady flow of students, researchers, and "
        "visiting families into the city — an audience that searches for everything from hostels "
        "to tutoring to local services almost entirely on their phone. A website built for how "
        "Aligarh actually searches, not a generic template, is what turns that traffic into "
        "real enquiries."
    ),
    ("aligarh", "software-development"): (
        "A lot of Aligarh's manufacturing and trading businesses run on a mix of registers, "
        "WhatsApp messages, and Excel sheets passed between staff — which works until the "
        "business grows past a certain size, or until the one person who understands the "
        "spreadsheet is on leave. Custom software doesn't mean ripping out how you work; it "
        "means turning that same process into something reliable that multiple people can use "
        "without stepping on each other. For a lock manufacturer tracking raw material stock "
        "across sheds, or a trader managing dozens of supplier relationships, a simple system "
        "built around how the business actually operates saves real hours every week — hours "
        "that add up to real money over a year. Being based in Aligarh means we've seen these "
        "exact patterns before, and we build software that fits the business, not the other "
        "way around."
    ),
    ("aligarh", "app-development"): (
        "Most Aligarh businesses don't need an app on day one — a mobile-friendly website "
        "usually covers the basics. Where an app genuinely earns its place is in day-to-day "
        "operations: a delivery team checking off orders as they go, a sales staff member "
        "logging visits to hardware shops across the city, or a manufacturer's supervisor "
        "tracking production stages from a phone on the shop floor. These are the situations "
        "where a simple, purpose-built app removes a genuine daily bottleneck, rather than "
        "being built because \"every business needs an app.\" Because we're in Aligarh "
        "ourselves, we understand the kind of operational friction that's specific to "
        "manufacturing and trading businesses here — and we'll tell you honestly if an app is "
        "the right fix, or if something simpler would do the job just as well."
    ),
    ("hathras", "web-development"): (
        "Hathras' hosiery and metal-goods manufacturers largely sell through established trade "
        "relationships, but new buyers — especially ones outside the immediate region — "
        "increasingly start their search online, and a business with no website simply doesn't "
        "show up in that search. A website built for a Hathras manufacturer needs to do a "
        "specific job: show the product range clearly, make it easy for a new buyer to get in "
        "touch, and load properly even on a modest mobile connection, since that's how most of "
        "that traffic will actually arrive. We build with that reality in mind rather than "
        "assuming every visitor has a fast connection and a laptop. Because we're a short "
        "distance away in Aligarh, we understand the trade patterns of this belt well enough to "
        "build a site that fits how Hathras businesses actually sell, not a generic template "
        "repurposed for a different market."
    ),
    ("hathras", "software-development"): (
        "For manufacturing businesses in Hathras, inventory and order tracking often still runs "
        "on paper registers or scattered spreadsheets — a system that works at a small scale but "
        "starts breaking down as the business grows or as more people need access to the same "
        "information. Custom software doesn't have to mean a big, disruptive project; a focused "
        "tool that tracks stock, billing, or orders can be built around the process you already "
        "use, digitized in stages rather than all at once. We design with the reality of "
        "variable internet connectivity in mind too, since that matters for a tool that needs to "
        "actually get used every day, not just look good in a demo. Being nearby in Aligarh means "
        "we understand the operational patterns of manufacturing businesses in this belt well "
        "enough to build something that fits, not a generic off-the-shelf package."
    ),
    ("hathras", "app-development"): (
        "An app makes sense for a Hathras business in specific situations — a sales team "
        "visiting shops across the district who need to log orders on the spot, or a production "
        "team tracking stages of a manufacturing run without waiting for someone to update a "
        "central register later. For most other cases, a mobile-friendly website already does "
        "the job, and we'll say so rather than push an app you don't need. When an app is the "
        "right call, we build for Android first, since that's where the overwhelming majority of "
        "users in this region actually are, and we design around real-world conditions like "
        "inconsistent connectivity rather than assuming a constant fast connection. Our office is "
        "in Aligarh, close enough to understand the operational rhythms of Hathras businesses "
        "without needing everything explained from scratch."
    ),
    ("khair", "web-development"): (
        "Khair sits close enough to Aligarh city that local businesses are effectively competing "
        "with Aligarh-based ones for the same customers, online and off — and a business without "
        "a proper website is at a real disadvantage in that comparison, regardless of how good "
        "the actual product or service is. A well-built website levels that specific gap: it "
        "puts a Khair business in front of the same searches, with the same credibility, as a "
        "competitor based in the city. We build these sites to load fast and work properly on a "
        "phone first, since that's how the large majority of local searches happen here, and we "
        "make sure the essentials — what you do, how to reach you, and a reason to choose you — "
        "are impossible to miss. Since Khair is part of the same Aligarh district we operate in, "
        "we already understand the local market context rather than needing it explained."
    ),
    ("khair", "software-development"): (
        "Most small and mid-sized businesses in Khair are still running on manual processes — "
        "paper records, spreadsheets, or a mix of both — which is completely normal at a certain "
        "size, but becomes a real cost in time and errors as the business grows. Custom software "
        "built specifically for how a Khair business operates, whether that's tracking "
        "agricultural trade, local retail inventory, or billing, removes that friction without "
        "forcing a wholesale change in how the business runs day to day. We start small where it "
        "makes sense — a single focused tool solving one real problem — rather than proposing an "
        "oversized system that takes months to adopt. Being based in the same district means we "
        "understand the scale and pace that actually fits a Khair business, not a "
        "one-size-fits-all enterprise template."
    ),
    ("khair", "app-development"): (
        "For a Khair-based business, an app is rarely the first thing worth building — a website "
        "usually covers more ground for less cost and effort. Where it does make sense is a "
        "specific operational need: a small sales or delivery team that needs a simple way to log "
        "visits or orders on the move, without depending on a phone call back to the office. We "
        "build those apps to work reliably on Android, where the vast majority of users in this "
        "region actually are, and we keep them deliberately simple, focused on the one job they "
        "need to do well rather than trying to be everything at once. Being part of the same "
        "Aligarh district, we understand what a realistic first app looks like for a business "
        "this size."
    ),
    ("atrauli", "web-development"): (
        "Atrauli's economy is still largely built on agriculture, trade, and small manufacturing, "
        "and most local businesses here don't have a real website yet — which means the ones "
        "that do get a genuine, visible advantage over the competition, not just a marginal one. "
        "A simple, well-built site is often enough to be the only serious result a potential "
        "customer or supplier finds when they search for a business like yours in the area. We "
        "keep these builds practical: fast to load, clear about what you offer, and easy to get "
        "in touch through, rather than an expensive project trying to do everything at once. As a "
        "business based in the same district, we understand what a first website realistically "
        "needs to achieve for an Atrauli business, and we build to that, not to a generic "
        "template."
    ),
    ("atrauli", "software-development"): (
        "Most businesses in and around Atrauli manage inventory, billing, or records manually "
        "today, and that's a reasonable starting point — but as a business grows, the cost of "
        "that manual process in time and mistakes grows with it. Custom software here doesn't "
        "need to be an ambitious, expensive project; a small, focused tool that solves one real "
        "problem — tracking stock, managing bills, or organizing customer records — is often "
        "enough to make a genuine difference, and can expand later if the business needs it to. "
        "We design around the process the business already follows rather than asking an owner "
        "to relearn how they work. Being based in the same district as Atrauli, we understand the "
        "realistic scale of software that actually gets adopted and used here."
    ),
    ("atrauli", "app-development"): (
        "An app is worth building for an Atrauli business only in specific situations — "
        "coordinating a small field or delivery team, for instance, where a simple mobile tool "
        "removes a real daily bottleneck. For most other needs, a website does the job for less "
        "cost and complexity, and we'll recommend that honestly rather than push an app that "
        "isn't necessary. When an app is the right fit, we build for Android, keep the feature "
        "set focused on the one problem it needs to solve, and test it on real devices rather "
        "than assuming ideal conditions. Being part of the same district, we understand the kind "
        "of operational gap an app is actually meant to close for a business here."
    ),
    ("delhi", "web-development"): (
        "Delhi's business landscape is enormous and covers almost every industry, from "
        "government-adjacent enterprises to fast-growing startups — which also means the market "
        "for web development is one of the most competitive in the country, with hundreds of "
        "agencies chasing the same searches. Standing out on price and marketing spend alone is "
        "a losing game against big Delhi-based shops with large sales teams. What we compete on "
        "instead is direct access and genuine attention: when you work with us, you're working "
        "with the person actually building your site, not a project manager relaying your "
        "feedback to a developer three layers removed. Lower overhead from being based outside "
        "Delhi also means more competitive pricing for the same quality of work. For a Delhi "
        "business evaluating vendors, that combination — real access, honest pricing, and a "
        "website that's actually built to generate enquiries rather than just look impressive in "
        "a pitch deck — is often the more practical choice over a bigger name."
    ),
    ("delhi", "software-development"): (
        "Custom software for a Delhi business usually means choosing between an expensive "
        "enterprise vendor and an underqualified freelancer, with not much in between. We sit in "
        "that gap deliberately — senior-level engineering without enterprise pricing, applied to "
        "a project sized honestly to what the business actually needs rather than what a bigger "
        "vendor would prefer to sell. A lot of growing Delhi businesses are still running "
        "critical processes through spreadsheets or disconnected tools, not because a proper "
        "system wouldn't help, but because the cost of getting one built has felt out of reach. "
        "Being based in Aligarh keeps our costs lower without cutting corners on the actual "
        "engineering, which changes that calculation for a mid-sized business. We build in "
        "visible stages so you're never waiting months for a single reveal, and we stay "
        "available after launch rather than disappearing once the invoice is paid."
    ),
    ("delhi", "app-development"): (
        "Delhi's app development market is dominated by agencies with large teams and "
        "correspondingly large budgets, which prices out a lot of businesses that would "
        "genuinely benefit from a focused, well-built app rather than a feature-bloated one. We "
        "build the opposite of that: apps scoped tightly around the actual problem — a delivery "
        "team that needs simple order tracking, a customer base that wants a straightforward "
        "ordering experience — rather than an ambitious feature list that takes a year to ship. "
        "Being based in Aligarh keeps our pricing genuinely competitive against Delhi-based shops "
        "without changing how the work itself gets done: the same development process, the same "
        "testing on real devices, the same store submission handling. For a Delhi business "
        "unsure whether an app is even the right move, we'll say so honestly rather than push a "
        "build that isn't needed — a website often covers the same ground for a fraction of the "
        "cost."
    ),
    ("noida", "web-development"): (
        "Noida's economy runs heavily on IT companies, media and production businesses, and a "
        "fast-growing startup scene — which means most Noida businesses already understand, "
        "better than most, what a genuinely good website looks like, and won't be impressed by a "
        "generic template. That raises the bar for what we build: fast load times, clean design, "
        "and a structure that actually supports lead generation or e-commerce conversion, not "
        "just a digital business card. Competing directly against Noida's own dense cluster of "
        "web agencies on marketing spend isn't realistic for a smaller, Aligarh-based team — so "
        "instead we compete on the work itself and on being genuinely accessible, without the "
        "account-manager layers a larger local agency often adds. For a Noida business evaluating "
        "who to work with, that usually means faster communication, more direct input into the "
        "actual build, and pricing that reflects lower overhead rather than a big-city office "
        "lease."
    ),
    ("noida", "software-development"): (
        "A large share of Noida's economy is IT and tech-adjacent, which means the businesses "
        "here are often more technically literate than average about what custom software should "
        "look like — and also more skeptical of vendors who overpromise. We lean into that by "
        "being specific rather than vague: we scope the actual problem before proposing a "
        "solution, build in stages so progress is visible early, and document the system properly "
        "instead of leaving it as a black box only we understand. For an early-stage Noida "
        "startup, that usually means a smaller, focused first version rather than an ambitious "
        "system that takes six months to see any value from. For a more established Noida "
        "business, it means integrating cleanly with the tools already in use rather than asking "
        "for a disruptive rebuild. Being based in Aligarh keeps the cost structure lean without "
        "changing the quality of the underlying engineering."
    ),
    ("noida", "app-development"): (
        "Noida's IT and media-heavy business base means there's no shortage of local app "
        "development talent and agencies — but that also means pricing here often reflects "
        "big-city overhead more than the actual complexity of the app being built. We build the "
        "same category of apps — customer-facing ordering apps, internal staff tools, media and "
        "content apps — at a cost structure that reflects being based in Aligarh rather than a "
        "Noida office lease, without cutting corners on the development or testing process. We'll "
        "also tell a Noida business honestly when a mobile-friendly website would do the same job "
        "for a fraction of the cost, rather than defaulting to recommending an app because that's "
        "the bigger invoice. When an app is genuinely the right call, we scope it tightly around "
        "the specific feature that matters, rather than proposing an ambitious build that takes "
        "months longer than it needs to."
    ),
    ("gurugram", "web-development"): (
        "Gurugram is one of India's biggest corporate and startup hubs, and that density means "
        "the web development market here is shaped heavily by large agencies serving MNCs and "
        "well-funded startups — a segment we're not trying to compete with directly. Where we fit "
        "is the mid-sized Gurugram business that wants agency-quality work without agency-scale "
        "pricing: a website that's fast, professional, and actually built to convert, delivered "
        "by the same small team from first call to launch rather than passed between departments. "
        "Being based in Aligarh keeps our overhead low, which shows up directly in more "
        "competitive pricing for comparable quality. We're upfront that very large, "
        "enterprise-scale projects with heavy compliance or integration requirements may be "
        "better served by a bigger local agency — but for the businesses in between, direct "
        "access to the people doing the actual work tends to matter more than a Gurugram office "
        "address."
    ),
    ("gurugram", "software-development"): (
        "Gurugram's business landscape leans heavily corporate and consulting-focused, and a lot "
        "of the custom software built here is priced accordingly — enterprise rates, enterprise "
        "timelines, enterprise sales processes. For a mid-sized Gurugram business that needs a "
        "genuinely useful internal tool rather than an enterprise-grade platform, that pricing "
        "often doesn't match the actual scope of the problem. We build software sized honestly to "
        "what's needed: a focused system solving one real operational problem, built and "
        "delivered in weeks rather than quarters, at a cost structure shaped by being based in "
        "Aligarh rather than a Gurugram corporate lease. We document what we build properly, so "
        "it isn't a black box dependent on us specifically, and we stay available for support "
        "after launch. For businesses evaluating a first custom software project, that "
        "combination of honest scoping and lower cost is often the more practical starting point "
        "than an enterprise vendor relationship."
    ),
    ("gurugram", "app-development"): (
        "Gurugram's corporate and startup density means app development pricing here is often "
        "set by agencies serving well-funded companies with correspondingly large budgets — which "
        "prices out a lot of smaller Gurugram businesses that would genuinely benefit from a "
        "simple, well-built app. We build apps scoped tightly to the actual operational need, "
        "whether that's a small sales team logging visits or a customer base wanting a "
        "straightforward way to place orders, rather than an ambitious feature set designed to "
        "impress in a pitch. Being based in Aligarh keeps our pricing structurally lower without "
        "changing the actual development or testing process — the same real-device testing, the "
        "same store submission handling. For a Gurugram business unsure if an app is worth the "
        "investment, we'll give a genuinely honest recommendation, including telling you when a "
        "website would do the job just as well for considerably less."
    ),
}


# ──────────────────────────────────────────────────────────────
# WHY CHOOSE — unique selling points per location × service,
# framed around what a local searcher actually cares about.
# ──────────────────────────────────────────────────────────────
WHY_CHOOSE = {
    ("aligarh", "web-development"): [
        ("Local Team, No Middlemen",
         "We're based right here in Aligarh. You speak directly to the people designing and coding your website, not an account manager forwarding emails. That means faster turnaround, fewer misunderstandings, and a website that actually matches what you asked for."),
        ("Websites That Rank in Aligarh Searches",
         "We build every site with on-page SEO baked in from the start, targeting the keywords Aligarh customers actually type into Google. From local schema markup to fast page speeds, your site is built to show up when it matters, not just look good."),
        ("Affordable Without Cutting Corners",
         "No Delhi-level pricing, no offshore quality issues. Our Aligarh base keeps costs genuinely lower while delivering the same professional standard you'd expect from a metro agency. Every rupee goes into the actual build, not our rent."),
        ("Ongoing Support After Launch",
         "Your website doesn't end at launch. We handle hosting guidance, content updates, performance monitoring, and SEO tweaks, and because we're local, we're a phone call away when something needs attention."),
    ],
    ("aligarh", "software-development"): [
        ("Built for How Aligarh Businesses Actually Work",
         "We've worked with enough local manufacturers, traders, and service businesses to understand the real workflows, like managing stock across multiple godowns, tracking dealer payments, or coordinating production schedules. The software we build fits those patterns, not a generic template."),
        ("Direct Access to Developers",
         "No project managers, no ticket queues. You talk directly to the engineers building your system, which means changes happen faster, questions get answered the same day, and the final product matches what you actually need."),
        ("Cost-Effective Custom Solutions",
         "Custom software doesn't have to mean enterprise budgets. We build focused tools that solve one real problem well, starting small and expanding only when the business genuinely needs it."),
        ("Proper Documentation and Handover",
         "Everything we build is documented so your team can understand it, and you're never locked into depending on us for basic changes."),
    ],
    ("aligarh", "app-development"): [
        ("Honest Recommendations, Not Upselling",
         "We'll tell you straight if your business actually needs an app, or if a mobile-friendly website would do the same job for less. Most Aligarh businesses we talk to benefit more from a good website first, and we'd rather build you the right thing."),
        ("Android-First for the Indian Market",
         "Over 95% of smartphone users in Aligarh are on Android. We build Android-first by default and add iOS only when your actual user data justifies the extra cost."),
        ("Real-Device Testing",
         "Every app we build is tested on actual phones in real network conditions, not just emulators in a lab. That matters when your users are on varying connections across the district."),
        ("Post-Launch Maintenance",
         "Apps need ongoing updates for OS changes, bug fixes, and new features. We stay available after launch for all of it."),
    ],
    ("hathras", "web-development"): [
        ("Nearby Team, Easy Communication",
         "Based in Aligarh, we're close enough for in-person meetings when needed, and most of the project runs smoothly over calls and screen-shares. You get local understanding without needing a Hathras-based agency."),
        ("Designed for Mobile-First Audiences",
         "Most web traffic in Hathras comes from mobile phones on varying connection speeds. We build lightweight, fast-loading sites that work reliably on the devices your customers are actually using."),
        ("SEO for Hathras-Specific Searches",
         "We optimize your site for the keywords people in and around Hathras actually search for, including local service queries, product searches, and business-name lookups."),
        ("Transparent Pricing",
         "No hidden fees, no vague estimates. We quote clearly before starting, so you know exactly what you're paying for and what you're getting."),
    ],
    ("hathras", "software-development"): [
        ("We Understand Manufacturing Workflows",
         "Hathras' hosiery and metalwork industries have specific inventory, billing, and order-tracking needs. We've built similar systems for businesses in this belt and understand the patterns."),
        ("Works on Limited Internet",
         "Software that needs a constant fast connection isn't practical for every location. We can build offline-capable features and lightweight interfaces when your team's connectivity is variable."),
        ("Start Small, Scale Later",
         "You don't need to automate everything at once. We typically start with the one process causing the most friction and expand from there."),
        ("Ongoing Support Included",
         "We don't disappear after delivery. Fixes, small changes, and questions are all part of how we work."),
    ],
    ("hathras", "app-development"): [
        ("Built for Field Teams",
         "The most common use case we see in this region is a sales or delivery team that needs to log orders and visits from the field. We build simple, focused apps for exactly that."),
        ("Android-First Development",
         "The overwhelming majority of users in Hathras district are on Android. We build for that reality first, rather than splitting budget across platforms most of your users aren't on."),
        ("Practical Scope, Not Feature Bloat",
         "We build the minimum set of features that actually solve your operational problem, rather than an ambitious feature list that takes months to ship and nobody fully uses."),
        ("Honest Advice on Whether You Need an App",
         "If a mobile-friendly website would serve the same purpose for less, we'll say so."),
    ],
    ("khair", "web-development"): [
        ("Compete with Aligarh-Based Businesses Online",
         "Khair businesses are competing with Aligarh city for the same customers online. A proper website puts you on equal footing in search results and first impressions."),
        ("Same-District Team",
         "We're in the same Aligarh district, so we understand the local market without needing it explained. In-person meetings are easy when needed."),
        ("Mobile-Optimized",
         "We build phone-first, because that's how most of your potential customers will actually find and browse your site."),
        ("Clear, Honest Pricing",
         "We quote upfront, with no hidden costs or vague ranges. You know what you're getting before any work starts."),
    ],
    ("khair", "software-development"): [
        ("Sized for Your Business",
         "Custom software doesn't have to be an enterprise-scale project. We build focused tools that match the actual size and pace of a Khair business."),
        ("Digitize Without Disruption",
         "We design around the process you already follow, rather than asking you to change how you work. The switch is gradual and practical."),
        ("Same-District Support",
         "Being in the same district means faster communication and understanding. We're available for support after the software goes live."),
        ("Secure and Documented",
         "Proper access controls and documentation are standard, so your data stays safe and your team isn't dependent on us for basic operations."),
    ],
    ("khair", "app-development"): [
        ("Realistic First Step",
         "We'll recommend a website first if that covers your needs. An app makes sense only for specific operational use cases, and we'll be upfront about which applies to you."),
        ("Built for Android",
         "For businesses in this region, Android-first is the practical and cost-effective choice. We build for where your users actually are."),
        ("Focused Feature Set",
         "We build apps that do one thing well, rather than trying to be a Swiss Army knife nobody fully adopts."),
        ("Nearby Support",
         "Same Aligarh district, easy communication, available after launch for updates and fixes."),
    ],
    ("atrauli", "web-development"): [
        ("First-Mover Advantage Online",
         "Most Atrauli businesses don't have a website yet. Being among the first gives you a visible, measurable advantage over competitors who are still invisible online."),
        ("Practical, Not Over-Engineered",
         "We build what your business actually needs right now, fast to load, clear about what you offer, easy to get in touch through, and we keep it within a realistic budget."),
        ("Local Understanding",
         "We're based in the same district. We understand the market context, the customer base, and what a first website realistically needs to achieve here."),
        ("No Lock-In",
         "You own your website and your content. We hand over a site you can manage, not one that depends on us for every small change."),
    ],
    ("atrauli", "software-development"): [
        ("From Manual to Digital, Gradually",
         "If you're running on paper and spreadsheets today, we digitize the most painful process first and expand from there. No big-bang rollout."),
        ("Sized for Atrauli Businesses",
         "We build focused tools, not oversized systems. A simple billing or inventory tracker is often enough to make a real operational difference."),
        ("Designed for Real Conditions",
         "Variable internet, shared devices, non-technical users, we design around these realities rather than assuming ideal conditions."),
        ("Ongoing Support",
         "Fixes, questions, and small changes after launch are all part of the engagement."),
    ],
    ("atrauli", "app-development"): [
        ("Honest Assessment First",
         "We'll tell you upfront if a website would serve your needs better than an app. We'd rather build the right thing than the more expensive thing."),
        ("Android-First, Field-Ready",
         "Built for the devices and network conditions your team actually uses, not lab-ideal ones."),
        ("Solve One Problem Well",
         "We scope apps tightly around the specific operational bottleneck they need to fix, rather than building a feature-heavy app nobody fully adopts."),
        ("Local Support",
         "Same district, easy communication, available for maintenance after launch."),
    ],
    ("delhi", "web-development"): [
        ("Metro-Quality Work, Without Metro Overhead",
         "You get the same professional standard of web development that a Delhi agency delivers, but without the inflated pricing that comes with a Connaught Place or GK office address."),
        ("Direct Access to Builders",
         "No account managers, no relay layers. You talk directly to the people designing and coding your site, which means faster decisions and fewer rounds of miscommunication."),
        ("SEO Built In From Day One",
         "Every website we build includes proper on-page SEO, schema markup, and performance optimization. We don't treat search visibility as an optional add-on."),
        ("Proven Remote Collaboration",
         "Most of our Delhi projects run fully remotely. Video calls, shared documents, and regular progress updates cover everything. We travel in for kickoff or milestone meetings when it helps."),
    ],
    ("delhi", "software-development"): [
        ("Senior Engineering Without Enterprise Pricing",
         "We sit in the gap between expensive enterprise vendors and underqualified freelancers. Focused, senior-level work applied to a project sized honestly to what your business actually needs."),
        ("Visible Progress in Weeks, Not Months",
         "We build in stages you can see and use early, rather than disappearing for six months before a single reveal."),
        ("Properly Documented Systems",
         "Everything we build is documented so it's not a black box only we can maintain. Your team can understand and manage the system."),
        ("Ongoing Support After Launch",
         "We stay available for fixes, changes, and scaling, not a one-time handoff."),
    ],
    ("delhi", "app-development"): [
        ("Competitive Pricing, Same Process",
         "Being based in Aligarh keeps our pricing structurally lower than Delhi agencies, without cutting corners on the actual development, testing, or submission process."),
        ("Tightly Scoped Builds",
         "We build apps around the specific problem they need to solve, rather than an ambitious feature list that takes a year to ship and costs a fortune."),
        ("Real-Device Testing",
         "Every app is tested on actual phones in real conditions before it reaches a store."),
        ("Honest Recommendations",
         "We'll tell you if a mobile-friendly website would do the same job for a fraction of the cost, rather than defaulting to the bigger invoice."),
    ],
    ("noida", "web-development"): [
        ("We Meet the Higher Bar",
         "Noida businesses know what a good website looks like. We build to that standard, fast load times, clean design, and structure that supports actual lead generation, not just a digital business card."),
        ("More Accessible Than Large Agencies",
         "No account-manager layers, no being one of fifty accounts. You get direct access to the team doing the work, which means faster communication and more input into the actual build."),
        ("Lower Overhead, Same Quality",
         "Our Aligarh base means pricing that reflects lower overhead, not a Noida office lease. The quality of the work doesn't change."),
        ("SEO and Performance by Default",
         "On-page SEO, schema markup, Core Web Vitals optimization, and mobile-first design are standard in every build, not premium add-ons."),
    ],
    ("noida", "software-development"): [
        ("Specific Scoping, Not Vague Promises",
         "We define the actual problem before proposing a solution. No inflated scope, no features you didn't ask for, no surprises on the invoice."),
        ("Stage-by-Stage Delivery",
         "You see working software early and often, not a single reveal after months of silence."),
        ("Clean Integration",
         "Connecting to your existing CRM, payment systems, or analytics tools is a standard part of the build."),
        ("Lean Cost Structure",
         "Aligarh-based overhead means competitive pricing without cutting corners on engineering quality."),
    ],
    ("noida", "app-development"): [
        ("Same Calibre, Lower Cost",
         "We build the same category of apps as Noida agencies, customer-facing tools, internal staff apps, content platforms, at a cost structure that reflects being based in Aligarh."),
        ("Honest About When Not to Build an App",
         "We'll tell you when a mobile-friendly website would do the same job for a fraction of the cost, rather than defaulting to the bigger project."),
        ("Tight Scoping",
         "We focus on the features that actually matter for your users, rather than an ambitious spec that takes months longer than it needs to."),
        ("Store Submission Included",
         "Play Store and App Store listing, submission, and optimization are part of every app build."),
    ],
    ("gurugram", "web-development"): [
        ("Agency-Quality Without Agency-Scale Pricing",
         "We serve the mid-sized Gurugram business that wants professional web development without paying corporate-agency rates. Lower overhead, same quality."),
        ("Small Team, Full Attention",
         "You work with the same small team from first call to launch, rather than being passed between departments in a large agency."),
        ("Built to Convert",
         "Every site we build is structured around lead generation and enquiry conversion, not just visual impressions."),
        ("Competitive Pricing",
         "Aligarh-based overhead means more competitive pricing for comparable quality. The savings go into your project, not our office lease."),
    ],
    ("gurugram", "software-development"): [
        ("Honest Scoping, Not Enterprise Sales",
         "We build software sized to what you actually need, not what maximizes the invoice. A focused tool solving one real problem, delivered in weeks."),
        ("Documented and Maintainable",
         "Everything is documented properly so your team isn't dependent on us for basic understanding or operations."),
        ("Available After Launch",
         "Ongoing support, fixes, and scaling are part of the engagement, not a separate upsell."),
        ("Lean Pricing",
         "Our cost structure reflects Aligarh, not Gurugram. The engineering quality doesn't change."),
    ],
    ("gurugram", "app-development"): [
        ("Practical Pricing for Smaller Budgets",
         "We serve the Gurugram businesses that need a well-built app but can't justify big-agency pricing. Same development process, lower cost."),
        ("Scoped to the Actual Need",
         "We build around the specific operational problem, not an impressive-sounding feature list. Focused apps ship faster and get adopted more."),
        ("Real Testing, Real Devices",
         "Every app is tested on actual phones in real conditions before submission."),
        ("Honest About Alternatives",
         "If a website would do the job, we'll tell you rather than push the more expensive option."),
    ],
}


# ──────────────────────────────────────────────────────────────
# PROCESS STEPS — same process, framed with local context per
# service so each page gets unique supporting text.
# ──────────────────────────────────────────────────────────────
PROCESS_STEPS = {
    "web-development": [
        ("Discovery and Planning",
         "We start by understanding your business, your customers, and what you actually need the website to achieve. No generic questionnaire; a real conversation about your goals."),
        ("Design and Prototyping",
         "We design the pages and layout for your approval before writing any code, so you can see exactly what you're getting and request changes while it's still easy to make them."),
        ("Development and Testing",
         "Clean, fast, mobile-first code. We build with SEO fundamentals baked in, test across devices and browsers, and optimize for real-world performance, not just lab scores."),
        ("Launch and Handover",
         "We handle deployment, run final checks, and hand over a site you can manage. Post-launch support is available for updates, fixes, and ongoing improvements."),
    ],
    "software-development": [
        ("Requirements Mapping",
         "We map out what your software actually needs to do by observing your current process, not just asking for a feature list. This prevents building something that sounds right but doesn't fit how you work."),
        ("Architecture and Design",
         "We design the system structure and user interface before building, so the foundation is solid and you can see what it will look and feel like early."),
        ("Iterative Development",
         "We build in visible stages so you see working software within weeks, not months. Each stage is tested and reviewed before moving to the next."),
        ("Deployment and Support",
         "Proper documentation, training where needed, and ongoing availability for fixes and changes. We don't disappear after the invoice is paid."),
    ],
    "app-development": [
        ("Use Case Analysis",
         "We figure out what the app genuinely needs to do for your business and your users, including whether an app is the right solution at all, before designing anything."),
        ("UI/UX Design",
         "We design every screen and flow for your review before development begins. You approve the experience your users will have before a single line of code is written."),
        ("Development and Testing",
         "Cross-platform or native development depending on the project, with testing on real devices in real network conditions, not just emulators."),
        ("Store Submission and Maintenance",
         "We handle Play Store and App Store submission, listing optimization, and ongoing maintenance for OS updates, bug fixes, and new features."),
    ],
}


EXTENDED_REACH_LINES = {
    "web-development": (
        "Beyond Aligarh city itself, we also build websites for businesses in "
        + ", ".join(EXTENDED_AREAS[:-1]) + f", and {EXTENDED_AREAS[-1]} — all handled remotely from our Aligarh office."
    ),
    "software-development": (
        "That same reach extends to " + ", ".join(EXTENDED_AREAS[:-1])
        + f", and {EXTENDED_AREAS[-1]}, where we build the same custom software remotely from our Aligarh office."
    ),
    "app-development": (
        "We also build apps for businesses across " + ", ".join(EXTENDED_AREAS[:-1])
        + f", and {EXTENDED_AREAS[-1]}, all supported remotely from our Aligarh office."
    ),
}


def build_location_pages():
    """Return {slug: page_data} for every service x location combination."""
    pages = {}
    for service_key, service in SERVICES.items():
        for loc_key, loc in LOCATIONS.items():
            slug = f"{service_key}-company-{loc_key}"
            faqs = FAQ_BY_LOCATION_SERVICE[(loc_key, service_key)]

            if loc["is_hq"]:
                intro = (
                    f"Nexa Solutions is a {service['label'].lower()} based right here in "
                    f"{loc['name']} — founded and run locally, not a branch office. "
                    f"{loc['context']}, and we help those businesses get a "
                    f"proper {service['short']} presence built for how they actually operate."
                )
                office_line = (
                    f"Because our office is in {loc['name']} itself, we're available for "
                    f"in-person meetings whenever that's useful, alongside the remote "
                    f"collaboration that covers most of a typical project."
                )
            else:
                intro = (
                    f"Nexa Solutions is a {service['label'].lower()} serving {loc['name']} "
                    f"from our founder-led office in {loc.get('aligarh_relation', 'nearby Aligarh')}. "
                    f"{loc['context']}, and we bring the same {service['short']} approach we use "
                    f"for Aligarh clients to businesses here."
                )
                office_line = loc.get("office_line") or (
                    f"Our office is based in Aligarh, a short distance from {loc['name']} — "
                    f"close enough for an in-person meeting when it helps, with most of the "
                    f"project itself handled remotely."
                )

            pages[slug] = {
                "slug": slug,
                "service_key": service_key,
                "location_key": loc_key,
                "service": service,
                "location": loc,
                "title": f"{service['label']} in {loc['name']} | Nexa Solutions",
                "h1": f"{service['label']} Serving {loc['name']}",
                "meta_description": (
                    f"Nexa Solutions is a {service['label'].lower()} serving {loc['name']} "
                    f"and {loc['nearby']}. Get a free consultation for your {service['short']} project."
                ),
                "intro": intro,
                "office_line": office_line,
                "nearby_line": f"We also work with businesses across {loc['nearby']}.",
                "breakdown": service["breakdown"],
                "faqs": faqs,
                "image": service["image"],
                "extended_areas": EXTENDED_AREAS,
                "extended_reach_line": EXTENDED_REACH_LINES[service_key] if loc["is_hq"] else "",
                "deep_dive": DEEP_DIVE[(loc_key, service_key)],
                "why_choose": WHY_CHOOSE[(loc_key, service_key)],
                "process_steps": PROCESS_STEPS[service_key],
            }
    return pages


LOCATION_PAGES = build_location_pages()
