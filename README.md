# HKInformation 香港資訊數據圖鑑

香港統計數據視覺化平台，提供樓市、經濟、人口等各項統計數據的深入分析與互動圖表。

## 技術架構

| 項目 | 方案 |
|------|------|
| 靜態網站生成器 | Python build.py |
| 圖表 | Apache ECharts 5 |
| CSS | TailwindCSS (CDN) |
| 部署 | GitHub Pages (via GitHub Actions) |
| 數據 | 政府統計處、差餉物業估價署、房屋委員會 |

## 使用方法

### 本地 build

`python build.py`

生成所有 HTML 到 `output/` 資料夾，直接用瀏覽器打開即可查看。

### 新增文章

1. 在 `src/articles/` 建立一個新的 JSON 檔，參照現有文章格式
2. 在 `build.py` 的 `article_slugs` 列表加入 slug
3. 執行 `python build.py`
4. 如在導航顯示，在 `src/data/config.json` 的 `nav` 加入連結

### 更換圖片

在 `src/images/` 放入新圖片，在文章 JSON 的 `heroImage` 填上檔名（不含副檔名）。

### 叫 Codex 幫你更新

直接同我講想加新指標 / 改數據 / 加文章，我幫你改 JSON 然後 rebuild，幾分鐘搞掂。

## 自動更新

GitHub Actions 每月 1 日自動執行 build + deploy。
也可手動觸發：GitHub Repo → Actions → Deploy to GitHub Pages → Run workflow

## Google AdSense / Analytics / Search Console

所有 Google 設定集中喺 `src/data/config.json`：

| 設定 | 位置 |
|------|------|
| AdSense publisher ID | `adsense.publisherId` |
| Google Analytics ID | `site.googleAnalyticsId`（GA4 用 `G-XXXXXXX`；只填數字會當 `UA-XXXXXXX-1`） |
| Search Console 驗證 | `seo.googleSiteVerification` |

改完執行 `python build.py` + `python gen_index.py`，再將 `output/` 內容複製到 repo root 並 push，所有頁面就會自動加入 AdSense script、Google Analytics gtag 同驗證 meta tag。

## 未來計劃

- [ ] 連接 data.gov.hk API 自動獲取最新數據
- [ ] 加入更多分析指標（GDP、就業、人口結構等）
- [ ] 互動式地圖（18區數據）
- [ ] 數據比較工具
- [ ] SEO 關鍵字表現追蹤

## 免責聲明

本網站所有數據均來自香港政府公開資料，僅供參考。
