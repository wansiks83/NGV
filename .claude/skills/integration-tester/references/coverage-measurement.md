# 함수커버리지·콜커버리지 측정 방법 (오픈소스 도구 사용)

Python(`coverage.py`, 오픈소스)과 표준 라이브러리 `ast` 모듈을 조합해 측정한다. 상용 임베디드 커버리지 도구가 제공하는 "함수커버리지/콜커버리지"를 별도 상용 도구 없이 구현하는 방법이다. 추측이나 코드를 눈으로 훑어본 결과가 아니라, 아래 절차로 실제 실행 데이터를 근거로 제시한다.

## 준비

```bash
pip install coverage
```

통합시험(실제 컴포넌트를 연결한 `unittest` 스위트)을 커버리지 측정과 함께 실행한다.

```bash
coverage run -m unittest discover -s <통합시험 디렉터리> -v
coverage json -o coverage.json
```

`coverage.json`에는 파일별로 실행된 라인 번호 목록(`executed_lines`)과 실행되지 않은 라인 번호 목록(`missing_lines`)이 들어있다.

## 함수커버리지 계산

1. 대상 소스 파일을 `ast.parse`로 파싱해 모든 `FunctionDef`/`AsyncFunctionDef` 노드와 그 라인 범위(시작~끝 라인)를 추출한다.
2. `coverage.json`의 `executed_lines`와 대조해, 함수의 라인 범위 안에 실행된 라인이 하나라도 있으면 그 함수를 "커버됨"으로 표시한다.
3. `함수커버리지 = 커버된 함수 수 / 전체 함수 수`.

```python
import ast, json

def listFunctionRanges(sourcePath):
    tree = ast.parse(open(sourcePath, encoding="utf-8").read())
    ranges = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            ranges.append((node.name, node.lineno, node.end_lineno))
    return ranges

def calculateFunctionCoverage(sourcePath, coverageJsonPath):
    coverageData = json.load(open(coverageJsonPath, encoding="utf-8"))
    executedLines = set(coverageData["files"][sourcePath]["executed_lines"])
    ranges = listFunctionRanges(sourcePath)
    coveredCount = sum(
        1 for _, start, end in ranges
        if executedLines.intersection(range(start, end + 1))
    )
    return coveredCount, len(ranges)
```

커버되지 않은 함수(호출된 적이 없는 함수)가 남으면, 그 함수를 호출하는 시험 케이스를 추가한다.

## 콜커버리지 계산

1. 같은 `ast` 트리에서 모든 `ast.Call` 노드(함수 호출 지점)를 찾아 그 라인 번호를 수집한다. 이것이 "전체 호출 지점" 목록이다.
2. `coverage.json`의 `executed_lines`와 대조해, 호출 지점이 위치한 라인이 실행되었으면 그 호출 지점을 "커버됨"으로 표시한다.
3. `콜커버리지 = 커버된 호출 지점 수 / 전체 호출 지점 수`.

```python
def listCallSites(sourcePath):
    tree = ast.parse(open(sourcePath, encoding="utf-8").read())
    return [node.lineno for node in ast.walk(tree) if isinstance(node, ast.Call)]

def calculateCallCoverage(sourcePath, coverageJsonPath):
    coverageData = json.load(open(coverageJsonPath, encoding="utf-8"))
    executedLines = set(coverageData["files"][sourcePath]["executed_lines"])
    callSites = listCallSites(sourcePath)
    coveredCount = sum(1 for line in callSites if line in executedLines)
    return coveredCount, len(callSites)
```

한 줄에 호출이 여러 개 있으면(예: `f(g(x))`) 줄 단위로는 구분되지 않는다. 이런 경우 코드를 줄 단위로 풀어 쓰거나(가독성에도 도움), `ast.Call` 노드의 `col_offset`까지 활용해 더 세밀하게 구분한다. 임의로 "대충 실행됐을 것"이라고 넘기지 않는다.

## 아키텍처 인터페이스와의 연결

- 아키텍처 설계서에 정의된 모든 제공 인터페이스 연산은 위 방식으로 계산한 함수커버리지 목록에서 반드시 100%여야 한다. 인터페이스 연산이 목록에서 빠져 있다면(예: 아직 구현되지 않음) 그 사실을 먼저 보고한다.
- 콜커버리지는 인터페이스를 사용하는 호출자 쪽 코드(다른 컴포넌트가 이 인터페이스를 호출하는 지점)까지 포함해야 의미가 있다. 인터페이스 제공자만 실행하고 호출자를 실행하지 않으면 콜커버리지를 과대평가하게 되므로, 통합시험은 반드시 호출자-被호출자 양쪽을 함께 실행한다.

## 보고 형식

| 소스 파일 | 함수커버리지 | 콜커버리지 | 미달 함수/호출지점 |
|---|---|---|---|
| brakeLogic.py | 100% (8/8) | 100% (23/23) | 없음 |
| sensorAdapter.py | 87.5% (7/8) | 91% (21/23) | `handleTimeout`(호출 안 됨), 12행 호출지점 |

100%에 도달하지 못한 항목이 있으면 "완료"로 보고하지 않고, 해당 함수/호출을 실행하는 시험 케이스를 추가한 뒤 재측정한다. 정말로 실행 불가능한 코드(예: 방어적으로만 존재하는 도달 불가능 분기)라면 그 이유를 근거와 함께 사용자에게 보고하고 예외 승인을 받는다.
