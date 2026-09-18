<!--
※ 임시 형식 안내
Python/Node 환경이 준비되지 않아 정식 양식(TPL-SWE1-001, .docx)에 직접 채우지 못하고,
같은 절 구조를 그대로 따르는 Markdown으로 우선 작성한다. Python 준비 후 .docx로 옮긴다.
-->

# ENG-SWE1-001_SW 요구사항 명세서

| 항목 | 내용 |
|---|---|
| 템플릿 ID | TPL-SWE1-001 |
| 적용 프로세스 | SWE.1 |
| 프로젝트 | VJ-ECL-2026 (전자식 차일드락 제어 SW) |
| 문서 ID/명칭 | ENG-SWE1-001_SW 요구사항 명세서 |
| 버전/베이스라인 | v0.1 (초안, BL-SWR-1.0 목표) |
| 작성자 | `requirements-analyst` (Claude Code) |
| 검토자 | (사용자 리뷰 대기) |
| 입력 | `OEM_Sample/OEM-SWR-001_OEM SW 요구사항 사양서.docx` |

## 문서 통제

이 문서는 OEM-SWR-001(OEM-A 공급자 입력)을 근거로 공급자(Volsojoda 역할) 소프트웨어 요구사항을 도출한 것이다. 실제 승인은 수행되지 않으며, 이 저장소의 PR 리뷰·병합이 사용자 승인 행위를 대체한다.

### 변경 이력

| Revision | 변경일 | 작성 역할 | 변경 내용 | 검토 상태 |
|---|---|---|---|---|
| 0.1 | 2026-09-18 | `requirements-analyst` | OEM-SWR-001 기반 초안 작성 | 검토중 |

## 1. 목적 및 적용범위

### 1.1 목적

OEM-A가 입력한 전자식 차일드락 제어 요구(`OEM-SWR-001`)를 분석하여, 검증 가능한 소프트웨어 요구사항(SWR)으로 변환한다. 이 문서는 A-SPICE SWE.1 산출물이며, 이후 SWE.2(아키텍처)·SWE.3(상세설계)·SWE.4~6(검증)의 입력이 된다.

### 1.2 적용범위

대한민국 판매용 2026년식 가상 OEM-A 승용차의 후석 좌/우 전자식 차일드락 제어 소프트웨어. ASIL B(안전) 요구와 QM(기능) 요구를 구분한다. 실행 환경은 Python 3.14(PC/SIL, CLAUDE.md 정책에 따라 OEM 문서의 3.12를 3.14로 통일), 표시는 Web 시뮬레이터다.

### 1.3 적용 경계

SW-only PC/SIL 및 Web 검증만 다룬다. HIL, 실차, 타깃 ECU, 시스템/HW 개발, ISO 26262 Part 3(HARA/ASIL 도출), 공식 심사·인증은 범위 밖이다(OEM-SWR-001 1.2~1.3절 그대로 계승). 대한민국 법규(KMVSS 관련 별표 14/14-2 등) 적용 여부는 OEM이 차종/GVW/문형식/트림을 확정하기 전까지 후보로만 취급하며, 이 프로젝트는 그 확정을 기다리지 않고 가상 입력으로 진행한다(사용자 확인됨).

## 2. 요구사항 작성 및 판정 규칙

### 2.1 식별 및 상태 규칙

- ID 체계: `SWR-NNN`(3자리, 001부터). OEM 문서의 추적성표(9절)가 이미 SWR-001~021 중 20개를 OEM 요구에 매핑해 두었으므로, 그 번호를 그대로 사용한다. **SWR-019는 예비 ID로 비워둔다**(사용자 확인).
- 상태: 초안 → 검토중 → 승인. 현재 모든 SWR은 "검토중"이다.
- 우선순위: OEM 문서의 안전분류(ASIL B/QM)를 그대로 우선순위 근거로 사용한다. ASIL B 요구는 QM 요구보다 검증 우선순위가 높다.

### 2.2 품질 판정 기준

각 SWR은 `requirements-analyst` 스킬의 명확성·일관성 체크리스트(원자성, 검증 가능성, 추적성, 용어 통일)를 만족해야 한다. 판정기준은 가능한 한 OEM 문서의 수용기준(정량값)을 그대로 가져오며, 수용기준이 불명확한 경우 8절 "분석 결과와 가정"에 그 가정을 명시한다.

## 3. 상태와 우선순위

소프트웨어가 도출하는 출력 상태(잠금 논리 상태)는 다음 값을 갖는다. 이 표는 OEM-IF-006(SW→Display)의 `state` 값 정의를 근거로 한다.

| 상태 | 의미 | 전이 우선순위 근거 |
|---|---|---|
| NORMAL | 정상 평가, 안전/강제 조건 없음 | 기본 상태 |
| SUPPRESSED | 접근위험으로 해제 억제 중 | SWR-005/006 |
| OVERRIDE | 접근위험 억제를 운전자가 명시적으로 override | SWR-006 |
| FORCED_RELEASE | 화재/과온/성인탑승/충돌로 강제 해제 | SWR-007, SWR-017 |
| FORCED_LOCK | ISOFIX로 강제 잠금 | SWR-018 |
| OFF | ignition-off로 초기화 | SWR-020 |
| DEGRADED | 필수 입력 stale | SWR-013 |
| FAULT | sensor_fault | SWR-021 |

**여러 상태가 동시에 성립할 수 있는 조건(예: 충돌 CONFIRMED와 ISOFIX 강제잠금이 동시에 발생)의 최종 우선순위는 이 문서에서 확정하지 않는다.** 사용자 확인에 따라, 이 정책 의사결정표 초안은 SWE.2 아키텍처 설계 단계(Phase 1 설계)에서 작성해 별도로 리뷰받는다(8절 가정 A-1 참고).

## 4. 기능 및 안전 관련 SW 요구사항

검증 수준 열은 OEM 문서에 이미 지정된 값을 그대로 사용한다.

### 4.1 기능 요구사항 (QM)

| SWR ID | 출처(OEM) | 요구사항 | 수용기준 | 검증 수준 |
|---|---|---|---|---|
| SWR-001 | OEM-FR-001 | SW는 물리버튼/AVN/음성/모바일앱 4개 입력경로로부터 LOCK/RELEASE 명령과 대상(LEFT/RIGHT/ALL)을 수신·해석해야 한다. | 정지·정상입력에서 4개 source 각각의 명령이 올바르게 해석된다. | PC/SIL/Web |
| SWR-002 | OEM-FR-001 | SW는 수신한 명령을 선택된 도어(LEFT/RIGHT/ALL)에만 적용해야 하며, 선택되지 않은 반대쪽 도어의 출력을 변경하지 않아야 한다. | LEFT 명령 시 RIGHT 출력이 변하지 않는다(그 역도 같다). | PC/SIL/Web |
| SWR-003 | OEM-FR-002 | SW는 유효 차속(`vehicle_speed_kph`)이 3 km/h 이상이 되는 첫 평가주기부터 좌/우 출력을 LOCK으로 전환해야 한다. | 차속이 3 km/h를 넘는 첫 평가주기에 두 출력이 LOCK이다. | PC/SIL |
| SWR-004 | OEM-FR-001 | SW는 안전/강제 우선순위 로직(SWR-005~009, 017, 018, 020, 021)에 의해 억제되지 않는 한, 일반 RELEASE 명령을 적용해야 한다. | 억제 조건이 없을 때 RELEASE 명령이 다음 평가주기에 적용된다. | PC/SIL/Web |
| SWR-014 | OEM-FR-004 | SW는 상태조회 요청에 현재 좌/우 출력, `state`, 입력 유효성을 응답해야 한다. | 상태조회 응답에 좌/우 출력, state, 입력유효성이 모두 포함된다. | 통합 및 Web |
| SWR-015 | OEM-FR-004 | SW는 상태조회 응답에 최근 결정의 `priority_reason`과 `reason_code`를 포함해야 한다. | 응답에 두 필드가 항상 존재한다(해당 없으면 기본값). | 통합 및 Web |
| SWR-017 | OEM-FR-005 | SW는 `fire_detected`, `overtemperature_detected`, `adult_present` 중 하나라도 유효한 TRUE 입력이면 다음 평가주기에 좌/우 출력을 RELEASE로 전환하고, 트리거된 입력별 이유코드를 기록해야 한다. | 각 입력을 단독 주입 시 다음 평가주기에 두 출력이 RELEASE이고 입력별 reason_code가 기록된다. | PC/SIL/Web |
| SWR-018 | OEM-FR-006 | SW는 `isofix_left`/`isofix_right` 입력이 TRUE인 도어를 다음 평가주기에 LOCK으로 전환해야 하며, 한쪽만 TRUE면 반대쪽 출력은 유지되어야 한다. | 한쪽 ISOFIX만 TRUE일 때 해당 출력만 LOCK, 반대쪽 유지. | PC/SIL/Web |
| SWR-020 | OEM-FR-007 | SW는 `ignition_on`이 FALSE가 되는 첫 평가주기에 좌/우 출력을 RELEASE로 전환하고 `OFF` 상태와 `ignition_off` 이유코드를 제공해야 한다. | ignition_on=FALSE 첫 평가주기에 두 출력 RELEASE, OFF 상태, 이유코드 제공. | PC/SIL/Web |

### 4.2 안전 관련 SW 요구사항 (ASIL B)

| SWR ID | 출처(OEM) | ASIL | 요구사항 | 수용기준 | 검증 수준 |
|---|---|---|---|---|---|
| SWR-005 | OEM-SR-002 | B | SW는 `rear_left_approach_risk`/`rear_right_approach_risk`가 TRUE인 도어를 LOCK 상태로 전환해야 한다. | 접근위험 TRUE가 되면 해당 출력이 LOCK이다. | PC/SIL SW 검증 |
| SWR-006 | OEM-SR-002, OEM-FR-003 | B | SW는 접근위험으로 LOCK된 도어의 RELEASE 요청을 억제하고 원인을 기록해야 하며, 억제 후 10초 이내 같은 도어에 대한 동일 RELEASE 재입력은 명시적 override로 처리해 RELEASE를 적용하고 override 상태/이유코드를 생성해야 한다. | (a) 억제 중 RELEASE 요청에도 LOCK이 유지되고 원인이 기록된다. (b) 최초 억제 후 10초 이내 재입력 시 override 상태·이유코드가 생성되고 RELEASE가 적용된다. | PC/SIL SW 검증 |
| SWR-007 | OEM-SR-001 | B | SW는 `crash_status`가 CONFIRMED가 되면 다른 모든 명령보다 우선하여 좌/우 잠금 해제를 요구해야 하며, 300 ms 이내 RELEASE로 전환하고 이후 입력 주기에도 유지해야 한다. | 유효 충돌 입력 시 두 출력이 300 ms 이내 RELEASE이고 이후 유지된다. | PC/SIL SW 검증 |
| SWR-008 | OEM-SR-001 | B | SW는 `crash_status`가 PENDING인 동안에는 CONFIRMED 해제를 트리거하지 않고 대기 상태로 처리해야 한다(가정 A-2 참고). | PENDING 상태에서 좌/우 출력이 CONFIRMED 해제 로직에 의해 변경되지 않는다. | PC/SIL SW 검증 |
| SWR-009 | OEM-SR-002 | B | SW는 좌/우 도어의 접근위험 판단과 억제를 서로 독립적으로 적용해야 한다(한쪽 도어의 위험 판정이 반대쪽 도어에 영향을 주지 않는다). | 한쪽만 접근위험 TRUE일 때 반대쪽 도어의 상태·억제 여부가 변하지 않는다. | PC/SIL SW 검증 |
| SWR-013 | OEM-SR-003 | B | SW는 필수 안전 입력이 200 ms를 초과해 갱신되지 않으면 100 ms 이내 DEGRADED 상태로 전이해야 하며, 형식/범위 오류가 있는 입력은 평가 전에 거절(INVALID)해야 한다. | stale 입력(>200ms) 발생 시 100ms 이내 DEGRADED. 형식/범위 오류 입력은 평가에 반영되지 않는다. | 단위 및 PC/SIL |
| SWR-021 | OEM-SR-004 | B | SW는 `sensor_fault`가 TRUE인 첫 평가주기에 새 명령을 적용하지 않고 직전 확정 출력을 유지해야 하며, FAULT 상태와 경고코드를 제공해야 한다. | sensor_fault=TRUE 첫 평가주기에 좌/우 출력 유지, FAULT 상태·경고코드 제공. | 단위 및 PC/SIL |

## 5. 입력 데이터 사전

OEM-SWR-001 6절(외부 인터페이스 계약)의 데이터를 그대로 계승한다.

| 데이터 | 단위/범위 | 유효성 오류 처리 |
|---|---|---|
| `vehicle_speed_kph` | 0.0~300.0 km/h | 누락/형식/범위 오류 → INVALID |
| `gear` | P/N/D/R | 누락/형식/범위 오류 → INVALID |
| `source_timestamp_s` | 초 | 누락/형식/범위 오류 → INVALID |
| `crash_status` | NONE/PENDING/CONFIRMED | 미정 값 → INVALID |
| `rear_left_approach_risk`, `rear_right_approach_risk` | boolean | 누락/형식 오류 → INVALID |
| `fire_detected`, `overtemperature_detected`, `adult_present` | boolean | 누락/형식 오류 → INVALID |
| `isofix_left`, `isofix_right` | boolean | 누락/형식 오류 → INVALID |
| `ignition_on`, `sensor_fault` | boolean | 누락/형식 오류 → INVALID |
| `side`, `action`, `source` (운전자 명령) | left/right/all; lock/unlock; physical_button/avn/voice/mobile_app | 누락/형식/미등록 enum → 거절 |

## 6. 외부 인터페이스 요구

| 인터페이스 ID | 방향 | 관련 SWR | 시간 제약 |
|---|---|---|---|
| OEM-IF-001 | Vehicle→SW | SWR-003 | 매 평가주기 |
| OEM-IF-002 | Vehicle→SW | SWR-007, SWR-008 | 300 ms 내 반영(SWR-007) |
| OEM-IF-003 | Vehicle→SW | SWR-005, SWR-006, SWR-009 | 매 평가주기 |
| OEM-IF-004 | Driver→SW | SWR-001, SWR-002, SWR-004, SWR-006(override) | 매 평가주기 |
| OEM-IF-005 | SW→Actuator model | 모든 출력 요구(SWR-002~009, 017, 018, 020, 021) | PC/SIL 논리 출력까지만 검증 |
| OEM-IF-006 | SW→Display | SWR-014, SWR-015 | 상태조회 응답 시 |
| OEM-IF-007 | Vehicle→SW | SWR-017 | 매 평가주기 |
| OEM-IF-008 | Vehicle→SW | SWR-018 | 매 평가주기 |
| OEM-IF-009 | Vehicle→SW | SWR-020, SWR-021 | 매 평가주기 |

## 7. 비기능 및 환경 제약

| SWR ID | 출처 | 품질특성(ISO 25010) | 요구사항 | 수용기준 | 검증방안 |
|---|---|---|---|---|---|
| SWR-016 | OEM-NFR-001 | 기능적합성(정확성) | 동일 입력순서와 초기상태에는 항상 동일한 제어결과가 생성되어야 한다. | 고정 시계로 같은 벡터 1,000회 재생 시 결과 해시가 모두 같다. | 시험 — 결정론 재생 테스트 하니스로 1,000회 반복 실행 후 해시 비교 |
| SWR-010 | OEM-NFR-002 | 신뢰성(성숙성) | 각 제어결정마다 고유 이벤트 ID를 부여해야 한다. | 생성된 모든 이벤트의 ID가 유일하다. | 시험 |
| SWR-011 | OEM-NFR-002 | 보안성(기밀성) | 이벤트 스키마는 허용 필드만 포함해야 하며 영상·음성·개인식별정보를 포함하지 않아야 한다. | 이벤트 레코드에 허용 필드 외 값이 없다(스키마 검증). | 검사 — 스키마 정의 대비 필드 검토 |
| SWR-012 | OEM-NFR-002 | 신뢰성(가용성) | 이벤트 저장소는 메모리 내(휘발성)로 최근 100건만 유지해야 하며, 프로세스 재기동 시 모두 소멸해야 한다. | 101건 입력 후 최신 100건만 조회되고, 재기동 후 조회 결과가 비어 있다. | 시험 |

실행 환경 제약: Python 3.14(CLAUDE.md 정책, 사용자 확인). `coding` 스킬의 코딩 표준·`tdd` 스킬의 TDD 절차를 그대로 적용한다.

## 8. 분석 결과와 가정

| ID | 가정/미결정 사항 | 처리 방안 |
|---|---|---|
| A-1 | 크래시해제/접근위험잠금/화재·과온·성인탑승 강제해제/ISOFIX강제잠금/ignition-off해제/운전자명령/자동잠금(속도) 7개 결정소스가 동시에 상충할 때의 최종 우선순위가 OEM 문서에 명시되어 있지 않다. | Phase 1 설계(SWE.2 아키텍처) 단계에서 정책 의사결정표 초안을 작성해 사용자 리뷰를 받는다(사용자 확인됨). |
| A-2 | `crash_status=PENDING`일 때의 정확한 동작(예: 경고 표시 여부, 다른 로직과의 상호작용)이 OEM 문서에 상세히 정의되어 있지 않다. | SWR-008로 "대기 상태 유지, 다른 로직에 영향 없음"으로 최소 정의했다. 설계 단계에서 구체화가 필요하면 다시 확인한다. |
| A-3 | 대한민국 법규(KMVSS 별표 14/14-2 등) 적용 대상(차종/GVW/문형식/트림), 충돌입력 신뢰도, 도어래치 물리안전, 개인정보처리 확인 4건은 OEM이 "미제공"으로 남겨두었다. | 이 교육용 프로젝트는 확정을 기다리지 않고 가상 입력으로 진행한다(사용자 확인됨). 실제 프로젝트라면 이 항목들이 확정되기 전에는 관련 요구사항의 상태를 "가정 기반"으로 유지해야 한다. |
| A-4 | SWR-019는 OEM 추적성표에서 어떤 요구에도 연결되어 있지 않다. | 예비 ID로 비워둔다(사용자 확인됨). |
| A-5 | OEM-IF-005(SW→Actuator model)는 "PC/SIL 논리 출력까지만 검증하며 적용 feedback은 범위 밖"이라고 명시한다. | 액추에이터가 실제로 잠금에 성공했는지 확인하는 피드백 루프는 이 프로젝트 범위 밖으로 유지한다. |

## 9. 하향 할당 및 검증 계획

아키텍처 요소로의 할당은 Phase 1 설계(SWE.2) 단계에서 확정한다. 이 절은 설계 완료 후 갱신한다. 검증 수준(단위/PC-SIL/통합/Web)은 4~7절의 각 SWR 표에 이미 명시했다.

## 10. 범위 밖 주장

- ECU/HW, HIL, 실차 시험, 시스템 수준 시험, 공식 A-SPICE 심사, ISO 26262 준수·인증·ASIL 달성 주장은 하지 않는다.
- HARA, ASIL 도출 근거(ISO 26262 Part 3)는 재구성하지 않으며, OEM이 제공한 ASIL B 분류를 입력으로만 사용한다.
- 대한민국 법규 적합성 판단은 하지 않으며, 관련 항목은 가정 A-3에 따라 후보로만 취급한다.
- 도어 래치/구동기 물리 안전, 센서 성능, 진단 설계는 공급자(SW) 책임 범위 밖이다.

## 11. 추적성

OEM 요구 ↔ SWR 매핑은 OEM-SWR-001 9절의 추적성표를 그대로 계승한다. 아키텍처/상세설계/코드/시험 열은 각 후속 Phase에서 채운다.

| OEM 요구 | SWR | 아키텍처 요소 | 상세설계 | 코드 | 시험 |
|---|---|---|---|---|---|
| OEM-SR-001 | SWR-007, SWR-008 | (Phase 1 설계 예정) | (Phase 2) | (Phase 2) | (Phase 2) |
| OEM-SR-002 | SWR-005, SWR-006, SWR-009 | (Phase 1 설계 예정) | (Phase 2) | (Phase 2) | (Phase 2) |
| OEM-SR-003 | SWR-013 | (Phase 1 설계 예정) | (Phase 1) | (Phase 1) | (Phase 1) |
| OEM-SR-004 | SWR-021 | (Phase 1 설계 예정) | (Phase 1) | (Phase 1) | (Phase 1) |
| OEM-FR-001 | SWR-001, SWR-002, SWR-004 | (Phase 1 설계 예정) | (Phase 4) | (Phase 4) | (Phase 4) |
| OEM-FR-002 | SWR-003 | (Phase 1 설계 예정) | (Phase 4) | (Phase 4) | (Phase 4) |
| OEM-FR-003 | SWR-006 | (Phase 1 설계 예정) | (Phase 2) | (Phase 2) | (Phase 2) |
| OEM-FR-004 | SWR-014, SWR-015 | (Phase 1 설계 예정) | (Phase 5) | (Phase 5) | (Phase 5) |
| OEM-FR-005 | SWR-017 | (Phase 1 설계 예정) | (Phase 3) | (Phase 3) | (Phase 3) |
| OEM-FR-006 | SWR-018 | (Phase 1 설계 예정) | (Phase 3) | (Phase 3) | (Phase 3) |
| OEM-FR-007 | SWR-020 | (Phase 1 설계 예정) | (Phase 3) | (Phase 3) | (Phase 3) |
| OEM-NFR-001 | SWR-016 | (Phase 1 설계 예정) | (Phase 5) | (Phase 5) | (Phase 5) |
| OEM-NFR-002 | SWR-010, SWR-011, SWR-012 | (Phase 1 설계 예정) | (Phase 5) | (Phase 5) | (Phase 5) |

## 12. 참고자료

- `OEM_Sample/OEM-SWR-001_OEM SW 요구사항 사양서.docx` (본 문서의 유일한 입력 근거)
- `CLAUDE.md` (개발 생명주기·구현·테스트 정책)
- `.claude/agents/README.md` (서브에이전트/스킬 경계 지도)
- OEM 문서가 인용한 참고자료(SRC-ISO-001 ISO 26262-6:2018, SRC-LAW-KMVSS-* 등) — 법규 확인 상태는 가정 A-3 참고
