"""!
@brief Phase 3 통합시험 — Phase 1/2 기반모듈 + ForcedReleasePolicy + IsofixLockPolicy + IgnitionOffPolicy
       (ENG-SWE2-001 11절 통합 전략 3단계, 8절 우선순위 P0~P5 검증).
       PriorityArbiter 본체는 Phase 5 대상이므로, 이 시험은 우선순위 규칙만 최소 로컬 헬퍼로 검증한다.
"""
import unittest

from vjecl.policies.approach_risk_policy import evaluate as evaluateApproachRisk
from vjecl.policies.crash_release_policy import evaluate as evaluateCrashRelease
from vjecl.policies.forced_release_policy import evaluate as evaluateForcedRelease
from vjecl.policies.ignition_off_policy import evaluate as evaluateIgnitionOff
from vjecl.policies.isofix_lock_policy import evaluate as evaluateIsofixLock
from vjecl.input_gateway import normalize
from vjecl.sensor_fault_gate import shouldHoldLastOutput
from vjecl.types import Action, Door

from fixtures import VALID_DRIVER, buildVehicle


def resolveByAsilPriority(door):
    """!
    @brief ENG-SWE2-001 8절 우선순위표 P0~P5를 반영한 최소 중재 헬퍼(시험 전용, 프로덕션 코드 아님).
           P0(SensorFaultGate) > P1(Crash) > P2(ForcedRelease) > P3(ApproachRisk) > P4(Isofix) > P5(IgnitionOff).
    """

    def resolve(snapshot, previousDecision):
        if shouldHoldLastOutput(snapshot):
            return "HOLD_LAST_OUTPUT"
        for evaluator in (
            evaluateCrashRelease,
            evaluateForcedRelease,
            evaluateApproachRisk,
            evaluateIsofixLock,
            evaluateIgnitionOff,
        ):
            vote = evaluator(snapshot, previousDecision, door)
            if vote is not None:
                return vote.action
        return None

    return resolve


class Phase3ForcedPriorityIntegrationTest(unittest.TestCase):
    def test_forcedReleaseAloneReleases(self):
        """!
        @brief 화재 단독 트리거는 해제로 귀결되어야 함을 검증한다.
        @technique 요구사항기반시험
        @case 긍정(Positive) - 강제해제 단독 시나리오 검증
        """
        snapshot = normalize(buildVehicle(fire_detected=True), VALID_DRIVER)
        resolve = resolveByAsilPriority(Door.LEFT)
        self.assertEqual(resolve(snapshot, None), Action.RELEASE)

    def test_forcedReleaseOverridesApproachRiskLock(self):
        """!
        @brief 화재(P2)와 접근위험(P3)이 동시에 발생하면 화재 강제해제가 우선해야 함을 검증한다.
        @technique 의사결정표기반
        @case 부정(Negative) - 두 조건 동시 발생 시 P2>P3 우선순위 검증
        """
        snapshot = normalize(
            buildVehicle(fire_detected=True, rear_left_approach_risk=True), VALID_DRIVER
        )
        resolve = resolveByAsilPriority(Door.LEFT)
        self.assertEqual(resolve(snapshot, None), Action.RELEASE)

    def test_isofixOverridesIgnitionOff(self):
        """!
        @brief ISOFIX(P4)와 ignition-off(P5)가 동시에 발생하면 ISOFIX 강제잠금이 우선해야 함을 검증한다.
        @technique 의사결정표기반
        @case 부정(Negative) - 두 조건 동시 발생 시 P4>P5 우선순위 검증
        """
        snapshot = normalize(buildVehicle(isofix_left=True, ignition_on=False), VALID_DRIVER)
        resolve = resolveByAsilPriority(Door.LEFT)
        self.assertEqual(resolve(snapshot, None), Action.LOCK)

    def test_crashOverridesForcedReleaseTiedResult(self):
        """!
        @brief 크래시(P1)와 화재(P2)가 동시에 발생해도 둘 다 RELEASE이므로 결과가 일치해야 하며,
               우선순위 체인이 예외 없이 끝까지 평가되어야 함을 검증한다.
        @technique 요구사항기반시험
        @case 긍정(Positive) - 동일 결과를 내는 두 안전조건의 통합 처리 검증
        """
        snapshot = normalize(
            buildVehicle(crash_status="CONFIRMED", fire_detected=True), VALID_DRIVER
        )
        resolve = resolveByAsilPriority(Door.RIGHT)
        self.assertEqual(resolve(snapshot, None), Action.RELEASE)

    def test_sensorFaultGateOverridesForcedReleaseAndIsofix(self):
        """!
        @brief sensor_fault(P0 게이트)가 화재/ISOFIX 등 하위 정책 vote보다 우선해
               직전 출력 유지로 귀결되어야 함을 검증한다.
        @technique 결함주입시험
        @case 부정(Negative) - 결함 상황에서의 최우선 게이트 검증(Phase 3 정책 포함)
        """
        snapshot = normalize(
            buildVehicle(fire_detected=True, isofix_left=True, sensor_fault=True), VALID_DRIVER
        )
        resolve = resolveByAsilPriority(Door.LEFT)
        self.assertEqual(resolve(snapshot, None), "HOLD_LAST_OUTPUT")

    def test_noHazardsProduceNoVoteAcrossAllPhase3Policies(self):
        """!
        @brief 아무 강제 조건도 없으면 Phase 1~3의 모든 정책이 vote를 내지 않아야 함을 검증한다.
        @technique 요구사항기반시험
        @case 긍정(Positive) - 정상 통합 흐름(트리거 없음) 검증
        """
        snapshot = normalize(buildVehicle(), VALID_DRIVER)
        resolve = resolveByAsilPriority(Door.LEFT)
        self.assertIsNone(resolve(snapshot, None))


if __name__ == "__main__":
    unittest.main()
