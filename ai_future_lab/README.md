# AI Future Lab 2035 — Öppet hus

Svensk Streamlit-app för årskurs 9. AI körs på en **Ollama-server på nätverket**, med automatiskt reservläge.

## Starta på Windows (laptop)

1. Installera Python 3.11 eller 3.12. Du behöver **inte installera Ollama på laptopen**.
2. Packa upp ZIP-filen och öppna terminalen i mappen `ai_future_lab`.
3. Kör `python -m pip install -r requirements.txt`
4. Kör `python -m streamlit run app.py`
5. Öppna http://localhost:8501
6. I sidopanelen: Ollama-server = `http://192.168.0.126:11434`, modell = `qwen3.5:9b`. Välj **Auto (AI + reserv)**.

## Kontrollera serveranslutningen

På laptopen, öppna http://192.168.0.126:11434/api/tags i webbläsaren. Du ska se JSON med serverns modeller. Kontrollera modellens exakta namn. Om sidan inte öppnas: kontrollera samma Wi-Fi/LAN, brandvägg och att Ollama lyssnar på nätverksgränssnittet. På servern kan Ollama behöva startas med `OLLAMA_HOST=0.0.0.0:11434` (konfigurera som miljövariabel för tjänsten och starta om). Öppna endast inom ett betrott lokalt nätverk, inte mot internet.

## Reservläge

**Demoläge** fungerar utan server. **Auto** försöker servern och visar färdiga texter om den inte svarar inom timeout. Alla illustrationer är lokala.

## Viktigt

Qwen3.5:9b måste vara installerad **på servern**, inte på laptopen. Om servern använder ett annat modellnamn ändrar du det i sidopanelen. Testa anslutningen före Öppet hus.
