"""!
@brief MOD-02 DegradedStateManager. ENG-SWE3-001 5절 함수 계약 참고. SWR-013.
"""
from vjecl.types import DegradedResult, NormalizedSnapshot

STALENESS_THRESHOLD_S = 0.2


def evaluate(
    snapshot: NormalizedSnapshot, previousTimestampS: float, currentTimestampS: float
) -> DegradedResult:
    """!
    @brief 필수 안전 입력의 staleness를 계산해 DEGRADED 여부를 판정한다.
    @param snapshot 정규화된 입력 스냅샷.
    @param previousTimestampS 마지막으로 유효했던 입력의 타임스탬프(초).
    @param currentTimestampS 현재 평가 시각(초).
    @return staleness가 200ms를 초과하면 isDegraded=True.
    """
    staleness = currentTimestampS - previousTimestampS
    if staleness > STALENESS_THRESHOLD_S:
        return DegradedResult(isDegraded=True, staleFields=["safetyCriticalInputs"])
    return DegradedResult(isDegraded=False, staleFields=[])
