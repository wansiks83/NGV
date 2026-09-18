"""!
@brief 단위/통합 시험에서 공통으로 쓰는 유효한 입력 픽스처. 중복 정의를 피하기 위해 이 모듈에서만 정의한다.
"""

VALID_VEHICLE = {
    "vehicle_speed_kph": 60.0,
    "gear": "D",
    "source_timestamp_s": 100.0,
    "crash_status": "NONE",
    "rear_left_approach_risk": False,
    "rear_right_approach_risk": False,
    "fire_detected": False,
    "overtemperature_detected": False,
    "adult_present": False,
    "isofix_left": False,
    "isofix_right": False,
    "ignition_on": True,
    "sensor_fault": False,
}

VALID_DRIVER = {"side": "left", "action": "lock", "source": "physical_button"}


def buildVehicle(**overrides):
    """!
    @brief 유효한 기본 Vehicle 입력을 복사한 뒤 일부 필드를 덮어써 테스트 입력을 만든다.
    """
    vehicle = dict(VALID_VEHICLE)
    vehicle.update(overrides)
    return vehicle
