"""!
@brief MOD-05 ApproachRiskPolicy 단위 시험 (SWR-005, SWR-006, SWR-009).
"""
import unittest

from vjecl.input_gateway import normalize
from vjecl.policies.approach_risk_policy import evaluate
from vjecl.types import Action, Decision, Door, DoorDecision

from fixtures import VALID_DRIVER, buildVehicle

NEUTRAL_DOOR_DECISION = DoorDecision(action=Action.LOCK, state="NORMAL", reasonCode="none")


def buildPreviousDecision(suppressedSinceTimestampS=None):
    """!
    @brief LEFT 도어가 특정 시각부터 억제된 상태였다고 가정하는 previousDecision 스텁을 만든다.
    """
    left = DoorDecision(
        action=Action.LOCK,
        state="SUPPRESSED",
        reasonCode="approach_risk_suppressed",
        suppressedSinceTimestampS=suppressedSinceTimestampS,
    )
    return Decision(left=left, right=NEUTRAL_DOOR_DECISION)


class ApproachRiskPolicyTest(unittest.TestCase):
    def test_noRiskReturnsNone(self):
        """!
        @brief 접근위험이 FALSE이면 이 정책은 투표하지 않아야 함을 검증한다.
        @technique 동치분할
        @case 긍정(Positive) - 정상 흐름(위험 없음) 검증
        """
        snapshot = normalize(buildVehicle(rear_left_approach_risk=False), VALID_DRIVER)
        vote = evaluate(snapshot, previousDecision=None, door=Door.LEFT)
        self.assertIsNone(vote)

    def test_invalidRiskFieldReturnsNone(self):
        """!
        @brief 접근위험 입력이 무효면 투표하지 않아야 함을 검증한다.
        @technique 오류추정
        @case 부정(Negative) - 무효 입력 처리 검증
        """
        vehicle = buildVehicle()
        del vehicle["rear_left_approach_risk"]
        snapshot = normalize(vehicle, VALID_DRIVER)
        vote = evaluate(snapshot, previousDecision=None, door=Door.LEFT)
        self.assertIsNone(vote)

    def test_riskTrueWithoutReleaseRequestSuppresses(self):
        """!
        @brief 접근위험 TRUE이고 운전자가 해제를 요청하지 않으면 LOCK(억제)해야 함을 검증한다.
        @technique 의사결정표기반
        @case 부정(Negative) - 접근위험 억제 동작 검증
        """
        vehicle = buildVehicle(rear_left_approach_risk=True)
        driver = {"side": "left", "action": "lock", "source": "physical_button"}
        snapshot = normalize(vehicle, driver)
        vote = evaluate(snapshot, previousDecision=None, door=Door.LEFT)
        self.assertEqual(vote.action, Action.LOCK)
        self.assertEqual(vote.reasonCode, "approach_risk_suppressed")

    def test_riskTrueWithReleaseButNeverSuppressedBeforeStaysLocked(self):
        """!
        @brief 이전에 억제된 적이 없으면(suppressedSince=None) 운전자가 해제를 요청해도
               override가 성립하지 않아야 함을 검증한다.
        @technique 의사결정표기반
        @case 부정(Negative) - override 사전조건 미충족 검증
        """
        vehicle = buildVehicle(rear_left_approach_risk=True)
        driver = {"side": "left", "action": "unlock", "source": "physical_button"}
        snapshot = normalize(vehicle, driver)
        vote = evaluate(snapshot, previousDecision=None, door=Door.LEFT)
        self.assertEqual(vote.action, Action.LOCK)

    def test_releaseWithinTenSecondsOfSuppressionIsOverride(self):
        """!
        @brief 억제 시작 후 10초 이내(경계값 포함) 같은 도어에 대한 RELEASE 재입력은
               override로 처리해야 함(SWR-006)을 검증한다.
        @technique 경계값분석
        @case 부정(Negative) - override 경계값 성립 검증
        """
        vehicle = buildVehicle(rear_left_approach_risk=True, source_timestamp_s=110.0)
        driver = {"side": "left", "action": "unlock", "source": "physical_button"}
        snapshot = normalize(vehicle, driver)
        previousDecision = buildPreviousDecision(suppressedSinceTimestampS=100.0)
        vote = evaluate(snapshot, previousDecision, door=Door.LEFT)
        self.assertEqual(vote.action, Action.RELEASE)
        self.assertEqual(vote.reasonCode, "approach_risk_override")

    def test_releaseAfterTenSecondsStaysSuppressed(self):
        """!
        @brief 억제 시작 후 10초를 초과한 재입력은 override로 인정하지 않아야 함을 검증한다.
        @technique 경계값분석
        @case 부정(Negative) - override 창 만료 검증
        """
        vehicle = buildVehicle(rear_left_approach_risk=True, source_timestamp_s=110.001)
        driver = {"side": "left", "action": "unlock", "source": "physical_button"}
        snapshot = normalize(vehicle, driver)
        previousDecision = buildPreviousDecision(suppressedSinceTimestampS=100.0)
        vote = evaluate(snapshot, previousDecision, door=Door.LEFT)
        self.assertEqual(vote.action, Action.LOCK)

    def test_releaseCommandForOtherSideDoesNotTriggerOverride(self):
        """!
        @brief 운전자 명령이 반대쪽 도어를 대상으로 하면 이 도어의 override가 성립하지 않아야 함을 검증한다.
        @technique 인터페이스시험
        @case 부정(Negative) - 명령 대상 불일치 검증
        """
        vehicle = buildVehicle(rear_left_approach_risk=True, source_timestamp_s=105.0)
        driver = {"side": "right", "action": "unlock", "source": "physical_button"}
        snapshot = normalize(vehicle, driver)
        previousDecision = buildPreviousDecision(suppressedSinceTimestampS=100.0)
        vote = evaluate(snapshot, previousDecision, door=Door.LEFT)
        self.assertEqual(vote.action, Action.LOCK)

    def test_allSideReleaseCommandTriggersOverride(self):
        """!
        @brief 운전자 명령이 ALL(전체)이면 개별 도어 override 조건도 성립해야 함을 검증한다.
        @technique 의사결정표기반
        @case 긍정(Positive) - ALL 명령의 정상 처리 검증
        """
        vehicle = buildVehicle(rear_left_approach_risk=True, source_timestamp_s=105.0)
        driver = {"side": "all", "action": "unlock", "source": "physical_button"}
        snapshot = normalize(vehicle, driver)
        previousDecision = buildPreviousDecision(suppressedSinceTimestampS=100.0)
        vote = evaluate(snapshot, previousDecision, door=Door.LEFT)
        self.assertEqual(vote.action, Action.RELEASE)

    def test_rightDoorUsesRightApproachRiskField(self):
        """!
        @brief door=RIGHT일 때는 rear_right_approach_risk 필드를 사용해야 함(SWR-009, 좌우 독립)을 검증한다.
        @technique 인터페이스시험
        @case 긍정(Positive) - 좌우 독립 판단 검증
        """
        vehicle = buildVehicle(rear_left_approach_risk=True, rear_right_approach_risk=False)
        snapshot = normalize(vehicle, VALID_DRIVER)
        vote = evaluate(snapshot, previousDecision=None, door=Door.RIGHT)
        self.assertIsNone(vote)

    def test_rightDoorSuppressedWithNoDriverCommandStaysLocked(self):
        """!
        @brief door=RIGHT이고 이전에 RIGHT 도어가 억제된 상태(suppressedSince 존재)에서
               운전자 명령이 없으면 override가 성립하지 않아야 함을 검증한다
               (previousDecision.right 경로 및 driverCommand=None 분기 검증).
        @technique 인터페이스시험, 오류추정
        @case 부정(Negative) - RIGHT 도어의 override 미성립 경로 검증
        """
        vehicle = buildVehicle(rear_right_approach_risk=True, source_timestamp_s=105.0)
        snapshot = normalize(vehicle, None)
        right = DoorDecision(
            action=Action.LOCK,
            state="SUPPRESSED",
            reasonCode="approach_risk_suppressed",
            suppressedSinceTimestampS=100.0,
        )
        previousDecision = Decision(left=NEUTRAL_DOOR_DECISION, right=right)
        vote = evaluate(snapshot, previousDecision, door=Door.RIGHT)
        self.assertEqual(vote.action, Action.LOCK)

    def test_noDriverCommandStillSuppresses(self):
        """!
        @brief 운전자 명령 자체가 없어도(driverCommand=None) 접근위험 억제는 그대로 적용되어야 함을 검증한다.
        @technique 오류추정
        @case 부정(Negative) - 명령 부재 시 안전 기본 동작 검증
        """
        vehicle = buildVehicle(rear_left_approach_risk=True)
        snapshot = normalize(vehicle, None)
        vote = evaluate(snapshot, previousDecision=None, door=Door.LEFT)
        self.assertEqual(vote.action, Action.LOCK)


if __name__ == "__main__":
    unittest.main()
