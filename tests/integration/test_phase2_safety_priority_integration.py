"""!
@brief Phase 2 통합시험 — Phase 1 기반모듈 + CrashReleasePolicy + ApproachRiskPolicy
       (ENG-SWE2-001 11절 통합 전략 2단계, 8절 우선순위 정책 의사결정표 P0~P3 검증).
       PriorityArbiter 본체는 Phase 5 구현 대상이므로, 이 시험은 P0~P3 우선순위 규칙만
       최소 로컬 헬퍼로 검증한다(실제 Arbiter 로직을 대체하지 않음).
"""
import unittest

from vjecl.degraded_state_manager import evaluate as evaluateDegraded
from vjecl.input_gateway import normalize
from vjecl.policies.approach_risk_policy import evaluate as evaluateApproachRisk
from vjecl.policies.crash_release_policy import evaluate as evaluateCrashRelease
from vjecl.sensor_fault_gate import shouldHoldLastOutput
from vjecl.types import Action, Door

from fixtures import VALID_DRIVER, buildVehicle


def resolveByAsilPriority(door):
    """!
    @brief ENG-SWE2-001 8절 우선순위표의 P0~P3만 반영한 최소 중재 헬퍼(시험 전용, 프로덕션 코드 아님).
           P1(CrashReleasePolicy)이 P3(ApproachRiskPolicy)보다 항상 우선한다.
    """

    def resolve(snapshot, previousDecision):
        if shouldHoldLastOutput(snapshot):
            return "HOLD_LAST_OUTPUT"
        crashVote = evaluateCrashRelease(snapshot, previousDecision, door)
        if crashVote is not None:
            return crashVote.action
        riskVote = evaluateApproachRisk(snapshot, previousDecision, door)
        if riskVote is not None:
            return riskVote.action
        return None

    return resolve


class Phase2SafetyPriorityIntegrationTest(unittest.TestCase):
    def test_noHazardsProduceNoForcedVoteFromEitherPolicy(self):
        """!
        @brief 크래시도 접근위험도 없으면 두 정책 모두 vote를 내지 않아야 함을 검증한다.
        @technique 요구사항기반시험
        @case 긍정(Positive) - 정상 통합 흐름 검증
        """
        snapshot = normalize(buildVehicle(), VALID_DRIVER)
        resolve = resolveByAsilPriority(Door.LEFT)
        self.assertIsNone(resolve(snapshot, None))

    def test_crashAloneReleasesRegardlessOfApproachRisk(self):
        """!
        @brief 크래시만 CONFIRMED이면 해제(RELEASE)로 귀결되어야 함을 검증한다.
        @technique 요구사항기반시험
        @case 긍정(Positive) - 크래시 단독 시나리오 검증
        """
        snapshot = normalize(buildVehicle(crash_status="CONFIRMED"), VALID_DRIVER)
        resolve = resolveByAsilPriority(Door.LEFT)
        self.assertEqual(resolve(snapshot, None), Action.RELEASE)

    def test_approachRiskAloneLocksWhenNoCrash(self):
        """!
        @brief 접근위험만 TRUE이면 LOCK(억제)로 귀결되어야 함을 검증한다.
        @technique 요구사항기반시험
        @case 긍정(Positive) - 접근위험 단독 시나리오 검증
        """
        snapshot = normalize(buildVehicle(rear_left_approach_risk=True), VALID_DRIVER)
        resolve = resolveByAsilPriority(Door.LEFT)
        self.assertEqual(resolve(snapshot, None), Action.LOCK)

    def test_crashConfirmedOverridesApproachRiskLock(self):
        """!
        @brief 크래시 CONFIRMED와 접근위험 TRUE가 동시에 발생하면 크래시 해제가 우선해야 함을
               검증한다(ENG-SWE2-001 8절 P1 > P3 우선순위 규칙의 통합 수준 검증).
        @technique 요구사항기반시험, 의사결정표기반
        @case 부정(Negative) - 두 안전 조건 동시 발생 시 우선순위 검증
        """
        snapshot = normalize(
            buildVehicle(crash_status="CONFIRMED", rear_left_approach_risk=True), VALID_DRIVER
        )
        resolve = resolveByAsilPriority(Door.LEFT)
        self.assertEqual(resolve(snapshot, None), Action.RELEASE)

    def test_sensorFaultGateOverridesBothPolicies(self):
        """!
        @brief sensor_fault=TRUE(P0 게이트)이면 크래시/접근위험 정책의 vote보다 우선해
               직전 출력 유지로 귀결되어야 함을 검증한다(Phase 1 게이트와 Phase 2 정책의 통합 검증).
        @technique 결함주입시험
        @case 부정(Negative) - 결함 상황에서의 최우선 게이트 검증
        """
        snapshot = normalize(
            buildVehicle(crash_status="CONFIRMED", rear_left_approach_risk=True, sensor_fault=True),
            VALID_DRIVER,
        )
        resolve = resolveByAsilPriority(Door.LEFT)
        self.assertEqual(resolve(snapshot, None), "HOLD_LAST_OUTPUT")

    def test_staleInputStillAllowsIndependentDegradedCheck(self):
        """!
        @brief 크래시/접근위험 판정과 무관하게 DegradedStateManager가 독립적으로 stale을
               감지해야 함을 검증한다(Phase 1 모듈과 Phase 2 정책의 결합도 검증).
        @technique 요구사항기반시험
        @case 부정(Negative) - stale 입력에서의 모듈 간 독립성 검증
        """
        snapshot = normalize(buildVehicle(crash_status="CONFIRMED"), VALID_DRIVER)
        degraded = evaluateDegraded(snapshot, previousTimestampS=100.0, currentTimestampS=100.3)
        resolve = resolveByAsilPriority(Door.LEFT)
        self.assertTrue(degraded.isDegraded)
        self.assertEqual(resolve(snapshot, None), Action.RELEASE)


if __name__ == "__main__":
    unittest.main()
