# Phase 3 분석 확인 — 강제 해제/잠금 로직 (QM)

이 문서는 새로운 요구사항 분석이 아니라, 이미 승인된 `ENG-SWE1-001_SW 요구사항 명세서`(BL-SWR-1.0)의 SWR-017, 018, 020이 Phase 3 범위에서 변경 없이 그대로 유효함을 확인하는 게이트 메모다.

## Phase 3 범위 SWR (ENG-SWE1-001 4.1절 원문)

| SWR ID | 출처 | 요구사항 | 수용기준 |
|---|---|---|---|
| SWR-017 | OEM-FR-005 | SW는 fire_detected, overtemperature_detected, adult_present 중 하나라도 유효한 TRUE 입력이면 다음 평가주기에 좌/우 출력을 RELEASE로 전환하고, 트리거된 입력별 이유코드를 기록해야 한다. | 각 입력을 단독 주입 시 다음 평가주기에 두 출력이 RELEASE이고 입력별 reason_code가 기록된다. |
| SWR-018 | OEM-FR-006 | SW는 isofix_left/isofix_right 입력이 TRUE인 도어를 다음 평가주기에 LOCK으로 전환해야 하며, 한쪽만 TRUE면 반대쪽 출력은 유지되어야 한다. | 한쪽 ISOFIX만 TRUE일 때 해당 출력만 LOCK, 반대쪽 유지. |
| SWR-020 | OEM-FR-007 | SW는 ignition_on이 FALSE가 되는 첫 평가주기에 좌/우 출력을 RELEASE로 전환하고 OFF 상태와 ignition_off 이유코드를 제공해야 한다. | ignition_on=FALSE 첫 평가주기에 두 출력 RELEASE, OFF 상태, 이유코드 제공. |

## 확인 사항

- SWR-017, 020은 **양쪽 도어(좌/우)에 동시 적용**되는 요구다(SWR-005/006/018처럼 도어별 독립 판단이 아님). 상세설계에서 이 차이를 명확히 반영한다.
- SWR-018은 SWR-005(접근위험)와 동일하게 **도어별 독립 판단**이다(한쪽만 TRUE면 그 도어만 영향).
- 아키텍처 요소 매핑(`ENG-SWE2-001` 3.1절): SWR-017 -> `ForcedReleasePolicy`, SWR-018 -> `IsofixLockPolicy`, SWR-020 -> `IgnitionOffPolicy`.
- 우선순위(`ENG-SWE2-001` 8절 정책 의사결정표, 초안): P2(ForcedReleasePolicy) > P3(ApproachRiskPolicy, Phase 2 완료) > P4(IsofixLockPolicy) > P5(IgnitionOffPolicy). 즉 화재/과온/성인탑승 강제해제가 접근위험 잠금보다도 우선한다.
- 입력 의존성: Phase 1의 `InputGateway`/`SensorFaultGate`, Phase 2의 우선순위 판단 방식(순수함수, PolicyVote 반환)을 그대로 따른다.
- 검증 수준: PC/SIL/Web(단위 TDD + Phase 통합시험).

## 결론

Phase 3 분석 게이트를 통과한다. 다음 단계(상세설계)로 진행한다.
