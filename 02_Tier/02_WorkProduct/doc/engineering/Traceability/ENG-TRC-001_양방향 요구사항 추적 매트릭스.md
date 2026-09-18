<!-- ※ 임시 형식 안내: TPL-TRC-001과 같은 목적의 Markdown 초안. Python 준비 후 .xlsx로 전환. -->

# ENG-TRC-001_양방향 요구사항 추적 매트릭스

| 항목 | 내용 |
|---|---|
| 템플릿 ID | TPL-TRC-001 |
| 적용 프로세스 | Common/SWE |
| 버전 | v0.2 (Phase 1 설계 반영) |

이 표는 Phase가 진행될 때마다 아키텍처/상세설계/코드/시험 열을 채워 갱신한다. 현재는 Phase 1(분석+설계) 완료 시점 기준이며, 상세설계/코드/시험 열은 이후 Phase에서 채운다.

| OEM 요구 | SWR | Use Case | 아키텍처 요소 | 상세설계 | 코드 | 단위/통합 시험 | 시스템 시험 |
|---|---|---|---|---|---|---|---|
| OEM-SR-001 | SWR-007, SWR-008 | UC-04 | `CrashReleasePolicy` | — | — | — | — |
| OEM-SR-002 | SWR-005, SWR-006, SWR-009 | UC-03 | `ApproachRiskPolicy` | — | — | — | — |
| OEM-SR-003 | SWR-013 | UC-09 | `InputGateway`, `DegradedStateManager` | — | — | — | — |
| OEM-SR-004 | SWR-021 | UC-08 | `SensorFaultGate` | — | — | — | — |
| OEM-FR-001 | SWR-001, SWR-002, SWR-004 | UC-01 | `DriverCommandPolicy` | — | — | — | — |
| OEM-FR-002 | SWR-003 | UC-02 | `AutoLockPolicy` | — | — | — | — |
| OEM-FR-003 | SWR-006 | UC-03 | `ApproachRiskPolicy`(override) | — | — | — | — |
| OEM-FR-004 | SWR-014, SWR-015 | UC-10 | `OutputMapper` | — | — | — | — |
| OEM-FR-005 | SWR-017 | UC-05 | `ForcedReleasePolicy` | — | — | — | — |
| OEM-FR-006 | SWR-018 | UC-06 | `IsofixLockPolicy` | — | — | — | — |
| OEM-FR-007 | SWR-020 | UC-07 | `IgnitionOffPolicy` | — | — | — | — |
| OEM-NFR-001 | SWR-016 | (전체 재생 시나리오) | `PriorityArbiter`(순수함수/결정론), 전체 파이프라인 | — | — | — | — |
| OEM-NFR-002 | SWR-010, SWR-011, SWR-012 | (이벤트 로그, 모든 UC 공통) | `EventLogStore` | — | — | — | — |
| (전체 공통) | — | — | `PriorityArbiter`(우선순위 중재, 8절 정책표) | — | — | — | — |
| (예비) | SWR-019 | — | — | — | — | — | — |

## 참고자료

`ENG-SWE1-001_SW 요구사항 명세서`, `ENG-SWE1-002_Use Case 명세서`, `OEM_Sample/OEM-SWR-001_OEM SW 요구사항 사양서.docx`
