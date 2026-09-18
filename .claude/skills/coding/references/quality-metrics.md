# 품질지표 측정 방법 (오픈소스 도구 사용)

CLAUDE.md는 "순환복잡도, 함수라인수 등 측정지표는 오픈소스 도구를 이용한다"고 명시한다. 추측이나 눈으로 어림잡은 수치를 보고하지 않고, 아래 도구로 실제 측정한 값을 근거로 제시한다.

## 함수 순수 코드 라인수 ≤ 50, 순환복잡도 ≤ 10 — `lizard`

`lizard`는 함수 단위로 NLOC(주석/공백을 제외한 순수 코드 라인수)와 CCN(순환복잡도)을 함께 측정하는 오픈소스 도구다.

```bash
pip install lizard
lizard path/to/module.py
```

출력의 각 행이 함수 하나에 대응하며 `NLOC`, `CCN` 열을 확인한다. 기준을 초과하는 함수를 찾으려면:

```bash
lizard --CCN 10 --length 50 path/to/module.py
```

이 명령은 CCN이 10을 넘거나 길이가 50을 넘는 함수를 경고로 표시한다. 경고가 남아있는 채로 구현을 끝내지 않는다.

## 중복 코드는 7라인까지 허용(8라인 이상 금지) — `pylint`

`pylint`의 유사성(Similarities) 검사기를 사용한다.

```bash
pip install pylint
pylint --disable=all --enable=duplicate-code --min-similarity-lines=8 path/to/module.py path/to/other_module.py
```

`min-similarity-lines=8`로 설정하면 8라인 이상 동일/유사한 코드 블록만 `R0801`로 보고한다(=7라인까지는 허용). 보고된 중복은 공통 함수로 추출해 제거한다.

## 주석 비율 20% 이상 — `radon raw`

`radon`은 원시 지표(총 라인수, 논리 라인수, 주석 라인수, 문서화 문자열 라인수, 공백)를 제공한다.

```bash
pip install radon
radon raw path/to/module.py
```

출력의 `LOC`(전체 라인), `comments`(주석 라인), `multi`(독스트링 등 여러줄 문자열, Doxygen 스타일 독스트링 포함)를 이용해 주석 비율을 계산한다.

```
주석비율 = (comments + multi) / LOC
```

0.2(20%) 미만이면 실질적인 Doxygen 주석을 보강한다.

## 네이밍(3자 이상, camelCase) — `pylint` 커스텀 설정

`.pylintrc`(또는 `pyproject.toml`의 `[tool.pylint]`)에서 아래처럼 설정한다.

```ini
[BASIC]
function-naming-style=camelCase
variable-naming-style=camelCase
argument-naming-style=camelCase
```

`pylint`의 네이밍 검사(`C0103` 등)로 camelCase 위반을 잡아낸다. 3자 이상 조건은 위 설정으로 기본 커버되지 않으므로, 짧은 이름(`i`, `x`, `n` 등)이 있는지 코드 리뷰 시 별도로 확인한다. 필요하면 `good-names=`를 빈 값으로 설정해 기본 허용 예외(`i`, `j`, `k` 등)를 없앤다.

## 측정 결과 보고 방식

구현을 마칠 때마다 아래 형식으로 실제 측정값을 보고한다. 추정치가 아니라 명령 실행 결과를 근거로 한다.

| 파일/함수 | NLOC | CCN | 중복(8줄↑) | 주석비율 | 네이밍 |
|---|---|---|---|---|---|
| module.py::calculateTimeToCollision | 32 | 4 | 없음 | 24% | 통과 |

기준을 초과한 항목이 있으면 "완료"로 보고하지 않고, TDD의 리팩터링 단계로 돌아가 해결한 뒤 재측정한다.
