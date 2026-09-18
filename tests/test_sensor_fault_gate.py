"""!
@brief MOD-03 SensorFaultGate 단위 시험 (SWR-021).
"""
import unittest

from vjecl.sensor_fault_gate import shouldHoldLastOutput
from vjecl.types import NormalizedField


def buildSnapshotStub(sensorFaultValue, sensorFaultValid=True):
    """!
    @brief 테스트용 최소 스냅샷 스텁. sensorFault 필드만 실제로 사용된다.
    """
    class SnapshotStub:
        pass

    stub = SnapshotStub()
    stub.sensorFault = NormalizedField(value=sensorFaultValue, valid=sensorFaultValid)
    return stub


class SensorFaultGateTest(unittest.TestCase):
    def test_sensorFaultTrueHoldsLastOutput(self):
        """!
        @brief sensor_fault가 유효하게 TRUE이면 직전 출력을 유지해야 함(True 반환)을 검증한다.
        @technique 사전조건·사후조건검증
        @case 부정(Negative) - 결함 상황에 대한 방어 동작 검증
        """
        snapshot = buildSnapshotStub(sensorFaultValue=True, sensorFaultValid=True)
        self.assertTrue(shouldHoldLastOutput(snapshot))

    def test_sensorFaultFalseDoesNotHoldOutput(self):
        """!
        @brief sensor_fault가 유효하게 FALSE이면 직전 출력을 유지하지 않아야 함(False 반환)을 검증한다.
        @technique 사전조건·사후조건검증
        @case 긍정(Positive) - 정상 흐름 검증
        """
        snapshot = buildSnapshotStub(sensorFaultValue=False, sensorFaultValid=True)
        self.assertFalse(shouldHoldLastOutput(snapshot))

    def test_invalidSensorFaultFieldDoesNotHoldOutput(self):
        """!
        @brief sensor_fault 입력 자체가 무효(valid=False)면 게이트를 발동하지 않아야 함을 검증한다.
        @technique 오류추정
        @case 부정(Negative) - 무효 입력에 대한 안전한 기본 동작 검증
        """
        snapshot = buildSnapshotStub(sensorFaultValue=True, sensorFaultValid=False)
        self.assertFalse(shouldHoldLastOutput(snapshot))


if __name__ == "__main__":
    unittest.main()
