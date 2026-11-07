# Marinara Engine 2.5.2 — 확장 0.3.0 대조 보고서

2026-11-07, 빠게뜨의 모바일 **채팅 설정 → 에이전트** 영어 표시 요청을 반영했습니다. `~/dev/marinara-engine-ref`와 공식 자료는 읽기 전용으로 확인했습니다.

- Engine `v2.5.2`: `fc0333c3fe978cda5e0b919bd6faec985901704e`.
- 공식 카탈로그 44개: `/tmp/marinara-agents-ko-252/catalog.json`, Git blob `e95b068e50c238e27d2588818a46db3867fa290f`.
- 공식 UI 팩: `~/dev/marinara/ko-ui-pack-8/ui/ko.json`, Git blob `00cf7ee86f8b119ce1af09d9da6dc70da4142029`.
- 공식 패키지 원본: `~/dev/marinara-agents-ko-contrib/packages/*/agents.json`. 카탈로그에 명시된 SHA-256을 전부 비교했습니다. 원본이 이후 버전이면 카탈로그가 지정하는 `artifacts/*.zip`의 SHA-256과 ZIP 안 `agents.json` SHA-256을 모두 확인하는 테스트도 포함합니다. 새로운 패키지 3개 등 고정 카탈로그 밖 항목은 포함하지 않습니다.

## 번역표

`data/catalog-reviewed.tsv`는 패키지 44행, `agent:<package>:<agent>` 44행, `active:<package>:<agent>` 12행으로 총 **100행**입니다. 이름·설명은 **123개 고유 정확 일치 문자열**, Organizer 첫 문장/90 UTF-16 단위 축약은 별도 **44개**입니다. 44개 per-Agent 중 **23개 설명**이 패키지 설명과 다릅니다. 모든 per-Agent 행에 원본 경로와 파일 SHA-256을 기록했습니다. 패키지와 같은 설명도 독립 행으로 보존해 누락 여부를 검사합니다.

활성 메뉴는 [ChatSettingsDrawer.tsx:509](https://github.com/Pasta-Devs/Marinara-Engine/blob/v2.5.2/packages/client/src/components/chat/ChatSettingsDrawer.tsx#L509)의 세 설치 안내 표식을 기준으로 설명을 자릅니다(515–520 함수). 이 정확한 표시문까지 검수표로 수록했습니다. `Character Tracker`, `Custom Tracker`, `World State`의 이름, 전체 설명, 설치 안내를 제거한 설명을 모두 지원합니다. 설치 경로의 분류명도 `작성 에이전트`, `추적 에이전트`, `기타 에이전트`로 통일했습니다.

## 채팅 설정의 하드코딩 예외

[ChatSettingsDrawer.tsx:9772](https://github.com/Pasta-Devs/Marinara-Engine/blob/v2.5.2/packages/client/src/components/chat/ChatSettingsDrawer.tsx#L9772)의 배열에는 **writer / tracker / misc 세 항목만** 있습니다. 이 배열의 값은 `localizeUi`를 거치지 않습니다. 제목은 9777·9784·9791, 설명은 9780·9787·9794에 있습니다. 실제 렌더링은 [AgentSettingsControls.tsx:66](https://github.com/Pasta-Devs/Marinara-Engine/blob/v2.5.2/packages/client/src/components/chat/AgentSettingsControls.tsx#L66) 및 84행입니다.

`data/ui-translations.json`의 6개 항목은 `data-drawer`, `data-chat-settings-section`, `data-chat-control-window`의 `-agents` 범위에서만 적용합니다. 동일한 영어 분류명이 카탈로그의 실제 의미 키로 렌더링될 때에는 확장이 번역하지 않습니다.

| 영어 | 한국어 / 근거 |
|---|---|
| Writer Agents | 작성 에이전트 — `ui.agents.agentcatalogview.writerAgents` |
| Tracker Agents | 추적 에이전트 — `ui.panels.agentspanel.trackerAgents` |
| Misc Agents | 기타 에이전트 — `ui.panels.agentspanel.miscAgents` |
| Improve prose quality, maintain continuity, and shape the narrative direction of your roleplay. | 문장의 완성도를 높이고, 이야기의 일관성을 유지하며, 롤플레이의 서사 방향을 잡습니다. |
| Automatically track world state, character stats, quests, expressions, and other data that changes over time. | 세계 상태, 캐릭터 스탯, 퀘스트, 표정 등 시간에 따라 변하는 데이터를 자동으로 추적합니다. |
| Specialized utilities — image generation, combat systems, music, summaries, and other extras. | 이미지 생성, 전투 시스템, 음악, 요약 등 다양한 부가 기능을 제공합니다. |

## 표시 위치와 선택자

아래 경로는 모두 `packages/client/src/components/` 기준입니다. 실제 등록값은 `data/surfaces.json`이며, 각 선택자의 DOM fixture가 `test/surface-fixtures.json`에 있습니다. 일반 채팅 이력 전체나 Home 피드 전체를 번역 루트로 삼지 않습니다. `Modal`은 추가 미리보기·에이전트 모음·게임 선택·카드 업데이트 검토·검수된 패키지 제목에 해당하는 영어/한국어 `aria-label`만 허용합니다. 제목을 식별하는 데 쓰는 UI 팩 문구 자체는 치환하지 않습니다.

| 선택자 | 소스 근거와 표시값 |
|---|---|
| `[data-component="AgentCatalogView"]` | [AgentCatalogView.tsx:642](https://github.com/Pasta-Devs/Marinara-Engine/blob/v2.5.2/packages/client/src/components/agents/AgentCatalogView.tsx#L642). OrganizerParts.tsx:204 이름·205 축약 설명, AgentPage.tsx:121·122·257 이름·축약·전체 설명. |
| `[data-component="FeatureAgentDetailHost"]` | [FeatureAgentDetailHost.tsx:141](https://github.com/Pasta-Devs/Marinara-Engine/blob/v2.5.2/packages/client/src/components/agents/FeatureAgentDetailHost.tsx#L141). 162 다른 분기, 67 이름·171 설명. |
| `[data-component="RightPanel"] [data-panel-key="agents"]:not([aria-hidden="true"])` | [RightPanel.tsx:229](https://github.com/Pasta-Devs/Marinara-Engine/blob/v2.5.2/packages/client/src/components/layout/RightPanel.tsx#L229). 169 루트·237 aria-hidden; AgentsPanel.tsx:1281·1787·1858 이름/설명. |
| `[data-drawer$="-agents"]` | [Drawer.tsx:285](https://github.com/Pasta-Devs/Marinara-Engine/blob/v2.5.2/packages/client/src/components/ui/Drawer.tsx#L285). ChatSettingsDrawer.tsx:7957의 `${chatMode}-agents`; 분리된 drawer도 Drawer.tsx:498에서 동일 속성. |
| `[data-chat-settings-section$="-agents"]` | [ChatControlWindow.tsx:198](https://github.com/Pasta-Devs/Marinara-Engine/blob/v2.5.2/packages/client/src/components/chat/ChatControlWindow.tsx#L198). 도킹된 채팅 에이전트 섹션. |
| `[data-chat-control-window$="-agents"]` | [ChatControlWindow.tsx:248](https://github.com/Pasta-Devs/Marinara-Engine/blob/v2.5.2/packages/client/src/components/chat/ChatControlWindow.tsx#L248). 분리된 채팅 에이전트 창. |
| `[data-chat-agent-entry]` | [ChatSettingsDrawer.tsx:9833](https://github.com/Pasta-Devs/Marinara-Engine/blob/v2.5.2/packages/client/src/components/chat/ChatSettingsDrawer.tsx#L9833). 9537·9567·9606·9625 활성 카드; 9843 이름·9859 설명. |
| `[id^="chat-settings-agent-menu-"]` | [ChatSettingsDrawer.tsx:505](https://github.com/Pasta-Devs/Marinara-Engine/blob/v2.5.2/packages/client/src/components/chat/ChatSettingsDrawer.tsx#L505). getAgentSettingsMenuId, 3667·9540·9570·9609·9659·9684 제목. |
| `[data-agent-menus]` | [ChatSettingsDrawer.tsx:8072](https://github.com/Pasta-Devs/Marinara-Engine/blob/v2.5.2/packages/client/src/components/chat/ChatSettingsDrawer.tsx#L8072). 활성 에이전트 메뉴 링크. |
| `[data-trackers-control]` | [ChatSettingsDrawer.tsx:8101](https://github.com/Pasta-Devs/Marinara-Engine/blob/v2.5.2/packages/client/src/components/chat/ChatSettingsDrawer.tsx#L8101). 8151 에이전트 이름 배지. |
| `[data-component="ChatSetupWizard"]` | [ChatSetupWizard.tsx:524](https://github.com/Pasta-Devs/Marinara-Engine/blob/v2.5.2/packages/client/src/components/chat/ChatSetupWizard.tsx#L524). 3336·3344 추가 미리보기, 3517·3519 선택 카드. |
| `[data-component="Modal"]` | [Modal.tsx:218](https://github.com/Pasta-Devs/Marinara-Engine/blob/v2.5.2/packages/client/src/components/ui/Modal.tsx#L218). 216 aria-label 허용 목록으로 제한. ChatSettingsDrawer.tsx:10395·10418·10426 추가 미리보기, AgentSuiteModal.tsx:892·914·931·947·948 모바일 select/데스크톱 rail/설명, ConversationGamesPicker.tsx:30·52·64 게임 선택, CharacterCardUpdateModal.tsx:258·274 제안자 이름. |
| `[data-command-center-result-row][data-result-id^="agent:"]` | [CommandCenterResultRow.tsx:122](https://github.com/Pasta-Devs/Marinara-Engine/blob/v2.5.2/packages/client/src/components/command-center/CommandCenterResultRow.tsx#L122). 123 행 표식. use-omnibar-entity-rows.ts:197 → lib/omnibar-entity-rows.ts:427–437 에이전트 메타데이터, lib/omnibar-search.ts:736 agent: ID. OmnibarResultList.tsx:178–186 전달. |
| `[data-command-center-result-row][data-result-id^="home-tab:"]` | [use-omnibar-entity-rows.ts:60](https://github.com/Pasta-Devs/Marinara-Engine/blob/v2.5.2/packages/client/src/components/layout/omnibar/use-omnibar-entity-rows.ts#L60). 65 home-tab: ID·66 제목. CommandCenterResultRow.tsx:122 행 표식. |
| `[data-component="HomeBrowserHub"] .mari-home-discovery-card` | [HomeBrowserHub.tsx:2618](https://github.com/Pasta-Devs/Marinara-Engine/blob/v2.5.2/packages/client/src/components/chat/HomeBrowserHub.tsx#L2618). 2634 이름·2638 설명, 1739 HomeBrowserHub 루트. |
| `[data-component="HomeBrowserHub.TabList"]` | [HomeBrowserHub.tsx:1809](https://github.com/Pasta-Devs/Marinara-Engine/blob/v2.5.2/packages/client/src/components/chat/HomeBrowserHub.tsx#L1809). 1880 aria-label·1895 탭 이름. |
| `[data-component="HomeBrowserHub.TabMenu"]` | [HomeBrowserHub.tsx:1958](https://github.com/Pasta-Devs/Marinara-Engine/blob/v2.5.2/packages/client/src/components/chat/HomeBrowserHub.tsx#L1958). 1993 접힌 탭 메뉴 이름. |
| `[data-component="HomeBrowserHub.MobileBookmarksMenu"]` | [HomeBrowserHub.tsx:2156](https://github.com/Pasta-Devs/Marinara-Engine/blob/v2.5.2/packages/client/src/components/chat/HomeBrowserHub.tsx#L2156). 모바일 북마크 메뉴. |
| `[data-component="HomeBrowserHub.WidgetManager"]` | [HomeBrowserHub.tsx:2961](https://github.com/Pasta-Devs/Marinara-Engine/blob/v2.5.2/packages/client/src/components/chat/HomeBrowserHub.tsx#L2961). 위젯 관리 목록의 ownerName/이름. |
| `[data-home-widget-id^="agent:"] header` | [HomeBrowserHub.tsx:587](https://github.com/Pasta-Devs/Marinara-Engine/blob/v2.5.2/packages/client/src/components/chat/HomeBrowserHub.tsx#L587). agent: 위젯 범위; 856 header·866 eyebrow·868 제목·871 설명. 패키지 내부 Shadow DOM은 미접근. |
| `[data-agent-activity]` | [AgentTaskStatus.tsx:49](https://github.com/Pasta-Devs/Marinara-Engine/blob/v2.5.2/packages/client/src/components/agents/AgentTaskStatus.tsx#L49). 87 진행 상태의 에이전트 이름. |
| `[data-window] .mari-window__title` | [FloatingWindow.tsx:847](https://github.com/Pasta-Devs/Marinara-Engine/blob/v2.5.2/packages/client/src/components/ui/FloatingWindow.tsx#L847). 877 .mari-window__title; ConversationView.tsx:355, RoleplayTrackerWindow.tsx:163, ChatRoleplaySurface.tsx:2376 패키지 창 제목. |
| `[data-drawer^="tracker-"] .mari-drawer__title` | [RoleplayTrackerWindow.tsx:265](https://github.com/Pasta-Devs/Marinara-Engine/blob/v2.5.2/packages/client/src/components/chat/RoleplayTrackerWindow.tsx#L265). tracker-${item.id}·266 패키지 이름 → Drawer.tsx:285·312 제목. |
| `[aria-labelledby$="-agent"]` | [ChatProfileBuilder.tsx:471](https://github.com/Pasta-Devs/Marinara-Engine/blob/v2.5.2/packages/client/src/components/chat/ChatProfileBuilder.tsx#L471). 496 option 이름; 240 공식 에이전트 이름 수집. |
| `[data-drawer$="-gallery"] [role="menu"]` | [Drawer.tsx:285](https://github.com/Pasta-Devs/Marinara-Engine/blob/v2.5.2/packages/client/src/components/ui/Drawer.tsx#L285). ChatSettingsDrawer.tsx:7923 gallery 섹션 → ChatGallery.tsx:655 menu·675 에이전트 이름. |
| `[data-chat-control-window$="-gallery"] [role="menu"]` | [ChatControlWindow.tsx:248](https://github.com/Pasta-Devs/Marinara-Engine/blob/v2.5.2/packages/client/src/components/chat/ChatControlWindow.tsx#L248). 같은 갤러리를 분리 창에서 표시. |
| `.mari-list__item:has([data-result-type="agent"])` | [mari-primitives.tsx:197](https://github.com/Pasta-Devs/Marinara-Engine/blob/v2.5.2/packages/client/src/components/chat/mari-primitives.tsx#L197). CompactMariMessage.tsx:220·230 에이전트 이름/설명 → 295 MariRow, 307 title·309 hint. ResultTypeIcon.tsx:72 agent 표식으로 다른 리소스 제외. |
| `[data-chat-input-popup="commands"]` | [ChatInput.tsx:1859](https://github.com/Pasta-Devs/Marinara-Engine/blob/v2.5.2/packages/client/src/components/chat/ChatInput.tsx#L1859). 1885 명령 선택 설명. ConversationInput.tsx:2050 명령 팝업도 같은 표식. |
| `[data-component="GameSetupWizard"]` | [GameSetupWizard.tsx:1845](https://github.com/Pasta-Devs/Marinara-Engine/blob/v2.5.2/packages/client/src/components/game/GameSetupWizard.tsx#L1845). 1942 NewGameExperienceChooser → NewGameExperienceChooser.tsx:139·141 패키지 이름/설명. |
| `#game-experience-setup-title` | [LegacyExperienceSetupDialog.tsx:153](https://github.com/Pasta-Devs/Marinara-Engine/blob/v2.5.2/packages/client/src/components/game/LegacyExperienceSetupDialog.tsx#L153). 154 패키지 이름; 게임 설정 본문은 제외. |
| `.mari-editor-panel button:has(.lucide-sparkles)` | [PresetEditor.tsx:1689](https://github.com/Pasta-Devs/Marinara-Engine/blob/v2.5.2/packages/client/src/components/presets/PresetEditor.tsx#L1689). 1724 Sparkles 아이콘 버튼·1725 에이전트 이름 텍스트 노드. semantic .mari-editor-panel만 사용, Tailwind 위치 선택자 없음. |
| `[data-agent-output] button:is([title="Collapse output"], [title="Expand output"], [title="출력 접기"], [title="출력 펼치기"])` | [RoleplayHUDActionsMenu.tsx:172](https://github.com/Pasta-Devs/Marinara-Engine/blob/v2.5.2/packages/client/src/components/chat/RoleplayHUDActionsMenu.tsx#L172). data-agent-output; ContextInjectionPanel.tsx:228–231 제목으로 출력 접기/펼치기 버튼 식별·242 에이전트 이름. 출력 본문은 제외. |

`OrganizerHome.tsx:118`의 업데이트 이름/버전 묶음과 `156`의 키트 이름 목록은 구성 요소마다 검수된 이름과 정확히 일치할 때만 번역합니다. 미검수 이름이 하나라도 섞이면 전체를 유지합니다.

`OrganizerParts`와 `AgentPage`는 기존 `AgentCatalogView` 루트에 포함됩니다. Omnibar 상세는 행 안에 펼쳐지므로 해당 `agent:` 행 범위가 이름·설명과 상세를 함께 포함합니다. 검색 강조는 `CommandCenterResultRow.tsx:69–80`에서 텍스트/`mark` 노드로 나뉩니다. 전체 이름/설명이 정확히 일치할 때만 합쳐 번역하고, 노드와 이벤트 구조를 유지한 채 복원 정보를 기록합니다.

## UI 팩에 남기는 문구

다음은 `localization/locales/en.json`에 실제 키가 있고 렌더러가 이를 호출하는 UI입니다. 번역표에 UI 재정의로 추가하지 않습니다. 특히 0.2.0의 `Not installed` 보완은 삭제했으며 현재 지정된 공식 ko 팩에 해당 키가 있습니다.

| 영어 | 의미 키 |
|---|---|
| Attach lorebook for the specific agent | `chat.agentLorebook.attach` |
| Not installed | `ui.agents.organizer.notInstalledTitle` |
| Installed | `ui.agents.organizer.installedTitle` |
| Writer Agents | `ui.agents.agentcatalogview.writerAgents` |
| Tracker Agents | `ui.agents.agentcatalogview.trackerAgents` |
| Misc Agents | `ui.agents.agentcatalogview.miscAgents` |
| Enable Agents | `ui.chat.chatsettingsdrawer.enableAgents` |
| No agents are active for this chat yet. Add one below to let it run here. | `ui.chat.chatsettingsdrawer.noAgentsAreActiveForThisChatYetAdd` |
| Add {{value1}} | `ui.chat.chatsettingsdrawer.addValue1` |
| Remove {{value1}}? | `ui.chat.chatsettingsdrawer.removeValue1` |
| Agent Suite | `ui.chat.agentsuitemodal.agentSuite` |
| Start a game | `ui.chat.conversationgamespicker.startAGame` |
| Choose an image agent | `ui.chat.chatgallery.chooseImageAgent` |
| Collapse {{value1}} | `ui.chat.agentsettingscard.collapseValue1` |
| Expand {{value1}} | `ui.chat.agentsettingscard.expandValue1` |
| Open {{name}} | `ui.agents.organizer.openName` |
| More for {{name}} | `ui.agents.organizer.moreFor` |
| {{value1}} artwork | `ui.agents.agentcatalogview.value1Artwork` |
| Back to {{name}} | `ui.chat.scenebanner.backToPackage` |
| Return to where this scene started in {{name}} | `ui.chat.scenebanner.returnToPackage` |

`chat.agentLorebook.attach`는 ChatSettingsDrawer의 로어북 연결 UI가 담당합니다. `Add {{value1}}`, `Open {{name}}`, 아트워크 대체 텍스트, SceneBanner의 패키지 복귀 문구처럼 UI 키 안에 이름이 보간된 **완성 문장**은 부분 치환하지 않습니다. 순수 이름/설명 텍스트 노드와 정확히 일치하는 속성만 바꿉니다. 따라서 패키지 이름이 매개변수로 들어간 UI 문장·토스트·확인 대화상자까지 모두 한국어가 된다고 보장하지 않습니다.

`Background`, `Illustrator`, `Combat`, `World State` 등은 실제 패키지 이름이면서 UI 팩의 일부 라벨과도 같은 영어입니다. 이름 번역은 메타데이터 표시 영역의 정확 일치용입니다. 사전 밖 텍스트, 이미 한국어인 값, 입력값, textarea, contenteditable(plaintext-only 포함), script/style, `.prose`는 제외합니다. DOM에는 공식 패키지 ID가 항상 제공되지 않으므로, 지원 영역 안에서 공식 이름/설명과 **완전히 같은 사용자 지정 문자열**은 구별할 수 없습니다. 일반 채팅 내용과 다른 Omnibar 리소스 행은 범위 밖입니다.

## 감시·복원과 검증

- 시작/언어 변경 때만 등록 루트를 검색합니다. 일반 mutation은 추가된 하위 트리·변경된 텍스트/속성만 처리하며 포함 관계로 중복 작업을 제거합니다. 전체 document를 매번 재검색하지 않습니다.
- `MutationObserver` 콜백에서 동기 치환하고 자체 쓰기 기록을 비웁니다. RAF 지연, 숨김 CSS, 반복 타이머가 없습니다. 별도 렌더 프레임을 기다리는 번역 깜빡임을 만들지 않습니다. 실제 페인트 동작은 아래 브라우저 검증 제한을 참고하세요.
- 변경한 노드의 조상은 WeakSet으로 추적합니다. 관련 노드가 제거되거나 범위가 바뀔 때만 복원 장부를 정리합니다. 일반 채팅 스트리밍의 제거 mutation 때문에 장부 전체를 훑지 않습니다.
- `en` 전환/비활성화/분리된 노드 재사용 시 원문을 복원합니다. 앱이 이후에 쓴 공식 번역이나 속성값은 보존합니다. cleanup은 중복 호출해도 안전합니다.
- `python tools/build.py`: 44 packages / 100 rows / 123 exact / 44 summaries / 6 section strings. 생성 파일 재현성 검사 포함.
- Python **15개 통과**: 고정 카탈로그, 공식 패키지 파일 SHA-256, per-Agent 전체 수록, 실제 Engine 축약 함수, 하드코딩 배열, UI 키 경계, 빌드 오류/재현성.
- LinkeDOM 오프라인 회귀: **32,278 assertions 통과**, **32개 선택자 × 123개 문자열**, 속성·분류 범위·동적 포털·검색 강조·영어 전환·비활성화·앱 수정 보존·분리 노드 복원·무관한 200개 mutation 비용 검사. `characterData` 이벤트와 실제 페인트는 LinkeDOM의 검증 범위가 아니므로 별도 Playwright 검사에 둡니다.
- Playwright fixture 실행은 **Chromium 시작 단계에서 차단**: `/usr/bin/chromium`은 `setsockopt: Operation not permitted`; 캐시된 headless shell도 `sandbox_host_linux.cc ... shutdown: Operation not permitted`. 실제 모바일 앱/브라우저 시각 검증은 미완료입니다. 브라우저 테스트에는 첫 RAF 전 치환, `characterData`, 강조 노드, 모든 등록 표면과 복원 검사를 추가했습니다.

앱 서버·금지 포트는 사용하지 않았습니다. 외부 다운로드 없이 기존 npm 캐시를 `/tmp`로 복사해 LinkeDOM만 오프라인 설치했습니다. 참조 저장소·UI 팩·패키지 원본은 수정하지 않았고, 커밋·푸시도 하지 않았습니다.
