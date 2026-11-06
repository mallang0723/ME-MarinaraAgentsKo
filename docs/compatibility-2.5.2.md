# Marinara Engine 2.5.2 대조 기록

2026-11-06, 확장 `0.2.0` 기준입니다. 참조 저장소 `~/dev/marinara-engine-ref`는 읽기 전용으로 확인했습니다.

- Engine 태그: `v2.5.2`, 커밋 `fc0333c3fe978cda5e0b919bd6faec985901704e`
- [공식 카탈로그](https://github.com/Pasta-Devs/Marinara-Agents/blob/main/catalog/v2/catalog.json): Git blob `e95b068e50c238e27d2588818a46db3867fa290f`, 44개
- [공식 한국어 UI 팩](https://github.com/Pasta-Devs/Marinara-Engine/blob/docs-i18n/ui/ko.json): Git blob `bc00e00f7ad4714c4dfdbb5eefb1036244a1c9ec`

요청된 `gh` 읽기 명령은 실행 환경에서 계정 토큰을 찾지 못하고 GitHub 연결에도 실패했습니다. 대신 GitHub 연결의 읽기 전용 파일·blob 조회를 사용했습니다. 내려받은 두 JSON의 `git hash-object` 결과가 위 blob ID와 일치합니다. 원본 스냅샷은 `/tmp/marinara-agents-ko-252/`에만 저장했고 테스트에서는 네트워크를 호출하지 않았습니다.

## 카탈로그 변경

설명 변경 23개: `beholder`, `card-evolution-auditor`, `character-tracker`, `continuity`, `custom-tracker`, `cyoa`, `expression`, `haptic`, `html`, `inventory-tracker`, `knowledge-retrieval`, `knowledge-router`, `long-term-memory`, `lorebook-keeper`, `memory-nag`, `spotify`, `director`, `noodle`, `persona-stats`, `prose-guardian`, `quest`, `storyboard`, `hierarchical-maps`.

신규 8개: `2d-avatars`(2D 아바타), `3d-avatars`(3D 아바타), `otome-forge`(Otome Hearth), `quartermaster`(병참관), `relationship-tracker`(관계 추적기), `saucelings`(Saucelings), `slurp2`(Slurp), `story-writer`(Story Writer). 이전 `slurp` 행과 설명은 삭제했습니다. 기존 패키지 이름과 변경되지 않은 13개 설명은 유지했습니다.

[organizer-model.ts:50](https://github.com/Pasta-Devs/Marinara-Engine/blob/v2.5.2/packages/client/src/components/agents/organizer/organizer-model.ts#L50)의 `taglineOf`는 별도 store tagline이 없으면 설명의 첫 문장을 골라 90 UTF-16 코드 단위를 넘을 때 89 단위와 `…`로 줄입니다. 관측한 44개 패키지에는 store 항목이 없습니다. 빌드는 이 정확한 영어 표시문과 검수된 한국어 설명의 동일 방식 축약문을 카탈로그 전용 사전에 생성합니다. 전체 설명은 기존 메타데이터 사전으로 번역합니다. [OrganizerParts.tsx:205](https://github.com/Pasta-Devs/Marinara-Engine/blob/v2.5.2/packages/client/src/components/agents/organizer/OrganizerParts.tsx#L205)는 축약 설명을, [AgentPage.tsx:257](https://github.com/Pasta-Devs/Marinara-Engine/blob/v2.5.2/packages/client/src/components/agents/organizer/AgentPage.tsx#L257)는 전체 설명을 표시합니다.

`Noodle`의 공식 ko 매니페스트 설명은 이전 영문 기준이고 `Slurp`의 공식 ko 설명은 설치 안내가 빠져 있습니다. 영어 fallback은 새 영어에 맞게 번역하되, [capability-package-localization.ts:27](https://github.com/Pasta-Devs/Marinara-Engine/blob/v2.5.2/packages/client/src/lib/capability-package-localization.ts#L27)에서 이미 선택한 공식 한국어 문구는 덮어쓰지 않습니다.

## UI 라벨 소유권

기존 UI 전용 키 14개를 제거했습니다. `Calls`는 별도의 UI 전용 키가 아니라 공식 패키지 이름이므로 `통화` 번역을 유지합니다.

공식 팩이 번역하는 11개는 다음과 같습니다. 줄 번호는 위 ko blob 기준입니다.

| 기존 영어 | 공식 의미 키 | 공식 한국어 | ko.json 줄 |
|---|---|---|---|
| All | ui.agents.agentcatalogview.allModes | 전체 | 6529 |
| Conversation | ui.agents.agentcatalogview.conversationMode | 대화 | 6538 |
| Roleplay | ui.agents.agentcatalogview.roleplayMode | 롤플레이 | 6569 |
| Game | ui.agents.agentcatalogview.gameMode | 게임 | 6545 |
| Filter agents by supported chat mode | ui.agents.agentcatalogview.filterByChatMode | 지원되는 채팅 모드로 에이전트 필터링 | 6544 |
| Writer Agents | ui.agents.agentcatalogview.writerAgents | 작성 에이전트 | 6594 |
| Tracker Agents | ui.agents.agentcatalogview.trackerAgents | 추적 에이전트 | 6576 |
| Misc Agents | ui.agents.agentcatalogview.miscAgents | 기타 에이전트 | 6557 |
| Agent | ui.agents.organizer.types.agent | 에이전트 | 7134 |
| Maps | ui.game.gamesessionhistory.maps | 지도 | 11640 |
| Agents | navigation.topbar.agents | 에이전트 | 5214 |

모드 필터는 [AgentModeFilter.tsx:7](https://github.com/Pasta-Devs/Marinara-Engine/blob/v2.5.2/packages/client/src/components/agents/AgentModeFilter.tsx#L7)과 [29행](https://github.com/Pasta-Devs/Marinara-Engine/blob/v2.5.2/packages/client/src/components/agents/AgentModeFilter.tsx#L29)에서 공식 의미 키를 사용합니다. `Maps`의 위 키는 게임 이력용이며, 카탈로그의 이전 maps 배지는 [agent-catalog-kind-badges.ts:5](https://github.com/Pasta-Devs/Marinara-Engine/blob/v2.5.2/packages/client/src/lib/agent-catalog-kind-badges.ts#L5)에서 turn-game 배지와 함께 숨깁니다.

나머지 3개는 2.5.2의 영어 UI 카탈로그와 해당 화면 소스에 더 이상 없습니다.

- `Installed Agents` → `Installed`: [AgentCatalogView.tsx:516](https://github.com/Pasta-Devs/Marinara-Engine/blob/v2.5.2/packages/client/src/components/agents/AgentCatalogView.tsx#L516)의 `ui.agents.organizer.installedTitle`, 공식 ko `설치된 항목`(7075행). 확장 번역을 삭제했습니다.
- `Uninstalled Agents` → `Not installed`: [AgentCatalogView.tsx:522](https://github.com/Pasta-Devs/Marinara-Engine/blob/v2.5.2/packages/client/src/components/agents/AgentCatalogView.tsx#L522), [OrganizerLists.tsx:194](https://github.com/Pasta-Devs/Marinara-Engine/blob/v2.5.2/packages/client/src/components/agents/organizer/OrganizerLists.tsx#L194)의 `ui.agents.organizer.notInstalledTitle`. 관측한 공식 ko 팩에는 이 키가 없습니다. 카탈로그에서만 `설치되지 않음`으로 보완하며, 공식 `ui.agents.organizer.statusNotInstalled`의 용어를 따릅니다. 공식 제목 번역이 추가되면 `data/ui-translations.json`의 이 항목도 제거합니다.
- `Conversation Game`: [organizer-model.ts:43](https://github.com/Pasta-Devs/Marinara-Engine/blob/v2.5.2/packages/client/src/components/agents/organizer/organizer-model.ts#L43)에서 turn-game 패키지는 `game` 유형으로 분류됩니다. 현재 게임 선반은 `ui.agents.organizer.sections.games.title`의 `Chat games` → 공식 ko `채팅 게임`(7098행)을 사용합니다. 이전 문구를 삭제했습니다.

## DOM 선택자 전수 대조

`tools/build.py` 템플릿의 모든 선택자를 아래에 기록했습니다. 앱 구조에 의존하는 선택자는 모두 2.5.2에 남아 있습니다. 일반 HTML 제외 선택자는 사용자 편집 영역 보호용이며 필수 화면 구조가 아닙니다.

| 선택자 | 2.5.2 근거 및 판단 |
|---|---|
| `[data-component="AgentCatalogView"]` | [AgentCatalogView.tsx:642](https://github.com/Pasta-Devs/Marinara-Engine/blob/v2.5.2/packages/client/src/components/agents/AgentCatalogView.tsx#L642). 카탈로그 루트 및 축약 설명·UI 보완 범위. |
| `[data-component="FeatureAgentDetailHost"]` | [FeatureAgentDetailHost.tsx:141](https://github.com/Pasta-Devs/Marinara-Engine/blob/v2.5.2/packages/client/src/components/agents/FeatureAgentDetailHost.tsx#L141), [162행](https://github.com/Pasta-Devs/Marinara-Engine/blob/v2.5.2/packages/client/src/components/agents/FeatureAgentDetailHost.tsx#L162). 두 상세 화면 분기 모두 존재. |
| `[data-component="RightPanel"]` | [RightPanel.tsx:169](https://github.com/Pasta-Devs/Marinara-Engine/blob/v2.5.2/packages/client/src/components/layout/RightPanel.tsx#L169). |
| `[data-panel-key="agents"]:not([aria-hidden="true"])` | [RightPanel.tsx:229](https://github.com/Pasta-Devs/Marinara-Engine/blob/v2.5.2/packages/client/src/components/layout/RightPanel.tsx#L229)의 `data-panel-key={key}`, [237행](https://github.com/Pasta-Devs/Marinara-Engine/blob/v2.5.2/packages/client/src/components/layout/RightPanel.tsx#L237)의 `aria-hidden={!active}`. `PANELS.agents`가 존재함을 오프라인 검사에서도 확인. `aria-hidden` 및 `data-panel-key` 변경을 관찰해 패널 활성화를 감지. |
| `[aria-label], [title], [placeholder]` | [AgentCatalogView.tsx:550](https://github.com/Pasta-Devs/Marinara-Engine/blob/v2.5.2/packages/client/src/components/agents/AgentCatalogView.tsx#L550), [551행](https://github.com/Pasta-Devs/Marinara-Engine/blob/v2.5.2/packages/client/src/components/agents/AgentCatalogView.tsx#L551), [650행](https://github.com/Pasta-Devs/Marinara-Engine/blob/v2.5.2/packages/client/src/components/agents/AgentCatalogView.tsx#L650). 속성은 패키지 메타데이터만 정확 일치로 치환. |
| `input, textarea` (제외) | [AgentCatalogView.tsx:545](https://github.com/Pasta-Devs/Marinara-Engine/blob/v2.5.2/packages/client/src/components/agents/AgentCatalogView.tsx#L545), [AgentEditor.tsx:3241](https://github.com/Pasta-Devs/Marinara-Engine/blob/v2.5.2/packages/client/src/components/agents/AgentEditor.tsx#L3241). 편집 텍스트를 건드리지 않는 보호 조건. |
| `script, style` (제외) | [index.html:17](https://github.com/Pasta-Devs/Marinara-Engine/blob/v2.5.2/packages/client/index.html#L17), [32행](https://github.com/Pasta-Devs/Marinara-Engine/blob/v2.5.2/packages/client/index.html#L32). 패키지 UI가 루트 아래에 삽입해도 코드·스타일 텍스트는 제외. |
| `[contenteditable="true"]` (제외) | 에이전트 화면의 정적 JSX에서 해당 편집 요소는 확인되지 않았습니다. 동적으로 삽입될 수 있는 편집 영역을 위한 방어 조건으로 유지합니다. Engine도 [ChatArea.tsx:357](https://github.com/Pasta-Devs/Marinara-Engine/blob/v2.5.2/packages/client/src/components/chat/ChatArea.tsx#L357)에서 같은 선택자를 사용합니다. |
| `h2` (삭제됨) | [RightPanel.tsx:189](https://github.com/Pasta-Devs/Marinara-Engine/blob/v2.5.2/packages/client/src/components/layout/RightPanel.tsx#L189)에 여전히 존재하지만 공식 패널 제목 번역을 존중하도록 확장의 헤더 탐색을 제거했습니다. |

언어 감지는 기존대로 `document.documentElement.lang`을 사용합니다. Engine은 [i18n.ts:53](https://github.com/Pasta-Devs/Marinara-Engine/blob/v2.5.2/packages/client/src/localization/i18n.ts#L53)에서 이를 갱신합니다.

## 검증과 찹쌀 QA

오프라인 Python 검사 **12개 통과**, `extension.js`와 `test/browser-test.cjs`의 JS 구문 검사 **2개 통과**, 빌드 재현성과 `git diff --check` 확인. Python 검사는 실제 2.5.2 `taglineOf` 함수 본문을 네트워크 없이 실행해 44개 축약 결과도 비교합니다.

브라우저 fixture는 실행을 시도했지만 참조 저장소에 `@playwright/test`가 없어 **미실행**입니다. 별도 headless Chromium 시작 확인도 `setsockopt: Operation not permitted`로 실패했습니다. 실제 브라우저 동작이 검증되었다고 간주하지 않습니다. QA 인스턴스는 실행·수정하지 않았고 커밋·푸시도 하지 않았습니다.

찹쌀은 QA 인스턴스에서 다음을 확인해 주세요.

1. 공식 한국어 팩과 확장 0.2.0을 함께 사용해 Organizer 목록·상세·설치된 에이전트 패널을 확인합니다. 23개 새 설명, 신규 8개 이름·설명, 축약 설명이 자연스럽게 표시되는지 확인합니다.
2. `Slurp`가 `slurp2` 기준으로 표시되는지, `Otome Hearth`, 병참관, Saucelings의 소원·소스 기질·Menagerie 용어가 실제 화면과 맞는지 확인합니다.
3. 공식 분류·모드·`설치된 항목` 번역이 유지되는지, 빠진 `Not installed` 제목만 보완되는지 확인합니다. Noodle·Slurp의 이미 한국어인 공식 문구는 변경되지 않아야 합니다.
4. 패널 전환·목록 재렌더링·`ko`/`ko-KR`/영어 전환·확장 비활성화를 확인합니다. 채팅·사용자 에이전트·편집 필드가 변하지 않는지도 확인합니다.
5. Playwright가 설치된 환경에서 README의 파일 기반 브라우저 검사를 실행합니다. 검증 대상은 132개 이름·설명 쌍과 축약 설명 44개입니다.
