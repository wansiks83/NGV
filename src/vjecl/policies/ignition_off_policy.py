"""!
@brief MOD-08 IgnitionOffPolicy. ENG-SWE3-003 5~6절 참고. SWR-020. QM, 양쪽 도어 공통.
"""
from typing import Optional

from vjecl.types import Action, Decision, Door, NormalizedSnapshot, PolicyVote


def evaluate(
    snapshot: NormalizedSnapshot, previousDecision: Optional[Decision], door: Door
) -> Optional[PolicyVote]:
    """!
    @brief ignition_on이 유효하게 FALSE이면 해제 투표를 반환한다.
    @param snapshot 정규화된 입력 스냅샷.
    @param previousDecision 이 정책은 사용하지 않는다.
    @param door 판정 대상 도어(양쪽에 동일하게 적용).
    @return ignition_on=FALSE(유효)이면 RELEASE 투표, 그 외(무효/TRUE)에는 None.
    """
    ignitionField = snapshot.ignitionOn
    if not ignitionField.valid:
        return None
    if ignitionField.value is True:
        return None
    return PolicyVote(door=door, action=Action.RELEASE, reasonCode="ignition_off", sourceAsil="QM")
