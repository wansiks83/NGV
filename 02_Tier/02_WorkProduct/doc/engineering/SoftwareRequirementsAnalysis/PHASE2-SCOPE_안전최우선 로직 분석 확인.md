# Phase 2 분석 확인 — 안전최우선 로직 (ASIL B)

이 문서는 새로운 요구사항 분석이 아니라, 이미 승인된 `ENG-SWE1-001_SW 요구사항 명세서`(BL-SWR-1.0)의 SWR-005~009가 Phase 2 범위에서 변경 없이 그대로 유효함을 확인하는 게이트 메모다.

## Phase 2 범위 SWR (ENG-SWE1-001 4.2절 원문)

| SWR ID | 출처 | ASIL | 요구사항 | 수용기준 |
|---|---|---|---|---|
| SWR-005 | OEM-SR-002 | B | SW는 rear_left/right_approach_risk가 TRUE인 도어를 LOCK 상태로 전환해야 한다. | 접근위험 TRUE가 되면 해당 출력이 LOCK이다. |
| SWR-006 | OEM-SR-002, OEM-FR-003 | B | SW는 접근위험으로 LOCK된 도어의 RELEASE 요청을 억제하고 원인을 기록해야 하며, 억제 후 10초 이내 같은 도어에 대한 동일 RELEASE 재입력은 override로 처리해 RELEASE를 적용하고 override 상태/이유코드를 생성해야 한다. | (a) 억제 중 RELEASE 요청에도 LOCK 유지+원인 기록. (b) 10초 이내 재입력 시 override+RELEASE. |
| SWR-007 | OEM-SR-001 | B | SW는 crash_status가 CONFIRMED가 되면 다른 모든 명령보다 우선하여 좌/우 잠금 해제를 요구해야 하며, 300 ms 이내 RELEASE로 전환하고 이후 입력 주기에도 유지해야 한다. | 유효 충돌 입력 시 두 출력이 300 ms 이내 RELEASE이고 이후 유지된다. |
| SWR-008 | OEM-SR-001 | B | SW는 crash_status가 PENDING인 동안에는 CONFIRMED 해제를 트리거하지 않고 대기 상태로 처리해야 한다(가정 A-2). | PENDING 상태에서 좌/우 출력이 변경되지 않는다. |
| SWR-009 | OEM-SR-002 | B | SW는 좌/우 도어의 접근위험 판단과 억제를 서로 독립적으로 적용해야 한다. | 한쪽만 접근위험 TRUE일 때 반대쪽 도어 상태가 변하지 않는다. |

## 확인 사항

- 위 SWR 문구·수용기준은 Phase 1에서 승인된 것과 동일하며, 이번 Phase에서 변경하지 않는다.
- 아키텍처 요소 매핑(`ENG-SWE2-001` 3.1절): SWR-005/006/009 -> `ApproachRiskPolicy`, SWR-007/008 -> `CrashReleasePolicy`.
- 우선순위: `ENG-SWE2-001` 8절 정책 의사결정표에서 P1(CrashReleasePolicy), P3(ApproachRiskPolicy)로 이미 정의됨(초안, 아직 사용자 최종 승인 대기 — 이번 Phase 상세설계에서 재확인).
- 입력 의존성: Phase 1에서 병합된 `InputGateway`(정규화), `SensorFaultGate`(sensor_fault 게이트)를 그대로 사용한다. 두 모듈의 계약은 변경하지 않는다.
- 검증 수준: PC/SIL SW 검증(단위 TDD + Phase 통합시험).

## 결론

Phase 2 분석 게이트를 통과한다. 다음 단계(상세설계)로 진행한다.
