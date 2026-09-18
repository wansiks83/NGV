# 서브에이전트 · 스킬 경계 지도

이 문서는 `.claude/agents/`의 서브에이전트와 `.claude/skills/`의 스킬이 각각 어떤 A-SPICE 프로세스/CLAUDE.md 생명주기 단계를 담당하는지, 서로 무엇을 참조하고 무엇을 중복하지 않는지 정리한 것이다. 새 서브에이전트/스킬을 추가하거나 기존 것을 고칠 때 이 문서를 먼저 갱신한다.

## 개발 생명주기 파이프라인 (CLAUDE.md 순서: 분석 → 설계 → 구현 → 테스트)

| 순서 | 단계 | A-SPICE 프로세스 | 서브에이전트 | 전용 스킬 | 실제 산출물 양식 |
|---|---|---|---|---|---|
| 1 | 분석 | SYS.2 / SWE.1 | `requirements-analyst` | `requirements-analyst` | `TPL-SWE1-001/002/003` |
| 2 | 설계(아키텍처) | SWE.2 | `architecture-designer` | `architecture-designer` | `TPL-SWE2-001/002` |
| 3 | 설계(상세) | SWE.3(설계 부분) | `detailed-designer` | `detailed-designer` | `TPL-SWE3-001/002`, `TPL-SBOM-001` |
| 4 | 구현 | SWE.3(구현 부분) | `coding` | `coding` + `tdd` | 소스 코드, `TPL-TRC-001`(갱신), `TPL-REV-001`(대상 정리) |
| 5 | 테스트(통합) | SWE.5 | `integration-tester` | `integration-tester` | `TPL-SWE5-001/002/003` |
| 6 | 테스트(시스템/자격) | SWE.6 | `sw-system-tester` | `sw-system-test` | `TPL-SWE6-001/002` |

**SWE.4(소프트웨어 유닛 검증)는 현재 전용 서브에이전트가 없다.** `coding`/`tdd`가 TDD로 실질적인 단위 시험을 수행하지만, `TPL-SWE4-001/002` 형식의 공식 단위검증 산출물 작성은 명시적으로 범위 밖이다(`coding` 스킬 6단계). 이 산출물이 필요하면 별도 서브에이전트를 새로 만들거나 `coding`의 범위를 의도적으로 넓혀야 한다.

## 파이프라인 밖 — 감사(횡단 관심사)

| 서브에이전트 | 역할 | 전용 스킬 |
|---|---|---|
| `aspice-cl2-auditor` | 위 파이프라인이 만든 산출물을 CL2(PA2.1/PA2.2) 관점에서 사후 점검. 산출물을 만들지 않고 점검만 한다. | `aspice-auditor` |

## 공용(여러 스킬이 함께 참조) 스킬 — 중복 정의 금지

아래 스킬은 특정 단계 하나에 속하지 않고, 여러 단계별 스킬이 공통으로 참조한다. **아래 항목의 정의는 각각 한 곳에만 존재하며, 다른 스킬은 그 파일을 가리키기만 한다.**

| 공용 지식 | 원본이 있는 스킬/파일 | 참조하는 스킬 |
|---|---|---|
| 응집력/결합도, SOLID 5원칙 | `architecture-designer`의 `references/cohesion-coupling.md`, `references/solid-principles.md` | `detailed-designer`, `coding` (컴포넌트 수준 원칙을 유닛/함수 수준까지 그대로 적용) |
| ISO 26262 코딩 수준 제약(포인터/동적메모리/전역변수/인터럽트/무조건분기) | `detailed-designer`의 `references/iso26262-swe3-constraints.md` | `coding` |
| ISO 25010/25000 품질특성 8종 분류 | `requirements-analyst`의 `references/iso25010-nfr.md` | `sw-system-test` (비기능 테스트 케이스 그룹화에 사용) |
| 시험 케이스 도출 기법(경계값분석/동치분할/조합·페어와이즈/엣지케이스/경험기반/의사결정표기반/상태전이기반/사전조건·사후조건검증/회귀테스트) + PICT 도구 | `test-design-techniques` 스킬 | `tdd`(단위), `integration-tester`(통합), `sw-system-test`(시스템) — 각자 "무엇을 시험할지"만 자기 단계 기준으로 정의하고, "어떤 값으로 케이스를 구성할지"는 이 공용 카탈로그를 따른다 |
| Doxygen 형식 테스트 주석(`@brief`/`@technique`/`@case`) | `tdd` 스킬 "테스트 함수 주석 규칙" | `integration-tester`(코드로 구현하는 통합시험도 동일 규칙 적용) |

## 테스트 베이시스 구분 (세 시험 단계가 서로 겹치지 않는 이유)

세 시험 스킬은 기법 카탈로그는 공유하지만, **테스트 베이시스(무엇을 근거로 케이스를 뽑는가)는 서로 다르다.** 이것이 세 스킬의 실질적 경계다.

| 스킬 | 테스트 베이시스 | 커버리지 목표 |
|---|---|---|
| `tdd` (단위) | 상세설계서의 함수 계약·의사결정표·상태전이 | `coding` 스킬의 품질지표(라인수/복잡도/중복/주석비율) — 커버리지 수치 목표는 별도 지정 없음 |
| `integration-tester` (통합) | 아키텍처 설계서의 인터페이스·통합순서 | 함수커버리지·콜커버리지 100% |
| `sw-system-test` (시스템) | SW 요구사항 명세서 | 프로젝트가 정한 요구사항 커버리지 목표(CLAUDE.md 등)를 따름, 별도 수치 강제는 없음 |

## 새 서브에이전트/스킬을 추가할 때 지켜야 할 원칙

1. 실제 프로젝트 산출물 양식(`WP_TEMPLATES/Engineering/...`, `PRC-TPL-001` 등록부)이 있으면 반드시 그 경로를 0단계에서 확인하고 그대로 쓴다. 임의로 시트/절 구조를 새로 만들지 않는다.
2. 다른 스킬이 이미 정의한 지식(원칙, 분류, 기법 카탈로그)을 다시 설명하지 않는다. 파일 경로로 가리킨다.
3. 이 문서(`agents/README.md`)의 표에 새 항목을 추가해 경계를 갱신한다.
