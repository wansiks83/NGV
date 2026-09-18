# Python 의존성 SBOM / FOSS 라이선스 관리 가이드

구현 경계(양식 13절)에 외부 라이브러리·오픈소스 의존성이 포함되는 경우, `WP_Templates/Engineering/SoftwareDetailedDesignAndUnitConstruction/TPL-SBOM-001_Python 의존성 SBOM FOSS 라이선스 목록 템플릿.xlsx`를 함께 채운다. 이 산출물은 A-SPICE SWE.3/SUP.8(형상관리) 양쪽에 걸친다.

## SBOM 시트

배포 또는 개발 환경에 포함되는 패키지마다 다음을 기록한다.

| 열 | 내용 |
|---|---|
| Package | 패키지 이름 |
| Version | 정확한 버전(범위 지정이 아닌 실제 고정 버전) |
| Dependency Type | 직접/전이 의존성, 런타임/개발용 구분 |
| SPDX | SPDX 라이선스 식별자(예: MIT, Apache-2.0) |
| Evidence Type | 근거 유형(패키지 메타데이터, 라이선스 파일 등) |
| Evidence Locator | 근거를 확인한 실제 위치(경로, URL 등) |
| Distribution | 배포물에 포함되는지(런타임 포함/개발 전용/미포함) |
| Remark | 특이사항(라이선스 의무사항 등) |

## FOSS Review 시트

의존성 목록 자체가 완전한지, 라이선스 의무를 이행할 수 있는지 검토한 결과를 기록한다.

| 열 | 내용 |
|---|---|
| Review ID | 검토 항목 식별자 |
| Scope | 검토 대상(전체 목록, 특정 패키지군 등) |
| Criterion | 검토 기준(완전성, 라이선스 의무, 배포 포함 여부 등) |
| Evidence | 검토에 사용한 근거 |
| Result | 결과(합격/조건부/불합격) |
| Owner | 검토 담당자 |
| Date | 검토일 |
| Limitation | 검토의 한계(확인하지 못한 부분) |

## 작성 원칙

- 실제 프로젝트의 의존성 파일(예: `requirements.txt`, `pyproject.toml`, 패키지 관리자의 잠금 파일)에 근거해서만 SBOM 항목을 작성한다. 확인하지 않은 패키지를 추측으로 채우지 않는다.
- 라이선스가 카피레프트 계열(GPL 등)이거나 배포 시 의무(고지, 소스 공개 등)가 있는 패키지는 Remark와 FOSS Review에 반드시 그 의무를 명시한다.
- 라이선스 정보를 확인할 수 없는 패키지는 Result를 "조건부" 또는 "불합격"으로 표시하고, 확인 방법을 사용자에게 안내한다(임의로 라이선스를 추정해 기재하지 않는다).
