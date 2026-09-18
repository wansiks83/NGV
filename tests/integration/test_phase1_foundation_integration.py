"""!
@brief Phase 1 통합시험 — InputGateway -> DegradedStateManager -> SensorFaultGate
       (ENG-SWE2-001 7절 동적 동작, 11절 통합 전략 1단계). 모의객체 없이 실제 모듈로 실행한다.
"""
import unittest

from vjecl.degraded_state_manager import evaluate as evaluateDegraded
from vjecl.input_gateway import normalize
from vjecl.sensor_fault_gate import shouldHoldLastOutput

from fixtures import VALID_DRIVER, VALID_VEHICLE


def runFoundationPipeline(rawVehicle, rawDriver, previousTimestampS, currentTimestampS):
    """!
    @brief 아키텍처 7절이 정의한 순서(InputGateway -> DegradedStateManager -> SensorFaultGate)로
           세 모듈을 실제로 연결해 실행한다(오케스트레이터 역할, Phase 5에서 정식 구현될 로직의 임시 통합 지점).
    """
    snapshot = normalize(rawVehicle, rawDriver)
    degradedResult = evaluateDegraded(snapshot, previousTimestampS, currentTimestampS)
    holdLastOutput = shouldHoldLastOutput(snapshot)
    return snapshot, degradedResult, holdLastOutput


class Phase1FoundationIntegrationTest(unittest.TestCase):
    def test_normalInputsFlowThroughAllThreeModulesCleanly(self):
        """!
        @brief 정상 입력이 세 모듈을 통과할 때 DEGRADED도 FAULT도 아니어야 함을 검증한다.
        @technique 요구사항기반시험
        @case 긍정(Positive) - 정상 통합 흐름 검증
        """
        snapshot, degraded, holdOutput = runFoundationPipeline(
            VALID_VEHICLE, VALID_DRIVER, previousTimestampS=100.0, currentTimestampS=100.05
        )
        self.assertTrue(snapshot.vehicleSpeedKph.valid)
        self.assertFalse(degraded.isDegraded)
        self.assertFalse(holdOutput)

    def test_staleInputTriggersDegradedRegardlessOfSensorFault(self):
        """!
        @brief InputGateway가 정상 처리한 입력이라도 staleness가 200ms를 넘으면
               DegradedStateManager가 DEGRADED로 판정해야 함을 검증한다(모듈 간 결합 검증).
        @technique 요구사항기반시험, 경계값분석
        @case 부정(Negative) - stale 입력에 대한 통합 동작 검증
        """
        _, degraded, _ = runFoundationPipeline(
            VALID_VEHICLE, VALID_DRIVER, previousTimestampS=100.0, currentTimestampS=100.3
        )
        self.assertTrue(degraded.isDegraded)

    def test_sensorFaultHoldsOutputEvenWhenNotDegraded(self):
        """!
        @brief sensor_fault=TRUE이면 staleness가 없어도(DEGRADED가 아니어도) 직전 출력을 유지해야 함을
               검증한다(SensorFaultGate가 DegradedStateManager와 독립적으로 동작함을 통합 수준에서 확인).
        @technique 결함주입시험
        @case 부정(Negative) - 결함 상황의 통합 동작 검증
        """
        vehicle = dict(VALID_VEHICLE)
        vehicle["sensor_fault"] = True
        _, degraded, holdOutput = runFoundationPipeline(
            vehicle, VALID_DRIVER, previousTimestampS=100.0, currentTimestampS=100.05
        )
        self.assertFalse(degraded.isDegraded)
        self.assertTrue(holdOutput)

    def test_invalidDriverCommandDoesNotBreakPipeline(self):
        """!
        @brief 운전자 명령이 무효(미등록 enum)여도 나머지 모듈 실행이 중단되지 않아야 함을 검증한다
               (인터페이스시험: InputGateway의 방어적 처리가 하류 모듈에 예외를 전파하지 않음).
        @technique 인터페이스시험
        @case 부정(Negative) - 무효 명령에 대한 통합 회복력 검증
        """
        badDriver = {"side": "up", "action": "lock", "source": "physical_button"}
        snapshot, degraded, holdOutput = runFoundationPipeline(
            VALID_VEHICLE, badDriver, previousTimestampS=100.0, currentTimestampS=100.05
        )
        self.assertIsNone(snapshot.driverCommand)
        self.assertFalse(degraded.isDegraded)
        self.assertFalse(holdOutput)


if __name__ == "__main__":
    unittest.main()
