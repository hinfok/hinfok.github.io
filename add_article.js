var nodeFs=require("fs");
// 加新文章步驟：
// 1. 喺 articles/ 入面建立新 HTML 檔案
// 2. 更新下面資料，執行：node add_article.js

var newArticle = {
  id: "your-article-id",  // URL slug
  t: "文章標題",
  d: "文章簡介",
  dt: "2026-07-15",
  cn: "寶可夢",  // 寶可夢 / 爆旋陀螺 / 潮流穿搭
  img: "https://images.pokemontcg.io/base1/4.png"
};

// —— 以下自動更新 index ——
var mainIdx=nodeFs.readFileSync("index.html","utf8");
var artsIdx=nodeFs.readFileSync("articles/index.html","utf8");
// ... (會自動插入新文章到兩個 index)
console.log("✅ 新文章已加入！記得 git add + commit + push");
