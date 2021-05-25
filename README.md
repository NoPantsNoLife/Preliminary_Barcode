# Preliminary_Barcode

## 实现

### 摄像头

opencv调用摄像头捕获

### 解码

直接调用Pyzbar扫描二维码

### 标注

opencv在图上画出二维码区域和解码结果

### get请求

调用requests库发起get请求

### 网页显示

使用PyQt5.QtWebEngineWidgets实现一个最简单的浏览器窗口，访问本地的网页

### 网页改变显示方式

JavaScript从网页的URL参数中获取code和word信息

例如display.htm?code=0&word=scutrobot996

获取到code=0，word=scutrobot996

判断code的值，修改对应<p>标记的style属性为不同的CSS，改变样式

