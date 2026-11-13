"""Lokala karriärkort och deterministiskt reservläge."""
import hashlib

CAREERS = {
    "robot": {"title": "AI-robotdesigner", "icon": "🤖", "category": "Teknik", "tagline": "Du bygger robotar som hjälper människor!", "programming": "Med Python lär du roboten att fatta smarta beslut.", "mission": "Designa en robot som hittar borttappade saker!", "colors": ("#00d4ff", "#7c3aed")},
    "space": {"title": "Rymdutforskare med AI", "icon": "🚀", "category": "Vetenskap", "tagline": "Du utforskar okända planeter med smarta robotar!", "programming": "Med kod styr du robotar och analyserar data från rymden.", "mission": "Programmera en robot som upptäcker vatten på Mars!", "colors": ("#ff8a4c", "#7434d4")},
    "game": {"title": "Spelvärldsarkitekt", "icon": "🎮", "category": "Spel", "tagline": "Du skapar spelvärldar som reagerar på spelaren!", "programming": "Python och AI kan ge spelkaraktärer smarta beteenden.", "mission": "Skapa en spelkaraktär som lär sig av dina val!", "colors": ("#20e3b2", "#3464ed")},
    "health": {"title": "Hälsoteknikuppfinnare", "icon": "🧬", "category": "Hälsa", "tagline": "Du uppfinner teknik som gör vården smartare!", "programming": "Kod hjälper dig analysera data och utveckla användbara verktyg.", "mission": "Bygg en app som påminner om att ta pauser!", "colors": ("#ff6ba9", "#5c6cff")},
    "ocean": {"title": "Havsmysteriedetektiv", "icon": "🌊", "category": "Natur", "tagline": "Du utforskar djuphavet med AI-drönare!", "programming": "Du programmerar sensorer och robotar som kartlägger haven.", "mission": "Hitta en okänd art med en undervattensrobot!", "colors": ("#00bcd4", "#064acb")},
    "art": {"title": "Digital drömkonstnär", "icon": "🎨", "category": "Design", "tagline": "Du skapar interaktiv konst och magiska upplevelser!", "programming": "Med kod bygger du konst som reagerar på ljud och rörelse.", "mission": "Gör en tavla som ändrar färg när någon ler!", "colors": ("#ff6b6b", "#8b5cf6")},
    "climate": {"title": "Klimathjälte 2035", "icon": "🌱", "category": "Miljö", "tagline": "Du använder teknik för att skydda planeten!", "programming": "Python kan analysera miljödata och hitta smartare lösningar.", "mission": "Skapa ett system som sparar energi i skolan!", "colors": ("#a3e635", "#0f9d89")},
    "security": {"title": "Cyberdetektiv", "icon": "🛡️", "category": "Säkerhet", "tagline": "Du löser digitala mysterier och skyddar information!", "programming": "Kod hjälper dig hitta misstänkta mönster och bygga säkra system.", "mission": "Skapa ett program som känner igen starka lösenord!", "colors": ("#f59e0b", "#ef4444")},
    "sport": {"title": "Sportteknikcoach", "icon": "🏆", "category": "Sport", "tagline": "Du hjälper idrottare att träna smartare med teknik!", "programming": "Python kan analysera träningsdata och visualisera framsteg.", "mission": "Bygg en app som räknar träningspoäng!", "colors": ("#f97316", "#ec4899")},
    "music": {"title": "Musikteknikskapare", "icon": "🎵", "category": "Musik", "tagline": "Du uppfinner nya sätt att skapa och uppleva musik!", "programming": "Med kod skapar du interaktiva instrument och ljusshower.", "mission": "Gör ett digitalt instrument med tre knappar!", "colors": ("#d946ef", "#3b82f6")},
    "food": {"title": "Framtidens matuppfinnare", "icon": "🍓", "category": "Mat", "tagline": "Du hittar nya sätt att laga god och hållbar mat!", "programming": "Kod kan hjälpa dig planera recept och minska matsvinn.", "mission": "Bygg en app som föreslår recept av rester!", "colors": ("#fb7185", "#f59e0b")},
    "city": {"title": "Smartstadens arkitekt", "icon": "🏙️", "category": "Samhälle", "tagline": "Du designar städer som är bättre att leva i!", "programming": "Du programmerar smarta trafikljus och energieffektiva system.", "mission": "Gör ett trafikljus som anpassar sig efter trafiken!", "colors": ("#38bdf8", "#6366f1")},
}

INTEREST_MAP = {
    "Teknik & robotar": ["robot", "security", "city"],
    "Spel & gaming": ["game", "robot", "art"],
    "Konst & design": ["art", "game", "music"],
    "Djur & natur": ["ocean", "climate", "space"],
    "Rymden & mysterier": ["space", "ocean", "security"],
    "Hjälpa människor": ["health", "city", "robot"],
    "Sport & rörelse": ["sport", "health", "city"],
    "Musik & kreativitet": ["music", "art", "game"],
    "Mat & uppfinningar": ["food", "climate", "health"],
}

def select_career(interest: str, strength: str, adventure: str, nonce: int = 0) -> str:
    options = INTEREST_MAP.get(interest, list(CAREERS))
    seed = f"{interest}|{strength}|{adventure}|{nonce}"
    idx = int(hashlib.sha256(seed.encode()).hexdigest(), 16) % len(options)
    return options[idx]

def fallback_result(career_id: str, name: str, strength: str) -> dict:
    c = CAREERS[career_id]
    greeting = f"{name}, du" if name.strip() else "Du"
    return {
        "career_id": career_id,
        "title": c["title"],
        "tagline": c["tagline"],
        "story": f"Året är 2035! {greeting} använder din styrka – {strength.lower()} – för att skapa något som världen aldrig sett förut. {c['tagline']} Det här är ett fantasifullt framtidsäventyr!",
        "programming": c["programming"],
        "mission": c["mission"],
    }
