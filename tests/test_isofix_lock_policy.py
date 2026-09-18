"""!
@brief MOD-07 IsofixLockPolicy 단위 시험 (SWR-018).
"""
import unittest

from vjecl.input_gateway import normalize
from vjecl.policies.isofix_lock_policy import evaluate
from vjecl.types import Action, Door

from fixtures import VALID_DRIVER, buildVehicle


class IsofixLockPolicyTest(unittest.TestCase):
    def test_noIsofixReturnsNone(self):
        """!
        @brief ISOFIX가 연결되지 않으면 투표하지 않아야 함을 검증한다.
        @technique 동치분할
        @case 긍정(Positive) - 정상 흐름(연결 없음) 검증
        """
        snapshot = normalize(buildVehicle(), VALID_DRIVER)
        vote = evaluate(snapshot, previousDecision=None, door=Door.LEFT)
        self.assertIsNone(vote)

    def test_leftIsofixLocksLeftDoorOnly(self):
        """!
        @brief 좌측 ISOFIX만 TRUE면 LEFT 도어만 LOCK 투표해야 하고 RIGHT는 영향받지 않아야 함(SWR-018)을 검증한다.
        @technique 의사결정표기반
        @case 긍정(Positive) - 도어별 독립 판단 검증
        """
        snapshot = normalize(buildVehicle(isofix_left=True, isofix_right=False), VALID_DRIVER)
        leftVote = evaluate(snapshot, previousDecision=None, door=Door.LEFT)
        rightVote = evaluate(snapshot, previousDecision=None, door=Door.RIGHT)
        self.assertEqual(leftVote.action, Action.LOCK)
        self.assertEqual(leftVote.reasonCode, "isofix_engaged")
        self.assertIsNone(rightVote)

    def test_invalidIsofixFieldReturnsNone(self):
        """!
        @brief ISOFIX 입력이 무효면 투표하지 않아야 함을 검증한다.
        @technique 오류추정
        @case 부정(Negative) - 무효 입력 처리 검증
        """
        vehicle = buildVehicle()
        del vehicle["isofix_left"]
        snapshot = normalize(vehicle, VALID_DRIVER)
        vote = evaluate(snapshot, previousDecision=None, door=Door.LEFT)
        self.assertIsNone(vote)


if __name__ == "__main__":
    unittest.main()
