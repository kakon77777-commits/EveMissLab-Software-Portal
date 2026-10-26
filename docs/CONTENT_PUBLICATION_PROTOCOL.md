# 公開資訊與內部專案隔離協議 (Portal Public Catalog v1)

## 原則

1. Portal 是面向使用者的軟體入口，不是任何內部管理系統的遠端前端。
2. 只接受單筆、經人工核准的最小公開 manifest；Portal 不連線讀取任何私有來源。
3. `maturity`、`visibility`、`publication_state`、`license_state` 獨立判斷；任何一個欄位都不能自動代替人類同意。
4. `published` 且 `publish_approved` 並不代表所有內部字段都能公開。從程式硬性限定輸出 id/name/summary/kind/tags/release_stage/launch_path/public links。
5. 未驗證、失聯、歷史 URL 不出現在公開列表；不得猜網址。
6. 不收集使用者輸入 JSON；內建 JSON 工作臺全部在瀏覽器記憶體運作。
7. 不假稱有 API、正式營運、GitHub 倉庫或測試 PASS。

## 開放內容批准 (人工)

- 逐項批准名稱、介紹、目的、版本狀態、網站、授權、可用性、相容環境及隱私聲明。
- 新產品直接透過經審核入口連到獨立產品網站；需要在 Portal 執行的純靜態工具才以 `/tools/` 或 `/apps/` 上架。
- 產品真的需要使用者註冊、資料庫、支付、計量與授權時，獨立新增 backend 與安全設計，不得暴露任何內部系統。
- 若更新 manifest 後觸發未知產品數量改變，reviewer 必須重新審查最終產出及 diff。

## 與其他 EveMissLab 站群的界線

- 無界智庫：知識論文與概念策展。
- Universal Directory：跨領域策展目錄。
- Software Portal：直接使用、下載、了解軟體的入口。
- 內部管理系統：不對外提供任何查詢介面，也不是本站的資料來源。
