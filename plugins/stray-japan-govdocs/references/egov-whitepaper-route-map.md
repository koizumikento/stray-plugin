# e-Gov Whitepaper Route Map

Checked on 2026-04-27 from the official e-Gov whitepaper index:

- Source index: <https://www.e-gov.go.jp/about-government/white-papers.html>

This file is a route-checking snapshot, not a permanent URL registry. Use it to know where to start verification. Before reading, citing, or downloading a document, re-check the e-Gov entry and the relevant official landing page.

## Route Status Labels

- `ok`: checked by direct HTTP fetch.
- `redirect`: e-Gov URL redirects to a newer final URL.
- `browser-ok`: direct scripted fetch failed or was blocked, but the page was confirmed in a browser-capable fetch.
- `moved`: the e-Gov URL reports movement or redirects to a generic page; find the current edition from the ministry site or search within the official domain.
- `shared-page`: multiple e-Gov entries intentionally point to the same ministry index page.

## Routes

| No. | Document | Route start from e-Gov | Current verification route | Status | Notes |
|---:|---|---|---|---|---|
| 1 | 水循環白書 | <https://www.cas.go.jp/jp/seisaku/mizu_junkan/materials/materials/white_paper.html> | 内閣官房 水循環政策本部事務局の白書ページ | ok | Series page. |
| 2 | 年次報告書 | <https://www.jinji.go.jp/kouho_houdo/koumuinhakusyo.html> | 人事院 公務員白書一覧 | ok | Series page. |
| 3 | 経済財政白書 | <https://www5.cao.go.jp/keizai3/whitepaper.html#keizai> | 内閣府 白書等ページの経済財政白書アンカー | ok | Anchor route. |
| 4 | 原子力白書 | <http://www.aec.go.jp/jicst/NC/about/hakusho/index.htm> | 原子力委員会 原子力白書ページ | browser-ok | Scripted fetch may report 404; browser fetch confirmed the page. |
| 5 | 防災白書 | <http://www.bousai.go.jp/kaigirep/hakusho/index.html> | <https://www.bousai.go.jp/kaigirep/hakusho/index.html> | redirect | Series page; editions expose HTML and PDF routes separately. |
| 6 | 高齢社会白書 | <https://www8.cao.go.jp/kourei/whitepaper/index-w.html> | 内閣府 高齢社会白書ページ | ok | Series page. |
| 7 | 障害者白書 | <https://www8.cao.go.jp/shougai/whitepaper/index-w.html> | 内閣府 障害者白書ページ | ok | Series page. |
| 8 | 交通安全白書 | <https://www8.cao.go.jp/koutu/taisaku/index-t.html> | 内閣府 交通安全白書ページ | ok | Series page. |
| 9 | 男女共同参画白書 | <http://www.gender.go.jp/about_danjo/whitepaper/index.html> | <https://www.gender.go.jp/about_danjo/whitepaper/index.html> | redirect | Series page. |
| 10 | 年次報告 | <http://www.jftc.go.jp/soshiki/nenpou/> | <https://www.jftc.go.jp/soshiki/nenpou/> | redirect | 公正取引委員会 年次報告ページ. |
| 11 | 警察白書 | <http://www.npa.go.jp/publications/whitepaper/index_keisatsu.html> | <https://www.npa.go.jp/publications/whitepaper/index_keisatsu.html> | redirect | 警察庁 白書ページ. |
| 12 | 犯罪被害者白書 | <http://www.npa.go.jp/hanzaihigai/kohyo/whitepaper/whitepaper.html> | <https://www.npa.go.jp/hanzaihigai/kohyo/whitepaper/whitepaper.html> | redirect | 警察庁 白書ページ. |
| 13 | 年次報告 | <https://www.ppc.go.jp/aboutus/report/> | 個人情報保護委員会 年次報告・上半期報告ページ | ok | Series page. |
| 14 | 金融庁の1年 | <https://www.fsa.go.jp/common/paper/index.html> | 金融庁 白書・年次報告等ページ | ok | Collection page. |
| 15 | 消費者白書 | <https://www.caa.go.jp/publication/annual_reports/> | 消費者庁 白書・年次報告書等ページ | ok | Collection page. |
| 16 | 少子化社会対策白書 | <https://www.cfa.go.jp/resources/white-paper> | こども家庭庁 白書ページ | ok shared-page | Same route as 子ども・若者白書. |
| 17 | 子ども・若者白書 | <https://www.cfa.go.jp/resources/white-paper> | こども家庭庁 白書ページ | ok shared-page | Same route as 少子化社会対策白書. |
| 18 | 地方財政白書 | <https://www.soumu.go.jp/menu_seisaku/hakusyo/index.html#chihou> | 総務省 白書ページの地方財政白書アンカー | ok | Encoding can vary; keep URL role-based. |
| 19 | 情報通信白書 | <https://www.soumu.go.jp/johotsusintokei/whitepaper/index.html> | 総務省 情報通信白書ページ | ok | Series page. |
| 20 | 公害紛争処理白書 | <https://www.soumu.go.jp/kouchoi/knowledge/nenji/main.html> | 公害等調整委員会 年次報告書ページ | ok | Series page. |
| 21 | 消防白書 | <https://www.fdma.go.jp/publication/#whitepaper> | 消防庁 刊行物ページの白書アンカー | ok | Anchor route. |
| 22 | 犯罪白書 | <http://www.moj.go.jp/housouken/houso_hakusho2.html> | <https://www.moj.go.jp/housouken/houso_hakusho2.html> | redirect | 法務省 犯罪白書ページ. |
| 23 | 再犯防止推進白書 | <http://www.moj.go.jp/hisho/saihanboushi/hisho04_00009.html> | <https://www.moj.go.jp/hisho/saihanboushi/hisho04_00009.html> | redirect | 法務省 白書ページ. |
| 24 | 人権教育・啓発白書 | <http://www.moj.go.jp/JINKEN/jinken04_00173.html> | <https://www.moj.go.jp/JINKEN/jinken04_00173.html> | redirect | 法務省 白書ページ. |
| 25 | 出入国在留管理白書 | <http://www.moj.go.jp/nyuukokukanri/kouhou/nyukan_nyukan42.html> | <https://www.moj.go.jp/isa/index.html> | moved | e-Gov route redirects to ISA home; search within `moj.go.jp/isa/` or use site search for current whitepaper page. |
| 26 | 外交青書 | <https://www.mofa.go.jp/mofaj/gaiko/bluebook/index.html> | 外務省 外交青書・白書ページ | browser-ok | Scripted fetch may get 403; browser fetch confirmed. |
| 27 | 開発協力白書・ODA白書 | <https://www.mofa.go.jp/mofaj/gaiko/oda/shiryo/hakusyo.html> | 外務省 開発協力白書・参考資料集ページ | browser-ok | Scripted fetch may get 403; browser fetch confirmed. |
| 28 | 科学技術白書 | <https://www.mext.go.jp/b_menu/hakusho/html/kagaku.htm> | 文部科学省 科学技術・イノベーション白書ページ | ok | Series page. |
| 29 | 文部科学白書 | <https://www.mext.go.jp/b_menu/hakusho/html/monbu.htm> | 文部科学省 文部科学白書ページ | ok | Series page. |
| 30 | 厚生労働白書 | <https://www.mhlw.go.jp/toukei_hakusho/hakusho/#title1> | 厚生労働省 白書・年次報告書ページのアンカー | ok shared-page | Same collection page as other MHLW whitepapers. |
| 31 | 労働経済白書 | <https://www.mhlw.go.jp/toukei_hakusho/hakusho/#title3> | 厚生労働省 白書・年次報告書ページのアンカー | ok shared-page | Same collection page as other MHLW whitepapers. |
| 32 | 自殺対策白書 | <https://www.mhlw.go.jp/toukei_hakusho/hakusho/#title5> | 厚生労働省 白書・年次報告書ページのアンカー | ok shared-page | Same collection page as other MHLW whitepapers. |
| 33 | 過労死等防止対策白書 | <https://www.mhlw.go.jp/toukei_hakusho/hakusho/#title6> | 厚生労働省 白書・年次報告書ページのアンカー | ok shared-page | Same collection page as other MHLW whitepapers. |
| 34 | 食料・農業・農村白書 | <https://www.maff.go.jp/j/wpaper/> | 農林水産省 白書情報ページ | ok shared-page | Same collection page as 食育白書. |
| 35 | 食育白書 | <https://www.maff.go.jp/j/wpaper/> | 農林水産省 白書情報ページ | ok shared-page | Same collection page as 食料・農業・農村白書. |
| 36 | 森林・林業白書 | <https://www.rinya.maff.go.jp/j/kikaku/hakusyo/index.html> | 林野庁 森林・林業白書ページ | ok | Series page. |
| 37 | 水産白書 | <https://www.jfa.maff.go.jp/j/kikaku/wpaper/index.html> | 水産庁 水産白書ページ | ok | Series page. |
| 38 | 通商白書 | <https://www.meti.go.jp/report/whitepaper/index_tuhaku.html> | 経済産業省 通商白書ページ | browser-ok | Scripted fetch timed out; browser fetch confirmed. |
| 39 | 製造基盤白書（ものづくり白書） | <https://www.meti.go.jp/report/whitepaper/index_mono.html> | 経済産業省 ものづくり白書ページ | browser-ok | Scripted fetch timed out; browser fetch confirmed. |
| 40 | エネルギー白書 | <https://www.enecho.meti.go.jp/about/whitepaper/> | 資源エネルギー庁 エネルギー白書ページ | browser-ok | Scripted fetch disconnected; browser fetch confirmed. |
| 41 | 特許行政年次報告書 | <https://www.jpo.go.jp/resources/report/nenji/index.html> | 特許庁 特許行政年次報告書ページ | browser-ok | Scripted fetch disconnected; browser fetch confirmed. |
| 42 | 中小企業白書 | <https://www.chusho.meti.go.jp/pamflet/hakusyo/index.html> | 中小企業庁 中小企業白書ページ | browser-ok | Scripted fetch timed out; browser fetch confirmed. |
| 43 | 小規模企業白書 | <https://www.chusho.meti.go.jp/pamflet/hakusyo/syoukiboindex.html> | 中小企業庁 小規模企業白書ページ | browser-ok | Scripted fetch timed out; browser fetch confirmed. |
| 44 | 国土交通白書 | <https://www.mlit.go.jp/statistics/file000004.html> | 国土交通省 国土交通白書ページ | ok | Series page. |
| 45 | 土地白書 | <https://www.mlit.go.jp/statistics/file000006.html> | 国土交通省 土地白書ページ | ok | Series page. |
| 46 | 首都圏整備に関する年次報告 | <https://www.mlit.go.jp/toshi/daisei/toshi_machi_tk_000058.html> | 国土交通省 首都圏整備法関連ページ | ok | Series or collection page. |
| 47 | 交通政策白書 | <https://www.mlit.go.jp/sogoseisaku/transport_policy/sosei_transport_policy_fr1_000009.html> | 国土交通省 交通政策白書ページ | ok | Series page. |
| 48 | レポート海難審判 | <https://www.mlit.go.jp/jmat/kankoubutsu/report.htm> | 海難審判所 レポート海難審判ページ | ok | Series page. |
| 49 | 観光白書 | <https://www.mlit.go.jp/statistics/file000008.html> | 国土交通省 観光白書ページ | ok | Series page. |
| 50 | 運輸安全委員会年報 | <https://www.mlit.go.jp/jtsb/bunseki-kankoubutu/jtsbannualreport/jtsbannualreport_new.html> | <https://jtsb.mlit.go.jp/bunseki-kankoubutu/jtsbannualreport/jtsbannualreport_new.html> | redirect | JTSB subdomain final URL. |
| 51 | 海上保安レポート | <https://www.kaiho.mlit.go.jp/doc/hakkou/report/top.html> | 海上保安庁 海上保安レポートページ | ok | Series page. |
| 52 | 環境白書・循環型社会白書・生物多様性白書 | <http://www.env.go.jp/policy/hakusyo/index.html> | <https://www.env.go.jp/policy/hakusyo/index.html> | redirect | Environment whitepaper collection page. |
| 53 | 年次報告 | <https://www.nra.go.jp/nra/seisakujikkou/houkoku/index.html> | 原子力規制委員会 年次報告等ページ | ok | Series page. |
| 54 | 防衛白書 | <https://www.mod.go.jp/j/publication/wp/> | Current editions are under `mod.go.jp/j/press/wp/` and data/PDF under `clearing.mod.go.jp/hakusho_data/` | moved | e-Gov route says page moved; verify via official MOD site search or current edition pages. |

## Practical Rules From The Route Check

1. Always start from e-Gov, but do not stop there.
2. Treat shared ministry pages and anchors as normal, especially CFA, MHLW, MAFF, and SOUMU.
3. Treat HTTP-to-HTTPS redirects as normal.
4. Treat 403, timeout, or remote disconnect from scripted clients as a fetch-mode problem when browser access confirms the page.
5. Treat moved pages as requiring official-domain search before use.
6. For MOD 防衛白書, the old e-Gov route is not enough. Use the MOD current-edition route and verify PDF/data links under the official `clearing.mod.go.jp` whitepaper data domain.
7. Default to the latest edition visible from the official series page. When a user specifies an edition year, era year, or comparison period, resolve that edition from the series page before reading.

## Canonical Slugs

Use these values for local cache paths and manifest records when the document is one of the e-Gov-listed whitepapers. Keep slugs ASCII, lowercase, and stable.

| No. | Document | ministry_slug | document_slug |
|---:|---|---|---|
| 1 | 水循環白書 | cas | water-cycle-white-paper |
| 2 | 年次報告書 | jinji | national-public-service-annual-report |
| 3 | 経済財政白書 | cao | economic-and-fiscal-white-paper |
| 4 | 原子力白書 | aec | atomic-energy-white-paper |
| 5 | 防災白書 | cao | disaster-management-white-paper |
| 6 | 高齢社会白書 | cao | aging-society-white-paper |
| 7 | 障害者白書 | cao | disability-white-paper |
| 8 | 交通安全白書 | cao | traffic-safety-white-paper |
| 9 | 男女共同参画白書 | cao-gender | gender-equality-white-paper |
| 10 | 年次報告 | jftc | fair-trade-annual-report |
| 11 | 警察白書 | npa | police-white-paper |
| 12 | 犯罪被害者白書 | npa | crime-victims-white-paper |
| 13 | 年次報告 | ppc | personal-information-protection-annual-report |
| 14 | 金融庁の1年 | fsa | financial-services-agency-annual-report |
| 15 | 消費者白書 | caa | consumer-white-paper |
| 16 | 少子化社会対策白書 | cfa | declining-birthrate-white-paper |
| 17 | 子ども・若者白書 | cfa | children-and-youth-white-paper |
| 18 | 地方財政白書 | soumu | local-public-finance-white-paper |
| 19 | 情報通信白書 | soumu | information-and-communications-white-paper |
| 20 | 公害紛争処理白書 | kouchoi | pollution-dispute-resolution-white-paper |
| 21 | 消防白書 | fdma | fire-service-white-paper |
| 22 | 犯罪白書 | moj | crime-white-paper |
| 23 | 再犯防止推進白書 | moj | recidivism-prevention-white-paper |
| 24 | 人権教育・啓発白書 | moj | human-rights-education-white-paper |
| 25 | 出入国在留管理白書 | isa | immigration-services-white-paper |
| 26 | 外交青書 | mofa | diplomatic-bluebook |
| 27 | 開発協力白書・ODA白書 | mofa | development-cooperation-white-paper |
| 28 | 科学技術白書 | mext | science-technology-innovation-white-paper |
| 29 | 文部科学白書 | mext | education-culture-sports-science-white-paper |
| 30 | 厚生労働白書 | mhlw | health-labour-welfare-white-paper |
| 31 | 労働経済白書 | mhlw | labour-economy-white-paper |
| 32 | 自殺対策白書 | mhlw | suicide-prevention-white-paper |
| 33 | 過労死等防止対策白書 | mhlw | karoshi-prevention-white-paper |
| 34 | 食料・農業・農村白書 | maff | food-agriculture-rural-white-paper |
| 35 | 食育白書 | maff | food-education-white-paper |
| 36 | 森林・林業白書 | rinya | forest-forestry-white-paper |
| 37 | 水産白書 | jfa | fisheries-white-paper |
| 38 | 通商白書 | meti | trade-white-paper |
| 39 | 製造基盤白書（ものづくり白書） | meti | manufacturing-white-paper |
| 40 | エネルギー白書 | enecho | energy-white-paper |
| 41 | 特許行政年次報告書 | jpo | patent-office-annual-report |
| 42 | 中小企業白書 | chusho | sme-white-paper |
| 43 | 小規模企業白書 | chusho | small-enterprise-white-paper |
| 44 | 国土交通白書 | mlit | land-infrastructure-transport-tourism-white-paper |
| 45 | 土地白書 | mlit | land-white-paper |
| 46 | 首都圏整備に関する年次報告 | mlit | capital-region-development-annual-report |
| 47 | 交通政策白書 | mlit | transport-policy-white-paper |
| 48 | レポート海難審判 | jmat | marine-accident-inquiry-report |
| 49 | 観光白書 | mlit | tourism-white-paper |
| 50 | 運輸安全委員会年報 | jtsb | transport-safety-board-annual-report |
| 51 | 海上保安レポート | kaiho | coast-guard-report |
| 52 | 環境白書・循環型社会白書・生物多様性白書 | env | environment-sound-material-cycle-biodiversity-white-paper |
| 53 | 年次報告 | nra | nuclear-regulation-authority-annual-report |
| 54 | 防衛白書 | mod | defense-white-paper |
