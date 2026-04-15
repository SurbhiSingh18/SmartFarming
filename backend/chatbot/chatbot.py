import re

def _normalize_text(text):
    return re.sub(r"[^a-z0-9\s]", " ", str(text).lower()).strip()

def _safe_number(value, fallback=0):
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return fallback

def _soil_status(moisture):
    if moisture < 30:
        return "dry"
    if moisture < 60:
        return "moderately wet"
    return "very wet"

def get_response(user_input, moisture, temperature):
    text = _normalize_text(user_input)
    moisture = _safe_number(moisture, fallback=0)
    temperature = _safe_number(temperature, fallback=0)

    tokens = set(text.split())

    greeting_words = {"hi", "hello", "hey", "good", "morning", "afternoon"}
    irrigation_words = {"irrigate", "irrigation", "water", "watering"}
    moisture_words = {"moisture", "soil", "wet", "dry"}
    temperature_words = {"temperature", "temp", "heat", "hot", "cold"}
    recommendation_words = {"advice", "recommend", "suggest", "tip", "status", "summary"}

    # 1. Greeting
    if tokens & greeting_words:
        return "Hello! I can help with soil, temperature, and irrigation advice 🌱"

    # 2. Irrigation (higher priority)
    if tokens & irrigation_words:
        if moisture < 30:
            return f"Soil moisture is {moisture}%. Irrigation recommended 🚿."
        return f"Soil moisture is {moisture}%. No irrigation needed ✅."

    # 3. Moisture / Soil
    if tokens & moisture_words:
        status = _soil_status(moisture)
        return f"Soil moisture is {moisture}%. Soil is {status}."

    # 4. Temperature
    if tokens & temperature_words:
        if temperature > 35:
            return f"Temperature is {temperature}°C 🔥 (high)."
        elif temperature < 15:
            return f"Temperature is {temperature}°C ❄️ (low)."
        return f"Temperature is {temperature}°C 🌡️ (normal)."

    # 5. Full Summary
    if tokens & recommendation_words:
        status = _soil_status(moisture)
        irrigation_needed = "Yes" if moisture < 30 else "No"
        return (
            f"Field Summary:\n"
            f"- Soil: {status}\n"
            f"- Moisture: {moisture}%\n"
            f"- Temperature: {temperature}°C\n"
            f"- Irrigation Needed: {irrigation_needed}"
        )

    # 6. Fallback
    return (
        "Sorry, I didn't understand.\n"
        "Try asking:\n"
        "- 'Is soil dry?'\n"
        "- 'What is temperature?'\n"
        "- 'Should I irrigate?'"
    )