import asyncio
import random
from sqlalchemy.ext.asyncio import AsyncSession
from database import async_session
from models import RadioTelemetryLog
from analytics import detect_harmonic_interference

async def generate_async_telemetry(records_count: int):
    """
    Асинхронный конвейер генерации и заливки логов БПЛА.
    Использует SQLAlchemy ORM для безопасной и быстрой вставки.
    """
    print(f"[SYSTEM] Старт асинхронной генерации массива на {records_count} записей...")
    
    
    async with async_session() as session:
        try:
            for i in range(records_count):
                base_freq = round(random.uniform(914.5, 915.5), 2)
                
                
                if i % 10 == 0:
                    noise_freq = round((base_freq * 2) + random.uniform(-0.3, 0.3), 2)
                elif i % 13 == 0:
                    noise_freq = round((base_freq * 3) + random.uniform(-0.2, 0.3), 2)
                else:
                    noise_freq = round(random.uniform(100.0, 3000.0), 2)
                
                
                analysis = detect_harmonic_interference(base_freq, noise_freq)
                
                
                new_log = RadioTelemetryLog(
                    base_frequency_mhz=base_freq,
                    noise_frequency_mhz=noise_freq,
                    is_anomaly=analysis["is_anomaly"],
                    harmonic_order=analysis["harmonic_order"],
                    deviation_percent=analysis["deviation_percent"]
                )
                
                
                session.add(new_log)
                
                
                if i % 50000 == 0 and i > 0:
                    print(f"[PROGRESS] Подготовлено строк к заливке: {i}...")
                    await session.commit()
            
            
            print("[SYSTEM] Запись пакета в PostgreSQL...")
            await session.commit()
            print(f"[FINISH] Асинхронный полигон готов! Успешно залито {records_count} логов через ORM.")
            
        except Exception as exc:
            await session.rollback() 
            print(f"[ERROR] Сбой асинхронного конвейера: {exc}")

if __name__ == "__main__":
    
    asyncio.run(generate_async_telemetry(1000000))
