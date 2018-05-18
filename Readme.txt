运行redis
运行本地web服务器
运行proxyManager.py
使用web api获取代理
请求格式 
get http://localhost:6324/proxy_get 获取一个有效ip
get http://localhost:6324/proxy_get?count=m 获取m个有效ip
get http://localhost:6324/proxy_get?count=m&score=n 获取m个分数大于n的有效ip