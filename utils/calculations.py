def calculate_heat_index(temp, humidity):
    # 간단한 체감온도 계산 (Steadman 근사식)
    hi = 0.5 * (temp + 61.0 + ((temp-68.0)*1.2) + (humidity*0.094))
    if hi >= 80:
        hi = -42.379 + 2.04901523*temp + 10.14333127*humidity \
             - 0.22475541*temp*humidity - 6.83783e-3*temp**2 \
             - 5.481717e-2*humidity**2 + 1.22874e-3*temp**2*humidity \
             + 8.5282e-4*temp*humidity**2 - 1.99e-6*temp**2*humidity**2
    return hi
