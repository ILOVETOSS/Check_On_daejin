def calculate_heat_index(temp_c, humidity):
    temp_f = (temp_c * 9/5) + 32
    HI = 0.5 * (temp_f + 61 + ((temp_f - 68) * 1.2) + (humidity * 0.094))
    if HI >= 80:
        HI = (-42.379 + 2.04901523*temp_f + 10.14333127*humidity
              - 0.22475541*temp_f*humidity - 0.00683783*temp_f**2
              - 0.05481717*humidity**2 + 0.00122874*temp_f**2*humidity
              + 0.00085282*temp_f*humidity**2 - 0.00000199*temp_f**2*humidity**2)
    return round((HI - 32) * 5/9,1)

def get_uv_level(uv_index):
    if uv_index < 3:
        return "낮음", "#10B981"
    elif uv_index < 6:
        return "보통", "#F59E0B"
    elif uv_index < 8:
        return "높음", "#EF4444"
    elif uv_index < 11:
        return "매우 높음", "#DC2626"
    else:
        return "위험", "#7C2D12"

def get_pm10_level(pm10):
    if pm10 <= 30:
        return "좋음", "#10B981"
    elif pm10 <= 80:
        return "보통", "#F59E0B"
    elif pm10 <= 150:
        return "나쁨", "#EF4444"
    else:
        return "매우 나쁨", "#7C2D12"
