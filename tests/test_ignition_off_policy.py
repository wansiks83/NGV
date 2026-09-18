"""!
@brief MOD-08 IgnitionOffPolicy 단위 시험 (SWR-020).
"""
import unittest

from vjecl.input_gateway import normalize
from vjecl.policies.ignition_off_policy import evaluate
from vjecl.types import Action, Door

from fixtures import VALID_DRIVER, buildVehicle


class IgnitionOffPolicyTest(unittest.TestCase):
    def test_ignitionOnReturnsNone(self):
        """!
        @brief ignition_on=TRUE(시동 켜짐)이면 투표하지 않아야 함을 검증한다.
        @technique 동치분할
        @case 긍정(Positive) - 정상 흐름(시동 켜짐) 검증
        """
        snapshot = normalize(buildVehicle(ignition_on=True), VALID_DRIVER)
        vote = evaluate(snapshot, previousDecision=None, door=Door.LEFT)
        self.assertIsNone(vote)

    def test_ignitionOffReleasesBothDoors(self):
        """!
        @brief ignition_on=FALSE이면 좌/우 모두 RELEASE 투표해야 함(SWR-020)을 검증한다.
        @technique 의사결정표기반
        @case 긍정(Positive) - 정상 흐름(시동 꺼짐) 검증
        """
        snapshot = normalize(buildVehicle(ignition_on=False), VALID_DRIVER)
        leftVote = evaluate(snapshot, previousDecision=None, door=Door.LEFT)
        rightVote = evaluate(snapshot, previousDecision=None, door=Door.RIGHT)
        self.assertEqual(leftVote.action, Action.RELEASE)
        self.assertEqual(leftVote.reasonCode, "ignition_off")
        self.assertEqual(rightVote.action, Action.RELEASE)

    def test_invalidIgnitionFieldReturnsNone(self):
        """!
        @brief ignition_on 입력이 무효면 투표하지 않아야 함을 검증한다.
        @technique 오류추정
        @case 부정(Negative) - 무효 입력 처리 검증
        """
        vehicle = buildVehicle()
        del vehicle["ignition_on"]
        snapshot = normalize(vehicle, VALID_DRIVER)
        vote = evaluate(snapshot, previousDecision=None, door=Door.LEFT)
        self.assertIsNone(vote)


if __name__ == "__main__":
    unittest.main()
