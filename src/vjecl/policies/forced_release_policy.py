"""!
@brief MOD-06 ForcedReleasePolicy. ENG-SWE3-003 5~6절 참고. SWR-017. QM, 양쪽 도어 공통.
"""
from typing import Optional

from vjecl.types import Action, Decision, Door, NormalizedSnapshot, PolicyVote

TRIGGER_FIELDS = ("fireDetected", "overtemperatureDetected", "adultPresent")
TRIGGER_NAMES = {
    "fireDetected": "fire_detected",
    "overtemperatureDetected": "overtemperature_detected",
    "adultPresent": "adult_present",
}


def collectTriggeredNames(snapshot: NormalizedSnapshot) -> list:
    """!
    @brief 유효하게 TRUE인 화재/과온/성인탑승 입력의 이름 목록을 모은다.
    """
    triggeredNames = []
    for attrName in TRIGGER_FIELDS:
        field = getattr(snapshot, attrName)
        if field.valid and field.value is True:
            triggeredNames.append(TRIGGER_NAMES[attrName])
    return triggeredNames


def evaluate(
    snapshot: NormalizedSnapshot, previousDecision: Optional[Decision], door: Door
) -> Optional[PolicyVote]:
    """!
    @brief 화재/과온/성인탑승 중 하나라도 유효하게 TRUE이면 강제 해제 투표를 반환한다.
    @param snapshot 정규화된 입력 스냅샷.
    @param previousDecision 이 정책은 사용하지 않는다.
    @param door 판정 대상 도어(양쪽에 동일하게 적용).
    @return 트리거가 있으면 RELEASE 투표(reasonCode에 트리거된 입력명을 ','로 결합), 없으면 None.
    """
    triggeredNames = collectTriggeredNames(snapshot)
    if not triggeredNames:
        return None
    return PolicyVote(door=door, action=Action.RELEASE, reasonCode=",".join(triggeredNames), sourceAsil="QM")
