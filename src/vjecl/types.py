"""!
@brief ENG-SWE3-001 4절(공통 자료형)에 정의된 데이터 구조와 열거형.
"""
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional


class Gear(Enum):
    """!
    @brief 기어 위치 열거형 (ENG-SWE1-001 5절 gear).
    """
    PARK = "P"
    NEUTRAL = "N"
    DRIVE = "D"
    REVERSE = "R"


class CrashStatus(Enum):
    """!
    @brief 충돌 상태 열거형 (OEM-IF-002).
    """
    NONE = "NONE"
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"


class Side(Enum):
    """!
    @brief 운전자 명령의 대상 도어 (OEM-IF-004).
    """
    LEFT = "left"
    RIGHT = "right"
    ALL = "all"


class Action(Enum):
    """!
    @brief 운전자 명령의 동작 (OEM-IF-004).
    """
    LOCK = "lock"
    RELEASE = "unlock"


class CommandSource(Enum):
    """!
    @brief 운전자 명령의 입력 경로 (OEM-IF-004).
    """
    PHYSICAL_BUTTON = "physical_button"
    AVN = "avn"
    VOICE = "voice"
    MOBILE_APP = "mobile_app"


@dataclass(frozen=True)
class NormalizedField:
    """!
    @brief 정규화된 입력 필드 하나. valid=False면 value는 판단 로직에 사용하지 않는다.
    """
    value: Any
    valid: bool
    reason: Optional[str] = None


@dataclass(frozen=True)
class DriverCommand:
    """!
    @brief 운전자 명령(side/action/source가 모두 유효할 때만 생성됨).
    """
    side: Side
    action: Action
    source: CommandSource


@dataclass(frozen=True)
class NormalizedSnapshot:
    """!
    @brief InputGateway.normalize()의 반환값. ENG-SWE3-001 4절 참고.
    """
    vehicleSpeedKph: NormalizedField
    gear: NormalizedField
    sourceTimestampS: NormalizedField
    crashStatus: NormalizedField
    rearLeftApproachRisk: NormalizedField
    rearRightApproachRisk: NormalizedField
    fireDetected: NormalizedField
    overtemperatureDetected: NormalizedField
    adultPresent: NormalizedField
    isofixLeft: NormalizedField
    isofixRight: NormalizedField
    ignitionOn: NormalizedField
    sensorFault: NormalizedField
    driverCommand: Optional[DriverCommand] = None


@dataclass(frozen=True)
class DegradedResult:
    """!
    @brief DegradedStateManager.evaluate()의 반환값.
    """
    isDegraded: bool
    staleFields: list = field(default_factory=list)


class Door(Enum):
    """!
    @brief 정책 판정의 대상 도어. Side(운전자 명령용, ALL 포함)와 달리 정책 판정은 항상 도어 단위다.
    """
    LEFT = "left"
    RIGHT = "right"


@dataclass(frozen=True)
class PolicyVote:
    """!
    @brief 정책모듈이 PriorityArbiter에 제출하는 투표. ENG-SWE3-002 5절 참고.
    """
    door: Door
    action: Action
    reasonCode: str
    sourceAsil: str


@dataclass(frozen=True)
class DoorDecision:
    """!
    @brief 도어 하나에 대한 PriorityArbiter의 확정 결정(Phase 5에서 실제 생성).
    """
    action: Action
    state: str
    reasonCode: str
    suppressedSinceTimestampS: Optional[float] = None


@dataclass(frozen=True)
class Decision:
    """!
    @brief PriorityArbiter의 출력이자, 다음 평가주기의 previousDecision 입력.
    """
    left: DoorDecision
    right: DoorDecision
