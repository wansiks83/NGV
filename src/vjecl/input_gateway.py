"""!
@brief MOD-01 InputGateway. ENG-SWE3-001 5~6절 참고. SWR-013.
"""
from typing import Optional

from vjecl.types import (
    Action,
    CommandSource,
    CrashStatus,
    DriverCommand,
    Gear,
    NormalizedField,
    NormalizedSnapshot,
    Side,
)


def validateRange(rawValue, minValue: float, maxValue: float) -> NormalizedField:
    """!
    @brief 값이 숫자이고 [minValue, maxValue] 범위 안인지 검증한다.
    """
    if not isinstance(rawValue, (int, float)) or isinstance(rawValue, bool):
        return NormalizedField(value=None, valid=False, reason="format")
    if not (minValue <= rawValue <= maxValue):
        return NormalizedField(value=rawValue, valid=False, reason="range")
    return NormalizedField(value=rawValue, valid=True)


def validateEnum(rawValue, enumClass) -> NormalizedField:
    """!
    @brief 값이 지정된 열거형의 등록된 값 중 하나인지 검증한다.
    """
    for member in enumClass:
        if member.value == rawValue:
            return NormalizedField(value=member, valid=True)
    return NormalizedField(value=None, valid=False, reason="enum")


def validateBoolean(rawValue) -> NormalizedField:
    """!
    @brief 값이 boolean 타입인지 검증한다.
    """
    if not isinstance(rawValue, bool):
        return NormalizedField(value=None, valid=False, reason="format")
    return NormalizedField(value=rawValue, valid=True)


def validatePresent(rawDict: Optional[dict], key: str, validator, *args) -> NormalizedField:
    """!
    @brief 키가 존재하는지 먼저 확인한 뒤, 존재하면 지정된 validator로 값을 검증한다.
    """
    if rawDict is None or key not in rawDict:
        return NormalizedField(value=None, valid=False, reason="missing")
    return validator(rawDict[key], *args)


def normalizeDriverCommand(rawDriver: Optional[dict]) -> Optional[DriverCommand]:
    """!
    @brief side/action/source가 모두 유효할 때만 DriverCommand를 생성하고, 그렇지 않으면 명령 전체를 거절(None)한다.
    """
    if rawDriver is None:
        return None
    side = validatePresent(rawDriver, "side", validateEnum, Side)
    action = validatePresent(rawDriver, "action", validateEnum, Action)
    source = validatePresent(rawDriver, "source", validateEnum, CommandSource)
    if side.valid and action.valid and source.valid:
        return DriverCommand(side=side.value, action=action.value, source=source.value)
    return None


def normalize(rawVehicle: Optional[dict], rawDriver: Optional[dict]) -> NormalizedSnapshot:
    """!
    @brief Vehicle/Driver 원시 입력을 검증하고 NormalizedSnapshot으로 정규화한다.
    @param rawVehicle Vehicle->SW 원시 입력 dict(OEM-IF-001~003, 007~009).
    @param rawDriver Driver->SW 원시 입력 dict(OEM-IF-004), 없으면 None.
    @return 모든 필드에 유효성 플래그가 포함된 NormalizedSnapshot. 예외를 던지지 않는다.
    """
    return NormalizedSnapshot(
        vehicleSpeedKph=validatePresent(rawVehicle, "vehicle_speed_kph", validateRange, 0.0, 300.0),
        gear=validatePresent(rawVehicle, "gear", validateEnum, Gear),
        sourceTimestampS=validatePresent(rawVehicle, "source_timestamp_s", validateRange, 0.0, float("inf")),
        crashStatus=validatePresent(rawVehicle, "crash_status", validateEnum, CrashStatus),
        rearLeftApproachRisk=validatePresent(rawVehicle, "rear_left_approach_risk", validateBoolean),
        rearRightApproachRisk=validatePresent(rawVehicle, "rear_right_approach_risk", validateBoolean),
        fireDetected=validatePresent(rawVehicle, "fire_detected", validateBoolean),
        overtemperatureDetected=validatePresent(rawVehicle, "overtemperature_detected", validateBoolean),
        adultPresent=validatePresent(rawVehicle, "adult_present", validateBoolean),
        isofixLeft=validatePresent(rawVehicle, "isofix_left", validateBoolean),
        isofixRight=validatePresent(rawVehicle, "isofix_right", validateBoolean),
        ignitionOn=validatePresent(rawVehicle, "ignition_on", validateBoolean),
        sensorFault=validatePresent(rawVehicle, "sensor_fault", validateBoolean),
        driverCommand=normalizeDriverCommand(rawDriver),
    )
