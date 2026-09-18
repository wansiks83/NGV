# 네이밍 규칙과 Doxygen 주석 규칙

## 네이밍 규칙

- 함수명과 변수명은 **3자 이상**이어야 한다(`i`, `n`, `x` 같은 한두 글자 이름은 반복문 인덱스라도 사용하지 않는다. 예: `idx`, `count`).
- 함수명과 변수명은 **낙타 표기법(camelCase)**을 사용한다. 예: `calculateTimeToCollision`, `obstacleDistance`.
- 클래스명은 이 프로젝트의 일반적인 관례에 맞춰 PascalCase를 사용하고(camelCase 규칙은 함수/변수에 적용), 상수는 프로젝트 내 다른 규칙이 없다면 대문자 스네이크케이스를 유지해도 된다. 단, 이 부분에서 사용자의 별도 지시가 있으면 그것을 따른다.
- 이름은 축약어 남발 없이 의미가 드러나야 한다("d" 대신 "distance", "cnt" 대신 "count").

## Python에서 camelCase를 쓸 때 주의할 점

Python 표준 스타일(PEP 8)은 기본적으로 snake_case를 권장하고, `flake8`의 `pep8-naming` 플러그인이나 기본 `pylint` 네이밍 검사기는 이를 위반으로 표시할 수 있다. 이 프로젝트는 CLAUDE.md에서 명시적으로 camelCase를 지정했으므로:

- `pep8-naming`(flake8 플러그인)을 사용하지 않거나, 사용한다면 함수/변수 네이밍 규칙(N802/N803/N806 등)을 비활성화한다.
- `pylint`를 쓴다면 `.pylintrc`의 `function-naming-style`, `variable-naming-style`, `argument-naming-style`을 `camelCase`로 설정한다.
- 대신 함수/변수명이 3자 이상인지, camelCase 형식(첫 글자 소문자, 이후 단어 경계 대문자)인지는 정규식으로 점검할 수 있다: `^[a-z][a-zA-Z0-9]{2,}$`이면서 두 단어 이상 결합 시 중간에 대문자가 있는지 확인.

## Doxygen 방식 주석

Doxygen은 Python 코드에도 적용 가능하다. 함수/클래스 정의 바로 앞이나 첫 줄에 아래와 같은 형식으로 작성한다.

```python
def calculateTimeToCollision(distanceM, relativeSpeedMps):
    """!
    @brief 장애물과의 충돌예상시간을 계산한다.
    @param distanceM 장애물까지의 거리(미터, 0 이상).
    @param relativeSpeedMps 상대속도(m/s).
    @return 충돌예상시간(초). 접근하지 않는 경우 math.inf.
    @exception ValueError distanceM이 음수인 경우.
    """
    ...
```

- 모든 공개 함수/클래스에는 `@brief`(요약), 필요 시 `@param`(매개변수별), `@return`(반환값), `@exception`(예외)을 포함한 Doxygen 스타일 주석을 작성한다.
- Doxyfile을 프로젝트에 둔다면 `OPTIMIZE_OUTPUT_JAVA = NO`, `JAVADOC_AUTOBRIEF = YES`로 설정해 위 스타일을 인식하게 한다.

## 테스트 함수의 주석 규칙

테스트 함수(`test_*`)에는 위 형식에 더해 `@technique`(사용한 시험 기법)과 `@case`(긍정/부정 여부)를 반드시 포함한다. 구체적인 규칙과 예시는 `tdd` 스킬의 `SKILL.md` "테스트 함수 주석 규칙" 절을 따른다.

## 주석 비율 20% 이상

"주석은 Doxygen 방식으로 작성하며, 20% 이상 작성해야 한다"는 요구는 파일 전체 라인 수 대비 주석 라인 수(문서화 문자열 포함) 비율로 측정한다. 측정 방법은 `quality-metrics.md`의 `radon raw` 사용법을 따른다. 20%에 못 미치면 의미 없는 주석을 채우지 말고, 설명이 필요한 함수/로직에 실질적인 Doxygen 주석을 보강해 비율을 높인다.
