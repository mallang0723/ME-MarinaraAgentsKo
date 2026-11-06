# Marinara 에이전트 라이브러리 임시 한글화

Marinara Engine의 정식 에이전트 메타데이터 현지화가 완료되기 전까지 사용하는 임시 Personal Extension입니다.

이 프로젝트는 Marinara Engine 공식 프로젝트가 아닌 커뮤니티 배포 확장입니다. 공식 영문 카탈로그를 기준으로 한국어 번역을 유지하며, 확장 소스 전체를 배포 ZIP에 포함합니다.

## 호환 범위

- 기준 앱: Marinara Engine `2.5.2` (`v2.5.2`)
- 기준 카탈로그: 2026-11-06에 확인한 `Pasta-Devs/Marinara-Agents` `main`의 공식 패키지 44개
- 적용 언어: Marinara UI 언어가 한국어(`ko`, `ko-*`)인 경우

Marinara 업데이트로 에이전트 이름·설명 또는 화면 구조가 바뀌면 일부 항목이 영어로 남을 수 있습니다. 이 경우 사용자 데이터에는 영향을 주지 않으며, 검수된 번역표 업데이트가 필요합니다.

## 번역 범위

- 에이전트 탭에 표시되는 공식 에이전트 이름과 설명
- 에이전트 라이브러리(공식 카탈로그)의 에이전트 이름과 설명
- Agent Organizer 목록의 축약 설명과 상세 페이지의 전체 설명
- 공식 한국어 팩에 빠진 `Not installed` 목록 제목(카탈로그 안에서만 적용)
- 공식 패키지 44개 (`slurp` 대신 `slurp2`, 표시명은 `Slurp`)

모드 필터·분류·설치 목록 등의 UI 라벨은 공식 한국어 팩에 맡깁니다. 이미 한국어로 표시된 패키지 설명도 덮어쓰지 않습니다. [2.5.2 소스 및 공식 번역 대조 기록](docs/compatibility-2.5.2.md)을 참고하세요.

사용자 작성 에이전트·폴더명·채팅 내용은 번역하지 않습니다. 새 패키지 또는 영문 설명이 변경된 패키지는 검수된 번역표에 추가되기 전까지 영어로 남습니다.

## 권한과 안전 경계

기존 Marinara 화면의 DOM을 바꾸기 위해 `full_page_access`가 필요합니다. 이 권한은 브라우저 개발자 콘솔 수준의 페이지 접근 권한이므로 설치 화면에서 소스와 hash를 확인하세요.

이 버전은 다음 기능을 사용하지 않습니다.

- 네트워크 및 Marinara API 호출
- localStorage, sessionStorage, IndexedDB, cookie 접근
- 채팅·캐릭터·페르소나·에이전트 데이터 쓰기
- 클릭, 폼 입력 또는 설정 변경

한국어(`ko`) UI에서만 검수된 영어 문자열을 정확히 일치시켜 화면에 치환합니다. 언어를 바꾸거나 확장을 비활성화하면 확장이 쓴 값만 원문으로 복원합니다.

## 설치

1. 배포 ZIP을 내려받습니다.
2. Marinara의 `Settings → Advanced → Danger Zone`에서 외부 확장 가져오기를 허용합니다.
3. `Settings → Addons → External Extensions`에서 ZIP을 가져옵니다.
4. 확장은 비활성 draft로 들어옵니다. `manifest.json`과 `extension.js`를 검토합니다.
5. 요청 권한이 `full_page_access` 하나뿐인지 확인하고 경고를 승인한 뒤 활성화합니다.
6. UI 언어를 한국어로 설정하고 에이전트 탭과 에이전트 라이브러리를 확인합니다.

제거할 때는 확장을 비활성화한 뒤 페이지를 새로고침하고 확장 기록을 삭제합니다.

## 배포 파일 검증

릴리스에 함께 적힌 SHA-256과 내려받은 ZIP의 checksum을 비교하세요.

```bash
sha256sum marinara-agents-ko-temporary-v0.2.0.zip
```

## 개발 검증

```bash
python tools/build.py
node --check extension.js
node --check test/browser-test.cjs
python test/catalog-test.py
# 이미 내려받은 공식 JSON과 읽기 전용 2.5.2 소스를 지정하면 12개 검사를 모두 실행합니다.
OFFICIAL_CATALOG=/tmp/catalog.json OFFICIAL_KO=/tmp/ko.json \
  MARINARA_REPO=/path/to/marinara-engine-ref python test/catalog-test.py
# @playwright/test가 이미 설치된 의존성 경로를 명시합니다. 앱 서버는 실행하지 않습니다.
MARINARA_REPO=/path/to/dependency-installation node test/browser-test.cjs
```

`data/catalog-reviewed.tsv`와 `data/ui-translations.json`이 편집 원본입니다. `tools/build.py`는 검수표에서 `data/exact-translations.json`과 `extension.js`를 함께 생성합니다. 생성 파일을 직접 편집하지 마세요.

Python 검사는 표준 라이브러리만 사용합니다. 기본 실행은 8개 통과·외부 입력이 필요한 4개 건너뜀이고, 위 환경 변수를 모두 지정하면 공식 카탈로그·한국어 팩·소스 계약을 포함한 12개 검사를 실행합니다. 테스트는 외부 네트워크를 호출하지 않습니다.

브라우저 fixture는 파일 URL만 열고 네트워크를 차단합니다. 44개 패키지를 카탈로그·에이전트 패널·상세 호스트에 표시해 132개 이름·설명 쌍과 목록 축약 설명 44개를 검증합니다. 공식 UI 번역 보존, 숨겨진 패널 활성화, SPA 재렌더링, 언어 전환, cleanup 복원도 검사합니다. Chromium 경로는 `CHROMIUM_PATH`로 지정할 수 있습니다(기본 `/usr/bin/chromium`).

이번 환경에서는 Python 검사 12개와 JS 구문 검사 2개가 통과했습니다. 브라우저 검사는 참조 저장소의 Playwright 의존성 부재로 실행하지 못했고, 별도 Chromium 시작 확인도 샌드박스 소켓 권한 오류로 실패했습니다. 실제 화면 검증은 찹쌀의 QA가 필요합니다.

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
| 2026-11-06 | v0.2.0: Engine 2.5.2·공식 패키지 44개 대응 |
| 2026-08-28 | v0.1.0 배포 후보 작성 (펌킨) |
| 2026-08-28 | 공개 배포 고지·호환 범위 추가 (펌킨) |
