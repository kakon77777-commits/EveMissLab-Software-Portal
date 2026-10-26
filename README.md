# EveMissLab Software Portal

**v0.1 static portal (2026-10-26) · 預覽版 / 尚未正式部署**

供外部使用者探索 EveMissLab **已核准公開** 的軟體、產品與線上工具。本站不持有任何私有原始碼、內部專案索引、本機狀態、存取權杖或發行權限；只顯示經人工核准的公開資訊。

## 快速啟動（Python 3.11+；純靜態無框架）

```bash
python -m http.server 8080 --bind 127.0.0.1
# http://127.0.0.1:8080
python -m unittest discover -s tests -v
python scripts/validate_catalog.py
```

Windows PowerShell：`py -3 -m http.server 8080 --bind 127.0.0.1`，用瀏覽器開啟 `http://127.0.0.1:8080`。

不要使用 `file://` 雙擊首頁，因為瀏覽器通常不允許該方式載入 `data/catalog.json`。

## 目前已有

- 繁體中文首頁（分類篩選、搜尋、使用入口、狀態標示）。
- `data/catalog.json` 公開資料契約 v1；無 API Key 或後台資料庫。
- 一個實際可操作的內建瀏覽器工具：**JSON 工作臺** `/tools/json/`，可驗證、格式化、壓縮、複製、下載 JSON，全部在瀏覽器端處理。
- 離線 Catalog 驗證 CLI；開放外部產品透過核准清單逐批加入。
- 無外部追蹤程式、CDN、廣告、登入、計量或隱藏資料回傳。

## 如何增加一款已公開的軟體

在 `data/catalog.json` 的 `products` 增加下列 JSON 欄位，務必符合 `scripts/validate_catalog.py`：

```json
{
  "id": "stable-public-id",
  "name": "Example Software",
  "summary": "經過審查的繁中產品介紹",
  "kind": "software",
  "tags": ["開放工具"],
  "release_stage": "preview",
  "launch_path": null,
  "links": [{"type": "website", "url": "https://example.com", "label": "開啟網站"}]
}
```

- `launch_path` 限本倉庫 `/tools/...` 或 `/apps/...` 的可用路徑；外部產品用 `links` 的已驗證 HTTPS 網址。
- `source_repo` 是否顯示，取決於真正的 repo 可見性與授權審查；**網站公開 ≠ 原始碼公開 ≠ 自動 MIT 授權**。
- 新增項目只接受經人工核准、欄位白名單化的公開資訊；合併前仍要人工檢視 diff。
- 本站是使用入口，不取代 EveMissLab 其他網站（例如無界智庫、Universal Directory）的策展職責。

## 部署前注意

目前**沒有** GitHub Actions、OAuth、任意上傳程式碼、遠端 API、付費與產品後端；只是可用的靜態 MVP。未來新產品應由其自己管理執行環境、版本、授權、隱私及資安，Portal 只負責已核准入口。若需整合第三方 SDK，應先進行授權與安全審查。

公開倉庫不自動附帶開源授權。最終 LICENSE 請由權利人決定；目前網站程式碼未授予第三方再散布權。

詳見 `docs/CONTENT_PUBLICATION_PROTOCOL.md`。

**Windows 快速入口**：使用 PowerShell `./scripts/TEST_PORTAL.ps1`、`./scripts/START_PORTAL.ps1`，或直接執行上述 Python 命令。無需先建立網站帳號。

**JSON 格式化注意**：瀏覽器原生 `JSON.parse` 不適合需要精確保留超出 JavaScript 安全整數範圍的數值、重複鍵或數位簽章的檔案；請將此工具用於一般 JSON 閱讀與整理，精密資料請在原本支援無損數字型別的系統處理。
