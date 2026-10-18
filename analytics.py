import math

SPEED_OF_LIGHT = 300_000_000
def calculate_wafelength(frequency_mhz: float) -> float:
    """
    РАДИОТЕХНИКА: Расчет длины волны лямбда (в метрах).
    Формула: lambda = c / f
    """
    frequency_hz = frequency_mhz * 1_000_000
    wafelength = SPEED_OF_LIGHT / frequency_hz
    return round(wafelength, 4)
def convert_mw_to_dbm(power_mw: float) -> float:
    if power_mw <= 0:
        return -140.0 #Радиотишина
    dbm = 10* math.log10(power_mw)
    return round(dbm, 2)
def detect_harmonic_interference(base_freq_mhz: float, noise_freq_mhz: float) -> dict:
    order = noise_freq_mhz / base_freq_mhz
    nearest_order = round(order)
    deviation = abs(order - nearest_order)
    is_harmonic = deviation < 0.05 and nearest_order > 1

    return {
        "is_anomaly": is_harmonic,
        "harmonic_order": nearest_order if is_harmonic else 0,
        "deviation_percent": round(deviation * 100, 2)
    }