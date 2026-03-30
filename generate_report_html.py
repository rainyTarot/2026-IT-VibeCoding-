from __future__ import annotations

import base64
from pathlib import Path


ROOT = Path(__file__).parent
REPORT_ASSETS = ROOT / "report_assets"
OUTPUT = ROOT / "project_report.html"


def image_data_uri(path: Path) -> str:
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    suffix = path.suffix.lower().lstrip(".")
    mime = "image/png" if suffix == "png" else f"image/{suffix}"
    return f"data:{mime};base64,{encoded}"


def main() -> None:
    start_img = image_data_uri(REPORT_ASSETS / "screenshot_start.png")
    play_img = image_data_uri(REPORT_ASSETS / "screenshot_play.png")
    game_over_img = image_data_uri(REPORT_ASSETS / "screenshot_game_over.png")

    html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Space Farm Mole Patrol 프로젝트 보고서</title>
  <style>
    :root {{
      --bg: #06101f;
      --panel: rgba(12, 28, 42, 0.88);
      --line: #47dfff;
      --line-soft: rgba(71, 223, 255, 0.22);
      --text: #eafcff;
      --muted: #96b9c2;
      --accent: #ff6a78;
      --accent2: #8fffd7;
      --warn: #ffd27a;
    }}
    * {{
      box-sizing: border-box;
    }}
    body {{
      margin: 0;
      font-family: "Segoe UI", "Malgun Gothic", sans-serif;
      background:
        radial-gradient(circle at top, rgba(47, 108, 156, 0.25), transparent 35%),
        linear-gradient(180deg, #07111f 0%, #040912 100%);
      color: var(--text);
      line-height: 1.7;
    }}
    .wrap {{
      width: min(1120px, calc(100% - 40px));
      margin: 0 auto;
      padding: 32px 0 72px;
    }}
    .hero {{
      padding: 28px 32px;
      border: 1px solid var(--line-soft);
      border-radius: 24px;
      background: linear-gradient(135deg, rgba(8, 20, 32, 0.94), rgba(11, 33, 48, 0.84));
      box-shadow: 0 0 0 1px rgba(71, 223, 255, 0.08) inset, 0 24px 80px rgba(0, 0, 0, 0.35);
    }}
    .eyebrow {{
      display: inline-block;
      padding: 6px 12px;
      border-radius: 999px;
      border: 1px solid var(--line-soft);
      color: var(--accent2);
      font-size: 13px;
      letter-spacing: 0.08em;
      text-transform: uppercase;
    }}
    h1 {{
      margin: 16px 0 10px;
      font-size: clamp(32px, 5vw, 56px);
      line-height: 1.1;
      letter-spacing: -0.03em;
    }}
    .hero p {{
      margin: 0;
      color: var(--muted);
      font-size: 18px;
    }}
    .meta {{
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 14px;
      margin-top: 24px;
    }}
    .meta-card {{
      padding: 16px 18px;
      border-radius: 18px;
      border: 1px solid var(--line-soft);
      background: rgba(10, 22, 32, 0.72);
    }}
    .meta-card strong {{
      display: block;
      color: var(--accent2);
      font-size: 13px;
      margin-bottom: 8px;
      letter-spacing: 0.05em;
    }}
    section {{
      margin-top: 22px;
      padding: 24px 28px;
      border-radius: 22px;
      border: 1px solid var(--line-soft);
      background: var(--panel);
      box-shadow: 0 10px 40px rgba(0, 0, 0, 0.22);
    }}
    h2 {{
      margin: 0 0 14px;
      font-size: 24px;
      color: #86f3ff;
    }}
    p {{
      margin: 0 0 14px;
    }}
    ul {{
      margin: 0;
      padding-left: 20px;
      color: var(--text);
    }}
    li + li {{
      margin-top: 8px;
    }}
    .grid-2 {{
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 18px;
    }}
    .cards {{
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 16px;
    }}
    .card {{
      padding: 18px;
      border-radius: 18px;
      border: 1px solid var(--line-soft);
      background: rgba(8, 20, 31, 0.8);
    }}
    .card h3 {{
      margin: 0 0 10px;
      font-size: 18px;
      color: var(--accent);
    }}
    .shot {{
      overflow: hidden;
      border-radius: 18px;
      border: 1px solid var(--line-soft);
      background: rgba(5, 12, 20, 0.9);
    }}
    .shot img {{
      display: block;
      width: 100%;
      height: auto;
    }}
    .shot .caption {{
      padding: 14px 16px 16px;
    }}
    .shot .caption strong {{
      color: var(--accent2);
      display: block;
      margin-bottom: 6px;
    }}
    .footer {{
      margin-top: 20px;
      text-align: center;
      color: var(--muted);
      font-size: 14px;
    }}
    @media (max-width: 920px) {{
      .meta,
      .grid-2,
      .cards {{
        grid-template-columns: 1fr;
      }}
    }}
  </style>
</head>
<body>
  <div class="wrap">
    <header class="hero">
      <span class="eyebrow">Project Report</span>
      <h1>Space Farm Mole Patrol</h1>
      <p>우주선 수경재배 구역을 침입한 두더지를 레이저 조준기로 제거하는 SF 스타일 두더지 잡기 게임 프로젝트 보고서입니다.</p>
      <div class="meta">
        <div class="meta-card">
          <strong>개발 목적</strong>
          짧은 시간 안에 직관적 재미를 제공하는 미니게임 구현
        </div>
        <div class="meta-card">
          <strong>개발 환경</strong>
          Python 3.12, pygame, PyInstaller
        </div>
        <div class="meta-card">
          <strong>산출물</strong>
          소스코드, 에셋, 효과음, 실행 파일, 보고서
        </div>
        <div class="meta-card">
          <strong>배포 형태</strong>
          Windows 실행 파일(.exe) + GitHub 저장소
        </div>
      </div>
    </header>

    <section>
      <h2>기획</h2>
      <p>이 프로젝트는 단순한 클릭 게임을 넘어, 짧은 시간 안에 즉각적인 몰입감을 주는 SF 콘셉트 게임을 만드는 것을 목표로 했습니다. 일반적인 두더지 잡기 게임은 규칙이 직관적이어서 누구나 쉽게 시작할 수 있지만, 시각적 개성과 피드백이 약하면 금방 단조롭게 느껴질 수 있습니다.</p>
      <p>그래서 본 프로젝트에서는 “우주선 텃밭 농사를 망치는 두더지를 레이저총으로 잡는다”는 테마를 설정해, 익숙한 장르를 SF 스타일로 재해석했습니다. 플레이어는 복잡한 설명 없이도 바로 게임을 이해할 수 있고, 시간 압박과 콤보 시스템을 통해 점점 긴장감이 높아지는 구조를 경험하게 됩니다.</p>
    </section>

    <section>
      <h2>구성물</h2>
      <div class="grid-2">
        <div>
          <ul>
            <li>`src/game.py`: 게임 메인 로직, 렌더링, 입력 처리, 난이도 제어</li>
            <li>`src/assets/`: 배경, 구멍, 두더지, UI 프레임, 조준선 이미지</li>
            <li>`src/generate_assets.py`: 그래픽 에셋 생성 스크립트</li>
            <li>`src/generate_sfx.py`: 효과음 생성 스크립트</li>
          </ul>
        </div>
        <div>
          <ul>
            <li>`Release/SpaceFarmMolePatrol/`: Windows 실행 파일 배포본</li>
            <li>`README.md`: 설치 및 실행 안내</li>
            <li>`project_report.html`: 본 프로젝트 보고서</li>
            <li>GitHub 저장소: 제출 및 버전 관리용 업로드 완료</li>
          </ul>
        </div>
      </div>
    </section>

    <section>
      <h2>주요 기능 목록</h2>
      <div class="cards">
        <div class="card">
          <h3>3x3 구멍 배치</h3>
          고정된 9개 구멍 좌표를 기반으로 두더지가 랜덤 위치에서 등장하도록 구성했습니다.
        </div>
        <div class="card">
          <h3>시간 + 콤보 난이도</h3>
          시간이 흐를수록 빨라지고, 콤보가 쌓일수록 더 빠르게 반응해야 하는 혼합 난이도 구조를 적용했습니다.
        </div>
        <div class="card">
          <h3>실시간 HUD</h3>
          점수, 남은 시간, 콤보, 위협 레벨을 SF 패널 UI로 표시해 상태를 즉시 파악할 수 있게 했습니다.
        </div>
        <div class="card">
          <h3>상태 전환</h3>
          시작 화면, 플레이 화면, 게임 오버 화면을 하나의 흐름으로 자연스럽게 전환하도록 구현했습니다.
        </div>
        <div class="card">
          <h3>직접 제작 효과음</h3>
          게임 시작, 명중, 실패, 게임 종료 사운드를 코드로 생성해 즉각적인 손맛을 강화했습니다.
        </div>
        <div class="card">
          <h3>실행 파일 배포</h3>
          PyInstaller로 Windows `.exe`를 빌드해 Python 설치 없이도 실행할 수 있도록 구성했습니다.
        </div>
      </div>
    </section>

    <section>
      <h2>실현 방법</h2>
      <p><strong>사용 기술</strong><br>Python 3.12와 pygame을 중심으로 게임 루프, 입력 처리, 타이머, 렌더링을 구현했습니다. 배포를 위해 PyInstaller를 사용했고, 에셋 자동 생성을 위해 Pillow를 활용했습니다.</p>
      <p><strong>AI 도구 활용 과정</strong><br>기획 단계에서 콘셉트와 기능 구조를 정리하고, 게임 플레이 흐름, UI 방향, 난이도 설계, 문서 구성까지 AI와 협업해 빠르게 구체화했습니다. 또한 반복적인 수정 작업에서 에셋 구조 정리, 보고서 초안 구성, 실행 파일 배포 이슈 점검 등을 AI 기반 코딩 보조 방식으로 진행했습니다.</p>
      <p><strong>구현 방식</strong><br>구멍별 상태를 객체 단위로 관리하고, 활성화된 두더지에 대해 클릭 판정을 수행하도록 설계했습니다. 난이도는 시간 경과에 따른 기본 속도 상승과 콤보에 따른 추가 압박을 동시에 반영해, 플레이 실력에 따라 체감 리듬이 달라지게 만들었습니다. 배포 단계에서는 `.exe` 실행 시 에셋 경로가 달라지는 문제를 고려해, 소스 실행과 frozen 실행 모두에서 에셋을 찾을 수 있는 경로 해석 로직을 추가했습니다.</p>
    </section>

    <section>
      <h2>결과</h2>
      <p>최종 결과물은 SF 세계관을 가진 완성형 미니게임입니다. 시작 화면, 실시간 플레이 화면, 게임 오버 화면이 모두 구현되었고, 전용 에셋과 효과음을 포함한 Windows 실행 파일까지 준비했습니다.</p>
      <div class="grid-2">
        <div class="shot">
          <img src="{start_img}" alt="시작 화면 스크린샷">
          <div class="caption">
            <strong>시작 화면</strong>
            SF 스타일 제목, 설명 문구, 시작 버튼을 배치해 바로 플레이 흐름으로 진입할 수 있게 구성했습니다.
          </div>
        </div>
        <div class="shot">
          <img src="{play_img}" alt="플레이 화면 스크린샷">
          <div class="caption">
            <strong>플레이 화면</strong>
            점수, 시간, 콤보, 위협 레벨을 상단 HUD로 제공하며, 등장한 두더지와 조준선을 통해 즉각적인 상호작용이 일어납니다.
          </div>
        </div>
      </div>
      <div class="shot" style="margin-top:18px;">
        <img src="{game_over_img}" alt="게임 오버 화면 스크린샷">
        <div class="caption">
          <strong>게임 오버 화면</strong>
          최종 점수와 최고 점수를 표시하고, 즉시 재시작할 수 있도록 구성했습니다.
        </div>
      </div>
    </section>

    <section>
      <h2>특장점</h2>
      <ul>
        <li>익숙한 두더지 잡기 규칙에 우주선 텃밭이라는 콘셉트를 더해 차별화된 분위기를 만들었습니다.</li>
        <li>이미지와 효과음을 직접 생성하는 구조를 갖춰, 프로젝트의 독립성과 재생산성이 높습니다.</li>
        <li>콤보가 높아질수록 난이도가 추가 상승해 플레이어 실력에 따라 리듬이 달라지는 점이 강점입니다.</li>
        <li>배포용 `.exe`까지 제공해 시연과 제출이 쉽고, README를 통해 실행 절차를 명확히 안내합니다.</li>
      </ul>
    </section>

    <section>
      <h2>한계점</h2>
      <ul>
        <li>현재는 적 종류가 기본 두더지 중심이라 패턴 다양성이 아직 제한적입니다.</li>
        <li>배경 음악, 스테이지 분기, 랭킹 저장 같은 장기 플레이 요소는 미구현 상태입니다.</li>
        <li>윈도우 실행 파일은 포함했지만, macOS나 Linux용 패키징은 아직 제공하지 않습니다.</li>
        <li>리포지토리 내부에 소스와 릴리스 산출물이 함께 존재해 구조가 다소 무거운 편입니다.</li>
      </ul>
    </section>

    <section>
      <h2>Todo</h2>
      <ul>
        <li>황금 두더지, 폭탄 두더지 등 특수 개체 추가</li>
        <li>배경 음악 및 추가 타격 이펙트 도입</li>
        <li>랭킹 저장과 난이도 선택 메뉴 구현</li>
        <li>스테이지 진행형 모드와 튜토리얼 모드 추가</li>
        <li>리포지토리 구조 경량화 및 빌드 산출물 관리 개선</li>
      </ul>
    </section>

    <div class="footer">
      단일 HTML 파일 제출 형식에 맞춰 작성되었으며, 모든 스크린샷 이미지는 base64 데이터로 문서 내부에 포함되어 있습니다.
    </div>
  </div>
</body>
</html>
"""

    OUTPUT.write_text(html, encoding="utf-8")


if __name__ == "__main__":
    main()
