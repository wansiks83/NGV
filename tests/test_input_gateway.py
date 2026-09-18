"""!
@brief MOD-01 InputGateway 단위 시험 (SWR-013).
"""
import unittest

from vjecl.input_gateway import normalize
from vjecl.types import Action, CommandSource, CrashStatus, Gear, Side

from fixtures import VALID_DRIVER, VALID_VEHICLE, buildVehicle


class InputGatewayTest(unittest.TestCase):
    def test_allValidInputsProduceValidSnapshot(self):
        """!
        @brief 모든 입력이 유효하면 스냅샷의 모든 필드가 valid=True여야 함을 검증한다.
        @technique 동치분할
        @case 긍정(Positive) - 정상 흐름 검증
        """
        snapshot = normalize(VALID_VEHICLE, VALID_DRIVER)
        self.assertTrue(snapshot.vehicleSpeedKph.valid)
        self.assertTrue(snapshot.gear.valid)
        self.assertEqual(snapshot.gear.value, Gear.DRIVE)
        self.assertTrue(snapshot.crashStatus.valid)
        self.assertEqual(snapshot.crashStatus.value, CrashStatus.NONE)
        self.assertTrue(snapshot.ignitionOn.valid)
        self.assertIsNotNone(snapshot.driverCommand)
        self.assertEqual(snapshot.driverCommand.side, Side.LEFT)
        self.assertEqual(snapshot.driverCommand.action, Action.LOCK)
        self.assertEqual(snapshot.driverCommand.source, CommandSource.PHYSICAL_BUTTON)

    def test_vehicleSpeedBoundaryValuesAreValid(self):
        """!
        @brief 차속 0.0과 300.0(경계값 자체)은 유효해야 함을 검증한다.
        @technique 경계값분석
        @case 긍정(Positive) - 경계값 자체의 정상 처리 검증
        """
        low = normalize(buildVehicle(vehicle_speed_kph=0.0), VALID_DRIVER)
        high = normalize(buildVehicle(vehicle_speed_kph=300.0), VALID_DRIVER)
        self.assertTrue(low.vehicleSpeedKph.valid)
        self.assertTrue(high.vehicleSpeedKph.valid)

    def test_vehicleSpeedOutOfRangeIsInvalid(self):
        """!
        @brief 차속이 0.0 미만이거나 300.0을 초과하면 무효(INVALID)여야 함을 검증한다.
        @technique 경계값분석
        @case 부정(Negative) - 경계 위반 입력 검증
        """
        low = normalize(buildVehicle(vehicle_speed_kph=-0.1), VALID_DRIVER)
        high = normalize(buildVehicle(vehicle_speed_kph=300.1), VALID_DRIVER)
        self.assertFalse(low.vehicleSpeedKph.valid)
        self.assertEqual(low.vehicleSpeedKph.reason, "range")
        self.assertFalse(high.vehicleSpeedKph.valid)

    def test_vehicleSpeedWrongTypeIsInvalid(self):
        """!
        @brief 차속이 숫자가 아니면 무효(형식 오류)여야 함을 검증한다.
        @technique 오류추정
        @case 부정(Negative) - 형식 오류 입력 검증
        """
        result = normalize(buildVehicle(vehicle_speed_kph="fast"), VALID_DRIVER)
        self.assertFalse(result.vehicleSpeedKph.valid)
        self.assertEqual(result.vehicleSpeedKph.reason, "format")

    def test_missingRequiredFieldIsInvalid(self):
        """!
        @brief 필수 입력 필드가 누락되면 무효(missing)여야 함을 검증한다.
        @technique 오류추정
        @case 부정(Negative) - 필드 누락 검증
        """
        vehicle = buildVehicle()
        del vehicle["vehicle_speed_kph"]
        result = normalize(vehicle, VALID_DRIVER)
        self.assertFalse(result.vehicleSpeedKph.valid)
        self.assertEqual(result.vehicleSpeedKph.reason, "missing")

    def test_gearInvalidEnumIsInvalid(self):
        """!
        @brief gear가 등록되지 않은 값이면 무효(enum)여야 함을 검증한다.
        @technique 의사결정표기반
        @case 부정(Negative) - 미등록 enum 값 검증
        """
        result = normalize(buildVehicle(gear="X"), VALID_DRIVER)
        self.assertFalse(result.gear.valid)
        self.assertEqual(result.gear.reason, "enum")

    def test_booleanFieldWrongTypeIsInvalid(self):
        """!
        @brief boolean 필드에 boolean이 아닌 값이 오면 무효여야 함을 검증한다.
        @technique 오류추정
        @case 부정(Negative) - 형식 오류 입력 검증
        """
        result = normalize(buildVehicle(sensor_fault="yes"), VALID_DRIVER)
        self.assertFalse(result.sensorFault.valid)
        self.assertEqual(result.sensorFault.reason, "format")

    def test_driverCommandMissingIsNone(self):
        """!
        @brief 운전자 명령 입력이 없으면 driverCommand는 None이어야 함을 검증한다.
        @technique 오류추정
        @case 부정(Negative) - 입력 없음 처리 검증
        """
        result = normalize(VALID_VEHICLE, None)
        self.assertIsNone(result.driverCommand)

    def test_driverCommandInvalidEnumResultsInNone(self):
        """!
        @brief side/action/source 중 하나라도 미등록 enum이면 명령 전체를 거절(None)해야 함을 검증한다.
        @technique 의사결정표기반
        @case 부정(Negative) - 명령 일부 필드 무효 시 전체 거절 검증
        """
        driver = dict(VALID_DRIVER)
        driver["side"] = "up"
        result = normalize(VALID_VEHICLE, driver)
        self.assertIsNone(result.driverCommand)


if __name__ == "__main__":
    unittest.main()
