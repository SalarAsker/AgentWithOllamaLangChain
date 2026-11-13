"""AI-text med LangChain/Ollama och trygg lokal reservfunktion."""
import json
import re
from careers import CAREERS, fallback_result

MODEL = "llama3.2:3b"
OLLAMA_URL = "http://192.168.0.126:11434"

def generate(career_id: str, name: str, interest: str, strength: str, adventure: str, model: str = MODEL, base_url: str = OLLAMA_URL, demo: bool = False) -> tuple[dict, str]:
    backup = fallback_result(career_id, name, strength)
    if demo:
        return backup, "Demoläge"
    try:
        from langchain_ollama import ChatOllama
        from langchain_core.messages import HumanMessage, SystemMessage
        c = CAREERS[career_id]
        llm = ChatOllama(model=model, base_url=base_url, temperature=0.7, num_predict=230, num_ctx=1024, format="json", client_kwargs={"timeout": 24})
        system = ("Du skriver fantasifulla, peppande karriärkort på enkel svenska för 15-åringar. "
                  "Det är en LEK, inte ett vetenskapligt karriärtest. Svara ENBART med ett JSON-objekt "
                  "med nycklarna story, programming, mission. Alla värden ska vara strängar. "
                  "story: 2 korta meningar, max 45 ord. programming: 1 mening om hur kod används. "
                  "mission: 1 rolig utmaning, max 12 ord. Inga procentsatser eller påståenden om verkliga förmågor. "
                  "Undvik personliga känsliga uppgifter och låt karriären vara exakt den angivna.")
        prompt = (f"Karriär: {c['title']}. Beskrivning: {c['tagline']}. "
                  f"Förnamn (valfritt): {name[:24]!r}. Intresse: {interest}. "
                  f"Styrka: {strength}. Äventyr: {adventure}. "
                  "Skriv lekfullt och engagerande. Svara bara med JSON.")
        response = llm.invoke([SystemMessage(content=system), HumanMessage(content=prompt)])
        raw = response.content if isinstance(response.content, str) else str(response.content)
        raw = re.sub(r"<think>.*?</think>", "", raw, flags=re.S).strip()
        data = json.loads(raw)
        for key, limit in (("story", 500), ("programming", 300), ("mission", 160)):
            if not isinstance(data.get(key), str) or not data[key].strip():
                raise ValueError(f"Missing {key}")
            backup[key] = data[key].strip()[:limit]
        return backup, "AI-genererat med Ollama"
    except Exception:
        return backup, "Reservläge (AI kunde inte nås)"
