"""!
@brief MOD-05 ApproachRiskPolicy. ENG-SWE3-002 5~7절 참고. SWR-005, SWR-006, SWR-009. ASIL B.
"""
from typing import Optional

from vjecl.types import Action, Decision, Door, DoorDecision, NormalizedSnapshot, PolicyVote, Side

OVERRIDE_WINDOW_S = 10.0


def selectRiskField(snapshot: NormalizedSnapshot, door: Door):
    """!
    @brief door에 대응하는 접근위험 입력 필드를 선택한다(SWR-009: 좌우 독립 판단의 기반).
    """
    if door == Door.LEFT:
        return snapshot.rearLeftApproachRisk
    return snapshot.rearRightApproachRisk


def selectDoorDecision(previousDecision: Optional[Decision], door: Door) -> Optional[DoorDecision]:
    """!
    @brief previousDecision에서 해당 door의 직전 결정을 선택한다. previousDecision이 없으면 None.
    """
    if previousDecision is None:
        return None
    if door == Door.LEFT:
        return previousDecision.left
    return previousDecision.right


def matchesDoorSide(door: Door, side: Side) -> bool:
    """!
    @brief 운전자 명령의 side가 이 door를 대상으로 하는지 확인한다(LEFT/RIGHT 정확히 일치 또는 ALL).
    """
    if side == Side.ALL:
        return True
    return (door == Door.LEFT and side == Side.LEFT) or (door == Door.RIGHT and side == Side.RIGHT)


def isOverrideRequested(snapshot: NormalizedSnapshot, priorDoorDecision: Optional[DoorDecision], door: Door) -> bool:
    """!
    @brief 억제 후 10초 이내 같은 도어에 대한 RELEASE 재입력(override 조건)을 확인한다(SWR-006).
    """
    if priorDoorDecision is None or priorDoorDecision.suppressedSinceTimestampS is None:
        return False
    driverCommand = snapshot.driverCommand
    if driverCommand is None or driverCommand.action != Action.RELEASE:
        return False
    if not matchesDoorSide(door, driverCommand.side):
        return False
    elapsed = snapshot.sourceTimestampS.value - priorDoorDecision.suppressedSinceTimestampS
    return elapsed <= OVERRIDE_WINDOW_S


def evaluate(
    snapshot: NormalizedSnapshot, previousDecision: Optional[Decision], door: Door
) -> Optional[PolicyVote]:
    """!
    @brief 접근위험이 있는 도어를 LOCK(억제)하고, override 조건을 만족하면 RELEASE로 전환한다.
    @param snapshot 정규화된 입력 스냅샷.
    @param previousDecision 직전 평가주기의 확정 결정(override 판정에 필요).
    @param door 판정 대상 도어.
    @return 접근위험이 없거나 무효면 None. 위험이 있으면 LOCK 또는 RELEASE(override) 투표.
    """
    riskField = selectRiskField(snapshot, door)
    if not riskField.valid:
        return None
    if riskField.value is False:
        return None

    priorDoorDecision = selectDoorDecision(previousDecision, door)
    if isOverrideRequested(snapshot, priorDoorDecision, door):
        return PolicyVote(door=door, action=Action.RELEASE, reasonCode="approach_risk_override", sourceAsil="B")
    return PolicyVote(door=door, action=Action.LOCK, reasonCode="approach_risk_suppressed", sourceAsil="B")
