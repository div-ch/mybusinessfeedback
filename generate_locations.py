#!/usr/bin/env python3
"""
Generate 176 location pages for mybusinessfeedback.com
- 1 hub page: /locations/index.html
- 25 city pages: /locations/[city]/index.html
- 150 city-vertical pages: /locations/[city]/[vertical]/index.html
"""

import os
import textwrap

BASE_DIR = os.path.expanduser("~/Desktop/mybusinessfeedback/locations")

# ---------------------------------------------------------------------------
# CITIES
# ---------------------------------------------------------------------------
CITIES = {
    "new-york": {
        "name": "New York",
        "state": "NY",
        "neighborhoods": ["Manhattan", "Brooklyn", "Queens", "Upper East Side", "Midtown", "Financial District", "Williamsburg", "Astoria", "Bronx", "Staten Island"],
        "context": "densest business market in the US, extreme competition in every vertical, multilingual clientele, borough-specific demographics, Wall Street and Midtown corporate density",
    },
    "los-angeles": {
        "name": "Los Angeles",
        "state": "CA",
        "neighborhoods": ["Beverly Hills", "Santa Monica", "West Hollywood", "Pasadena", "Downtown LA", "Venice", "Silver Lake", "Encino", "Brentwood", "Culver City"],
        "context": "entertainment industry adjacency, sprawling metro requiring neighborhood-level marketing, diverse demographics, wellness culture driving med spa demand, traffic patterns affecting service scheduling",
    },
    "chicago": {
        "name": "Chicago",
        "state": "IL",
        "neighborhoods": ["The Loop", "River North", "Lincoln Park", "Wicker Park", "Gold Coast", "Logan Square", "Hyde Park", "West Loop", "Lakeview", "Streeterville"],
        "context": "strong neighborhood identities, harsh winters affecting home service demand, major legal and medical corridors, Midwestern service expectations, deep roots in trades and construction",
    },
    "houston": {
        "name": "Houston",
        "state": "TX",
        "neighborhoods": ["River Oaks", "Montrose", "The Heights", "Galleria", "Memorial", "Midtown", "Medical Center", "Rice Village", "Sugar Land", "Katy"],
        "context": "energy sector driving professional services, Texas Medical Center proximity, rapid suburban growth, diverse immigrant communities, extreme heat creating HVAC demand year-round",
    },
    "phoenix": {
        "name": "Phoenix",
        "state": "AZ",
        "neighborhoods": ["Scottsdale", "Tempe", "Chandler", "Gilbert", "Mesa", "Arcadia", "Biltmore", "Paradise Valley", "Ahwatukee", "Desert Ridge"],
        "context": "fastest-growing metro, retiree population driving medical and dental demand, extreme heat creating year-round home service needs, Scottsdale luxury market, new construction boom",
    },
    "philadelphia": {
        "name": "Philadelphia",
        "state": "PA",
        "neighborhoods": ["Center City", "Rittenhouse Square", "Old City", "Fishtown", "Northern Liberties", "University City", "Manayunk", "Society Hill", "Main Line", "Chestnut Hill"],
        "context": "historic neighborhoods with distinct identities, strong university presence, competitive medical market with major hospital systems, Main Line affluence, tight-knit community referral networks",
    },
    "san-antonio": {
        "name": "San Antonio",
        "state": "TX",
        "neighborhoods": ["Downtown", "Alamo Heights", "Stone Oak", "The Dominion", "Terrell Hills", "Olmos Park", "Shavano Park", "Helotes", "Boerne", "Castle Hills"],
        "context": "military community creating transient population, strong Hispanic heritage influencing service expectations, tourism economy, rapid northern suburban growth, cost-conscious market",
    },
    "san-diego": {
        "name": "San Diego",
        "state": "CA",
        "neighborhoods": ["La Jolla", "Del Mar", "Carmel Valley", "North Park", "Hillcrest", "Encinitas", "Chula Vista", "Mission Valley", "Pacific Beach", "Rancho Santa Fe"],
        "context": "MBF's home base, military and biotech industries, beach community lifestyle expectations, cross-border dynamics with Tijuana, La Jolla and Rancho Santa Fe luxury segments",
    },
    "dallas": {
        "name": "Dallas",
        "state": "TX",
        "neighborhoods": ["Uptown", "Highland Park", "University Park", "Preston Hollow", "Deep Ellum", "Oak Lawn", "Bishop Arts", "Plano", "Frisco", "Las Colinas"],
        "context": "corporate relocations driving population growth, Highland Park and Preston Hollow affluence, strong legal market, suburban sprawl requiring local presence, business-friendly culture",
    },
    "austin": {
        "name": "Austin",
        "state": "TX",
        "neighborhoods": ["Downtown", "South Congress", "East Austin", "Westlake", "Tarrytown", "Barton Hills", "Mueller", "The Domain", "Zilker", "Clarksville"],
        "context": "tech boom transforming service expectations, young professional demographic, rapid growth straining existing businesses, keeping Austin culture while scaling, live music and hospitality",
    },
    "seattle": {
        "name": "Seattle",
        "state": "WA",
        "neighborhoods": ["Capitol Hill", "Ballard", "Queen Anne", "Fremont", "South Lake Union", "Bellevue", "Kirkland", "West Seattle", "Green Lake", "Magnolia"],
        "context": "tech-savvy clientele expecting digital-first experiences, Amazon and Microsoft influence on service expectations, rain driving indoor service demand, Eastside growth in Bellevue and Kirkland",
    },
    "miami": {
        "name": "Miami",
        "state": "FL",
        "neighborhoods": ["Brickell", "South Beach", "Coral Gables", "Coconut Grove", "Wynwood", "Aventura", "Bal Harbour", "Key Biscayne", "Pinecrest", "Doral"],
        "context": "bilingual service requirements, luxury hospitality and real estate market, seasonal population fluctuations, Latin American business connections, Brickell financial district concentration",
    },
    "nashville": {
        "name": "Nashville",
        "state": "TN",
        "neighborhoods": ["The Gulch", "Germantown", "12 South", "East Nashville", "Green Hills", "Belle Meade", "Franklin", "Brentwood", "Sylvan Park", "Midtown"],
        "context": "fastest-growing mid-size city, healthcare industry concentration (HCA headquarters), music industry adjacency, tourism-driven hospitality, Franklin and Brentwood affluent suburbs",
    },
    "denver": {
        "name": "Denver",
        "state": "CO",
        "neighborhoods": ["LoDo", "RiNo", "Cherry Creek", "Highlands", "Wash Park", "Capitol Hill", "Stapleton", "Platt Park", "Congress Park", "Sloan's Lake"],
        "context": "outdoor lifestyle creating specific home service patterns, health-conscious population driving wellness demand, altitude and dry climate considerations, tech sector growth, legal marijuana industry",
    },
    "boston": {
        "name": "Boston",
        "state": "MA",
        "neighborhoods": ["Back Bay", "Beacon Hill", "South End", "North End", "Cambridge", "Brookline", "Newton", "Somerville", "Seaport", "Jamaica Plain"],
        "context": "academic and medical center density, old-money neighborhoods with high expectations, seasonal weather driving home service demand, Cambridge innovation corridor, compact walkable neighborhoods",
    },
    "atlanta": {
        "name": "Atlanta",
        "state": "GA",
        "neighborhoods": ["Buckhead", "Midtown", "Virginia Highland", "Inman Park", "Westside", "Sandy Springs", "Decatur", "Brookhaven", "Dunwoody", "Old Fourth Ward"],
        "context": "major corporate headquarters concentration, diverse neighborhoods, Buckhead luxury market, significant medical and legal communities, rapid suburban expansion",
    },
    "portland": {
        "name": "Portland",
        "state": "OR",
        "neighborhoods": ["Pearl District", "Nob Hill", "Hawthorne", "Alberta Arts", "Sellwood", "Laurelhurst", "Beaverton", "Lake Oswego", "Northwest", "Division"],
        "context": "sustainability-focused consumer base, small business density, neighborhood-specific culture, wellness and holistic health demand, Pacific Northwest service expectations",
    },
    "washington-dc": {
        "name": "Washington",
        "state": "DC",
        "neighborhoods": ["Georgetown", "Dupont Circle", "Logan Circle", "Capitol Hill", "Adams Morgan", "Bethesda", "Arlington", "Alexandria", "Foggy Bottom", "Chevy Chase"],
        "context": "government and lobbying industry, international clientele, affluent suburbs in Virginia and Maryland, security-conscious clientele, transient population from administration changes",
    },
    "minneapolis": {
        "name": "Minneapolis",
        "state": "MN",
        "neighborhoods": ["Uptown", "North Loop", "Northeast", "Linden Hills", "Kenwood", "Edina", "St. Paul", "Wayzata", "Lake Calhoun", "Longfellow"],
        "context": "strong community-oriented culture, extreme weather driving home service demand, Scandinavian heritage influencing communication preferences, healthcare concentration, Twin Cities split",
    },
    "tampa": {
        "name": "Tampa",
        "state": "FL",
        "neighborhoods": ["Hyde Park", "Davis Islands", "Westshore", "Channel District", "South Tampa", "Carrollwood", "Temple Terrace", "St. Petersburg", "Clearwater", "Brandon"],
        "context": "retirement and snowbird population, rapid growth from northeast migration, waterfront properties creating specific home service needs, St. Petersburg and Clearwater as distinct markets",
    },
    "charlotte": {
        "name": "Charlotte",
        "state": "NC",
        "neighborhoods": ["Uptown", "SouthPark", "Myers Park", "Dilworth", "NoDa", "Ballantyne", "Cotswold", "South End", "Plaza Midwood", "Matthews"],
        "context": "banking and financial services hub, rapid population growth, strong Southern hospitality expectations, Ballantyne corporate corridor, emerging tech scene",
    },
    "orlando": {
        "name": "Orlando",
        "state": "FL",
        "neighborhoods": ["Winter Park", "College Park", "Dr. Phillips", "Baldwin Park", "Thornton Park", "Lake Nona", "Windermere", "Altamonte Springs", "Oviedo", "Celebration"],
        "context": "tourism-adjacent service businesses, theme park employee population, rapidly growing residential communities, seasonal fluctuations, Winter Park affluence",
    },
    "las-vegas": {
        "name": "Las Vegas",
        "state": "NV",
        "neighborhoods": ["Summerlin", "Henderson", "Downtown", "The Lakes", "Green Valley", "Anthem", "Centennial Hills", "Seven Hills", "Paradise", "Spring Valley"],
        "context": "24/7 service economy, tourism-dependent businesses, rapid suburban growth in Summerlin and Henderson, extreme heat driving home service demand, transient population",
    },
    "san-francisco": {
        "name": "San Francisco",
        "state": "CA",
        "neighborhoods": ["Pacific Heights", "Marina", "Noe Valley", "Mission", "SoMa", "Nob Hill", "Russian Hill", "Presidio Heights", "Cole Valley", "Hayes Valley"],
        "context": "highest income density, tech industry influence, steep service expectations, neighborhood-specific demographics, startup culture, Pacific Heights and Marina affluence",
    },
    "raleigh": {
        "name": "Raleigh",
        "state": "NC",
        "neighborhoods": ["North Hills", "Cameron Village", "Five Points", "Brier Creek", "Cary", "Durham", "Chapel Hill", "Wake Forest", "Morrisville", "Apex"],
        "context": "Research Triangle knowledge economy, rapid growth from tech migration, university-driven demographics, Southern charm with tech sophistication, affordable compared to peer cities",
    },
}

# ---------------------------------------------------------------------------
# VERTICALS
# ---------------------------------------------------------------------------
VERTICALS = {
    "law-firms": {
        "label": "law firms",
        "singular": "law firm",
        "person": "Client",
        "person_lower": "client",
        "industry_page": "/for-law-firms/",
    },
    "medical-practices": {
        "label": "medical practices",
        "singular": "medical practice",
        "person": "Patient",
        "person_lower": "patient",
        "industry_page": "/for-medical-practices/",
    },
    "med-spas": {
        "label": "med spas",
        "singular": "med spa",
        "person": "Client",
        "person_lower": "client",
        "industry_page": "/for-med-spas/",
    },
    "dental-practices": {
        "label": "dental practices",
        "singular": "dental practice",
        "person": "Patient",
        "person_lower": "patient",
        "industry_page": "/for-dental-practices/",
    },
    "home-services": {
        "label": "home service businesses",
        "singular": "home service business",
        "person": "Customer",
        "person_lower": "customer",
        "industry_page": "/for-home-services/",
    },
    "service-businesses": {
        "label": "service businesses",
        "singular": "service business",
        "person": "Customer",
        "person_lower": "customer",
        "industry_page": "/for-service-businesses/",
    },
}

# ---------------------------------------------------------------------------
# UNIQUE CONTENT PER CITY-VERTICAL
# ---------------------------------------------------------------------------
# For each city, we generate unique paragraphs for each vertical using
# city-specific context. These are large content dictionaries.

def get_market_content(city_slug, vert_slug):
    """Return unique H2 'market' section content for a city-vertical page."""
    c = CITIES[city_slug]
    v = VERTICALS[vert_slug]
    city = c["name"]
    state = c["state"]
    hoods = c["neighborhoods"]

    # --- Large unique content map ---
    content_map = {
        # NEW YORK
        ("new-york", "law-firms"): f"""
        <p>{city} is the densest legal market in the United States. From the corporate towers of Midtown and the Financial District to the neighborhood practices serving Brooklyn and Queens, the city supports every legal specialty at an intensity found nowhere else. Thousands of law firms compete for a multilingual, borough-specific clientele that demands responsiveness and results.</p>
        <p>In a market this saturated, the firms that stand apart are those that build lasting relationships with their clients. A personal injury practice on the Upper East Side competes not just on outcomes but on how well the client felt cared for during the process. An immigration firm in Astoria serving Greek and South Asian communities needs to understand the cultural nuances of its clientele. Structured feedback gives these firms a direct line to the perceptions that matter most.</p>
        """,
        ("new-york", "medical-practices"): f"""
        <p>{city}'s medical landscape is shaped by world-renowned hospital systems, private specialty practices, and an enormous patient population spread across five boroughs. From concierge medicine on the Upper East Side to community health centers in the Bronx, the range of care models here is unmatched in the country.</p>
        <p>Patients in {city} are discerning and vocal. They compare experiences across providers constantly, and a single frustrating encounter with scheduling or billing can send them to a competitor down the block. For medical practices in Manhattan, Brooklyn, and beyond, understanding patient sentiment is not optional. It is a survival skill in the most competitive healthcare market in America.</p>
        """,
        ("new-york", "med-spas"): f"""
        <p>The {city} med spa market reflects the city's broader culture of exacting standards and intense competition. From luxury clinics in SoHo and the Upper East Side to trendy locations in Williamsburg and West Village, med spas here cater to a clientele that is well-informed, comparison-driven, and deeply influenced by peer recommendations.</p>
        <p>Client expectations in {city} med spas are shaped by proximity to the fashion and media industries. Clients often arrive having researched specific treatments extensively. They expect not just clinical results but an experience that feels polished from the booking call to the follow-up. Structured feedback helps med spas identify whether the full experience matches the clinical excellence they deliver.</p>
        """,
        ("new-york", "dental-practices"): f"""
        <p>Dental practices in {city} operate in a market where patients have dozens of options within walking distance. In neighborhoods like Midtown, the Financial District, and the Upper East Side, cosmetic dentistry and general practices sit side by side, each competing for the same time-pressed professional clientele. In Brooklyn and Queens, family practices serve diverse communities with specific language and cultural needs.</p>
        <p>Patient retention in {city} dental is driven by convenience, communication, and trust. A practice that runs consistently behind schedule or fails to explain treatment options clearly will lose patients to the practice one subway stop away. Understanding these friction points requires hearing directly from patients in a structured, consistent way.</p>
        """,
        ("new-york", "home-services"): f"""
        <p>Home service businesses in {city} navigate a market unlike any other in the country. The density of apartment buildings, co-ops, and townhouses creates constant demand for plumbing, electrical, HVAC, and renovation work. But building access rules, board approvals, and the logistical challenges of working in a vertical city add layers of complexity that suburban contractors never face.</p>
        <p>Customers in {city} rely heavily on word-of-mouth and neighborhood-specific reputation. A plumber trusted in Brooklyn Heights may be unknown in Astoria. Building supers and doormen serve as informal gatekeepers. For home service businesses, understanding what customers value most, from punctuality in Manhattan to clear pricing in Staten Island, requires a feedback system that captures these local realities.</p>
        """,
        ("new-york", "service-businesses"): f"""
        <p>{city} supports the most diverse concentration of service businesses in America. From financial advisors on Wall Street to wedding planners in Brooklyn, personal trainers in SoHo to accounting firms in Midtown, the common thread is competition. Every service business in {city} competes against dozens of alternatives, and the difference between growing and shrinking often comes down to customer perception.</p>
        <p>The multilingual, multicultural nature of {city}'s clientele means that service expectations vary significantly by neighborhood. A cleaning service in the Upper East Side operates under different expectations than one in Jackson Heights. Structured feedback helps service businesses understand the specific standards of the communities they serve, rather than guessing from generic industry benchmarks.</p>
        """,

        # LOS ANGELES
        ("los-angeles", "law-firms"): f"""
        <p>{city}'s legal market is shaped by the entertainment industry, real estate, and a sprawling metro area that makes neighborhood-level reputation essential. A law firm in Beverly Hills serves a fundamentally different clientele than a firm in Pasadena or Downtown LA, even within the same practice area. The geographic spread of the city means that clients often choose attorneys based on proximity and community standing as much as credentials.</p>
        <p>For {city} law firms, client feedback reveals patterns that would otherwise stay hidden beneath the surface. A family law practice in West Hollywood might discover that clients feel well-represented but uncertain about billing timelines. An employment firm in Santa Monica might learn that its initial intake process feels rushed. These insights drive concrete improvements that strengthen the firm's standing in its specific corner of the Los Angeles market.</p>
        """,
        ("los-angeles", "medical-practices"): f"""
        <p>The {city} medical market is massive and fragmented. Patients in Beverly Hills and Brentwood expect concierge-level attention, while those in the San Fernando Valley and Pasadena prioritize accessibility and affordability. The wellness culture that defines Southern California raises the bar for how medical practices present themselves, from the waiting room ambiance to the follow-up communication after a visit.</p>
        <p>Traffic and commute times play a real role in patient retention in {city}. A patient who has a mediocre experience is unlikely to fight the 405 to return for a follow-up when another practice exists closer to home. Medical practices across LA need to ensure that every interaction, clinical and administrative, meets the expectations of a population that has abundant choices and little tolerance for friction.</p>
        """,
        ("los-angeles", "med-spas"): f"""
        <p>{city} is one of the largest and most competitive med spa markets in the world. The intersection of entertainment, wellness culture, and year-round warm weather creates a population that invests heavily in aesthetic treatments. From boutique clinics in West Hollywood to full-service centers in Brentwood and Beverly Hills, clients come in well-researched and expect premium experiences from start to finish.</p>
        <p>The LA med spa market is also heavily influenced by social media, where a single viral post can drive a surge of new clients or amplify a negative experience. Understanding client sentiment before it becomes a public narrative is critical. Structured feedback provides {city} med spas with an early warning system and a consistent channel for client voices to reach the people who can act on them.</p>
        """,
        ("los-angeles", "dental-practices"): f"""
        <p>Dental practices in {city} contend with the aesthetic expectations of a population that places enormous value on appearance. Cosmetic dentistry is not a specialty here; it is a baseline expectation. From veneer consultations in Beverly Hills to orthodontic work in Pasadena, patients arrive with detailed expectations shaped by media images and peer influence.</p>
        <p>The sprawling geography of {city} means dental practices compete within micro-markets. A practice in Encino draws from a different patient pool than one in Venice, even though both serve the broader LA area. Traffic congestion means patients rarely travel far for routine care. Understanding what keeps patients returning, and what makes them look elsewhere, requires listening at a practice-specific level.</p>
        """,
        ("los-angeles", "home-services"): f"""
        <p>Home service demand in {city} is driven by aging housing stock, year-round outdoor living, and a population that invests heavily in their properties. From pool maintenance in Encino to drought-resistant landscaping in Silver Lake, the range of services reflects the diversity of the city itself. Traffic patterns significantly affect scheduling: a two-hour window in {city} can mean very different things depending on the time of day and the route.</p>
        <p>Customers in {city} expect responsiveness and clear communication about timing. The frustration of a missed service window is amplified in a city where rescheduling might mean waiting days. Home service businesses that systematically collect feedback learn which operational details matter most, whether that is an arrival text, transparent pricing, or post-job cleanup standards.</p>
        """,
        ("los-angeles", "service-businesses"): f"""
        <p>The {city} service economy reflects the city's diversity and scale. Personal trainers, event planners, bookkeepers, and consultants all operate in a market where reputation travels through tight-knit neighborhood networks. A business that earns loyalty in Santa Monica may be invisible in Culver City. The entertainment industry's presence creates a subset of clients with extremely high service expectations and little patience for anything that feels generic.</p>
        <p>For service businesses across the LA metro, structured feedback is a way to bridge the gap between perception and reality. The business owner who believes they are delivering outstanding service may discover that clients find the invoicing confusing or the response time too slow. These are solvable problems, but only if someone surfaces them consistently.</p>
        """,

        # CHICAGO
        ("chicago", "law-firms"): f"""
        <p>{city}'s legal market reflects the city's strong neighborhood identities and Midwestern values. The Loop and River North host major corporate firms, while neighborhood practices in Lincoln Park, Wicker Park, and Hyde Park serve the communities where they are rooted. Chicago clients tend to value straightforward communication and follow-through, and they remember when a firm falls short on either.</p>
        <p>The harsh winters that define {city} life also shape the cadence of legal work. Real estate transactions, personal injury claims from weather-related incidents, and estate planning tend to follow seasonal patterns. Law firms that understand these rhythms and use client feedback to refine their service can build the kind of long-term loyalty that Chicago's relationship-driven market rewards.</p>
        """,
        ("chicago", "medical-practices"): f"""
        <p>{city}'s medical landscape includes some of the nation's most respected hospital systems alongside a dense network of independent practices. The city's neighborhood structure means patients often identify strongly with their local medical providers. A practice in the Gold Coast may draw patients from Streeterville and River North, while a family medicine office in Logan Square serves a different demographic entirely.</p>
        <p>Midwestern service expectations play a significant role in patient satisfaction in {city}. Patients here expect to be treated as people, not numbers. Long wait times, impersonal interactions, or difficulty reaching the office by phone can erode trust quickly in a market where patients have strong community ties and will share their experiences with neighbors and colleagues.</p>
        """,
        ("chicago", "med-spas"): f"""
        <p>The {city} med spa market has grown significantly as the city's young professional population invests in aesthetic treatments. River North, the Gold Coast, and Lincoln Park are home to a concentration of med spas catering to clients who want clinical expertise paired with a welcoming environment. The Midwestern culture of understated self-care creates clients who value results and discretion over flashiness.</p>
        <p>Chicago's seasonal climate also influences med spa demand. Winter months bring increased interest in skin treatments, while summer drives demand for body contouring and pre-event services. Med spas that track client feedback across seasons can anticipate demand shifts and adjust their marketing and staffing accordingly.</p>
        """,
        ("chicago", "dental-practices"): f"""
        <p>Dental practices in {city} benefit from a population that values long-term provider relationships. Unlike coastal markets where patient turnover is common, {city} patients often stay with the same dentist for years, provided the experience remains consistent. This makes patient satisfaction not just a marketing issue but a retention imperative.</p>
        <p>The city's strong neighborhood identities shape dental practice demographics. A practice in Lakeview draws a different patient base than one in West Loop or Streeterville. Understanding the specific expectations of each neighborhood, from appointment scheduling preferences to treatment explanation depth, helps dental practices maintain the trust that keeps patients coming back through Chicago's long winters and beyond.</p>
        """,
        ("chicago", "home-services"): f"""
        <p>{city}'s extreme winters create year-round demand for home services, from furnace repair and pipe insulation in January to roofing and siding work in summer. The city's deep roots in trades and construction mean that homeowners often have strong opinions about craftsmanship and expect work that meets a high standard. A poorly sealed window or a delayed gutter repair during fall can have serious consequences by December.</p>
        <p>For home service businesses in {city}, the difference between a one-time job and a long-term customer relationship often comes down to communication. Did the crew arrive on time? Was the estimate accurate? Did the business follow up after the work was completed? Structured feedback captures these details and turns them into actionable improvements that strengthen a business's standing in its service area.</p>
        """,
        ("chicago", "service-businesses"): f"""
        <p>{city}'s service economy is anchored by the same values that define the city's culture: hard work, directness, and follow-through. From accounting firms in the West Loop to catering businesses in Wicker Park, service providers succeed when they deliver on their promises and treat clients with straightforward respect. The Midwestern preference for substance over style means that flashy marketing cannot substitute for a consistently good experience.</p>
        <p>The city's strong neighborhood networks mean that word-of-mouth remains a powerful force. A financial advisor in Lincoln Park who consistently delivers for clients will benefit from referrals within that community. But a single disappointing experience can travel just as fast. Structured feedback gives service businesses visibility into how clients actually feel, rather than relying on the assumption that no news is good news.</p>
        """,

        # HOUSTON
        ("houston", "law-firms"): f"""
        <p>{city}'s legal market is heavily influenced by the energy sector, with oil and gas disputes, corporate transactions, and regulatory matters forming a significant portion of the city's legal workload. Beyond energy, the Texas Medical Center's proximity fuels a concentration of medical malpractice, personal injury, and healthcare compliance work. Rapid suburban growth in areas like Sugar Land and Katy has also expanded demand for real estate and estate planning services.</p>
        <p>Houston's diverse immigrant communities add another dimension to client expectations. A law firm serving Vietnamese clients in Midtown operates under different communication norms than one representing corporate clients in River Oaks. Understanding these distinctions requires actually listening to clients, not just tracking billable hours and case outcomes.</p>
        """,
        ("houston", "medical-practices"): f"""
        <p>The proximity of the Texas Medical Center, one of the largest medical complexes in the world, shapes the entire {city} medical landscape. Private practices compete with hospital-affiliated clinics for patients who are accustomed to having options. The city's rapid growth means new patients are constantly entering the market, often without established provider relationships and relying on reputation to guide their choices.</p>
        <p>Houston's diverse population creates specific expectations around language, cultural sensitivity, and appointment accessibility. A practice in the Medical Center corridor serves a different patient demographic than one in The Heights or Montrose. Structured patient feedback helps practices understand whether they are meeting the specific needs of their community, not just the clinical standards of their specialty.</p>
        """,
        ("houston", "med-spas"): f"""
        <p>The {city} med spa market has expanded rapidly alongside the city's overall growth. River Oaks, the Galleria area, and Montrose are home to a growing number of aesthetic clinics catering to a clientele that ranges from energy industry executives to young professionals. The year-round warm climate keeps body-focused treatments in demand regardless of season, unlike markets with distinct winter slowdowns.</p>
        <p>Houston's cultural diversity also influences med spa preferences. Client expectations around consultation depth, treatment pacing, and follow-up communication vary across the city's communities. A med spa in River Oaks may need to emphasize exclusivity and personalized attention, while one near the Galleria might focus on efficiency and convenience for clients fitting treatments into busy schedules.</p>
        """,
        ("houston", "dental-practices"): f"""
        <p>Dental practices in {city} serve a rapidly growing population that includes both long-time residents and newcomers drawn by corporate relocations and the energy industry. Suburban growth in Sugar Land, Katy, and The Woodlands has created demand for new family dental practices, while established practices in Montrose and The Heights compete for a younger, urban-oriented patient base.</p>
        <p>The competitive landscape means that patient experience matters as much as clinical quality. A practice that makes scheduling difficult or fails to communicate treatment plans clearly will lose patients to the new office opening down the road. In a city growing as fast as {city}, dental practices need structured feedback to stay ahead of the changing expectations of their evolving patient base.</p>
        """,
        ("houston", "home-services"): f"""
        <p>{city}'s extreme heat creates year-round demand for HVAC services, and the city's flat topography and clay soils contribute to foundation issues that drive a steady stream of repair work. The rapid suburban expansion in Katy, Sugar Land, and surrounding areas means that new construction and renovation work are constant. Flooding events, a recurring reality in {city}, generate urgent demand for restoration and waterproofing services.</p>
        <p>For home service businesses in {city}, customer trust is built through reliability in extreme conditions. When a homeowner's air conditioning fails in August heat, the speed and quality of the response defines the relationship going forward. Structured feedback helps home service businesses understand whether they are meeting the urgency and professionalism standards that Houston homeowners expect.</p>
        """,
        ("houston", "service-businesses"): f"""
        <p>{city}'s business culture is shaped by the energy industry's influence: direct, results-oriented, and relationship-driven. Service businesses from consultants to caterers operate in a market where personal connections open doors and follow-through keeps them open. The city's diverse population, with significant Vietnamese, Mexican, Indian, and Nigerian communities, creates a service economy where cultural awareness is a genuine competitive advantage.</p>
        <p>The rapid growth of suburban communities like Sugar Land and Katy has expanded the geographic footprint of service businesses that once focused on the Inner Loop. Serving clients across a sprawling metro area requires consistent quality regardless of location, and structured feedback ensures that the experience in a new suburb matches the standard set in established neighborhoods.</p>
        """,

        # PHOENIX
        ("phoenix", "law-firms"): f"""
        <p>{city} is one of the fastest-growing metro areas in the country, and its legal market is expanding to match. The influx of retirees from the Midwest and Northeast has created steady demand for estate planning and elder law, while the new construction boom fuels real estate and construction litigation. Scottsdale's luxury market supports high-end estate and family law practices, while suburban communities like Chandler, Gilbert, and Mesa need general practice firms that serve growing families.</p>
        <p>The transient nature of the {city} population means that law firms cannot rely on generational reputation alone. Many clients are new to the area and choose firms based on online presence and early interactions. Structured client feedback helps {city} law firms understand whether they are making strong first impressions and following through with consistent service quality.</p>
        """,
        ("phoenix", "medical-practices"): f"""
        <p>The {city} metro area's retiree population drives significant demand for medical services, particularly in geriatrics, cardiology, and orthopedics. Paradise Valley and Scottsdale support concierge medical practices, while rapidly growing suburbs like Gilbert and Chandler need primary care offices that can handle the volume of new residents arriving every month. The extreme heat also creates a steady flow of heat-related health issues that shape urgent care demand.</p>
        <p>Medical practices in {city} face the challenge of serving both an older, established patient base and a younger population moving to the area for tech and manufacturing jobs. These two groups have different expectations around communication, scheduling, and digital tools. Patient feedback reveals whether a practice is successfully meeting both sets of needs or inadvertently optimizing for one at the expense of the other.</p>
        """,
        ("phoenix", "med-spas"): f"""
        <p>The {city} and Scottsdale corridor is one of the most competitive med spa markets outside of LA and New York. Scottsdale in particular has become a national destination for aesthetic treatments, with clients traveling from out of state for procedures. The local market is driven by an affluent, appearance-conscious population that spends time outdoors year-round, creating consistent demand for skin protection, repair, and rejuvenation treatments.</p>
        <p>Competition in the Scottsdale med spa space means that client retention depends on the complete experience, not just clinical outcomes. Atmosphere, staff demeanor, wait times, and follow-up communication all influence whether a client returns or moves to the clinic that opened last month. Structured feedback gives {city}-area med spas the data they need to maintain the premium experience their market demands.</p>
        """,
        ("phoenix", "dental-practices"): f"""
        <p>The {city} metro area's rapid population growth has created a boom in dental practice openings, particularly in suburban communities like Gilbert, Chandler, and Mesa. New residents arriving from other states bring expectations shaped by their previous providers, and they are actively shopping for a dental home. The retiree population in areas like Sun City and Paradise Valley drives demand for restorative and implant dentistry.</p>
        <p>For dental practices in {city}, the window to earn a new patient's loyalty is narrow. A first visit that feels disorganized or impersonal may be the last, because another new practice is opening within a short drive. Patient feedback after the first and second visits is particularly valuable in this growth market, revealing whether the experience matches the expectations that brought the patient through the door.</p>
        """,
        ("phoenix", "home-services"): f"""
        <p>Extreme heat defines the home service market in {city}. HVAC systems run nearly year-round, and a broken air conditioner in July is not an inconvenience but a genuine emergency. The new construction boom means that landscaping, pool installation, and exterior maintenance businesses have a steady pipeline of work, while the desert climate creates unique demands for roofing, insulation, and outdoor living space construction.</p>
        <p>Homeowners in {city} expect rapid response times, especially during summer months when demand peaks. A home service business that is slow to respond, unclear about pricing, or inconsistent in quality will struggle in a market where new competitors emerge constantly alongside the housing growth. Structured feedback helps these businesses maintain the responsiveness and reliability that the {city} climate demands.</p>
        """,
        ("phoenix", "service-businesses"): f"""
        <p>The {city} service economy is expanding as rapidly as the metro area itself. New residents bring demand for everything from financial planning to pet grooming, and the speed of population growth means that established businesses and newcomers compete on relatively equal footing. Scottsdale's luxury market supports premium service providers, while the broader metro area values efficiency and value.</p>
        <p>The retiree demographic in {city} brings specific service expectations: patience, clarity, and personal attention. Meanwhile, the tech workers and young families settling in Tempe, Chandler, and Gilbert expect digital-first convenience. Service businesses that serve both populations need feedback systems that capture these divergent expectations and help them calibrate their approach accordingly.</p>
        """,

        # PHILADELPHIA
        ("philadelphia", "law-firms"): f"""
        <p>{city}'s legal market is deeply intertwined with the city's historic neighborhoods and tight-knit community networks. Center City and Rittenhouse Square host established corporate and litigation firms, while neighborhood practices in Fishtown, Northern Liberties, and University City serve the communities they are embedded in. The Main Line suburbs support a concentration of estate planning and family law practices serving affluent clients with high expectations.</p>
        <p>Philadelphia's legal community operates through referral networks that reward reputation and consistency. A personal injury firm's standing in Society Hill or Old City depends not just on case results but on how past clients describe their experience to friends, neighbors, and colleagues. Structured client feedback helps firms understand and strengthen the narrative that existing clients share about them.</p>
        """,
        ("philadelphia", "medical-practices"): f"""
        <p>The {city} medical market is defined by the presence of major hospital systems including Penn Medicine, Jefferson, and Temple. Private practices compete for patients who have access to these large systems, making differentiation through patient experience essential. The Main Line and Chestnut Hill support specialty practices with a patient base that expects attentive, personalized care.</p>
        <p>Philadelphia's strong university presence creates a dual patient population: long-term residents with established provider relationships and a rotating student and academic population that is new to the area. Medical practices need to excel at onboarding new patients while maintaining the personalized attention that keeps established patients loyal. Feedback from both groups reveals whether the practice is striking this balance effectively.</p>
        """,
        ("philadelphia", "med-spas"): f"""
        <p>The {city} med spa market is concentrated in Rittenhouse Square, Center City, and the Main Line, serving a clientele that is educated, discerning, and well-connected. Philadelphia's med spa clients tend to value clinical credibility and straightforward communication over luxury trappings. The city's strong community networks mean that word-of-mouth carries significant weight, and a single client's experience can influence decisions across an entire social circle.</p>
        <p>For med spas in {city}, the emphasis on trust and transparency aligns with the city's broader cultural values. Clients want to understand what a treatment involves, what results to expect, and what the realistic timeline looks like. Feedback systems help med spas ensure their consultations and follow-up communications meet these expectations consistently.</p>
        """,
        ("philadelphia", "dental-practices"): f"""
        <p>Dental practices in {city} serve neighborhoods with distinct identities and expectations. A cosmetic dentistry practice in Rittenhouse Square competes differently than a family practice in Manayunk or Chestnut Hill. The city's competitive medical market, anchored by major hospital systems, extends to dentistry, where patients compare their dental experience to the standard set by their broader healthcare interactions.</p>
        <p>Philadelphia's tight-knit neighborhood culture means that dental practices depend on community reputation. A practice in Fishtown or Northern Liberties builds its patient base through local word-of-mouth, and that reputation is shaped by every interaction, from the first phone call to the post-treatment follow-up. Structured patient feedback provides a consistent measure of how well the practice is serving its specific community.</p>
        """,
        ("philadelphia", "home-services"): f"""
        <p>{city}'s housing stock includes centuries-old row homes, Main Line estates, and modern developments, each presenting distinct home service challenges. The seasonal climate drives demand for heating system maintenance in winter and exterior work in summer, creating clear peaks that home service businesses must manage. The city's historic properties require contractors who understand older construction methods, from slate roofing to plaster repair.</p>
        <p>Homeowners in {city} rely on referral networks within their neighborhoods. A good plumber in Society Hill becomes known throughout the neighborhood quickly, but so does a bad experience. For home service businesses, structured feedback provides a proactive way to identify and address issues before they become the negative story circulating through a close-knit community.</p>
        """,
        ("philadelphia", "service-businesses"): f"""
        <p>{city}'s service economy is shaped by the city's neighborhood-centric culture and strong institutional presence. Accounting firms near University City serve the academic community, while financial advisors on the Main Line cater to established wealth. The growing creative and tech scene in Fishtown and Northern Liberties has introduced a new generation of service businesses that blend digital convenience with the personal relationships Philadelphia values.</p>
        <p>In a market where community ties run deep, service businesses in {city} succeed when they demonstrate genuine understanding of their clients' needs. A caterer in Rittenhouse Square operates under different expectations than one in Manayunk, and a financial planner in Chestnut Hill serves a different clientele than one in Center City. Structured feedback helps service businesses calibrate their approach to the specific community they serve.</p>
        """,

        # SAN ANTONIO
        ("san-antonio", "law-firms"): f"""
        <p>{city}'s legal market serves a unique blend of military families, a strong Hispanic community, and a growing suburban population in the northern corridors of Stone Oak, The Dominion, and Boerne. The military presence at Joint Base San Antonio creates a transient population that needs legal services quickly and often works with a firm only once before relocating. Family law, estate planning, and personal injury are significant practice areas across the city.</p>
        <p>The tourism economy centered on the River Walk and the Alamo generates hospitality-related legal needs, from employment disputes to premises liability. {city}'s cost-conscious market means that clients are sensitive to billing practices and value firms that communicate clearly about fees. Structured feedback reveals whether clients feel the value they received matched their expectations, information that is particularly valuable in a price-aware market.</p>
        """,
        ("san-antonio", "medical-practices"): f"""
        <p>{city}'s medical market is shaped by the military healthcare system, which sets expectations for a significant portion of the population. Veterans and military families transitioning to civilian providers bring specific expectations about efficiency and thoroughness that differ from the general population. The city's rapid northern suburban growth in Stone Oak and Alamo Heights has created demand for new primary care and specialty practices.</p>
        <p>The strong Hispanic heritage of {city} means that bilingual service is not a differentiator but an expectation for many practices. Patients value warmth, respect, and clear communication in their healthcare interactions. Medical practices that collect structured feedback from their patient population gain insight into whether they are meeting these culturally informed expectations or falling short in ways they might not otherwise recognize.</p>
        """,
        ("san-antonio", "med-spas"): f"""
        <p>The {city} med spa market is growing as the city's population expands and the aesthetics industry matures beyond its traditional coastal strongholds. Alamo Heights and Stone Oak support a growing number of med spas serving clients who want quality treatments without the premium pricing of markets like Dallas or Houston. The military spouse community represents a significant and often underserved segment of the med spa client base.</p>
        <p>In a cost-conscious market like {city}, med spa clients are attentive to value. They want to understand what they are paying for and what results they can realistically expect. Clear communication before, during, and after treatments builds the trust that drives rebooking in a market where clients are willing to try alternatives if they feel underserved. Feedback systems help {city} med spas maintain the transparency their market demands.</p>
        """,
        ("san-antonio", "dental-practices"): f"""
        <p>Dental practices in {city} serve a population that values family-oriented care and clear communication. The military community's frequent relocations mean that many patients are establishing new dental relationships and evaluating practices based on first impressions. In neighborhoods like Alamo Heights and Terrell Hills, family dental practices compete for patients who expect a personal, community-connected experience.</p>
        <p>The cost-conscious nature of the {city} market means that patients pay close attention to whether the care they receive feels proportional to what they spend. Unexpected charges, unclear treatment plans, or feeling rushed through an appointment can drive patients to look elsewhere. Structured patient feedback helps dental practices in {city} identify these friction points before they result in lost patients.</p>
        """,
        ("san-antonio", "home-services"): f"""
        <p>The {city} home service market is driven by rapid suburban growth in the northern corridors and the ongoing maintenance needs of the city's older neighborhoods. Hot summers create constant HVAC demand, and the Texas climate means that exterior painting, roofing, and landscape maintenance are year-round activities. The military community's frequent relocations generate a steady stream of move-in and move-out related work.</p>
        <p>{city}'s cost-conscious market means that homeowners compare bids carefully and expect transparent pricing. Home service businesses that earn trust through clear communication and consistent quality build the kind of referral networks that sustain growth in this market. Structured feedback provides the data to ensure that every crew and every job meets the standard the business has set for itself.</p>
        """,
        ("san-antonio", "service-businesses"): f"""
        <p>{city}'s service economy reflects the city's blend of military efficiency, Hispanic hospitality traditions, and the pragmatism of a Texas market. Service businesses here succeed when they combine professional execution with genuine warmth. The tourism economy around the River Walk creates a subset of service businesses, from event planners to photographers, that serve both visitors and the local community.</p>
        <p>The rapid growth of northern suburbs like Stone Oak and Boerne has expanded the service area for many {city} businesses, requiring them to maintain quality across a larger geographic footprint. Structured feedback helps service businesses ensure that the experience a customer receives in a new suburban office matches the one delivered at the original location, protecting the reputation they have built over time.</p>
        """,

        # SAN DIEGO
        ("san-diego", "law-firms"): f"""
        <p>As My Business Feedback's home base, {city} is the market we know best. The city's legal landscape is shaped by military families at multiple bases, a growing biotech sector, and the cross-border dynamics of its proximity to Tijuana. Personal injury, immigration, family law, and corporate transactions all represent significant practice areas. The luxury segments of La Jolla and Rancho Santa Fe support estate planning and wealth management practices with high-net-worth clients.</p>
        <p>San Diego's beach community culture creates clients who expect approachability and responsiveness from their attorneys. The laid-back surface of the culture does not mean clients are casual about their legal needs; it means they expect their attorney to be both competent and easy to communicate with. Structured feedback reveals whether a firm's communication style matches the expectations of its specific {city} clientele.</p>
        """,
        ("san-diego", "medical-practices"): f"""
        <p>{city}'s medical landscape serves an active, health-conscious population that expects modern facilities and responsive communication. The biotech corridor creates a patient population that is scientifically literate and asks informed questions about treatment options. Military families at MCAS Miramar and Naval Base San Diego transition to civilian providers with specific expectations shaped by military healthcare efficiency.</p>
        <p>The geographic spread from Chula Vista to Encinitas means that medical practices serve distinct communities with different demographics and needs. A practice in La Jolla serves a different patient base than one in North Park or Mission Valley. As MBF's local market, we understand these neighborhood-level distinctions and help {city} medical practices collect feedback that reflects the specific communities they serve.</p>
        """,
        ("san-diego", "med-spas"): f"""
        <p>{city}'s med spa market thrives on the city's outdoor lifestyle and year-round sun exposure. Clients in La Jolla, Del Mar, and Carmel Valley invest in skin health as a practical necessity, not just a cosmetic choice. The beach community culture creates a clientele that values natural-looking results and expects providers to understand the specific dermatological challenges of living in a sun-intensive climate.</p>
        <p>As MBF's home market, we have firsthand insight into what {city} med spa clients prioritize. The competition is concentrated in the coastal communities, where clients have immediate access to multiple options. Retention depends on the complete experience: from the ease of booking to the quality of follow-up care. Structured feedback helps med spas in Pacific Beach, Hillcrest, and across the county maintain the standards their clientele expects.</p>
        """,
        ("san-diego", "dental-practices"): f"""
        <p>Dental practices in {city} serve a population that is active, health-conscious, and accustomed to high-quality healthcare. The military presence brings a steady stream of new patients who are establishing civilian dental care for the first time. La Jolla and Rancho Santa Fe support cosmetic dentistry practices with clients who have specific aesthetic expectations, while family practices in Carmel Valley and Encinitas serve growing suburban communities.</p>
        <p>As our home market, we understand the {city} dental landscape at a granular level. Patient expectations here are shaped by the overall quality of healthcare in the region, which means dental practices are judged not just against other dentists but against every healthcare interaction a patient has. Structured feedback helps {city} dental practices meet this high bar consistently.</p>
        """,
        ("san-diego", "home-services"): f"""
        <p>The {city} home service market is shaped by the coastal climate, which creates specific demands for exterior maintenance, HVAC efficiency, and drought-conscious landscaping. Properties in La Jolla and Rancho Santa Fe require premium service standards, while the military housing community creates steady demand for move-in preparation and turnover maintenance. The city's topography, with canyon homes and hillside properties, adds complexity to many standard home service jobs.</p>
        <p>As MBF's home base, we work with {city} home service businesses that understand the local market intimately. The expectation in beach communities like Pacific Beach and Encinitas differs from the standards in inland areas like Mission Valley or Chula Vista. Structured feedback ensures that service quality remains consistent across the diverse neighborhoods that make up the {city} metro area.</p>
        """,
        ("san-diego", "service-businesses"): f"""
        <p>{city}'s service economy is influenced by the military community, the biotech industry, and a lifestyle-oriented population that values quality and convenience. From financial advisors in La Jolla to wedding planners in Del Mar, service businesses here operate in a market where personal reputation travels quickly through tight-knit community networks. The cross-border relationship with Tijuana also creates a bilingual service demand in many parts of the county.</p>
        <p>As our hometown market, we see the {city} service landscape with particular clarity. The businesses that thrive here are the ones that listen carefully to their clients and adapt to the specific expectations of their neighborhood. Structured feedback provides the data to do this systematically, rather than relying on occasional conversations or online reviews alone.</p>
        """,

        # DALLAS
        ("dallas", "law-firms"): f"""
        <p>{city}'s legal market has grown significantly alongside the corporate relocations that continue to reshape the metro area. Highland Park and Preston Hollow support estate planning and wealth management practices serving high-net-worth clients, while the business-friendly culture of Texas fuels corporate law, real estate transactions, and employment disputes across the metro. Suburban growth in Plano, Frisco, and Las Colinas has expanded demand for family law and general practice firms.</p>
        <p>The {city} market rewards firms that combine professional excellence with the relationship-driven culture of Texas business. A firm that delivers strong results but fails to maintain personal connections will lose clients to competitors who do both. Structured client feedback helps {city} law firms understand how their clients perceive not just the legal outcome but the quality of the relationship throughout the engagement.</p>
        """,
        ("dallas", "medical-practices"): f"""
        <p>{city}'s medical landscape reflects the city's rapid growth and affluent demographics. Highland Park and University Park support concierge and specialty practices, while the suburban expansion in Plano and Frisco has created a boom in new primary care, pediatrics, and dermatology offices. The corporate relocation pipeline brings new patients who are actively searching for providers and evaluating practices based on early experiences.</p>
        <p>In a market where new patients arrive constantly, {city} medical practices need to excel at first impressions while maintaining the quality that retains existing patients. Patient feedback after the first visit is particularly valuable in this growth-driven market, revealing whether the intake process, wait times, and initial provider interaction meet the expectations of newcomers who have abundant alternatives.</p>
        """,
        ("dallas", "med-spas"): f"""
        <p>The {city} med spa market reflects the city's culture of investment in personal appearance and its concentration of affluent communities. Uptown, Highland Park, and Preston Hollow are home to med spas that serve a sophisticated clientele accustomed to high-end service. The suburban growth in Plano and Frisco has created a secondary market of med spas serving a younger, family-oriented demographic that is newer to aesthetic treatments.</p>
        <p>Dallas clients tend to value efficiency and results, reflecting the business-oriented culture of the city. A med spa that wastes a client's time with a poorly organized booking system or unclear pre-treatment communication will lose ground to competitors who respect the client's schedule. Structured feedback helps {city} med spas identify these operational details that influence retention as much as treatment quality.</p>
        """,
        ("dallas", "dental-practices"): f"""
        <p>Dental practices in {city} benefit from a growing population that brings diverse expectations and a competitive landscape that drives innovation. Highland Park and University Park support cosmetic dentistry and orthodontics practices with affluent patient bases, while Plano and Frisco see steady demand for family dentistry in new residential developments. The business-friendly culture of Texas encourages dental entrepreneurs, which means competition continues to increase.</p>
        <p>The corporate relocations feeding {city}'s growth bring patients who compare their new dental experience to their previous provider, wherever that was. A practice that feels disorganized or impersonal next to a polished previous experience will struggle to retain these newcomers. Structured feedback gives {city} dental practices a clear view of how they measure up in the eyes of both established patients and recent arrivals.</p>
        """,
        ("dallas", "home-services"): f"""
        <p>The {city} home service market is driven by new construction, suburban sprawl, and the Texas climate. Hot summers create constant HVAC demand, while the city's mix of new builds and older homes in neighborhoods like Highland Park and Oak Lawn generates a wide range of repair and renovation work. The rapid growth of Frisco, Plano, and Las Colinas means that home service businesses can build substantial customer bases in developing areas.</p>
        <p>{city}'s business-friendly culture extends to how homeowners evaluate service providers. They expect professionalism, clear communication, and fair pricing. A home service business that delivers inconsistent quality across its expanding service area will struggle to maintain the reputation that fueled its initial growth. Structured feedback ensures that the experience in a new Frisco development matches the standard set in established {city} neighborhoods.</p>
        """,
        ("dallas", "service-businesses"): f"""
        <p>The {city} service economy reflects the city's identity as a business hub. Financial advisors, marketing consultants, and professional service firms compete in a market shaped by corporate culture and relationship-driven dealmaking. The Preston Hollow and Highland Park affluent communities support premium service providers, while the broader metro area values efficiency and results-oriented delivery.</p>
        <p>The steady stream of corporate relocations into {city} introduces new service clients who bring expectations from their previous markets, often from the coasts. These transplants compare their {city} experiences against the standards of New York, San Francisco, or Chicago. Structured feedback helps service businesses understand whether they are meeting the expectations of both long-time Texans and the newcomers who are reshaping the {city} market.</p>
        """,

        # AUSTIN
        ("austin", "law-firms"): f"""
        <p>{city}'s legal market has been transformed by the tech boom that has reshaped the city's demographics. Employment law, intellectual property, and startup-related transactions have grown alongside the influx of tech companies and their employees. Traditional practice areas like family law and estate planning remain strong, but the client base is increasingly younger, tech-literate, and accustomed to fast, digital-first communication.</p>
        <p>The culture of {city} creates clients who expect informality without sacrificing competence. A law firm that communicates too stiffly may feel out of step with the South Congress and East Austin ethos, while one that is too casual may not inspire confidence in Westlake or Tarrytown. Structured client feedback helps {city} law firms find the right tone for their specific clientele, an increasingly important differentiator in a market where newcomers are still finding their preferred providers.</p>
        """,
        ("austin", "medical-practices"): f"""
        <p>{city}'s medical market is growing as fast as the city itself, with new practices opening to serve the influx of tech workers and young families. The population's health-conscious orientation, influenced by the outdoor culture and active lifestyle that define Austin, creates demand for providers who engage in preventive care and wellness-oriented practice. Westlake and Tarrytown support established practices, while East Austin and Mueller serve a younger, rapidly growing demographic.</p>
        <p>The tech-influenced expectations of {city} patients include digital scheduling, prompt response to portal messages, and transparent communication about costs and treatment options. Medical practices that rely on outdated systems or phone-heavy workflows risk losing patients who are accustomed to the convenience standards set by the tech companies many of them work for. Patient feedback reveals which operational gaps matter most to this increasingly demanding population.</p>
        """,
        ("austin", "med-spas"): f"""
        <p>The {city} med spa market reflects the city's blend of health consciousness and growing affluence. The young professional demographic that has arrived with the tech boom has brought increased demand for aesthetic treatments, particularly among clients who are newer to med spa services and value education and transparency in the consultation process. Westlake and The Domain have emerged as hubs for premium med spa experiences.</p>
        <p>{city}'s culture prizes authenticity, and this extends to how clients evaluate med spas. A hard-sell approach that might work in other markets can feel off-putting in Austin. Clients here respond to providers who take time to explain options, present realistic expectations, and follow up genuinely after treatments. Structured feedback helps {city} med spas ensure their approach aligns with the city's values while still growing their client base effectively.</p>
        """,
        ("austin", "dental-practices"): f"""
        <p>Dental practices in {city} serve a population that has grown dramatically in the past decade. New residents from California, the Northeast, and other tech hubs bring expectations shaped by their previous dental experiences, and they are actively choosing providers in a market with increasing options. Family practices in Mueller and Zilker compete with cosmetic-focused offices in Westlake and The Domain for a patient base that values both quality and convenience.</p>
        <p>The rapid growth of {city} means that dental practices have a continuous opportunity to add new patients, but also face continuous pressure to retain them. A patient who has a subpar first visit has numerous alternatives within a short drive. Structured feedback after initial visits helps {city} dental practices identify and correct the issues that determine whether a new patient becomes a long-term one.</p>
        """,
        ("austin", "home-services"): f"""
        <p>{city}'s rapid growth has strained the home service market, creating both opportunity and challenge for businesses in plumbing, HVAC, electrical, and renovation. The influx of new construction in areas like Mueller and The Domain generates steady work, while older homes in Tarrytown and Clarksville require the specialized knowledge that comes with maintaining mid-century properties. The Texas heat makes air conditioning service a year-round necessity.</p>
        <p>The tech-savvy {city} customer expects modern communication from home service businesses: online booking, text updates, and prompt follow-up. A business that relies solely on phone calls and paper invoices may struggle to meet the expectations of a population accustomed to the convenience standards of their employers. Structured feedback helps {city} home service businesses identify which operational upgrades matter most to their evolving customer base.</p>
        """,
        ("austin", "service-businesses"): f"""
        <p>{city}'s service economy has been reshaped by the same tech boom that has transformed the city's demographics. New service businesses, from boutique fitness studios to creative agencies, compete alongside established providers in a market where the client base is younger, more demanding, and more willing to switch providers than in traditional Texas markets. South Congress and East Austin's creative corridor drives a subset of the service economy rooted in the city's cultural identity.</p>
        <p>Keeping the character of Austin while scaling is a challenge that service businesses face daily. The personal touch that built a catering company or a bookkeeping firm can erode as the business grows to serve The Domain's corporate tenants alongside Zilker's neighborhood clients. Structured feedback helps service businesses monitor whether growth is diluting the quality that earned their initial reputation.</p>
        """,

        # SEATTLE
        ("seattle", "law-firms"): f"""
        <p>{city}'s legal market is heavily influenced by the tech industry, with intellectual property, employment law, and corporate transactions forming a significant share of the legal workload. The presence of Amazon, Microsoft, and a broad startup ecosystem creates a client base that is accustomed to fast, efficient communication and is intolerant of outdated processes. Capitol Hill and Ballard support smaller practices serving the neighborhoods, while downtown and South Lake Union house larger firms.</p>
        <p>The tech-savvy nature of {city}'s clientele means that law firms here face higher expectations for digital communication, document management, and responsiveness than firms in many other markets. A client who communicates through Slack at work expects a similar level of responsiveness from their attorney. Structured feedback helps {city} law firms understand whether they are meeting these high communication expectations or falling behind the standard their clients experience elsewhere in their lives.</p>
        """,
        ("seattle", "medical-practices"): f"""
        <p>{city}'s medical market serves a tech-industry population that expects digital-first experiences, from online scheduling to patient portal communication. The rain-driven indoor lifestyle of the Pacific Northwest creates demand for mental health services, dermatology, and wellness-oriented primary care. Bellevue and Kirkland on the Eastside have seen significant medical practice growth, driven by the tech workers who have settled there for shorter commutes.</p>
        <p>Patients in {city} are typically well-informed and arrive at appointments with research in hand. They expect providers to engage with their questions rather than dismissing them. Medical practices that create space for this kind of dialogue, and that follow up consistently after visits, build stronger patient relationships. Structured feedback reveals whether these expectations are being met and where the communication gaps exist.</p>
        """,
        ("seattle", "med-spas"): f"""
        <p>The {city} med spa market caters to a tech-industry clientele that approaches aesthetic treatments with the same research intensity they bring to their professional lives. Clients in Capitol Hill, Queen Anne, and Bellevue are well-informed about treatment options and expect data-driven consultations. The Pacific Northwest emphasis on natural, understated aesthetics means that {city} med spa clients typically prefer subtle results over dramatic transformations.</p>
        <p>The growth of the Eastside market in Bellevue and Kirkland has created a secondary hub for med spa services, serving tech workers who prefer not to cross the bridge for treatments. This geographic split means that {city}-area med spas must maintain consistent quality and branding across locations that serve slightly different demographics. Structured feedback ensures that the experience at each location meets the expectations of its specific client base.</p>
        """,
        ("seattle", "dental-practices"): f"""
        <p>Dental practices in {city} serve a population that expects modern technology, clear communication, and efficient scheduling. The tech industry influence means that patients here are more likely to research procedures online before their appointment and less tolerant of practices that use outdated systems or communicate primarily by phone. Neighborhoods like Ballard, Fremont, and Green Lake support family practices, while downtown and Bellevue are home to cosmetic-focused offices.</p>
        <p>The Eastside growth in Bellevue and Kirkland has created significant demand for new dental practices, while established offices in {city} proper compete to retain patients who might move east for a shorter commute. Patient feedback helps dental practices in both areas understand what drives loyalty: is it the provider relationship, the convenience of the location, or the quality of the digital experience between visits?</p>
        """,
        ("seattle", "home-services"): f"""
        <p>The {city} climate drives specific home service demands: constant rain creates gutter, roofing, and moisture management needs, while mild temperatures mean HVAC systems focus on heating efficiency rather than cooling capacity. The city's aging housing stock in neighborhoods like Queen Anne, Magnolia, and West Seattle requires contractors who understand older construction, while new development in South Lake Union and the Eastside brings modern building maintenance needs.</p>
        <p>Homeowners in {city} expect the same digital convenience from their home service providers that they experience in their professional lives. Online booking, real-time arrival updates, and digital invoicing are baseline expectations, not differentiators. Home service businesses that systematically collect feedback learn which aspects of their digital and in-person experience are meeting these high standards and which need improvement.</p>
        """,
        ("seattle", "service-businesses"): f"""
        <p>The {city} service economy is shaped by the tech industry's influence on expectations. Service businesses from financial advisors to house cleaners compete in a market where clients expect transparency, efficiency, and responsive communication. The Amazon effect, where customers expect fast delivery and easy returns, has spilled into how {city} residents evaluate every service interaction.</p>
        <p>The geographic split between {city} proper and the Eastside creates distinct micro-markets. A service business that performs well in Fremont may need to adapt its approach for Bellevue clients who have different expectations and price sensitivity. Structured feedback helps service businesses navigate these differences and maintain quality across the metro area's diverse neighborhoods and demographics.</p>
        """,

        # MIAMI
        ("miami", "law-firms"): f"""
        <p>{city}'s legal market is defined by its international connections, bilingual requirements, and the concentration of real estate and financial services in Brickell and downtown. Immigration law, international business transactions, and real estate litigation are dominant practice areas, reflecting the city's role as a gateway to Latin America. Coral Gables and Coconut Grove support established firms with deep community roots, while Brickell's towers house firms focused on cross-border commerce.</p>
        <p>Bilingual capability is not a bonus in {city}; it is a requirement for firms serving a significant portion of the market. But language is just the beginning. Client expectations around communication frequency, personal relationships, and family involvement in legal decisions reflect Latin American business culture. Structured feedback helps {city} law firms understand whether they are meeting these culturally specific expectations or inadvertently alienating clients through assumptions about how legal relationships should work.</p>
        """,
        ("miami", "medical-practices"): f"""
        <p>The {city} medical market serves a diverse population with significant seasonal fluctuations. Snowbirds from the Northeast and international patients from Latin America supplement the year-round resident population, creating demand patterns that shift with the calendar. Practices in Coral Gables, Aventura, and Pinecrest serve affluent, long-term residents, while Brickell and South Beach attract a younger, more transient patient base.</p>
        <p>Bilingual service delivery is essential for {city} medical practices serving the city's large Spanish-speaking population. Beyond language, patient expectations around communication warmth, family involvement in care decisions, and follow-up frequency reflect the cultural values of the community. Structured feedback helps practices understand whether their service model resonates with the specific cultural expectations of their patient population.</p>
        """,
        ("miami", "med-spas"): f"""
        <p>The {city} med spa market thrives on the city's emphasis on appearance, year-round warm weather, and international sophistication. Brickell, South Beach, and Bal Harbour are home to med spas that cater to a clientele comfortable with aesthetic treatments and willing to invest in premium experiences. The international client base, particularly from Latin America, brings specific treatment preferences and expectations that differ from domestic clients.</p>
        <p>Seasonal population fluctuations in {city} create unique business challenges for med spas. The winter surge of seasonal residents and tourists provides a revenue boost but requires staff scalability and consistent quality under increased volume. Structured feedback during peak and off-peak seasons reveals whether the experience holds up when the practice is busy, and whether year-round clients feel the same level of attention regardless of how full the schedule is.</p>
        """,
        ("miami", "dental-practices"): f"""
        <p>Dental practices in {city} serve a bilingual population that expects cultural sensitivity and communication in the language they are most comfortable with. Cosmetic dentistry is a significant segment in areas like Brickell and Coral Gables, where appearance standards are high and clients are willing to invest in smile aesthetics. Family practices in Pinecrest and Doral serve a more diverse demographic with an emphasis on accessibility and convenience.</p>
        <p>The seasonal population of {city} affects dental practices differently than most markets. Snowbird patients may need to maintain continuity of care between their {city} dentist and their northern provider. International patients visiting for treatment create spikes in demand for specific procedures. Structured feedback helps dental practices manage these complexities while maintaining a consistent standard for their year-round patient base.</p>
        """,
        ("miami", "home-services"): f"""
        <p>The {city} home service market is shaped by waterfront property maintenance, hurricane preparedness, and the demands of a tropical climate. Impact windows, roofing, pool maintenance, and landscape services are year-round necessities, and the city's high-end residential market in Key Biscayne, Coral Gables, and Bal Harbour creates demand for premium service providers. The seasonal population influx also drives cleaning, maintenance, and property management services.</p>
        <p>Homeowners in {city} often manage properties as investments, particularly in Brickell and South Beach, where short-term rentals and seasonal usage are common. This creates a customer base that evaluates home service businesses on reliability and consistency, since they may not be physically present to oversee every job. Structured feedback provides these absentee property owners with confidence that their service providers are delivering the quality they expect.</p>
        """,
        ("miami", "service-businesses"): f"""
        <p>{city}'s service economy reflects the city's international character and its role as a gateway between the Americas. Financial services, real estate support, hospitality consulting, and personal services all thrive in a market where bilingual capability and cultural fluency are essential. The Brickell financial district concentrates professional services, while Wynwood and Coconut Grove support a creative service economy.</p>
        <p>The Latin American business connections that define {city}'s economy create a client base that values personal relationships and loyalty. Service businesses that invest in understanding their clients' cultural backgrounds and communication preferences build deeper connections than those that treat the market as homogeneous. Structured feedback helps service businesses in {city} maintain the personal touch that drives retention in a relationship-first market.</p>
        """,

        # NASHVILLE
        ("nashville", "law-firms"): f"""
        <p>{city}'s legal market is shaped by the healthcare industry (HCA Healthcare's headquarters is here), the music and entertainment sector, and the rapid population growth that has made Nashville one of the most-watched cities in America. The Gulch and Germantown have attracted firms serving startups and creative businesses, while Franklin and Brentwood support estate planning and family law practices serving affluent suburban families.</p>
        <p>The pace of growth in {city} means that law firms are serving an increasing number of clients who are new to the city and new to Tennessee's legal landscape. These clients bring expectations from their previous markets and are actively evaluating which firm will become their long-term legal home. First impressions matter enormously, and structured client feedback helps {city} firms understand how their intake process, communication style, and follow-through compare to what these new residents have experienced elsewhere.</p>
        """,
        ("nashville", "medical-practices"): f"""
        <p>As the home of HCA Healthcare, {city} has a healthcare industry concentration that shapes the medical landscape for the entire metro area. Private practices compete with hospital-affiliated clinics in a market where patients are accustomed to institutional efficiency but may prefer the personal touch of an independent provider. Green Hills and Belle Meade support specialty practices, while East Nashville and Germantown attract younger providers opening practices for a growing millennial population.</p>
        <p>The tourism industry that drives much of Nashville's economy also affects medical practices. Urgent care and walk-in clinics serving tourists and visiting performers supplement the primary care market. For established practices, the challenge is maintaining the attentive, personal experience that retains year-round patients while the city's infrastructure strains under growth. Structured patient feedback helps practices keep a pulse on whether that personal touch is holding up.</p>
        """,
        ("nashville", "med-spas"): f"""
        <p>The {city} med spa market has grown alongside the city's transformation from a mid-size Southern city into a national destination. The music industry's presence creates a clientele that is image-conscious and comfortable with aesthetic treatments. The Gulch, 12 South, and Green Hills are home to a growing number of med spas serving both the creative community and the young professionals drawn by Nashville's economic boom.</p>
        <p>The affluent suburbs of Franklin and Brentwood represent another significant market segment, with clients who prefer a more private, residential-area setting for their treatments. Structured feedback helps Nashville med spas understand whether their atmosphere, communication style, and follow-up approach resonate with their specific clientele, whether that is the music industry crowd in Midtown or the suburban families in Franklin.</p>
        """,
        ("nashville", "dental-practices"): f"""
        <p>Dental practices in {city} are riding the wave of population growth that has defined the city's recent history. New residents from across the country are establishing dental care, creating a steady stream of patients evaluating practices based on first impressions. The music industry and its associated smile-consciousness drive cosmetic dentistry demand in Midtown and East Nashville, while family practices in Franklin and Brentwood serve the suburban growth.</p>
        <p>Nashville's Southern hospitality culture sets a high bar for patient experience. Patients here expect warmth, friendliness, and genuine care from their dental team. A practice that is clinically excellent but feels impersonal will lose ground to one that combines quality care with the welcoming atmosphere that {city} residents value. Structured patient feedback measures whether a practice is delivering on both fronts.</p>
        """,
        ("nashville", "home-services"): f"""
        <p>{city}'s home service market has been supercharged by the construction boom that accompanies the city's rapid growth. New homes in Brentwood, Franklin, and east of the city create demand for landscaping, smart home installation, and ongoing maintenance. The older housing stock in East Nashville and Sylvan Park generates renovation and repair work as new residents update homes in established neighborhoods.</p>
        <p>The hospitality-driven culture of {city} extends to how homeowners evaluate home service businesses. They expect friendliness, clear communication, and respect for their property. A contractor who delivers excellent work but leaves a mess or communicates poorly about timing will struggle in a market where courtesy is as important as craftsmanship. Structured feedback helps home service businesses in {city} ensure they are meeting both standards.</p>
        """,
        ("nashville", "service-businesses"): f"""
        <p>The {city} service economy has expanded dramatically as the city's population has grown. Event planners, personal trainers, financial advisors, and creative professionals all compete in a market that is simultaneously Southern and increasingly cosmopolitan. The tourism industry creates a layer of service demand that overlaps with the local market, as businesses serve both visitors and the growing resident base.</p>
        <p>Nashville's culture of hospitality creates a baseline expectation for service businesses that is higher than many other markets. Clients expect to feel valued and respected, and they remember when they do not. In a city where personal recommendations still carry significant weight, the experience of each individual client matters enormously. Structured feedback ensures that service businesses hear from their clients consistently, not just when something goes very right or very wrong.</p>
        """,

        # DENVER
        ("denver", "law-firms"): f"""
        <p>{city}'s legal market reflects the city's unique blend of outdoor culture, tech sector growth, and the regulatory landscape created by the legal marijuana industry. Cannabis law, environmental regulation, and real estate transactions are significant practice areas alongside the traditional mainstays of personal injury and family law. Cherry Creek and the Highlands support established practices, while LoDo and RiNo attract younger firms serving the startup community.</p>
        <p>The health-conscious, active culture of {city} creates clients who value efficiency and directness in their legal relationships. They want their attorneys to communicate clearly, respect their time, and be transparent about costs. The altitude and dry climate may be unique to Colorado, but the expectation for straightforward legal service is universal. Structured feedback helps {city} law firms confirm that their communication style and service delivery match what their specific clientele values.</p>
        """,
        ("denver", "medical-practices"): f"""
        <p>{city}'s medical market serves a health-conscious population that takes an active interest in their care. Altitude-related health considerations, an active outdoor lifestyle, and a growing interest in integrative medicine create a patient population that asks questions, researches treatments, and expects providers to engage with their perspective. Cherry Creek and Wash Park support specialty practices, while Capitol Hill and Stapleton serve a mix of young professionals and families.</p>
        <p>The tech sector growth in {city} has brought patients who expect digital convenience from their healthcare providers. Online scheduling, telehealth options, and responsive patient portal communication are not bonuses but expected features. Medical practices that lag in these areas risk losing patients to competitors who deliver the modern experience that Denver's growing tech workforce takes for granted. Structured feedback reveals where these gaps exist.</p>
        """,
        ("denver", "med-spas"): f"""
        <p>The {city} med spa market is driven by a health-conscious population that views aesthetic treatments as part of a broader wellness approach. Cherry Creek is the epicenter of the luxury med spa market, with clients who appreciate clinical sophistication and a relaxed, Colorado-appropriate atmosphere. The altitude and dry climate create specific skin care needs, from intense hydration treatments to UV damage repair, that differentiate the Denver market from coastal cities.</p>
        <p>Wellness culture in {city} means that med spa clients often arrive already engaged in fitness, nutrition, and holistic health practices. They want their aesthetic provider to understand this broader context and to integrate treatments into a lifestyle-oriented framework rather than treating them in isolation. Structured feedback helps {city} med spas understand whether their consultation approach resonates with this wellness-minded clientele.</p>
        """,
        ("denver", "dental-practices"): f"""
        <p>Dental practices in {city} serve an active, outdoors-oriented population that values both function and aesthetics. Sports-related dental injuries are more common here than in many markets, creating demand for restorative and emergency dentistry alongside routine care. Cherry Creek supports cosmetic-focused practices, while family dentistry thrives in the growing neighborhoods of Stapleton, Sloan's Lake, and Platt Park.</p>
        <p>The {city} population's health-conscious orientation means patients are attentive to how their dental care fits into their broader wellness routine. They ask questions about materials, treatment alternatives, and preventive strategies. Dental practices that take time to educate and engage with these questions build stronger patient loyalty. Structured feedback reveals whether the educational component of the patient experience is meeting the expectations of Denver's informed population.</p>
        """,
        ("denver", "home-services"): f"""
        <p>The {city} home service market is shaped by the outdoor lifestyle, with significant demand for deck and patio construction, outdoor living spaces, and landscaping that thrives at altitude. The dry climate creates specific challenges for exterior wood maintenance and roofing, while variable mountain weather means that heating system reliability is non-negotiable. New construction in Stapleton and infill development in RiNo and the Highlands generate steady renovation work.</p>
        <p>Homeowners in {city} often invest heavily in their homes as extensions of their outdoor lifestyle, and they evaluate home service businesses through that lens. A deck builder who understands UV exposure at altitude, or a landscaper who designs for water conservation, earns trust that translates into long-term relationships. Structured feedback helps home service businesses in {city} confirm that their specialized local knowledge is being recognized and valued by customers.</p>
        """,
        ("denver", "service-businesses"): f"""
        <p>The {city} service economy reflects the city's blend of outdoor culture, tech sector growth, and entrepreneurial energy. From fitness studios in RiNo to financial advisors in Cherry Creek, service businesses here compete for a clientele that is active, health-conscious, and increasingly affluent. The legal marijuana industry has also created a new category of service businesses, from compliance consultants to specialized accountants, that are unique to Colorado.</p>
        <p>Denver's culture values authenticity and substance. Service businesses that feel corporate or generic may struggle to connect with a clientele that prizes genuine relationships and local identity. Structured feedback helps service businesses understand whether their brand, communication style, and service delivery align with the values of the {city} market, and where adjustments might strengthen their connection with clients.</p>
        """,

        # BOSTON
        ("boston", "law-firms"): f"""
        <p>{city}'s legal market is anchored by its academic and medical institutions, its old-money neighborhoods, and the Cambridge innovation corridor. The concentration of universities, hospitals, and biotech companies creates demand for intellectual property, employment law, and corporate transactions alongside traditional practice areas. Back Bay and Beacon Hill host established firms with generations of reputation, while Seaport and Cambridge attract firms aligned with the innovation economy.</p>
        <p>Client expectations in {city} are shaped by the city's educated, discerning population. Clients here tend to be well-informed about legal processes and intolerant of vagueness or delay. The compact, walkable nature of {city}'s neighborhoods means that competing firms are often within blocks of each other, making differentiation through service quality essential. Structured feedback helps {city} law firms understand how they compare in the eyes of clients who have no shortage of alternatives.</p>
        """,
        ("boston", "medical-practices"): f"""
        <p>The {city} medical landscape is defined by renowned hospital systems including Mass General, Brigham and Women's, and Beth Israel. Private practices compete for patients who have access to these institutions, making patient experience a critical differentiator when clinical quality is table stakes. Back Bay, Brookline, and Newton support specialty practices serving an affluent patient base with exacting standards.</p>
        <p>The academic density of {city} creates a patient population that is highly educated and research-oriented. Patients arrive at appointments having read the latest studies and expect their providers to engage at that level. The seasonal weather, with harsh winters and brief summers, also drives specific healthcare demand patterns from flu season to seasonal affective disorder. Structured feedback helps practices understand whether they are meeting the high intellectual and service expectations of the Boston patient.</p>
        """,
        ("boston", "med-spas"): f"""
        <p>The {city} med spa market serves an educated, high-income population that values clinical credibility above all else. Back Bay, Beacon Hill, and the South End are home to med spas that emphasize medical credentials and evidence-based treatments. The academic culture of the city means that clients research treatments thoroughly and expect providers to cite specific evidence for recommended procedures.</p>
        <p>Boston's old-money aesthetic creates clients who prefer subtle, natural-looking results. The cultural norm here is understatement, which influences how consultations should be framed and what treatment recommendations should emphasize. Structured feedback helps {city} med spas ensure their clinical communication style and treatment philosophy align with the expectations of a clientele that values sophistication and discretion.</p>
        """,
        ("boston", "dental-practices"): f"""
        <p>Dental practices in {city} compete in a market where the overall quality of healthcare is among the highest in the nation. Patients who receive care at Mass General or Brigham and Women's bring those service expectations to their dental provider. Practices in Back Bay, Brookline, and Newton serve a patient base that values both clinical excellence and a polished, professional experience.</p>
        <p>The student and academic population adds a layer of complexity to {city}'s dental market. University-affiliated neighborhoods see a rotating patient base, while established neighborhoods like Beacon Hill and Jamaica Plain provide long-term patient relationships. Structured feedback helps dental practices calibrate their approach for different segments and ensure that the high expectations of the Boston market are met consistently.</p>
        """,
        ("boston", "home-services"): f"""
        <p>{city}'s historic housing stock and harsh seasonal weather create a demanding home service market. Brownstone maintenance in Back Bay, heating system reliability in Beacon Hill, and storm preparation across the metro area drive year-round demand. The compact urban layout means that home service businesses often work in tight spaces with limited parking and access, adding logistical challenges that suburban contractors rarely face.</p>
        <p>Homeowners in {city}'s older neighborhoods have high expectations for craftsmanship, particularly when it comes to work on historic properties. A contractor who understands period-appropriate materials and techniques earns trust in these communities. But the newer developments in Seaport and Somerville bring different expectations focused on modern efficiency and smart home technology. Structured feedback helps home service businesses navigate these diverse demands across the {city} metro.</p>
        """,
        ("boston", "service-businesses"): f"""
        <p>The {city} service economy is shaped by the city's academic and medical institutions, which create both demand for services and a highly educated clientele. Financial advisors in Back Bay, consultants in Cambridge, and personal service providers across the metro compete for clients who are well-informed, comparison-driven, and accustomed to institutional excellence. The compact geography means that reputation travels quickly through professional and social networks.</p>
        <p>Boston's cultural expectations around professionalism and follow-through are higher than many markets. A service business that misses a deadline or fails to communicate proactively will face scrutiny from clients who notice details and share their assessments within tight-knit professional circles. Structured feedback provides an early warning system for service quality issues and a consistent channel for the client voices that shape a business's reputation in this demanding market.</p>
        """,

        # ATLANTA
        ("atlanta", "law-firms"): f"""
        <p>{city}'s legal market benefits from the city's concentration of corporate headquarters, including those of Coca-Cola, Delta, Home Depot, and UPS. Corporate law, employment litigation, and real estate transactions are major practice areas, while Buckhead's affluent community supports estate planning and family law practices. The rapid suburban expansion into Sandy Springs, Decatur, and Dunwoody has created demand for general practice firms serving growing residential communities.</p>
        <p>Atlanta's diverse neighborhoods create distinct client expectations. A law firm in Buckhead serves a different clientele than one in Inman Park or Old Fourth Ward, even within the same practice area. The city's significant medical and legal communities are deeply interconnected, with referral networks that reward consistency and professionalism. Structured client feedback helps {city} law firms strengthen their standing within these networks by ensuring that every client experience reinforces the firm's reputation.</p>
        """,
        ("atlanta", "medical-practices"): f"""
        <p>The {city} medical landscape includes major hospital systems like Emory Healthcare and Piedmont alongside a dense network of private practices. Buckhead and Midtown support specialty practices, while the suburban expansion has created demand for primary care and pediatrics in Sandy Springs, Brookhaven, and Dunwoody. The diversity of {city}'s population creates a medical market where cultural competency and communication sensitivity are increasingly important.</p>
        <p>Medical practices in {city} compete not just with each other but with the large health systems that offer convenience through extensive networks. The advantage of a private practice lies in the personal relationship, the shorter wait times, and the individualized attention that a large system cannot replicate. Structured patient feedback helps private practices confirm that they are delivering these advantages consistently and identify areas where the patient experience could be improved.</p>
        """,
        ("atlanta", "med-spas"): f"""
        <p>The {city} med spa market is concentrated in Buckhead and Midtown, where an image-conscious clientele invests in aesthetic treatments with the same intentionality they bring to other aspects of their appearance. The city's growing tech scene and its status as a cultural hub for the Southeast have expanded the med spa client base beyond the traditional luxury demographic to include younger professionals and creative industry workers.</p>
        <p>Virginia Highland and Inman Park represent an emerging med spa market segment, with clients who value a more intimate, neighborhood-oriented experience than the larger Buckhead clinics provide. Structured feedback helps {city} med spas understand the specific expectations of their neighborhood's clientele and adapt their service model accordingly, whether that means adjusting consultation depth, treatment pacing, or follow-up communication.</p>
        """,
        ("atlanta", "dental-practices"): f"""
        <p>Dental practices in {city} serve a rapidly growing population across neighborhoods with distinct identities. Buckhead supports cosmetic and restorative dentistry for an affluent patient base, while Midtown and Virginia Highland attract younger patients who prioritize convenience and modern office environments. The suburban growth in Sandy Springs, Dunwoody, and Decatur has created demand for family dental practices that can absorb the volume of new residents.</p>
        <p>Southern hospitality expectations influence how patients evaluate their dental experience in {city}. A friendly greeting, a genuine connection with the hygienist, and a dentist who takes time to explain options are not extras but expected elements of the experience. Structured feedback helps dental practices measure whether they are meeting these interpersonal expectations alongside their clinical standards.</p>
        """,
        ("atlanta", "home-services"): f"""
        <p>The {city} home service market is driven by the city's rapid suburban expansion and the diverse housing stock that ranges from historic Inman Park bungalows to new construction in Dunwoody and Sandy Springs. Hot, humid summers create HVAC demand, while the tree canopy that defines many {city} neighborhoods generates steady work for arborists, gutter cleaners, and roofing contractors. The pollen season, one of the most intense in the country, drives demand for pressure washing and exterior cleaning.</p>
        <p>Homeowners in {city} value reliability and follow-through, reflecting the broader Southern emphasis on keeping commitments. A home service business that shows up when it says it will and finishes the job right builds a reputation that spreads through neighborhood associations and community networks. Structured feedback helps these businesses track their performance against these fundamental expectations across their growing service areas.</p>
        """,
        ("atlanta", "service-businesses"): f"""
        <p>The {city} service economy benefits from the city's corporate concentration, diverse population, and the Southern business culture that prizes relationships. Financial advisors in Buckhead, event planners in Midtown, and personal service providers across the metro operate in a market where trust is built through personal connection and maintained through consistent follow-through. The rapid population growth means that new service businesses enter the market regularly, keeping competition dynamic.</p>
        <p>The diversity of {city}'s neighborhoods creates a service market where one approach does not fit all. A caterer serving Buckhead weddings operates under different expectations than one working in Old Fourth Ward or Decatur. Structured feedback helps service businesses understand the specific needs and values of their target community, enabling them to refine their offerings rather than relying on a generic approach.</p>
        """,

        # PORTLAND
        ("portland", "law-firms"): f"""
        <p>{city}'s legal market reflects the city's values: sustainability, community orientation, and a preference for businesses that are genuine rather than corporate. The density of small businesses creates demand for business law and employment services, while the city's progressive values drive environmental and civil rights practice. Pearl District and Nob Hill host established firms, while Alberta Arts and Hawthorne support smaller practices embedded in their neighborhoods.</p>
        <p>Portland clients tend to value transparency and authenticity in their legal relationships. A law firm that communicates in plain language and demonstrates genuine concern for its clients' wellbeing builds trust more effectively than one that relies on credentials and formality alone. Structured feedback helps {city} law firms understand whether their communication style and values alignment resonate with the clientele they serve in this distinctive market.</p>
        """,
        ("portland", "medical-practices"): f"""
        <p>{city}'s medical market is shaped by a population that takes an active, holistic approach to health. Integrative medicine, naturopathy, and wellness-oriented primary care thrive alongside conventional practices. The Pacific Northwest emphasis on natural health creates patients who ask about alternative treatments and expect providers to consider the whole person, not just the presenting complaint. Nob Hill, Hawthorne, and Laurelhurst support practices aligned with these values.</p>
        <p>The sustainability-focused consumer base in {city} extends to healthcare, where patients evaluate practices on environmental consciousness, community involvement, and alignment with progressive values. While clinical quality remains paramount, practices that demonstrate social responsibility and genuine community engagement earn deeper trust from Portland patients. Structured feedback reveals how well a practice's stated values match the lived experience of its patients.</p>
        """,
        ("portland", "med-spas"): f"""
        <p>The {city} med spa market caters to a clientele that approaches aesthetics through a wellness lens. Clean beauty, natural ingredients, and subtle results align with Portland's broader cultural values. Pearl District and Northwest are home to med spas that emphasize clinical transparency and eco-conscious practices. The city's wellness community creates informed clients who research ingredients, question protocols, and expect their providers to share their commitment to responsible treatment approaches.</p>
        <p>Portland's neighborhood-specific culture means that a med spa's atmosphere and ethos should match its location. A clinical, high-tech environment might work in the Pearl District but feel out of place in Hawthorne or Alberta Arts. Structured feedback helps {city} med spas ensure their brand experience aligns with the values and expectations of their specific neighborhood clientele.</p>
        """,
        ("portland", "dental-practices"): f"""
        <p>Dental practices in {city} serve a patient base that values holistic health, environmental responsibility, and transparent communication. Mercury-free fillings, BPA-free materials, and eco-friendly office practices are not niche concerns here but factors that influence practice selection. Neighborhoods like Sellwood, Laurelhurst, and Hawthorne support family practices that align with these values, while Lake Oswego and Beaverton serve a more traditional suburban demographic.</p>
        <p>The small business density of {city} creates a dental market where independent practices are the norm rather than the exception. Patients choose these practices specifically because they want the personal relationship that a large dental group cannot provide. Structured feedback helps Portland dental practices maintain the intimacy and responsiveness that attracted their patients in the first place, even as they grow.</p>
        """,
        ("portland", "home-services"): f"""
        <p>The {city} home service market is driven by the Pacific Northwest climate, with rain creating constant demand for roofing, gutter maintenance, and moisture management. The city's older housing stock in neighborhoods like Sellwood, Alberta Arts, and Laurelhurst requires contractors who understand pre-war construction techniques. Portland homeowners also prioritize eco-friendly solutions, from energy-efficient upgrades to sustainable landscaping, creating demand for service providers with green credentials.</p>
        <p>The sustainability focus of {city} homeowners extends to how they evaluate home service businesses. They want to know about materials sourcing, waste disposal practices, and energy efficiency ratings. A contractor who can articulate their environmental approach earns a competitive advantage in this market. Structured feedback helps home service businesses understand whether their sustainability practices are being recognized and valued by Portland's environmentally conscious homeowners.</p>
        """,
        ("portland", "service-businesses"): f"""
        <p>{city}'s service economy is rooted in the city's small business culture, where neighborhood identity and community connection drive customer loyalty. From coffee roasters in Division to tax preparers in Beaverton, service businesses in {city} succeed when they demonstrate genuine commitment to their community. The keep-it-local ethos means that customers actively prefer neighborhood businesses over chains or corporate providers.</p>
        <p>The Portland market rewards authenticity and penalizes what feels manufactured or insincere. Service businesses that collect feedback demonstrate that they care about their clients' experiences, not just their revenue. This aligns with the values of a customer base that wants to support businesses that listen. Structured feedback helps {city} service businesses stay connected to the community values that are central to their identity and success.</p>
        """,

        # WASHINGTON DC
        ("washington-dc", "law-firms"): f"""
        <p>The {city} legal market is shaped by government, lobbying, and international diplomacy. Regulatory compliance, government contracts, and political law are dominant practice areas that exist alongside the full range of traditional legal services. Georgetown and Dupont Circle host established firms with deep Washington roots, while the Virginia suburbs of Arlington and Alexandria and the Maryland suburbs of Bethesda and Chevy Chase support practices serving the federal workforce.</p>
        <p>The transient nature of Washington's population, which shifts with every administration change, creates a client base that frequently establishes new legal relationships. Professionals arriving from across the country for government appointments bring expectations shaped by their home markets and evaluate firms quickly based on early interactions. Structured feedback helps {city} law firms understand how their intake and onboarding processes perform with this continuously refreshing client base.</p>
        """,
        ("washington-dc", "medical-practices"): f"""
        <p>The {city} medical market serves a highly educated, demanding population that includes government officials, international diplomats, and a large professional class. Georgetown, Dupont Circle, and Logan Circle support concierge and specialty practices, while the suburban corridors of Bethesda, Arlington, and Chevy Chase are home to medical practices serving families and established professionals. The international diplomatic community creates demand for providers experienced with diverse patient populations.</p>
        <p>Patients in the {city} area are typically well-informed about their health and expect to be treated as partners in their care, not passive recipients. Security consciousness, particularly among government and diplomatic clients, adds a layer of sensitivity to patient communications and record handling. Structured feedback helps practices understand whether they are meeting the high expectations of a clientele that is accustomed to high performance in every professional interaction.</p>
        """,
        ("washington-dc", "med-spas"): f"""
        <p>The {city} med spa market serves a professional, image-conscious clientele that includes government officials, consultants, and diplomats who value discretion and results. Georgetown, Dupont Circle, and Bethesda are home to med spas that emphasize privacy and clinical sophistication. The international client base brings diverse aesthetic preferences and treatment expectations that require cultural awareness from providers.</p>
        <p>The professional culture of {city} means that med spa clients are often fitting treatments into demanding schedules and expect efficiency without sacrificing quality. Lunch-hour treatments, minimal-downtime procedures, and rapid results are particularly valued in a market where appearance matters professionally but time is scarce. Structured feedback helps {city} med spas optimize their scheduling and service flow for this time-constrained, high-expectation clientele.</p>
        """,
        ("washington-dc", "dental-practices"): f"""
        <p>Dental practices in {city} serve a population that includes federal employees, diplomatic personnel, and a large professional class across the District and its Virginia and Maryland suburbs. The transient nature of the government workforce means practices regularly onboard new patients who arrive from across the country with varying expectations and dental histories. Georgetown, Capitol Hill, and Bethesda support practices serving affluent, detail-oriented patients.</p>
        <p>The diplomatic and international community in {city} creates a patient base with specific needs around language, cultural sensitivity, and continuity of care for patients who may divide their time between Washington and overseas posts. Structured feedback helps dental practices understand whether their onboarding process, communication style, and scheduling flexibility meet the needs of this uniquely mobile and demanding patient population.</p>
        """,
        ("washington-dc", "home-services"): f"""
        <p>The {city} home service market is shaped by a mix of historic Georgetown row houses, Capitol Hill brownstones, and modern construction in rapidly developing areas. The security consciousness of the government community influences how home service businesses are vetted and trusted, with background checks and references carrying particular weight. The distinct seasons, from hot, humid summers to cold winters, create year-round demand across HVAC, roofing, and exterior maintenance.</p>
        <p>Homeowners in affluent areas like Georgetown, Chevy Chase, and Bethesda expect premium service standards and are willing to pay for reliability and professionalism. The transient nature of the population means that home service businesses must continuously earn trust with new homeowners rather than relying on decades-long customer relationships. Structured feedback provides the consistent quality assurance that this demanding, high-turnover market requires.</p>
        """,
        ("washington-dc", "service-businesses"): f"""
        <p>The {city} service economy is closely tied to government, consulting, and international affairs. Financial planners, caterers, personal assistants, and professional service providers all serve a clientele that is educated, demanding, and accustomed to high-performance environments. The suburban communities of Bethesda, Arlington, and Alexandria each have distinct service economies that reflect their demographic and cultural differences.</p>
        <p>The administration-driven population changes in {city} create a continuously refreshing client base for service businesses. Every two to four years, a significant portion of the professional population turns over, bringing new clients with new expectations. Service businesses that rely on long-term relationship inertia are at a disadvantage compared to those that consistently deliver excellent experiences to new clients. Structured feedback ensures that each new client relationship starts strong and develops based on genuine satisfaction.</p>
        """,

        # MINNEAPOLIS
        ("minneapolis", "law-firms"): f"""
        <p>{city}'s legal market reflects the Twin Cities' strong community-oriented culture and its concentration of corporate headquarters, including Target, UnitedHealth Group, and 3M. Corporate law, healthcare regulation, and estate planning are significant practice areas. The North Loop and Uptown neighborhoods host firms serving the urban creative class, while Edina and Wayzata support practices serving established suburban families.</p>
        <p>The Scandinavian heritage that shapes the culture of {city} influences client communication preferences. Clients here tend to value straightforward, no-nonsense communication and may be slower to express dissatisfaction directly. This cultural tendency makes structured feedback particularly valuable for {city} law firms, as it creates a safe, systematic channel for clients to share honest assessments they might not volunteer in conversation.</p>
        """,
        ("minneapolis", "medical-practices"): f"""
        <p>{city}'s healthcare concentration, anchored by Mayo Clinic's influence on the broader Minnesota medical culture, creates a patient population with high expectations for care quality and communication. The Twin Cities support a dense network of specialty and primary care practices, with the North Loop and Linden Hills serving urban patients and Edina and Wayzata catering to suburban families. Extreme winters drive specific healthcare demand, from seasonal affective disorder treatment to cold-weather injury care.</p>
        <p>The community-oriented culture of {city} means that patients value long-term provider relationships built on mutual respect and clear communication. A practice that treats patients as partners in their care earns loyalty that transcends convenience factors. Structured feedback helps medical practices in the Twin Cities measure whether they are building these relationships effectively and where communication improvements might strengthen patient retention.</p>
        """,
        ("minneapolis", "med-spas"): f"""
        <p>The {city} med spa market is growing as the city's professional population invests in wellness and aesthetic treatments. The North Loop and Uptown are home to med spas that blend clinical expertise with a relaxed, approachable atmosphere that fits the Midwest sensibility. Edina and Wayzata support premium med spas serving a suburban clientele that values quality and discretion.</p>
        <p>The long winters of {city} create specific med spa demand patterns, with skin treatments peaking during the cold, dry months and body-focused treatments gaining momentum as summer approaches. The Scandinavian-influenced culture of understatement means that clients generally prefer natural-looking results and providers who present options without pressure. Structured feedback helps {city} med spas calibrate their consultation approach to match these cultural preferences.</p>
        """,
        ("minneapolis", "dental-practices"): f"""
        <p>Dental practices in {city} benefit from a community-oriented culture where patients tend to maintain long-term provider relationships. The Twin Cities' educated population values clear explanations and shared decision-making in their dental care. Practices in Kenwood and Linden Hills serve established families, while Northeast and the North Loop attract younger patients who prioritize modern offices and digital convenience.</p>
        <p>The extreme weather of {city} affects dental practice operations in ways that are unique to northern markets. Winter storms can disrupt scheduling and create appointment backlog, making communication about rescheduling and availability particularly important. Structured patient feedback helps dental practices understand how well they handle these seasonal disruptions and whether their contingency communication meets patient expectations during Minnesota's challenging winter months.</p>
        """,
        ("minneapolis", "home-services"): f"""
        <p>Extreme weather defines the {city} home service market. Furnace maintenance, insulation upgrades, and ice dam prevention are critical fall services, while spring brings a rush of exterior work deferred through the long winter. The housing stock ranges from century-old bungalows in Longfellow and Lake Calhoun to new construction in suburban Edina and Wayzata, each requiring different expertise and approaches.</p>
        <p>Homeowners in {city} understand the consequences of deferred maintenance better than most markets, because a small issue in October can become a significant problem by January. They value home service businesses that are proactive about seasonal preparation and reliable when emergencies arise. Structured feedback helps these businesses understand whether their communication about seasonal needs and their responsiveness during urgent situations meet the expectations of homeowners who depend on them through harsh conditions.</p>
        """,
        ("minneapolis", "service-businesses"): f"""
        <p>The {city} service economy reflects the Twin Cities' community values and corporate concentration. Service businesses from financial planners to caterers operate in a market where personal recommendations carry enormous weight and consistency is valued over flashiness. The split between Minneapolis and St. Paul creates two distinct urban markets with different demographics and expectations, while suburban communities like Edina and Wayzata support their own service ecosystems.</p>
        <p>The Scandinavian-influenced communication culture of {city} creates a market where service businesses must be attentive to unspoken dissatisfaction. A client who is unhappy may not complain directly but simply not return. Structured feedback provides a channel for these unexpressed concerns, giving service businesses visibility into issues they might never hear about through normal interactions. In a market where keeping a client is often easier than winning a new one, this visibility is invaluable.</p>
        """,

        # TAMPA
        ("tampa", "law-firms"): f"""
        <p>{city}'s legal market is shaped by the influx of northeast migrants, the retirement and snowbird community, and the waterfront property dynamics that drive real estate and maritime law. Estate planning, elder law, and personal injury are major practice areas, reflecting the demographics of a population that skews older than many other growth markets. Hyde Park and Davis Islands support established firms, while growing areas like Channel District and Westshore attract newer practices.</p>
        <p>The mix of long-time Florida residents and recent transplants creates a dual client base with different expectations. Snowbirds and retirees may value patience and thoroughness, while younger professionals arriving from the Northeast expect the pace and responsiveness they experienced in their previous market. Structured client feedback helps {city} law firms understand which communication style serves each segment of their clientele most effectively.</p>
        """,
        ("tampa", "medical-practices"): f"""
        <p>{city}'s medical market serves a population with significant geriatric and retirement-age healthcare needs alongside a growing younger demographic. The retirement community creates steady demand for cardiology, orthopedics, and primary care, while the northeast migration brings families and young professionals who need pediatrics and general practice. St. Petersburg and Clearwater function as distinct medical markets within the broader Tampa Bay area.</p>
        <p>The snowbird population creates seasonal demand fluctuations that affect staffing, scheduling, and revenue planning for medical practices. A practice that handles these fluctuations smoothly earns loyalty from seasonal residents who have options in two markets. Structured feedback from both year-round and seasonal patients helps {city} medical practices manage this dual-population challenge and ensure that quality remains consistent regardless of when a patient visits.</p>
        """,
        ("tampa", "med-spas"): f"""
        <p>The {city} med spa market is growing alongside the metro area's population, with South Tampa and Hyde Park supporting established clinics and newer areas like Channel District and Westshore attracting boutique providers. The year-round warm climate keeps body-focused treatments in constant demand, and the retirement community's interest in anti-aging procedures creates a patient base that is both knowledgeable and loyal to providers they trust.</p>
        <p>The distinct markets of Tampa, St. Petersburg, and Clearwater mean that a med spa's brand and positioning need to fit its specific community. A clinic in trendy St. Petersburg serves a different clientele than one in family-oriented Carrollwood. Structured feedback helps {city}-area med spas understand the expectations of their specific market and adjust their service approach to match.</p>
        """,
        ("tampa", "dental-practices"): f"""
        <p>Dental practices in {city} serve a growing and demographically diverse population. The retirement community drives demand for restorative, implant, and denture services, while the influx of young families from the Northeast creates a need for pediatric and family dentistry. South Tampa and Hyde Park support established practices, while rapidly growing areas like Brandon and Temple Terrace see new offices opening regularly to serve expanding residential communities.</p>
        <p>The seasonal population of snowbirds creates a unique challenge for {city} dental practices: maintaining continuity of care for patients who split their time between Florida and the Northeast. Clear communication about treatment plans, records accessibility, and scheduling flexibility for seasonal returns are all factors that influence whether these patients remain loyal. Structured feedback helps practices understand how well they are managing these seasonal relationships.</p>
        """,
        ("tampa", "home-services"): f"""
        <p>The {city} home service market is driven by waterfront property maintenance, hurricane preparation, and the demands of a tropical climate. Pool maintenance, exterior painting, HVAC, and pest control are year-round necessities, and the rapid growth of the metro area creates steady construction and renovation demand. Waterfront homes in Davis Islands and South Tampa require specialized maintenance knowledge, from seawall repair to moisture management.</p>
        <p>Hurricane season creates a predictable but intense surge in home service demand, from pre-storm preparation to post-storm repair. Home service businesses that handle these periods professionally earn long-term loyalty from homeowners who remember which company showed up when it mattered most. Structured feedback helps {city} home service businesses understand how their storm-season performance and year-round reliability shape their overall reputation.</p>
        """,
        ("tampa", "service-businesses"): f"""
        <p>The {city} service economy is expanding rapidly as the metro area absorbs migrants from the Northeast and grows into a major commercial center. Financial advisors, personal service providers, and professional consultants serve a mix of retirees and young professionals with different expectations and needs. St. Petersburg and Clearwater each maintain their own service economies with distinct client demographics.</p>
        <p>The northeast migration that is reshaping {city}'s demographics brings clients who compare their Tampa Bay service experiences to the standards they experienced in New York, New Jersey, and Connecticut. These transplants often have higher expectations for responsiveness and follow-through than the local baseline, creating an opportunity for service businesses that meet this high standard. Structured feedback helps service businesses understand which expectations are shifting and adapt their approach accordingly.</p>
        """,

        # CHARLOTTE
        ("charlotte", "law-firms"): f"""
        <p>{city}'s legal market is anchored by the banking and financial services industry, with Bank of America and Truist headquartered here. Corporate law, regulatory compliance, and financial litigation are significant practice areas. Myers Park and SouthPark support estate planning and family law practices serving affluent families, while the Ballantyne corporate corridor generates demand for employment law and business transactions. The emerging tech scene is beginning to create new demand for intellectual property and startup-focused legal services.</p>
        <p>Southern hospitality expectations shape how {city} law firms are evaluated by their clients. Technical competence is expected; the differentiator is whether the client feels genuinely cared for throughout the engagement. A firm that communicates warmly, follows up proactively, and demonstrates personal investment in the client's outcome earns the kind of loyalty and referrals that drive growth in {city}'s relationship-oriented market. Structured feedback helps firms measure whether they are delivering on these interpersonal expectations.</p>
        """,
        ("charlotte", "medical-practices"): f"""
        <p>The {city} medical landscape is shaped by the city's rapid population growth and the concentration of healthcare systems including Atrium Health and Novant Health. Private practices compete for patients who have access to these large systems, making personalized service the primary differentiator. SouthPark and Myers Park support specialty practices, while the growing suburbs of Ballantyne and Matthews need primary care and pediatric offices to serve expanding residential communities.</p>
        <p>The Southern hospitality that defines {city}'s culture extends to patient expectations in healthcare. Patients want to feel known, not processed. A front desk staff member who remembers a patient's name, a provider who asks about family, and a follow-up call after a procedure are the touches that build loyalty in this market. Structured feedback reveals whether these interpersonal elements are being delivered consistently or eroding as a practice grows.</p>
        """,
        ("charlotte", "med-spas"): f"""
        <p>The {city} med spa market is growing alongside the city's affluent population, with SouthPark and Myers Park supporting premium clinics and South End attracting a younger, trend-conscious clientele. The banking and finance community creates a professional client base that values discretion and efficiency. The rapid population growth means that new med spa clients are constantly entering the market, often without established provider relationships and open to trying different clinics.</p>
        <p>Charlotte's Southern charm creates expectations around warmth and personal attention that extend to the med spa experience. Clients want to feel welcomed and valued, not processed through a clinical routine. A med spa that combines quality treatments with genuine hospitality earns the kind of word-of-mouth recommendations that drive growth in {city}'s tight-knit social and professional circles. Structured feedback measures whether this balance is being maintained.</p>
        """,
        ("charlotte", "dental-practices"): f"""
        <p>Dental practices in {city} serve a rapidly growing population that includes both established Southern families and newcomers drawn by the banking industry and emerging tech sector. Myers Park and Dilworth support practices with long-standing patient relationships, while new offices in Ballantyne and Matthews compete for families settling in the suburban growth areas. The pace of new resident arrivals means that dental practices have a continuous stream of potential patients evaluating first-visit experiences.</p>
        <p>The strong Southern hospitality expectations in {city} influence how patients evaluate their dental care. A practice where the hygienist greets patients by name and the dentist takes time for genuine conversation earns loyalty that transcends clinical considerations. Structured feedback helps {city} dental practices ensure that the hospitality element of the patient experience remains strong even as patient volumes grow and scheduling pressure increases.</p>
        """,
        ("charlotte", "home-services"): f"""
        <p>The {city} home service market is driven by rapid residential growth in suburban communities like Ballantyne, Matthews, and Waxhaw, alongside the maintenance needs of established neighborhoods like Myers Park and Dilworth. The humid subtropical climate creates demand for HVAC, pest control, and exterior maintenance, while the construction boom means that landscaping, painting, and smart home installation are thriving service categories.</p>
        <p>Charlotte homeowners value courtesy, punctuality, and clear communication, reflecting the broader Southern emphasis on respectful business interactions. A home service provider who shows up on time, explains the work clearly, and cleans up thoroughly earns referrals in a market where neighbors talk and community recommendations carry significant weight. Structured feedback helps home service businesses in {city} track their performance on these fundamentals that drive reputation and growth.</p>
        """,
        ("charlotte", "service-businesses"): f"""
        <p>{city}'s service economy reflects the city's dual identity as a banking center and a fast-growing Sun Belt metro. Financial services, wealth management, and corporate consulting serve the banking community, while the rapid population growth creates demand across every service category from personal training to event planning. The Ballantyne corporate corridor generates a concentrated demand for professional services within a suburban setting.</p>
        <p>The Southern hospitality culture of {city} sets a high bar for service delivery. Clients expect to be treated with warmth and respect, and they notice when a business feels transactional rather than relational. In a market where personal recommendations drive a significant share of new business, every client interaction contributes to a service business's long-term growth trajectory. Structured feedback ensures that the relational quality of service delivery is being maintained across every client engagement.</p>
        """,

        # ORLANDO
        ("orlando", "law-firms"): f"""
        <p>{city}'s legal market is shaped by the tourism economy, the growing residential communities spreading outward from the city center, and the hospitality and entertainment industries that are the region's economic backbone. Employment law, personal injury, and real estate transactions are major practice areas. Winter Park supports established firms with deep community roots, while Lake Nona and Celebration attract newer practices serving rapidly growing residential populations.</p>
        <p>The theme park industry's influence on {city}'s economy creates legal needs around hospitality employment, commercial leasing, and visitor-related incidents. The seasonal fluctuations in the tourism economy also affect the timing and volume of legal work. Structured client feedback helps {city} law firms understand how they are perceived by both the permanent resident community and the tourism-adjacent businesses that form a significant part of their client base.</p>
        """,
        ("orlando", "medical-practices"): f"""
        <p>{city}'s medical market serves a population that includes long-time residents, a growing influx of new families, and the large hospitality workforce employed by the theme parks and tourism industry. Lake Nona has emerged as a medical innovation hub, attracting both providers and patients. Winter Park supports specialty practices serving an affluent population, while rapidly growing communities like Celebration and Oviedo need primary care and pediatric offices to keep pace with residential development.</p>
        <p>The seasonal population fluctuations that define {city}'s economy extend to healthcare, with tourist-season urgent care demand supplementing the year-round resident patient base. Medical practices must balance the needs of established patients with the volume pressures created by seasonal peaks. Structured feedback helps practices ensure that year-round patients do not feel deprioritized during busy periods, maintaining the loyalty that sustains the practice when tourist season ends.</p>
        """,
        ("orlando", "med-spas"): f"""
        <p>The {city} med spa market is influenced by the year-round warm climate, the tourism industry's emphasis on appearance, and the growing affluence of communities like Winter Park and Dr. Phillips. The hospitality workforce creates a client base that is image-conscious and accustomed to service industry standards, while the residential growth areas bring clients who are newer to aesthetic treatments and value education and transparency during consultations.</p>
        <p>Winter Park's established wealth and its village-like atmosphere make it a natural hub for premium med spa experiences, while the broader Orlando market supports a range of providers from boutique clinics to full-service centers. Structured feedback helps {city} med spas understand whether their approach resonates with their specific community, be it the sophisticated Winter Park clientele or the value-conscious families in rapidly growing suburbs.</p>
        """,
        ("orlando", "dental-practices"): f"""
        <p>Dental practices in {city} serve a rapidly growing population that is expanding outward from the city center into Lake Nona, Celebration, and Oviedo. These new communities need family dental practices that can establish trust quickly with patients who are new to the area. Winter Park and College Park support established practices with long-term patient relationships, while the tourism employee population creates a large pool of patients working non-traditional schedules who need flexible appointment availability.</p>
        <p>The theme park workforce, one of the largest employer groups in the {city} area, includes many workers who need dental care that accommodates shift schedules and may be navigating employer-provided insurance for the first time. Dental practices that can serve this population effectively while maintaining the experience quality expected by their Winter Park or Baldwin Park patients need feedback from both segments to balance their approach.</p>
        """,
        ("orlando", "home-services"): f"""
        <p>The {city} home service market is driven by the rapid growth of residential communities, the tropical climate's demands on exterior maintenance, and the property management needs of vacation rental properties. Pool maintenance, pest control, HVAC, and landscape services are year-round necessities, while the hurricane season creates seasonal spikes in preparation and repair work. New construction in Lake Nona and Celebration generates steady demand for installation and finishing work.</p>
        <p>The vacation rental market in the greater {city} area creates a subset of customers who manage properties remotely and rely entirely on their home service providers' professionalism and consistency. These absentee owners evaluate service businesses based on reliability and communication, since they cannot inspect work in person. Structured feedback from both resident homeowners and property investors helps {city} home service businesses maintain quality across their diverse customer base.</p>
        """,
        ("orlando", "service-businesses"): f"""
        <p>{city}'s service economy is shaped by the tourism industry, the growing residential base, and the emergence of Lake Nona as a hub for innovation and professional services. Event planners, caterers, and hospitality consultants serve the tourism-adjacent economy, while financial advisors, accountants, and personal services cater to the permanent residential population. Winter Park's affluent community supports premium service providers who emphasize personal relationships.</p>
        <p>The seasonal fluctuations of the {city} economy affect service businesses differently depending on their niche. Those serving the tourism industry experience winter peaks, while residential service providers see steadier demand. Structured feedback helps service businesses across the Orlando market understand how seasonal dynamics affect customer satisfaction and where adjustments to staffing, scheduling, or communication might improve the client experience during high-demand periods.</p>
        """,

        # LAS VEGAS
        ("las-vegas", "law-firms"): f"""
        <p>{city}'s legal market is shaped by the tourism and hospitality industry, the rapid suburban growth in Summerlin and Henderson, and the unique regulatory environment of a city built on gaming and entertainment. Business law, employment disputes, and personal injury are major practice areas. The 24/7 nature of the city's economy creates legal needs that do not follow standard business hours, from contract disputes to liability claims that arise at any hour.</p>
        <p>The transient nature of parts of the {city} population creates a client base that includes both long-time residents with deep community ties in Summerlin and Henderson and newer arrivals who may need legal services quickly without established referral networks. Structured feedback helps {city} law firms understand how different segments of their clientele perceive the firm, from the long-term relationship clients to the one-time transactional clients who together make up the diverse Vegas legal market.</p>
        """,
        ("las-vegas", "medical-practices"): f"""
        <p>{city}'s medical market is growing rapidly alongside the metro area's population, with Summerlin and Henderson developing significant concentrations of medical practices. The extreme heat creates specific healthcare needs, from heat-related conditions to dermatological concerns from intense sun exposure. The transient nature of the population means that many patients are establishing new provider relationships and evaluating practices based on accessibility and first-visit experience.</p>
        <p>The 24/7 economy of {city} creates a workforce with non-traditional schedules, and medical practices that offer flexible hours, evening, or weekend appointments can capture a patient segment that traditional-hours practices miss entirely. Structured feedback reveals whether scheduling flexibility, wait times, and communication responsiveness are meeting the expectations of a population that does not operate on a standard nine-to-five timetable.</p>
        """,
        ("las-vegas", "med-spas"): f"""
        <p>The {city} med spa market benefits from the city's emphasis on appearance, entertainment, and the year-round warm climate. Summerlin and Henderson host established med spas serving a suburban clientele, while the resort corridor creates a secondary market of visitors seeking treatments during their stay. The extreme sun exposure at {city}'s altitude and latitude creates specific demand for skin repair and protection treatments.</p>
        <p>The rapid suburban growth in Summerlin, Henderson, and Centennial Hills has brought new med spa clients who are establishing provider relationships for the first time. These clients are comparison-shopping and forming loyalties based on early experiences. Structured feedback after the first and second visits is particularly valuable in this growth market, revealing whether the initial impression translates into the kind of experience that drives rebooking and referrals.</p>
        """,
        ("las-vegas", "dental-practices"): f"""
        <p>Dental practices in {city} serve a population that is growing rapidly through domestic migration and includes a significant tourism workforce with non-traditional schedules. Summerlin and Henderson support family dental practices and cosmetic dentistry in their suburban communities, while the city center area serves the hospitality industry workforce and transient population. The extreme heat and dry climate create specific oral health considerations, including dehydration-related dental concerns.</p>
        <p>The growth of {city}'s suburban communities means dental practices face continuous opportunity to add new patients, but competition from newly opened offices is equally constant. Patient retention depends on consistently good experiences, from scheduling convenience to chairside manner. Structured feedback helps {city} dental practices identify the factors that keep patients coming back in a market where alternatives are always appearing.</p>
        """,
        ("las-vegas", "home-services"): f"""
        <p>The extreme heat of {city} drives year-round HVAC demand that defines the home service market. Air conditioning failure in summer is not an inconvenience but a potential health hazard, creating urgency expectations that shape how homeowners evaluate service providers. The rapid suburban growth in Summerlin, Henderson, and Centennial Hills generates constant demand for landscaping, pool maintenance, and new home services, while the dry climate requires specific approaches to exterior maintenance and water conservation.</p>
        <p>Homeowners in {city} who experience a responsive, professional service call during a summer HVAC emergency become loyal customers for years. The high-stakes nature of climate-dependent home services means that first impressions carry more weight here than in milder markets. Structured feedback helps home service businesses understand whether their emergency responsiveness and routine service quality are building the reputation that sustains growth in this rapidly expanding market.</p>
        """,
        ("las-vegas", "service-businesses"): f"""
        <p>The {city} service economy operates at the intersection of the tourism industry and a rapidly growing residential market. Service businesses from caterers to financial advisors navigate a split between the 24/7 hospitality economy and the suburban normalcy of Summerlin and Henderson. The transient population means that service businesses must continuously attract new clients while building loyalty among those who have settled permanently.</p>
        <p>The extreme growth of {city}'s residential areas has created opportunity for service businesses willing to establish a local presence in communities that are still forming their service provider preferences. A financial advisor who opens in a new Henderson development or a personal trainer who launches in Summerlin has an early-mover advantage, but only if the service quality justifies the initial loyalty clients extend. Structured feedback ensures that the experience matches the promise as these businesses scale.</p>
        """,

        # SAN FRANCISCO
        ("san-francisco", "law-firms"): f"""
        <p>{city}'s legal market is driven by the tech industry, venture capital, and the highest income density in the country. Intellectual property, corporate transactions, and employment law are dominant practice areas, with startup-related legal work forming a significant and growing segment. Pacific Heights and Nob Hill host established firms, while SoMa and the Mission are home to practices aligned with the tech ecosystem.</p>
        <p>Client expectations in {city} are shaped by the tech industry's standards for speed, transparency, and digital communication. Lawyers here are judged not just on legal outcomes but on responsiveness, clear fee structures, and the quality of their digital presence. Structured feedback helps {city} law firms understand whether they are meeting the high expectations of a clientele that benchmarks every professional interaction against the standards of the companies they work for.</p>
        """,
        ("san-francisco", "medical-practices"): f"""
        <p>{city}'s medical market serves the highest-income patient population in the country, with correspondingly high expectations for care quality and service. Pacific Heights, the Marina, and Nob Hill support concierge and specialty practices, while neighborhoods like the Mission and Hayes Valley attract younger, tech-industry patients who expect digital-first healthcare experiences. UCSF's presence sets a clinical standard that private practices must meet or exceed.</p>
        <p>The neighborhood-specific demographics of {city} create micro-markets within the medical landscape. A practice in Noe Valley serves a family-oriented patient base, while one in SoMa sees more single professionals. The tech-influenced expectation for data transparency extends to healthcare, where patients want access to their records, clear explanations of costs, and responsive portal communication. Structured feedback reveals whether these expectations are being met consistently across a practice's patient population.</p>
        """,
        ("san-francisco", "med-spas"): f"""
        <p>The {city} med spa market serves a tech-affluent clientele that researches treatments extensively, asks data-driven questions during consultations, and expects premium experiences. Pacific Heights and the Marina are home to luxury med spas, while newer clinics in Hayes Valley and Cole Valley attract a slightly younger, wellness-oriented demographic. The city's fog and microclimates create specific skin care concerns that differ from the sun-damage focus of Southern California markets.</p>
        <p>The income density of {city} means that med spa clients here have high standards and the means to seek alternatives if those standards are not met. The tech industry's influence creates clients who expect measurable outcomes, clear before-and-after documentation, and evidence-based treatment recommendations. Structured feedback helps {city} med spas ensure their communication and clinical approach match the analytical expectations of this informed, affluent clientele.</p>
        """,
        ("san-francisco", "dental-practices"): f"""
        <p>Dental practices in {city} compete in a market where patients have high incomes, high expectations, and abundant choices. Pacific Heights and Nob Hill support cosmetic dentistry practices with affluent patient bases, while neighborhoods like Noe Valley and Cole Valley attract family-focused practices. The tech industry's influence means patients expect online scheduling, digital records, and prompt communication through modern channels.</p>
        <p>The compact, walkable nature of {city} means that competing dental practices are often blocks apart, making patient experience a critical differentiator. A practice that provides excellent clinical care but has a disorganized front desk or an outdated scheduling system will lose patients to the modern office around the corner. Structured feedback helps {city} dental practices identify the operational details that influence retention in a market where patients have no tolerance for inefficiency.</p>
        """,
        ("san-francisco", "home-services"): f"""
        <p>The {city} home service market is shaped by the city's historic housing stock, its compact urban layout, and the highest service expectations in the country. Victorian homes in Pacific Heights and the Marina require specialized maintenance knowledge, while modern construction in SoMa and Mission Bay presents different challenges. The city's fog and salt air create specific exterior maintenance needs, from painting to window replacement, that differ from inland markets.</p>
        <p>Homeowners in {city} are willing to pay premium rates for home services, but they expect premium execution in return. The income density means that sloppy work or poor communication will lead to a lost customer who has no difficulty finding an alternative. The tech-savvy population expects digital booking, real-time updates, and transparent pricing. Structured feedback helps home service businesses in {city} maintain the high standards that justify premium pricing in the most demanding residential market in the country.</p>
        """,
        ("san-francisco", "service-businesses"): f"""
        <p>{city}'s service economy serves the highest-income metropolitan population in the country, with expectations to match. Financial advisors, personal assistants, cleaning services, and professional consultants all operate in a market where clients are accustomed to the efficiency and polish of the tech companies they work for. The startup culture creates a subset of clients who move fast, demand transparency, and are intolerant of outdated processes.</p>
        <p>The neighborhood-specific demographics of {city} create distinct service markets within a seven-by-seven mile area. A service business in Pacific Heights serves a different clientele than one in the Mission, and the expectations around pricing, communication style, and service delivery reflect those demographic differences. Structured feedback helps service businesses in {city} calibrate their approach to the specific community they serve, ensuring that quality meets the high standards this market demands.</p>
        """,

        # RALEIGH
        ("raleigh", "law-firms"): f"""
        <p>{city}'s legal market is shaped by the Research Triangle's knowledge economy, the steady influx of tech workers, and the region's universities. Intellectual property, employment law, and corporate transactions have grown alongside the tech migration, while traditional practice areas like estate planning and family law remain strong in established communities. North Hills and Cameron Village support practices serving long-time residents, while Cary and Morrisville attract firms serving the growing tech professional community.</p>
        <p>The blend of Southern charm and tech sophistication that defines {city} creates clients who expect both personal warmth and digital efficiency from their law firms. A firm that communicates with genuine care but also offers modern digital tools for document sharing and case updates positions itself well in this hybrid market. Structured feedback helps {city} law firms understand whether they are successfully blending these two cultural expectations.</p>
        """,
        ("raleigh", "medical-practices"): f"""
        <p>{city}'s medical market benefits from the university-driven demographics that bring both a young, health-conscious population and a concentration of academic medical expertise. Duke and UNC's medical systems set a high bar for care quality in the region, and private practices must differentiate through patient experience and accessibility. The rapid growth from tech migration has created demand for new primary care and specialty practices in Cary, Morrisville, and Apex.</p>
        <p>The affordability of the {city} market compared to coastal cities means that practices can often offer more personalized attention per patient, but the influx of transplants from New York, San Francisco, and other high-cost markets brings expectations shaped by those environments. Structured feedback helps {city} medical practices understand how transplant patients compare their experience to what they left behind, and where the Triangle's healthcare advantages should be highlighted.</p>
        """,
        ("raleigh", "med-spas"): f"""
        <p>The {city} med spa market is emerging alongside the region's population growth and increasing affluence. North Hills and Cameron Village support established clinics, while newer communities like Brier Creek and Morrisville represent a growing market of tech professionals who are newer to aesthetic treatments. The affordability of the Triangle compared to coastal cities means clients here may be more price-sensitive, but they still expect quality and transparency.</p>
        <p>The university influence on the {city} market creates a client base that values evidence-based treatment recommendations and clear explanations of procedures and expected outcomes. Med spa clients in the Triangle tend to do their research and arrive at consultations with informed questions. Structured feedback helps {city} med spas ensure their consultation process meets the expectations of this educated, research-oriented clientele.</p>
        """,
        ("raleigh", "dental-practices"): f"""
        <p>Dental practices in {city} serve a rapidly growing population that includes both established Triangle families and newcomers from across the country. The Research Triangle's educated population values clear explanations and shared decision-making in their dental care. Family practices in Cary, Apex, and Wake Forest serve the suburban growth, while Five Points and Cameron Village support practices with long-standing community ties.</p>
        <p>The affordability of {city} compared to coastal markets means that dental practices can often offer competitive pricing while maintaining the service quality that transplant patients expect. Structured feedback helps dental practices understand whether their pricing transparency, treatment explanations, and overall patient experience meet the expectations of a population that, while cost-conscious, has experienced dental care in many different markets and brings those comparisons to every visit.</p>
        """,
        ("raleigh", "home-services"): f"""
        <p>The {city} home service market is fueled by rapid residential growth in communities like Cary, Apex, Wake Forest, and Morrisville. New construction generates demand for landscaping, smart home installation, and exterior finishing, while the mild four-season climate creates year-round maintenance needs without the extreme peaks of northern or deep southern markets. The mix of new builds and established homes in Five Points and Cameron Village requires contractors who can work across different eras of construction.</p>
        <p>Homeowners in {city} benefit from the region's affordability, which extends to home services, but they bring expectations from higher-cost markets. A transplant from New York or San Francisco may compare their Raleigh home service experience against the standards they knew before. Structured feedback helps home service businesses in the Triangle understand these evolving expectations and maintain the service quality that turns new residents into loyal customers.</p>
        """,
        ("raleigh", "service-businesses"): f"""
        <p>The {city} service economy is growing as the Research Triangle attracts tech companies, startups, and the professionals who work for them. The blend of Southern hospitality and tech-sector sophistication creates a market where service businesses must combine personal warmth with digital efficiency. Durham and Chapel Hill each maintain their own service ecosystems, reflecting the distinct character of each Triangle city.</p>
        <p>The affordability of the {city} market compared to peer tech hubs gives service businesses an opportunity to deliver premium experiences at competitive price points. But the influx of transplants raises expectations continuously, and a service business that was considered excellent five years ago may now be measured against the standards of San Francisco or Seattle. Structured feedback helps {city} service businesses track these shifting expectations and evolve their service delivery to match the market's growing sophistication.</p>
        """,
    }

    key = (city_slug, vert_slug)
    return content_map.get(key, f"""
        <p>{city}'s {v['label']} market is shaped by the unique characteristics of the local community and its business landscape. {c['context'].capitalize()}.</p>
        <p>For {v['label']} in {city}, understanding how {v['person_lower']}s perceive their experience is essential for building lasting relationships and maintaining a strong local reputation.</p>
    """)


def get_feedback_content(city_slug, vert_slug):
    """Return H2 'why feedback matters' section content."""
    c = CITIES[city_slug]
    v = VERTICALS[vert_slug]
    city = c["name"]

    # Vertical-specific feedback content with city flavor
    feedback_map = {
        "law-firms": f"""
        <p>{v['person']} retention in legal services depends on trust, and trust is built through attentive communication and consistent follow-through. After a case closes, the {v['person_lower']} has a complete experience to reflect on. They know whether they felt informed throughout the process, whether their calls were returned promptly, and whether the outcome met the expectations set at intake.</p>
        <p>For {v['label']} in {city}, structured feedback creates a systematic way to capture these reflections at the moment they are most vivid. Rather than waiting for an online review or a casual mention to a colleague, the firm receives direct, private input from each {v['person_lower']} after every matter. These insights are specific enough to act on and consistent enough to reveal patterns across your {city} practice.</p>
        """,
        "medical-practices": f"""
        <p>{v['person']} loyalty in healthcare depends on more than clinical outcomes. The experience of scheduling an appointment, the wait time at the office, the way a diagnosis is communicated, and the clarity of follow-up instructions all shape whether a {v['person_lower']} returns or looks elsewhere. In a market like {city} where alternatives are accessible, these experience details determine retention.</p>
        <p>Structured feedback gives {v['label']} in {city} a reliable channel for hearing from {v['person_lower']}s after every visit. Instead of learning about issues through attrition or online complaints, the practice receives honest input that identifies what is working and what needs attention. Over time, this data reveals trends that inform staffing decisions, workflow changes, and communication improvements specific to your {city} practice.</p>
        """,
        "med-spas": f"""
        <p>In the med spa industry, the relationship between {v['person_lower']} satisfaction and rebooking is direct and measurable. A {v['person_lower']} who feels well-cared-for will return for their next treatment and recommend the clinic to friends. One who feels rushed, pressured, or under-informed will not. In {city}'s competitive market, understanding the factors that influence this decision is essential for sustained growth.</p>
        <p>Structured feedback gives {v['label']} in {city} a way to hear from {v['person_lower']}s after every treatment, capturing their assessment of the full experience from booking through follow-up. These responses reveal whether the clinical results matched expectations, whether the staff made the {v['person_lower']} feel comfortable, and whether the communication about aftercare was clear. This information drives improvements that increase retention and referrals across your {city} client base.</p>
        """,
        "dental-practices": f"""
        <p>{v['person']} retention in dentistry is built on comfort, communication, and consistency. A {v['person_lower']} who feels anxious about dental visits is particularly sensitive to how they are treated, from the tone of the front desk greeting to the gentleness of the hygienist. In {city}, where {v['person_lower']}s have numerous alternatives, the practices that retain their patients are those that pay attention to these experience details.</p>
        <p>Structured feedback gives {v['label']} in {city} consistent insight into how {v['person_lower']}s perceive each visit. Did the wait time feel reasonable? Was the treatment plan explained clearly? Did the {v['person_lower']} feel rushed or respected? These are questions that {v['person_lower']}s have answers to but rarely share unprompted. A structured system creates the channel for these honest assessments, providing the data practices need to improve retention and build loyalty.</p>
        """,
        "home-services": f"""
        <p>{v['person']} satisfaction in home services is driven by reliability, communication, and craftsmanship. A {v['person_lower']} who books a service wants to know when the crew will arrive, what the work will cost, and that the job will be done right the first time. In {city}, where word-of-mouth and neighborhood reputation carry significant weight, meeting these expectations consistently is the foundation of business growth.</p>
        <p>Structured feedback gives {v['label']} in {city} a direct line to how {v['person_lower']}s evaluate each job. Was the estimate accurate? Did the crew arrive on time? Was the work area left clean? These operational details, which are often invisible to management, determine whether a one-time job becomes a long-term {v['person_lower']} relationship. Consistent feedback turns these individual interactions into data that drives measurable improvement.</p>
        """,
        "service-businesses": f"""
        <p>{v['person']} satisfaction in service businesses depends on whether the experience matches the expectation. A {v['person_lower']} who hires a service provider expects clear communication, reliable follow-through, and results that justify the investment. In {city}, where competition is strong and alternatives are accessible, the businesses that retain their {v['person_lower']}s are those that consistently deliver on these fundamentals.</p>
        <p>Structured feedback gives {v['label']} in {city} a systematic way to measure how well they are meeting {v['person_lower']} expectations across every interaction. Instead of relying on the assumption that silence means satisfaction, the business receives direct input from each {v['person_lower']} after each engagement. These responses identify strengths to maintain and weaknesses to address, creating a feedback loop that drives continuous improvement.</p>
        """,
    }
    return feedback_map.get(vert_slug, "")


def get_how_it_works_content(city_slug, vert_slug):
    """Return H2 'how it works' section content."""
    c = CITIES[city_slug]
    v = VERTICALS[vert_slug]
    city = c["name"]

    return f"""
        <p>My Business Feedback is based in San Diego, California, and works with {v['label']} across the United States, including those serving {city}, {c['state']}. The system is designed to be simple to implement and immediately useful for your team.</p>
        <p>After each {v['person_lower']} interaction, your team sends a short feedback link. The {v['person_lower']} opens a clean, branded page and shares their rating and any additional thoughts. The entire process takes less than a minute from the {v['person_lower']}'s perspective.</p>
        <p>On your side, responses arrive in real time. Your team sees the rating, reads the comment, and can respond personally when appropriate. When a {v['person_lower']} shares a concern, you have the opportunity to address it directly and privately. When a {v['person_lower']} expresses satisfaction, your team sees that recognition immediately.</p>
        <p>There is no complicated software to learn, no lengthy onboarding process, and no contracts that lock you in. Setup takes days, not weeks. For {v['label']} in {city} that want to start hearing from their {v['person_lower']}s consistently, the path from interest to implementation is straightforward.</p>
    """


# ---------------------------------------------------------------------------
# HTML TEMPLATE PIECES
# ---------------------------------------------------------------------------

CSS = """    :root {
      --cream: #FAF8F3;
      --cream-warm: #F3EFE4;
      --paper: #FFFFFF;
      --ink: #0F0F0E;
      --ink-soft: #2A2925;
      --muted: #57564F;
      --muted-light: #8B8A82;
      --rule: rgba(15, 15, 14, 0.14);
      --rule-soft: rgba(15, 15, 14, 0.06);
      --forest: #1A4D3C;
      --forest-dark: #143729;
      --rust: #A04030;
      --gold: #C89B3C;
      --star-gold: #E8B84D;

      --font-display: 'Fraunces', Georgia, 'Times New Roman', serif;
      --font-body: 'Instrument Sans', -apple-system, BlinkMacSystemFont, sans-serif;

      --container-wide: 1280px;
      --container: 1120px;
      --container-narrow: 860px;

      --pad-x: clamp(1.25rem, 4vw, 3rem);
    }

    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    html { scroll-behavior: smooth; -webkit-text-size-adjust: 100%; }
    body {
      background: var(--cream);
      color: var(--ink);
      font-family: var(--font-body);
      font-size: 17px;
      line-height: 1.55;
      -webkit-font-smoothing: antialiased;
      -moz-osx-font-smoothing: grayscale;
      overflow-x: hidden;
    }
    a { color: inherit; text-decoration: none; }
    button { font: inherit; color: inherit; background: none; border: 0; cursor: pointer; }
    img, svg { display: block; max-width: 100%; }
    ::selection { background: var(--ink); color: var(--cream); }

    .display {
      font-family: var(--font-display);
      font-weight: 400;
      letter-spacing: -0.025em;
      line-height: 0.98;
      font-variation-settings: "opsz" 144;
    }
    .eyebrow {
      font-family: var(--font-body);
      font-size: 12px;
      font-weight: 500;
      letter-spacing: 0.18em;
      text-transform: uppercase;
      color: var(--muted);
      display: inline-block;
    }

    .masthead {
      border-bottom: 1px solid var(--rule);
      padding: 14px var(--pad-x);
      background: var(--cream);
      position: sticky;
      top: 0;
      z-index: 50;
      backdrop-filter: blur(8px);
      -webkit-backdrop-filter: blur(8px);
    }
    .masthead-inner {
      max-width: var(--container-wide);
      margin: 0 auto;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 24px;
    }
    .wordmark {
      font-family: var(--font-display);
      font-weight: 500;
      font-size: 18px;
      letter-spacing: -0.01em;
      font-variation-settings: "opsz" 14;
      display: flex;
      align-items: center;
      gap: 12px;
      color: var(--ink);
    }
    .wordmark-mark { width: 34px; height: 34px; flex-shrink: 0; transition: transform 0.4s ease; }
    .wordmark:hover .wordmark-mark { transform: rotate(8deg); }
    .masthead nav { display: flex; align-items: center; gap: 28px; font-size: 14px; }
    .masthead nav a { color: var(--ink-soft); transition: color 0.2s ease; }
    .masthead nav a:hover { color: var(--forest); }
    .masthead nav .nav-cta {
      padding: 8px 16px;
      border: 1px solid var(--ink);
      border-radius: 999px;
      font-size: 13px;
      font-weight: 500;
      transition: all 0.2s ease;
    }
    .masthead nav .nav-cta:hover { background: var(--ink); color: var(--cream); }
    @media (max-width: 720px) {
      .masthead nav a:not(.nav-cta) { display: none; }
    }

    .meta-strip {
      border-bottom: 1px solid var(--rule);
      padding: 10px var(--pad-x);
      font-size: 11px;
      letter-spacing: 0.16em;
      text-transform: uppercase;
      color: var(--muted);
      background: var(--cream);
    }
    .meta-strip-inner {
      max-width: var(--container-wide);
      margin: 0 auto;
      display: flex;
      justify-content: space-between;
      gap: 24px;
      flex-wrap: wrap;
    }
    .meta-strip span { display: inline-flex; align-items: center; gap: 8px; }
    .meta-strip .dot { width: 3px; height: 3px; border-radius: 50%; background: var(--muted); display: inline-block; }
    @media (max-width: 720px) {
      .meta-strip-inner > :nth-child(n+3) { display: none; }
    }

    .hero {
      padding: clamp(4rem, 10vw, 9rem) var(--pad-x) clamp(5rem, 12vw, 10rem);
    }
    .hero-inner {
      max-width: var(--container-wide);
      margin: 0 auto;
      display: grid;
      grid-template-columns: minmax(0, 1fr);
      gap: clamp(2rem, 5vw, 4rem);
    }
    .hero-headline {
      font-size: clamp(2.5rem, 7vw, 6rem);
      letter-spacing: -0.035em;
      line-height: 0.96;
      max-width: 20ch;
      font-variation-settings: "opsz" 144, "SOFT" 30;
      font-weight: 400;
    }
    .hero-headline em {
      font-style: italic;
      font-weight: 300;
      color: var(--ink);
      font-variation-settings: "opsz" 144, "SOFT" 100;
    }
    .hero-bottom {
      display: grid;
      grid-template-columns: 1fr;
      gap: clamp(2rem, 4vw, 3.5rem);
      align-items: end;
    }
    @media (min-width: 900px) {
      .hero-bottom { grid-template-columns: 1fr minmax(0, 440px); }
    }
    .hero-deck {
      font-family: var(--font-display);
      font-size: clamp(1.125rem, 1.6vw, 1.35rem);
      line-height: 1.45;
      color: var(--ink-soft);
      font-weight: 400;
      font-variation-settings: "opsz" 24;
      max-width: 46ch;
    }
    .hero-deck em { font-style: italic; color: var(--rust); font-weight: 400; }

    .hero-ctas { display: flex; gap: 14px; flex-wrap: wrap; align-items: center; }
    .btn {
      display: inline-flex;
      align-items: center;
      gap: 10px;
      padding: 14px 24px;
      border-radius: 999px;
      font-size: 15px;
      font-weight: 500;
      letter-spacing: 0.005em;
      transition: all 0.25s ease;
      cursor: pointer;
      white-space: nowrap;
      line-height: 1;
    }
    .btn-primary { background: var(--ink); color: var(--cream); border: 1px solid var(--ink); }
    .btn-primary:hover { background: var(--forest); border-color: var(--forest); transform: translateY(-1px); }
    .btn-ghost { color: var(--ink); border: 1px solid var(--rule); background: transparent; }
    .btn-ghost:hover { border-color: var(--ink); }
    .btn-arrow { transition: transform 0.25s ease; }
    .btn:hover .btn-arrow { transform: translateX(3px); }

    .section { padding: clamp(4rem, 9vw, 8rem) var(--pad-x); }
    .section-inner { max-width: var(--container-wide); margin: 0 auto; }
    .section-head { max-width: var(--container); margin: 0 auto clamp(3rem, 6vw, 5rem); }
    .section-head--narrow { max-width: var(--container-narrow); }
    .section-head .eyebrow { margin-bottom: 18px; }
    .section-title {
      font-family: var(--font-display);
      font-size: clamp(2rem, 5vw, 3.75rem);
      line-height: 1.02;
      letter-spacing: -0.025em;
      font-weight: 400;
      font-variation-settings: "opsz" 72;
      max-width: 20ch;
    }
    .section-title em { font-style: italic; color: var(--rust); }
    .section-sub {
      margin-top: 20px;
      color: var(--muted);
      font-size: 17px;
      line-height: 1.6;
      max-width: 54ch;
    }
    .section-sub a { color: var(--ink); border-bottom: 1px solid var(--rule); transition: border-color 0.2s; }
    .section-sub a:hover { border-color: var(--ink); }

    .content-section {
      max-width: var(--container-narrow);
      margin: 0 auto;
      padding: clamp(3rem, 6vw, 5rem) var(--pad-x);
      border-bottom: 1px solid var(--rule);
    }
    .content-section:last-of-type { border-bottom: none; }
    .content-section h2 {
      font-family: var(--font-display);
      font-size: clamp(1.5rem, 3vw, 2.25rem);
      line-height: 1.1;
      letter-spacing: -0.02em;
      font-weight: 400;
      font-variation-settings: "opsz" 48;
      margin-bottom: 24px;
    }
    .content-section h2 em { font-style: italic; color: var(--rust); }
    .content-section h3 {
      font-family: var(--font-display);
      font-size: clamp(1.15rem, 2vw, 1.4rem);
      line-height: 1.2;
      letter-spacing: -0.015em;
      font-weight: 500;
      font-variation-settings: "opsz" 24;
      margin-top: 32px;
      margin-bottom: 12px;
    }
    .content-section p {
      color: var(--muted);
      font-size: 17px;
      line-height: 1.65;
      margin-bottom: 16px;
      max-width: 62ch;
    }
    .content-section p:last-child { margin-bottom: 0; }
    .content-section a { color: var(--ink); border-bottom: 1px solid var(--rule); transition: border-color 0.2s; }
    .content-section a:hover { border-color: var(--ink); }

    .cta-band {
      background: var(--ink);
      color: var(--cream);
      padding: clamp(4rem, 8vw, 7rem) var(--pad-x);
      text-align: center;
    }
    .cta-band-inner {
      max-width: var(--container-narrow);
      margin: 0 auto;
    }
    .cta-band h2 {
      font-family: var(--font-display);
      font-size: clamp(2rem, 4.5vw, 3.5rem);
      line-height: 1.05;
      letter-spacing: -0.025em;
      font-weight: 400;
      font-variation-settings: "opsz" 72;
      margin-bottom: 20px;
    }
    .cta-band h2 em { font-style: italic; color: var(--star-gold); }
    .cta-band p {
      color: var(--muted-light);
      font-size: 17px;
      line-height: 1.6;
      max-width: 48ch;
      margin: 0 auto 32px;
    }
    .btn-cream { background: var(--cream); color: var(--ink); border: 1px solid var(--cream); }
    .btn-cream:hover { background: var(--paper); transform: translateY(-1px); }

    .cross-links {
      max-width: var(--container-narrow);
      margin: 0 auto;
      padding: clamp(2rem, 4vw, 3rem) var(--pad-x);
    }
    .cross-links-label {
      font-size: 11px;
      letter-spacing: 0.16em;
      text-transform: uppercase;
      color: var(--muted);
      margin-bottom: 14px;
    }
    .cross-links ul {
      list-style: none;
      display: flex;
      flex-wrap: wrap;
      gap: 10px 24px;
      font-size: 15px;
    }
    .cross-links a {
      color: var(--ink-soft);
      border-bottom: 1px solid var(--rule);
      transition: border-color 0.2s;
    }
    .cross-links a:hover { border-color: var(--ink); }

    footer {
      border-top: 1px solid var(--rule);
      padding: clamp(2.5rem, 5vw, 4rem) var(--pad-x) clamp(1.5rem, 3vw, 2rem);
      background: var(--cream);
    }
    .footer-inner {
      max-width: var(--container-wide);
      margin: 0 auto;
      display: grid;
      grid-template-columns: 1fr;
      gap: clamp(2rem, 4vw, 3rem);
    }
    @media (min-width: 760px) { .footer-inner { grid-template-columns: 2fr 1fr 1fr 1fr; } }
    .footer-brand-row {
      display: flex;
      align-items: center;
      gap: 14px;
      margin-bottom: 18px;
    }
    .footer-brand-mark { width: 36px; height: 36px; flex-shrink: 0; }
    .footer-brand-name {
      font-family: var(--font-display);
      font-size: 20px;
      letter-spacing: -0.01em;
      font-weight: 500;
      color: var(--ink);
      font-variation-settings: "opsz" 18;
    }
    .footer-brand {
      font-family: var(--font-display);
      font-size: clamp(1.5rem, 2.4vw, 2rem);
      line-height: 1.1;
      letter-spacing: -0.02em;
      font-weight: 400;
      max-width: 22ch;
      font-variation-settings: "opsz" 48;
      color: var(--ink-soft);
    }
    .footer-brand em { font-style: italic; color: var(--rust); }
    .footer-col-title {
      font-size: 11px;
      letter-spacing: 0.16em;
      text-transform: uppercase;
      color: var(--muted);
      margin-bottom: 14px;
    }
    .footer-links { list-style: none; display: flex; flex-direction: column; gap: 10px; font-size: 14px; }
    .footer-links a {
      color: var(--ink-soft);
      border-bottom: 1px solid transparent;
      transition: border-color 0.2s;
    }
    .footer-links a:hover { border-color: var(--ink-soft); }
    .footer-bottom {
      max-width: var(--container-wide);
      margin: clamp(2.5rem, 5vw, 4rem) auto 0;
      padding-top: 20px;
      border-top: 1px solid var(--rule);
      display: flex;
      justify-content: space-between;
      gap: 20px;
      flex-wrap: wrap;
      font-size: 12px;
      color: var(--muted);
      letter-spacing: 0.04em;
    }

    .reveal { opacity: 1; transform: none; }
    html.js-anim-ready .reveal {
      opacity: 0;
      transform: translateY(16px);
      transition: opacity 0.8s cubic-bezier(0.22, 1, 0.36, 1), transform 0.8s cubic-bezier(0.22, 1, 0.36, 1);
    }
    html.js-anim-ready .reveal.is-in { opacity: 1; transform: none; }
    html.js-anim-ready .reveal-stagger > * {
      opacity: 0;
      transform: translateY(18px);
      transition: opacity 0.9s cubic-bezier(0.22, 1, 0.36, 1), transform 0.9s cubic-bezier(0.22, 1, 0.36, 1);
    }
    html.js-anim-ready .reveal-stagger.is-in > * { opacity: 1; transform: none; }
    html.js-anim-ready .reveal-stagger.is-in > *:nth-child(1) { transition-delay: 0.05s; }
    html.js-anim-ready .reveal-stagger.is-in > *:nth-child(2) { transition-delay: 0.15s; }
    html.js-anim-ready .reveal-stagger.is-in > *:nth-child(3) { transition-delay: 0.25s; }
    html.js-anim-ready .reveal-stagger.is-in > *:nth-child(4) { transition-delay: 0.35s; }
    html.js-anim-ready .reveal-stagger.is-in > *:nth-child(5) { transition-delay: 0.45s; }

    @media (prefers-reduced-motion: reduce) {
      *, *::before, *::after {
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.01ms !important;
      }
      html.js-anim-ready .reveal,
      html.js-anim-ready .reveal-stagger > * { opacity: 1 !important; transform: none !important; }
    }

    /* Industries dropdown */
    .nav-dropdown { position: relative; }
    .nav-dropdown-trigger { display: inline-flex; align-items: center; gap: 4px; cursor: pointer; color: var(--ink-soft); transition: color 0.2s ease; font: inherit; font-size: inherit; }
    .nav-dropdown-trigger:hover, .nav-dropdown:focus-within .nav-dropdown-trigger { color: var(--forest); }
    .nav-dropdown-trigger::after { content: ""; border-left: 3.5px solid transparent; border-right: 3.5px solid transparent; border-top: 4px solid currentColor; margin-top: 1px; }
    .nav-dropdown-menu { display: none; position: absolute; top: 100%; left: 50%; transform: translateX(-50%); background: var(--paper); border: 1px solid var(--rule); border-radius: 8px; padding: 6px 0; min-width: 200px; margin-top: 10px; box-shadow: 0 4px 20px rgba(15, 15, 14, 0.1); z-index: 60; }
    .nav-dropdown-menu::before { content: ""; position: absolute; top: -10px; left: 0; right: 0; height: 10px; }
    .nav-dropdown:hover .nav-dropdown-menu, .nav-dropdown:focus-within .nav-dropdown-menu { display: block; }
    .nav-dropdown-menu a { display: block; padding: 8px 18px; font-size: 13px; color: var(--ink-soft); transition: background 0.15s, color 0.15s; white-space: nowrap; }
    .nav-dropdown-menu a:hover { background: var(--cream-warm); color: var(--ink); }
    @media (max-width: 720px) { .nav-dropdown { display: none; } }

    /* Hub page styles */
    .city-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
      gap: 16px;
      margin-top: 32px;
    }
    .city-card {
      border: 1px solid var(--rule);
      border-radius: 10px;
      padding: 20px 24px;
      transition: border-color 0.2s, transform 0.2s;
    }
    .city-card:hover { border-color: var(--ink); transform: translateY(-2px); }
    .city-card h3 {
      font-family: var(--font-display);
      font-size: 1.15rem;
      font-weight: 500;
      margin-bottom: 8px;
    }
    .city-card p {
      font-size: 14px;
      color: var(--muted);
      line-height: 1.5;
    }
    .vertical-list {
      list-style: none;
      display: flex;
      flex-wrap: wrap;
      gap: 8px 16px;
      margin-top: 16px;
    }
    .vertical-list a {
      font-size: 14px;
      color: var(--ink-soft);
      border-bottom: 1px solid var(--rule);
      transition: border-color 0.2s;
    }
    .vertical-list a:hover { border-color: var(--ink); }
"""

SVG_DEFS = """  <svg width="0" height="0" style="position:absolute" aria-hidden="true">
    <defs>
      <symbol id="mbf-mark" viewBox="0 0 44 44">
        <circle cx="15" cy="18" r="7" fill="none" stroke="currentColor" stroke-width="1.5"/>
        <circle cx="29" cy="26" r="7" fill="none" stroke="#A04030" stroke-width="1.5"/>
        <circle cx="22" cy="22" r="1.9" fill="#A04030"/>
      </symbol>
    </defs>
  </svg>"""

NAV = """  <header class="masthead">
    <div class="masthead-inner">
      <a href="/" class="wordmark" aria-label="My Business Feedback home">
        <svg class="wordmark-mark" aria-hidden="true"><use href="#mbf-mark"/></svg>
        <span>My Business Feedback</span>
      </a>
      <nav aria-label="Primary">
        <a href="/how-it-works/">How it works</a>
        <span class="nav-dropdown">
          <button class="nav-dropdown-trigger" aria-expanded="false" aria-haspopup="true">Industries</button>
          <span class="nav-dropdown-menu" role="menu">
            <a href="/for-law-firms/" role="menuitem">For Law Firms</a>
            <a href="/for-medical-practices/" role="menuitem">For Medical Practices</a>
            <a href="/for-service-businesses/" role="menuitem">For Service Businesses</a>
          </span>
        </span>
        <a href="/pricing/">Pricing</a>
        <a href="/blog/">Blog</a>
        <a href="/faq/">FAQ</a>
        <a href="/partner-with-us/" class="nav-cta">Partner with us</a>
      </nav>
    </div>
  </header>"""

FOOTER = """  <footer>
    <div class="footer-inner">
      <div>
        <div class="footer-brand-row">
          <svg class="footer-brand-mark" aria-hidden="true"><use href="#mbf-mark"/></svg>
          <span class="footer-brand-name">My Business Feedback</span>
        </div>
        <p class="footer-brand">For businesses <em>that listen</em>, and the customers who appreciate it.</p>
      </div>

      <div>
        <p class="footer-col-title">Company</p>
        <ul class="footer-links">
          <li><a href="/about/">About</a></li>
          <li><a href="/how-it-works/">How It Works</a></li>
          <li><a href="/pricing/">Pricing</a></li>
          <li><a href="/faq/">FAQ</a></li>
        </ul>
      </div>

      <div>
        <p class="footer-col-title">Industries</p>
        <ul class="footer-links">
          <li><a href="/for-law-firms/">For Law Firms</a></li>
          <li><a href="/for-medical-practices/">For Medical Practices</a></li>
          <li><a href="/for-service-businesses/">For Service Businesses</a></li>
        </ul>
      </div>

      <div>
        <p class="footer-col-title">Contact</p>
        <ul class="footer-links">
          <li><!--email_off--><a href="mailto:div@nexusmultimedia.ai">div@nexusmultimedia.ai</a><!--/email_off--></li>
          <li><a href="tel:+16193075951">(619) 307-5951</a></li>
          <li>San Diego, California</li>
        </ul>
      </div>
    </div>

    <div class="footer-bottom">
      <span>&copy; 2026 Nexus Multimedia. All rights reserved.</span>
    </div>
  </footer>"""

ANIM_JS = """  <script type="module">
    try {
      document.documentElement.classList.add('js-anim-ready');
      const reveals = document.querySelectorAll('.reveal, .reveal-stagger');
      if ('IntersectionObserver' in window) {
        const io = new IntersectionObserver((entries) => {
          entries.forEach(entry => {
            if (entry.isIntersecting) {
              entry.target.classList.add('is-in');
              io.unobserve(entry.target);
            }
          });
        }, { rootMargin: '0px 0px -10% 0px', threshold: 0.1 });
        reveals.forEach(el => io.observe(el));
      } else {
        reveals.forEach(el => el.classList.add('is-in'));
      }
      setTimeout(() => {
        reveals.forEach(el => {
          if (!el.classList.contains('is-in')) el.classList.add('is-in');
        });
      }, 2000);
    } catch (err) {
      document.documentElement.classList.remove('js-anim-ready');
    }
  </script>"""

GA_TAG = """  <script async src="https://www.googletagmanager.com/gtag/js?id=G-QN8FS3SJ5R"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
    gtag('config', 'G-QN8FS3SJ5R');
  </script>"""

FAVICON = """  <link rel="icon" type="image/svg+xml" href="data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 44 44'><rect width='44' height='44' fill='%23FAF8F3'/><circle cx='15' cy='18' r='7' fill='none' stroke='%230F0F0E' stroke-width='1.6'/><circle cx='29' cy='26' r='7' fill='none' stroke='%23A04030' stroke-width='1.6'/><circle cx='22' cy='22' r='1.9' fill='%23A04030'/></svg>" />"""

FONTS = """  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300..900;1,9..144,300..900&family=Instrument+Sans:ital,wght@0,400..700;1,400..700&display=swap" />"""


def vert_title(slug):
    """Return a display title for a vertical slug."""
    return {
        "law-firms": "Law Firms",
        "medical-practices": "Medical Practices",
        "med-spas": "Med Spas",
        "dental-practices": "Dental Practices",
        "home-services": "Home Services",
        "service-businesses": "Service Businesses",
    }[slug]


# ---------------------------------------------------------------------------
# GENERATORS
# ---------------------------------------------------------------------------

def generate_hub_page():
    """Generate /locations/index.html"""
    city_cards = []
    for slug, c in CITIES.items():
        city_cards.append(f"""
        <a href="/locations/{slug}/" class="city-card">
          <h3>{c['name']}, {c['state']}</h3>
          <p>{len(VERTICALS)} industry guides available</p>
        </a>""")

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Locations We Serve | My Business Feedback</title>
  <meta name="description" content="My Business Feedback works with businesses across the United States. Find structured feedback solutions for your industry in your city." />
  <link rel="canonical" href="https://mybusinessfeedback.com/locations/" />
  <meta property="og:type" content="website" />
  <meta property="og:title" content="Locations We Serve | My Business Feedback" />
  <meta property="og:description" content="My Business Feedback works with businesses across the United States. Find structured feedback solutions for your industry in your city." />
  <meta property="og:url" content="https://mybusinessfeedback.com/locations/" />
  <meta name="twitter:card" content="summary" />
  <meta name="twitter:title" content="Locations We Serve | My Business Feedback" />
  <meta name="twitter:description" content="My Business Feedback works with businesses across the United States. Find structured feedback solutions for your industry in your city." />

{FAVICON}
{FONTS}
{GA_TAG}

  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@graph": [
      {{
        "@type": "Organization",
        "name": "My Business Feedback",
        "url": "https://mybusinessfeedback.com",
        "email": "div@nexusmultimedia.ai",
        "telephone": "+16193075951",
        "address": {{
          "@type": "PostalAddress",
          "addressLocality": "San Diego",
          "addressRegion": "CA",
          "addressCountry": "US"
        }}
      }},
      {{
        "@type": "BreadcrumbList",
        "itemListElement": [
          {{
            "@type": "ListItem",
            "position": 1,
            "name": "Home",
            "item": "https://mybusinessfeedback.com/"
          }},
          {{
            "@type": "ListItem",
            "position": 2,
            "name": "Locations",
            "item": "https://mybusinessfeedback.com/locations/"
          }}
        ]
      }}
    ]
  }}
  </script>

  <style>
{CSS}
  </style>
</head>
<body>

{SVG_DEFS}

{NAV}

  <div class="meta-strip">
    <div class="meta-strip-inner">
      <span>Locations</span>
      <span><span class="dot"></span> Nationwide service</span>
      <span><span class="dot"></span> San Diego, California</span>
      <span><span class="dot"></span> Est. 2016</span>
    </div>
  </div>

  <main>

    <section class="hero">
      <div class="hero-inner">
        <h1 class="display hero-headline reveal">Structured feedback for businesses <em>across America</em></h1>
        <div class="hero-bottom reveal">
          <p class="hero-deck">
            My Business Feedback is based in San Diego, California, and works with businesses across the United States. <em>Every market has its own expectations. We help you hear them clearly.</em>
          </p>
          <div class="hero-ctas">
            <a href="/partner-with-us/" class="btn btn-primary">
              Partner with us
              <span class="btn-arrow" aria-hidden="true">&rarr;</span>
            </a>
            <a href="/how-it-works/" class="btn btn-ghost">How it works</a>
          </div>
        </div>
      </div>
    </section>

    <article>

      <div class="content-section reveal">
        <h2>Local markets, <em>national platform</em></h2>
        <p>Every city has its own business culture, customer expectations, and competitive dynamics. A law firm in New York faces different challenges than one in Nashville. A med spa in San Francisco serves a different clientele than one in Phoenix. What they share is the need to hear from their clients and patients in a structured, consistent way.</p>
        <p>My Business Feedback provides a simple feedback system that works across every industry and every market. We help law firms, medical practices, med spas, dental practices, home service businesses, and service businesses understand how their clients and patients perceive their experience. The insights are private, actionable, and specific to your practice.</p>
        <p>Below you will find guides for 25 major cities across the United States. Each guide explains how structured feedback applies to the specific business landscape, client expectations, and competitive dynamics of that market. Whether you are an established practice or a new business building your reputation, we can help you listen to the people you serve.</p>
        <p>Our approach is built on a simple principle: businesses that ask for honest feedback and act on what they hear build stronger relationships, improve their service, and grow through the trust they earn. That principle applies in every city, but the details of how it plays out are shaped by local culture, demographics, and market conditions.</p>
      </div>

      <div class="content-section reveal">
        <h2>Find your <em>city</em></h2>
        <div class="city-grid">
{"".join(city_cards)}
        </div>
      </div>

    </article>

    <section class="cta-band reveal">
      <div class="cta-band-inner">
        <h2>Ready to start <em>listening</em>?</h2>
        <p>No matter where your business is located, structured feedback can help you understand your clients better and improve the experience you deliver.</p>
        <a href="/partner-with-us/" class="btn btn-cream">
          Partner with us
          <span class="btn-arrow" aria-hidden="true">&rarr;</span>
        </a>
      </div>
    </section>

    <div class="cross-links reveal">
      <p class="cross-links-label">Continue reading</p>
      <ul>
        <li><a href="/how-it-works/">How it works</a></li>
        <li><a href="/pricing/">Pricing</a></li>
        <li><a href="/for-law-firms/">For law firms</a></li>
        <li><a href="/for-medical-practices/">For medical practices</a></li>
      </ul>
    </div>

  </main>

{FOOTER}

{ANIM_JS}

</body>
</html>"""

    path = os.path.join(BASE_DIR, "index.html")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(html)
    print(f"  Created {path}")


def generate_city_page(city_slug):
    """Generate /locations/[city]/index.html"""
    c = CITIES[city_slug]
    city = c["name"]
    state = c["state"]

    vert_links = []
    for vs, v in VERTICALS.items():
        vert_links.append(f"""
        <li><a href="/locations/{city_slug}/{vs}/">For {vert_title(vs)} in {city}</a></li>""")

    hood_text = ", ".join(c["neighborhoods"][:8])

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Business Feedback Solutions in {city}, {state} | My Business Feedback</title>
  <meta name="description" content="Structured feedback for law firms, medical practices, dental practices, med spas, and service businesses in {city}, {state}. Based in San Diego, serving businesses nationwide." />
  <link rel="canonical" href="https://mybusinessfeedback.com/locations/{city_slug}/" />
  <meta property="og:type" content="website" />
  <meta property="og:title" content="Business Feedback Solutions in {city}, {state} | My Business Feedback" />
  <meta property="og:description" content="Structured feedback for law firms, medical practices, dental practices, med spas, and service businesses in {city}, {state}." />
  <meta property="og:url" content="https://mybusinessfeedback.com/locations/{city_slug}/" />
  <meta name="twitter:card" content="summary" />
  <meta name="twitter:title" content="Business Feedback Solutions in {city}, {state} | My Business Feedback" />
  <meta name="twitter:description" content="Structured feedback for law firms, medical practices, dental practices, med spas, and service businesses in {city}, {state}." />

{FAVICON}
{FONTS}
{GA_TAG}

  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@graph": [
      {{
        "@type": "Organization",
        "name": "My Business Feedback",
        "url": "https://mybusinessfeedback.com",
        "email": "div@nexusmultimedia.ai",
        "telephone": "+16193075951",
        "address": {{
          "@type": "PostalAddress",
          "addressLocality": "San Diego",
          "addressRegion": "CA",
          "addressCountry": "US"
        }}
      }},
      {{
        "@type": "BreadcrumbList",
        "itemListElement": [
          {{
            "@type": "ListItem",
            "position": 1,
            "name": "Home",
            "item": "https://mybusinessfeedback.com/"
          }},
          {{
            "@type": "ListItem",
            "position": 2,
            "name": "Locations",
            "item": "https://mybusinessfeedback.com/locations/"
          }},
          {{
            "@type": "ListItem",
            "position": 3,
            "name": "{city}, {state}",
            "item": "https://mybusinessfeedback.com/locations/{city_slug}/"
          }}
        ]
      }},
      {{
        "@type": "Service",
        "name": "Business Feedback Solutions in {city}",
        "description": "Structured feedback for businesses in {city}, {state}.",
        "provider": {{
          "@type": "Organization",
          "name": "My Business Feedback"
        }},
        "serviceType": "Customer Feedback Management",
        "areaServed": {{
          "@type": "City",
          "name": "{city}",
          "containedInPlace": {{
            "@type": "State",
            "name": "{state}"
          }}
        }}
      }}
    ]
  }}
  </script>

  <style>
{CSS}
  </style>
</head>
<body>

{SVG_DEFS}

{NAV}

  <div class="meta-strip">
    <div class="meta-strip-inner">
      <span>{city}, {state}</span>
      <span><span class="dot"></span> Structured feedback</span>
      <span><span class="dot"></span> San Diego, California</span>
      <span><span class="dot"></span> Est. 2016</span>
    </div>
  </div>

  <main>

    <section class="hero">
      <div class="hero-inner">
        <h1 class="display hero-headline reveal">Structured feedback for businesses in <em>{city}</em></h1>
        <div class="hero-bottom reveal">
          <p class="hero-deck">
            My Business Feedback is based in San Diego, California, and works with businesses across the United States, including {city}, {state}. <em>Hear from your clients after every interaction.</em>
          </p>
          <div class="hero-ctas">
            <a href="/partner-with-us/" class="btn btn-primary">
              Partner with us
              <span class="btn-arrow" aria-hidden="true">&rarr;</span>
            </a>
            <a href="/how-it-works/" class="btn btn-ghost">How it works</a>
          </div>
        </div>
      </div>
    </section>

    <article>

      <div class="content-section reveal">
        <h2>The {city} <em>business landscape</em></h2>
        <p>{c['context'].capitalize()}. These factors shape how businesses in {city} build relationships with their clients and patients, and they influence the kind of feedback that matters most.</p>
        <p>Whether your practice is in {c['neighborhoods'][0]}, {c['neighborhoods'][1]}, or {c['neighborhoods'][2]}, the need to hear from the people you serve is the same. My Business Feedback provides a simple, structured way to collect honest feedback after every client or patient interaction, giving you the insights you need to improve service and strengthen relationships.</p>
        <p>We serve {city} businesses across six industries: law firms, medical practices, med spas, dental practices, home service businesses, and service businesses. Each industry guide below explains how structured feedback applies to the specific challenges and opportunities of operating in {city}.</p>
      </div>

      <div class="content-section reveal">
        <h2>Industry guides for <em>{city}</em></h2>
        <ul class="vertical-list">
{"".join(vert_links)}
        </ul>
      </div>

      <div class="content-section reveal">
        <h2>Serving neighborhoods across <em>{city}</em></h2>
        <p>We work with businesses serving clients and patients throughout the {city} metro area, including {hood_text}, and surrounding communities. No matter where your business is located, structured feedback helps you understand how the people you serve perceive their experience.</p>
      </div>

    </article>

    <section class="cta-band reveal">
      <div class="cta-band-inner">
        <h2>Start hearing from every <em>client</em> in {city}</h2>
        <p>Setup takes days, not weeks. No contracts. No complicated software. Just a simple way for your {city} business to listen to the people it serves.</p>
        <a href="/partner-with-us/" class="btn btn-cream">
          Partner with us
          <span class="btn-arrow" aria-hidden="true">&rarr;</span>
        </a>
      </div>
    </section>

    <div class="cross-links reveal">
      <p class="cross-links-label">Continue reading</p>
      <ul>
        <li><a href="/locations/">All locations</a></li>
        <li><a href="/how-it-works/">How it works</a></li>
        <li><a href="/pricing/">Pricing</a></li>
      </ul>
    </div>

  </main>

{FOOTER}

{ANIM_JS}

</body>
</html>"""

    path = os.path.join(BASE_DIR, city_slug, "index.html")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(html)
    print(f"  Created {path}")


def generate_city_vertical_page(city_slug, vert_slug):
    """Generate /locations/[city]/[vertical]/index.html"""
    c = CITIES[city_slug]
    v = VERTICALS[vert_slug]
    city = c["name"]
    state = c["state"]
    hoods = c["neighborhoods"]
    person = v["person"]
    person_lower = v["person_lower"]
    label = v["label"]

    title = f"Feedback for {vert_title(vert_slug)} in {city}, {state} | My Business Feedback"
    desc = f"Structured {person_lower} feedback for {label} in {city}, {state}. My Business Feedback helps you hear from every {person_lower} after every interaction."
    canonical = f"https://mybusinessfeedback.com/locations/{city_slug}/{vert_slug}/"

    market_content = get_market_content(city_slug, vert_slug)
    feedback_content = get_feedback_content(city_slug, vert_slug)
    how_content = get_how_it_works_content(city_slug, vert_slug)

    # Neighborhoods section - pick 4-5
    selected_hoods = hoods[:5]
    hood_list = ", ".join(selected_hoods[:-1]) + f", and {selected_hoods[-1]}"

    # Cross-links: other verticals in same city (pick 3)
    other_verts = [vs for vs in VERTICALS if vs != vert_slug]
    cross_vert_links = []
    for vs in other_verts[:3]:
        cross_vert_links.append(f'        <li><a href="/locations/{city_slug}/{vs}/">For {vert_title(vs)} in {city}</a></li>')

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title}</title>
  <meta name="description" content="{desc}" />
  <link rel="canonical" href="{canonical}" />
  <meta property="og:type" content="website" />
  <meta property="og:title" content="{title}" />
  <meta property="og:description" content="{desc}" />
  <meta property="og:url" content="{canonical}" />
  <meta name="twitter:card" content="summary" />
  <meta name="twitter:title" content="{title}" />
  <meta name="twitter:description" content="{desc}" />

{FAVICON}
{FONTS}
{GA_TAG}

  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@graph": [
      {{
        "@type": "Organization",
        "name": "My Business Feedback",
        "url": "https://mybusinessfeedback.com",
        "email": "div@nexusmultimedia.ai",
        "telephone": "+16193075951",
        "address": {{
          "@type": "PostalAddress",
          "addressLocality": "San Diego",
          "addressRegion": "CA",
          "addressCountry": "US"
        }}
      }},
      {{
        "@type": "BreadcrumbList",
        "itemListElement": [
          {{
            "@type": "ListItem",
            "position": 1,
            "name": "Home",
            "item": "https://mybusinessfeedback.com/"
          }},
          {{
            "@type": "ListItem",
            "position": 2,
            "name": "Locations",
            "item": "https://mybusinessfeedback.com/locations/"
          }},
          {{
            "@type": "ListItem",
            "position": 3,
            "name": "{city}, {state}",
            "item": "https://mybusinessfeedback.com/locations/{city_slug}/"
          }},
          {{
            "@type": "ListItem",
            "position": 4,
            "name": "For {vert_title(vert_slug)}",
            "item": "{canonical}"
          }}
        ]
      }},
      {{
        "@type": "Service",
        "name": "{person} Feedback for {vert_title(vert_slug)} in {city}",
        "description": "Structured {person_lower} feedback for {label} in {city}, {state}.",
        "provider": {{
          "@type": "Organization",
          "name": "My Business Feedback"
        }},
        "serviceType": "Customer Feedback Management",
        "areaServed": {{
          "@type": "City",
          "name": "{city}",
          "containedInPlace": {{
            "@type": "State",
            "name": "{state}"
          }}
        }}
      }}
    ]
  }}
  </script>

  <style>
{CSS}
  </style>
</head>
<body>

{SVG_DEFS}

{NAV}

  <div class="meta-strip">
    <div class="meta-strip-inner">
      <span>For {vert_title(vert_slug)} in {city}</span>
      <span><span class="dot"></span> {person} feedback, structured</span>
      <span><span class="dot"></span> San Diego, California</span>
      <span><span class="dot"></span> Est. 2016</span>
    </div>
  </div>

  <main>

    <section class="hero">
      <div class="hero-inner">
        <h1 class="display hero-headline reveal">{person} feedback for {label} in <em>{city}</em></h1>
        <div class="hero-bottom reveal">
          <p class="hero-deck">
            My Business Feedback is based in San Diego, California, and works with {label} across the United States, including those serving {city}, {state}. <em>Hear from every {person_lower} after every interaction.</em>
          </p>
          <div class="hero-ctas">
            <a href="/partner-with-us/" class="btn btn-primary">
              Partner with us
              <span class="btn-arrow" aria-hidden="true">&rarr;</span>
            </a>
            <a href="/how-it-works/" class="btn btn-ghost">How it works</a>
          </div>
        </div>
      </div>
    </section>

    <article>

      <div class="content-section reveal">
        <h2>The {city} <em>{label}</em> market</h2>
{market_content}
      </div>

      <div class="content-section reveal">
        <h2>Why structured feedback matters for <em>{label} in {city}</em></h2>
{feedback_content}
      </div>

      <div class="content-section reveal">
        <h2>How My Business Feedback works for <em>{city} {label}</em></h2>
{how_content}
      </div>

      <div class="content-section reveal">
        <h2>Serving {label} across <em>{city}</em></h2>
        <p>We work with {label} serving {person_lower}s throughout the {city} metro area, including those in {hood_list}. Whether your practice draws {person_lower}s from a single neighborhood or across the entire metro, structured feedback helps you understand how the people you serve perceive their experience.</p>
        <p>Each community within {city} has its own expectations and communication preferences. A {v['singular']} in {hoods[0]} may face different {person_lower} expectations than one in {hoods[3]} or {hoods[5]}. Structured feedback captures these local nuances, giving you insights that are specific to the {person_lower}s you actually serve, not generic industry averages.</p>
      </div>

    </article>

    <section class="cta-band reveal">
      <div class="cta-band-inner">
        <h2>Start hearing from every <em>{person_lower}</em> in {city}</h2>
        <p>Setup takes days, not weeks. No contracts. No complicated software. Just a simple way for your {city} {v['singular']} to listen to the people it serves.</p>
        <a href="/partner-with-us/" class="btn btn-cream">
          Partner with us
          <span class="btn-arrow" aria-hidden="true">&rarr;</span>
        </a>
      </div>
    </section>

    <div class="cross-links reveal">
      <p class="cross-links-label">Continue reading</p>
      <ul>
{chr(10).join(cross_vert_links)}
      </ul>
    </div>

  </main>

{FOOTER}

{ANIM_JS}

</body>
</html>"""

    path = os.path.join(BASE_DIR, city_slug, vert_slug, "index.html")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(html)
    print(f"  Created {path}")


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("Generating location pages...")
    print()

    # 1. Hub page
    print("[1/3] Hub page")
    generate_hub_page()
    print()

    # 2. City pages
    print("[2/3] City pages")
    for slug in CITIES:
        generate_city_page(slug)
    print()

    # 3. City-vertical pages
    print("[3/3] City-vertical pages")
    count = 0
    for city_slug in CITIES:
        for vert_slug in VERTICALS:
            generate_city_vertical_page(city_slug, vert_slug)
            count += 1
    print()

    total = 1 + len(CITIES) + count
    print(f"Done. Generated {total} pages total.")
    print(f"  Hub: 1")
    print(f"  City: {len(CITIES)}")
    print(f"  City-vertical: {count}")
