"""!
@brief MOD-06 ForcedReleasePolicy 단위 시험 (SWR-017).
"""
import unittest

from vjecl.input_gateway import normalize
from vjecl.policies.forced_release_policy import evaluate
from vjecl.types import Action, Door

from fixtures import VALID_DRIVER, buildVehicle


class ForcedReleasePolicyTest(unittest.TestCase):
    def test_noTriggerReturnsNone(self):
        """!
        @brief 화재/과온/성인탑승이 모두 FALSE이면 투표하지 않아야 함을 검증한다.
        @technique 동치분할
        @case 긍정(Positive) - 정상 흐름(트리거 없음) 검증
        """
        snapshot = normalize(buildVehicle(), VALID_DRIVER)
        vote = evaluate(snapshot, previousDecision=None, door=Door.LEFT)
        self.assertIsNone(vote)

    def test_fireAloneReleasesWithReasonCode(self):
        """!
        @brief fire_detected 단독 TRUE이면 RELEASE하고 이유코드에 fire_detected가 포함되어야 함을 검증한다.
        @technique 의사결정표기반
        @case 긍정(Positive) - 단독 트리거 정상 처리 검증
        """
        snapshot = normalize(buildVehicle(fire_detected=True), VALID_DRIVER)
        vote = evaluate(snapshot, previousDecision=None, door=Door.RIGHT)
        self.assertEqual(vote.action, Action.RELEASE)
        self.assertEqual(vote.reasonCode, "fire_detected")
        self.assertEqual(vote.sourceAsil, "QM")

    def test_multipleTriggersJoinReasonCodes(self):
        """!
        @brief 여러 입력이 동시에 TRUE이면 이유코드가 모두 결합되어야 함(SWR-017 '입력별 이유코드')을 검증한다.
        @technique 의사결정표기반
        @case 부정(Negative) - 복수 트리거 동시 발생 검증
        """
        snapshot = normalize(
            buildVehicle(overtemperature_detected=True, adult_present=True), VALID_DRIVER
        )
        vote = evaluate(snapshot, previousDecision=None, door=Door.LEFT)
        self.assertEqual(vote.reasonCode, "overtemperature_detected,adult_present")

    def test_invalidFieldsAreNotCountedAsTriggers(self):
        """!
        @brief 무효(형식 오류) 입력은 트리거로 인정하지 않아야 함을 검증한다.
        @technique 오류추정
        @case 부정(Negative) - 무효 입력 처리 검증
        """
        vehicle = buildVehicle(fire_detected="yes")
        snapshot = normalize(vehicle, VALID_DRIVER)
        vote = evaluate(snapshot, previousDecision=None, door=Door.LEFT)
        self.assertIsNone(vote)


if __name__ == "__main__":
    unittest.main()
