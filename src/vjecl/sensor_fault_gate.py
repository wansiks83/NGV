"""!
@brief MOD-03 SensorFaultGate. ENG-SWE3-001 5절 함수 계약 참고. SWR-021.
"""
from vjecl.types import NormalizedSnapshot


def shouldHoldLastOutput(snapshot: NormalizedSnapshot) -> bool:
    """!
    @brief sensor_fault가 유효하게 TRUE이면 직전 확정 출력을 유지해야 하는지 판정한다.
    @param snapshot 정규화된 입력 스냅샷(sensorFault 필드 사용).
    @return sensorFault가 valid=True이고 value=True이면 True, 그 외는 False.
    """
    sensorFault = snapshot.sensorFault
    return bool(sensorFault.valid and sensorFault.value is True)
