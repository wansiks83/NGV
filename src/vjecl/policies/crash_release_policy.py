"""!
@brief MOD-04 CrashReleasePolicy. ENG-SWE3-002 5~6절 참고. SWR-007, SWR-008. ASIL B.
"""
from typing import Optional

from vjecl.types import Action, CrashStatus, Decision, Door, NormalizedSnapshot, PolicyVote


def evaluate(
    snapshot: NormalizedSnapshot, previousDecision: Optional[Decision], door: Door
) -> Optional[PolicyVote]:
    """!
    @brief crash_status가 CONFIRMED이면 다른 모든 명령보다 우선하는 해제 투표를 반환한다.
    @param snapshot 정규화된 입력 스냅샷.
    @param previousDecision 이 정책은 사용하지 않는다(계약상 항상 전달됨).
    @param door 판정 대상 도어.
    @return crash_status=CONFIRMED이면 RELEASE 투표, 그 외(PENDING/NONE/무효)에는 None.
    """
    crashStatus = snapshot.crashStatus
    if not crashStatus.valid:
        return None
    if crashStatus.value == CrashStatus.CONFIRMED:
        return PolicyVote(door=door, action=Action.RELEASE, reasonCode="crash_confirmed", sourceAsil="B")
    return None
