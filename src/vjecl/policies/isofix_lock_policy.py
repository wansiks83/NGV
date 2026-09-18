"""!
@brief MOD-07 IsofixLockPolicy. ENG-SWE3-003 5~6절 참고. SWR-018. QM, 도어별 독립.
"""
from typing import Optional

from vjecl.types import Action, Decision, Door, NormalizedSnapshot, PolicyVote


def selectIsofixField(snapshot: NormalizedSnapshot, door: Door):
    """!
    @brief door에 대응하는 ISOFIX 입력 필드를 선택한다(SWR-018: 도어별 독립 판단).
    """
    if door == Door.LEFT:
        return snapshot.isofixLeft
    return snapshot.isofixRight


def evaluate(
    snapshot: NormalizedSnapshot, previousDecision: Optional[Decision], door: Door
) -> Optional[PolicyVote]:
    """!
    @brief 해당 도어의 ISOFIX가 유효하게 TRUE이면 강제 잠금 투표를 반환한다.
    @param snapshot 정규화된 입력 스냅샷.
    @param previousDecision 이 정책은 사용하지 않는다.
    @param door 판정 대상 도어.
    @return ISOFIX가 유효하게 TRUE면 LOCK 투표, 그 외(무효/FALSE)에는 None.
    """
    isofixField = selectIsofixField(snapshot, door)
    if not isofixField.valid:
        return None
    if isofixField.value is False:
        return None
    return PolicyVote(door=door, action=Action.LOCK, reasonCode="isofix_engaged", sourceAsil="QM")
