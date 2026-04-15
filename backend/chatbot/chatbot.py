def get_response(user_input, moisture, temperature):
    user_input = user_input.lower()

    # Soil moisture check
    if "moisture" in user_input or "soil" in user_input:
        if moisture < 30:
            return "Soil is dry 🌵. Irrigation needed."
        elif moisture < 60:
            return "Soil is moderately wet 🌱."
        else:
            return "Soil is very wet 💧. No irrigation needed."

    # Irrigation advice
    elif "irrigate" in user_input or "water" in user_input:
        if moisture < 30:
            return "Yes, you should irrigate the field 🚿."
        else:
            return "No, irrigation is not required now ❌."

    # Temperature check
    elif "temperature" in user_input:
        if temperature > 35:
            return f"Temperature is {temperature}°C 🔥. Too hot for crops."
        else:
            return f"Temperature is {temperature}°C 🌡️."

    else:
        return "Ask me about soil, moisture, temperature or irrigation."