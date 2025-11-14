import serial
import threading
import time

# ==== 설정: 필요 시 포트 변경 ====
SERIAL_PORT = 'COM3'
BAUDRATE = 9600
TIMEOUT = 1

# 전역 상태
latest_temperature = None
latest_humidity = None
stop_thread = False

# 안전하게 시리얼 초기화 (예외 처리 포함)
def open_serial():
    try:
        ser = serial.Serial(SERIAL_PORT, BAUDRATE, timeout=TIMEOUT)
        # 아두이노 리셋/초기화 대기
        time.sleep(2)
        ser.reset_input_buffer()
        print(f"[INFO] Serial opened on {SERIAL_PORT} @ {BAUDRATE}")
        return ser
    except Exception as e:
        print(f"[WARN] 시리얼 포트 열기 실패: {e}")
        return None

arduino = open_serial()

def serial_listener():
    global latest_temperature, latest_humidity, stop_thread, arduino

    while not stop_thread:
        try:
            if arduino is None:
                # 포트가 없으면 재시도 (1초 간격)
                arduino = open_serial()
                time.sleep(1)
                continue

            if arduino.in_waiting > 0:
                line = arduino.readline().decode('utf-8', errors='ignore').strip()

                if not line:
                    continue

                # 아두이노 오류 메시지 필터링
                if "Error" in line:
                    print("[센서 오류] DHT 읽기 실패")
                    continue

                # "온도,습도" 형태만 처리
                if "," not in line:
                    # 의심되는 잡음 무시
                    continue

                parts = line.split(",")
                if len(parts) < 2:
                    continue

                temp_str, hum_str = parts[0].strip(), parts[1].strip()

                try:
                    temp_val = float(temp_str)
                    hum_val = float(hum_str)
                except ValueError:
                    # 파싱 실패시 무시
                    continue

                # 현실적인 범위 필터 (너무 엄격하지 않게)
                if  -40 <= temp_val <= 100 and 0 <= hum_val <= 100:
                    latest_temperature = temp_val
                    latest_humidity = hum_val
                    print("[OK]", f"{temp_val:.1f}", f"{hum_val:.1f}")
                else:
                    print("[WARN] 범위 밖 값 무시:", temp_val, hum_val)

        except Exception as e:
            print("[ERROR] serial_listener:", e)
            # 잠깐 대기 후 반복
            time.sleep(0.2)

# 데몬 쓰레드로 리스너 시작
listener_thread = threading.Thread(target=serial_listener, daemon=True)
listener_thread.start()

# 외부 접근용 읽기 함수
def read_temperature():
    return latest_temperature

def read_humidity():
    return latest_humidity

# 종료시 정리
def stop_sensor_reader():
    global stop_thread, arduino
    stop_thread = True
    # 쓰레드가 정리될 시간
    time.sleep(0.1)
    try:
        if arduino and arduino.is_open:
            arduino.close()
            print("[INFO] Serial closed")
    except Exception as e:
        print("[WARN] close serial failed:", e)
