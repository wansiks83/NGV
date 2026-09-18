"""!
@brief MOD-02 DegradedStateManager 단위 시험 (SWR-013).
"""
import unittest

from vjecl.degraded_state_manager import evaluate
from vjecl.types import NormalizedField


def buildSnapshotStub():
    """!
    @brief 테스트용 최소 스냅샷 스텁(현재 evaluate 로직은 타임스탬프만 사용하지만, 계약(ENG-SWE3-001 5절)에 맞춰 snapshot을 전달한다).
    """
    class SnapshotStub:
        pass

    stub = SnapshotStub()
    stub.sourceTimestampS = NormalizedField(value=0.0, valid=True)
    return stub


class DegradedStateManagerTest(unittest.TestCase):
    def test_freshInputIsNotDegraded(self):
        """!
        @brief staleness가 0(입력이 방금 갱신됨)이면 DEGRADED가 아니어야 함을 검증한다.
        @technique 경계값분석
        @case 긍정(Positive) - 정상 흐름 검증
        """
        result = evaluate(buildSnapshotStub(), previousTimestampS=10.0, currentTimestampS=10.0)
        self.assertFalse(result.isDegraded)

    def test_exactlyTwoHundredMsIsNotYetDegraded(self):
        """!
        @brief staleness가 정확히 200ms(0.2s)이면 아직 DEGRADED가 아니어야 함을 검증한다(">"조건, 경계값 자체는 포함 안 됨).
        @technique 경계값분석
        @case 긍정(Positive) - 경계값 자체의 정상 처리 검증
        """
        result = evaluate(buildSnapshotStub(), previousTimestampS=10.0, currentTimestampS=10.2)
        self.assertFalse(result.isDegraded)

    def test_justOverTwoHundredMsIsDegraded(self):
        """!
        @brief staleness가 200ms를 초과하면 DEGRADED로 전이해야 함을 검증한다.
        @technique 경계값분석
        @case 부정(Negative) - 경계 초과 시의 비정상 상황 처리 검증
        """
        result = evaluate(buildSnapshotStub(), previousTimestampS=10.0, currentTimestampS=10.2001)
        self.assertTrue(result.isDegraded)
        self.assertIn("safetyCriticalInputs", result.staleFields)


if __name__ == "__main__":
    unittest.main()
