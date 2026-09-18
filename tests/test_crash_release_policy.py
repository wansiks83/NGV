"""!
@brief MOD-04 CrashReleasePolicy 단위 시험 (SWR-007, SWR-008).
"""
import unittest

from vjecl.policies.crash_release_policy import evaluate
from vjecl.types import Action, Door

from fixtures import buildVehicle, VALID_DRIVER
from vjecl.input_gateway import normalize


class CrashReleasePolicyTest(unittest.TestCase):
    def test_confirmedCrashReturnsReleaseVote(self):
        """!
        @brief crash_status=CONFIRMED이면 RELEASE 투표를 반환해야 함을 검증한다.
        @technique 사전조건·사후조건검증
        @case 긍정(Positive) - 정상 흐름 검증
        """
        snapshot = normalize(buildVehicle(crash_status="CONFIRMED"), VALID_DRIVER)
        vote = evaluate(snapshot, previousDecision=None, door=Door.LEFT)
        self.assertIsNotNone(vote)
        self.assertEqual(vote.action, Action.RELEASE)
        self.assertEqual(vote.reasonCode, "crash_confirmed")
        self.assertEqual(vote.sourceAsil, "B")

    def test_pendingCrashReturnsNone(self):
        """!
        @brief crash_status=PENDING이면 투표하지 않아야 함(SWR-008)을 검증한다.
        @technique 의사결정표기반
        @case 부정(Negative) - 대기 상태 처리 검증
        """
        snapshot = normalize(buildVehicle(crash_status="PENDING"), VALID_DRIVER)
        vote = evaluate(snapshot, previousDecision=None, door=Door.LEFT)
        self.assertIsNone(vote)

    def test_noneStatusReturnsNone(self):
        """!
        @brief crash_status=NONE(충돌 없음)이면 투표하지 않아야 함을 검증한다.
        @technique 동치분할
        @case 긍정(Positive) - 정상 흐름(충돌 없음) 검증
        """
        snapshot = normalize(buildVehicle(crash_status="NONE"), VALID_DRIVER)
        vote = evaluate(snapshot, previousDecision=None, door=Door.RIGHT)
        self.assertIsNone(vote)

    def test_invalidCrashStatusReturnsNone(self):
        """!
        @brief crash_status 입력이 무효면 투표하지 않아야 함을 검증한다.
        @technique 오류추정
        @case 부정(Negative) - 무효 입력 처리 검증
        """
        vehicle = buildVehicle()
        del vehicle["crash_status"]
        snapshot = normalize(vehicle, VALID_DRIVER)
        vote = evaluate(snapshot, previousDecision=None, door=Door.LEFT)
        self.assertIsNone(vote)


if __name__ == "__main__":
    unittest.main()
