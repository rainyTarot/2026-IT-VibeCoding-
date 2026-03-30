# Space Farm Mole Patrol

Space Farm Mole Patrol은 Python과 pygame으로 제작한 SF 스타일 두더지 잡기 게임입니다.

## 저장소 구조

```text
GitHub Repository
├─ src/                              # 소스코드
│  ├─ game.py
│  ├─ generate_assets.py
│  ├─ generate_sfx.py
│  └─ assets/
├─ Release/                          # 실행 파일 배포본
│  ├─ SpaceFarmMolePatrol/
│  │  ├─ SpaceFarmMolePatrol.exe
│  │  └─ _internal/                  # 실행에 필요한 런타임 DLL 및 에셋
│  └─ run_game.bat
├─ requirements.txt
└─ README.md
```

## 권장 실행 방법

실행 파일 배포본은 Python 설치 없이 바로 실행할 수 있습니다.

1. `Release/SpaceFarmMolePatrol/` 폴더를 엽니다.
2. `SpaceFarmMolePatrol.exe`를 실행합니다.

Windows SmartScreen 경고가 나타나면 `추가 정보`를 누른 뒤 `실행`을 선택하면 됩니다.

## 대체 실행 방법

소스코드 버전으로 실행하려면 아래 순서로 진행합니다.

1. Python 3.12 이상을 설치합니다.
2. 저장소 루트 폴더에서 터미널을 엽니다.
3. 아래 명령어를 실행합니다.

```bash
pip install -r requirements.txt
python src/game.py
```

## 조작 방법

- 마우스 이동: 레이저 조준
- 마우스 왼쪽 클릭: 두더지 공격
- 시작 버튼 클릭: 게임 시작
- 재시작 버튼 클릭: 다시 플레이

## 게임 규칙

- 제한 시간은 30초입니다.
- 두더지를 맞히면 점수가 올라갑니다.
- 콤보가 높을수록 추가 점수를 얻습니다.
- 난이도는 시간 경과와 콤보에 따라 함께 상승합니다.

## 제출 전 확인 사항

업로드 전에 아래 순서대로 꼭 확인합니다.

1. `Release/SpaceFarmMolePatrol/` 폴더를 엽니다.
2. `SpaceFarmMolePatrol.exe`를 실행합니다.
3. 시작 화면이 정상적으로 표시되는지 확인합니다.
4. 두더지가 3x3 구멍에서 등장하는지 확인합니다.
5. 클릭 시 점수와 효과음이 정상 동작하는지 확인합니다.

## 참고

- 메인 게임 소스: `src/game.py`
- 에셋 생성 스크립트: `src/generate_assets.py`
- 효과음 생성 스크립트: `src/generate_sfx.py`
