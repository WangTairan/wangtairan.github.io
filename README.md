## 快速使用

本地预览：  
```sh
python3 -m http.server 4173 -d static-html
```  
然后打开 http://localhost:4173

一键部署到 GitHub Pages（将 `static-html/` 推到 `gh-pages` 分支）：  
```sh
git subtree split --prefix static-html -b gh-pages && git push -f origin gh-pages && git branch -D gh-pages
```  
  需要在仓库设置里启用 Pages 并指向 `gh-pages` 分支根目录。

更新主分支（保存完整站点）

一行提交并推送：
```sh
git add -A && git commit -m "update site" && git push origin master
```