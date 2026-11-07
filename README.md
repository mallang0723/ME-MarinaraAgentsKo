# Marinara 에이전트 라이브러리 임시 한글화

Marinara Engine의 정식 에이전트 메타데이터 현지화가 완료되기 전까지 사용하는 임시 Personal Extension입니다.

이 프로젝트는 Marinara Engine 공식 프로젝트가 아닌 커뮤니티 배포 확장입니다. 공식 영문 카탈로그를 기준으로 한국어 번역을 유지하며, 확장 소스 전체를 저장소에서 공개합니다.

## 호환 범위

- 기준 앱: Marinara Engine `2.5.2` (`v2.5.2`)
- 기준 카탈로그: 2026-11-06에 확인한 `Pasta-Devs/Marinara-Agents` `main`의 공식 패키지 44개
- 적용 언어: Marinara UI 언어가 한국어(`ko`, `ko-*`)인 경우

Marinara 업데이트로 에이전트 이름·설명 또는 화면 구조가 바뀌면 일부 항목이 영어로 남을 수 있습니다. 이 경우 사용자 데이터에는 영향을 주지 않으며, 검수된 번역표 업데이트가 필요합니다.

## 번역 범위

- 에이전트 탭에 표시되는 공식 에이전트 이름과 설명
- 에이전트 라이브러리(공식 카탈로그)의 에이전트 이름과 설명
- Agent Organizer 목록의 축약 설명과 상세 페이지의 전체 설명
- 채팅 설정의 하드코딩된 분류 3개와 설명(작성·추적·기타 에이전트)
- 채팅 에이전트 카드·선택기·배지·설정 창·진행 상태, Omnibar 에이전트 행, 홈 추천·탭
- 공식 패키지의 per-Agent 이름·설명과 활성 메뉴에서 설치 안내를 제거한 설명
- 공식 패키지 44개 (`slurp` 대신 `slurp2`, 표시명은 `Slurp`)

실제 i18n 키를 사용하는 모드 필터·분류·설치 목록 등의 UI 라벨은 공식 한국어 팩에 맡깁니다. `Not installed`, `Attach lorebook for the specific agent`도 확장이 번역하지 않습니다. 채팅 설정 배열의 하드코딩 문구만 해당 영역에서 보완합니다. 이미 한국어로 표시된 패키지 설명도 덮어쓰지 않습니다. [2.5.2 소스 및 공식 번역 대조 기록](docs/compatibility-2.5.2.md)을 참고하세요.

일반 채팅 내용과 편집 필드는 번역하지 않습니다. 지원 영역 안에서 공식 메타데이터와 완전히 동일한 사용자 지정 이름·설명은 DOM만으로 구별할 수 없어 함께 번역될 수 있습니다. 새 패키지 또는 영문 설명이 변경된 패키지는 검수된 번역표에 추가되기 전까지 영어로 남습니다.

## 권한과 안전 경계

기존 Marinara 화면의 DOM을 바꾸기 위해 `full_page_access`가 필요합니다. 이 권한은 브라우저 개발자 콘솔 수준의 페이지 접근 권한이므로 설치 화면에서 소스와 hash를 확인하세요.

이 버전은 다음 기능을 사용하지 않습니다.

- 네트워크 및 Marinara API 호출
- localStorage, sessionStorage, IndexedDB, cookie 접근
- 채팅·캐릭터·페르소나·에이전트 데이터 쓰기
- 클릭, 폼 입력 또는 설정 변경

한국어(`ko`) UI에서만 검수된 영어 문자열을 정확히 일치시켜 화면에 치환합니다. 언어를 바꾸거나 확장을 비활성화하면 확장이 쓴 값만 원문으로 복원합니다.

## 설치

1. Marinara의 `Settings → Advanced → Danger Zone`에서 외부 확장 가져오기를 허용합니다.
2. 아래 방법 중 하나로 확장을 가져옵니다. 확장은 비활성 draft로 들어옵니다.
3. `manifest.json`과 `extension.js`를 검토합니다.
4. 요청 권한이 `full_page_access` 하나뿐인지 확인하고 경고를 승인한 뒤 활성화합니다.
5. UI 언어를 한국어로 설정하고 에이전트 탭·라이브러리·채팅 설정 → 에이전트를 확인합니다.

제거할 때는 확장을 비활성화한 뒤 페이지를 새로고침하고 확장 기록을 삭제합니다.

### GitHub로 설치

Marinara 2.5.2의 `Settings → Addons → External Extensions`에는 GitHub 가져오기 항목이 없습니다. 위의 외부 확장 허용 설정을 마친 뒤 아래 도우미 확장 중 하나를 설치하고 활성화하세요.

- [**ME.Fetchy**](https://github.com/FigCake/ME.Fetchy): 도우미 확장의 입력란에 다음을 입력합니다.

  ```text
  mallang0723/ME-MarinaraAgentsKo
  ```

- [**GitHub 확장 관리자**](https://github.com/f-en-rep/Marinara-GitHub-Manager): 저장소 기본 주소만 입력합니다(`/tree/main/...` 경로는 붙이지 않습니다).

  ```text
  https://github.com/mallang0723/ME-MarinaraAgentsKo
  ```

  이어서 "설치 대상 선택"에서 `manifest.json` 항목을 고릅니다.

### 직접 가져오기

설치 도우미 없이 설치하려면 현재 소스로 ZIP을 만들어 `Settings → Addons → External Extensions`에서 가져옵니다. ZIP 루트에 `manifest.json`과 `extension.js`가 함께 들어갑니다. 폴더로 가져오려면 `Import Extension Folder`로 저장소 루트의 `manifest.json`과 `extension.js`가 있는 폴더를 선택해도 됩니다.

```bash
zip marinara-agents-ko.zip manifest.json extension.js
```

## 개발 검증

```bash
python tools/build.py
node --check extension.js
node --check test/browser-test.cjs
node --check test/dom-test.cjs
python test/catalog-test.py
# 공식 자료는 읽기 전용으로 사용합니다. 외부 네트워크 호출은 없습니다.
OFFICIAL_CATALOG=/tmp/marinara-agents-ko-252/catalog.json \
  OFFICIAL_PACKAGES=/home/syhekate/dev/marinara-agents-ko-contrib \
  OFFICIAL_KO=/home/syhekate/dev/marinara/ko-ui-pack-8/ui/ko.json \
  MARINARA_REPO=/home/syhekate/dev/marinara-engine-ref python test/catalog-test.py
# 선택: 추출된 per-Agent JSON까지 비교하려면 OFFICIAL_AGENTS를 지정합니다.
# LinkeDOM이 이미 설치된 디렉터리. 렌더링 없는 DOM/MutationObserver 회귀 검사입니다.
TEST_DEPS=/path/to/dependency-installation node test/dom-test.cjs
# @playwright/test가 이미 설치된 디렉터리. 파일 URL만 사용하며 네트워크를 차단합니다.
MARINARA_REPO=/path/to/dependency-installation node test/browser-test.cjs
```

`data/catalog-reviewed.tsv`, `data/ui-translations.json`, `data/surfaces.json`이 편집 원본입니다. `tools/build.py`는 검수표와 선택자 목록에서 `data/exact-translations.json`과 `extension.js`를 생성합니다. 생성 파일은 직접 편집하지 마세요.

표에는 패키지 44행, per-Agent 44행, 활성 메뉴 표시문 12행이 있습니다. Python 검사는 SHA-256으로 고정된 공식 패키지 파일과 실제 Engine 표시 함수를 비교하고 빌드 재현성을 검사합니다. 브라우저와 DOM 검사는 32개 등록 선택자, 123개 정확 일치 문자열, 속성, 포털 삽입, 검색 강조, 편집 영역 제외, 언어 전환, cleanup 복원과 감시 비용을 검증합니다. Chromium 경로는 `CHROMIUM_PATH`로 지정합니다(기본 `/usr/bin/chromium`).

0.3.0 검증: Python 15개 통과, 오프라인 DOM 회귀 통과, JS 구문 검사 통과. Playwright는 실행했으나 Chromium이 샌드박스 소켓 권한 오류로 시작하지 못했습니다. 실제 페인트·모바일 화면 검증은 미완료이며, 재현 명령과 한계는 [대조 보고서](docs/compatibility-2.5.2.md)에 기록했습니다.

## 한계와 제거 기준

이 확장은 정식 데이터 계층 현지화가 아니라 DOM 표시용 임시 어댑터입니다. upstream에서 에이전트 이름·설명 localization, 카탈로그·에이전트 탭 locale 적용, 한국어 검색까지 지원하면 이 확장을 제거합니다.

## 라이선스와 고지

- 확장 코드와 번역 배포물: GNU Affero General Public License v3.0 (`AGPL-3.0`)
- upstream: <https://github.com/Pasta-Devs/Marinara-Engine>
- 자세한 내용은 `LICENSE`와 `THIRD_PARTY_NOTICES.md`를 확인하세요.
- `LICENSE`는 법률 문서의 정확성을 위해 AGPL-3.0 영어 원문을 그대로 제공합니다.

## 리비전 이력

| 날짜 | 변경 |
|------|------|
| 2026-11-07 | 설치 안내: 릴리스 ZIP 제거, GitHub 설치 도우미 안내 추가 |
| 2026-11-07 | v0.3.0: 채팅 에이전트 표면·per-Agent 설명·Omnibar·홈 대응 |
| 2026-11-06 | v0.2.0: Engine 2.5.2·공식 패키지 44개 대응 |
| 2026-08-28 | v0.1.0 배포 후보 작성 (펌킨) |
| 2026-08-28 | 공개 배포 고지·호환 범위 추가 (펌킨) |
