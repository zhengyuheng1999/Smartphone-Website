本web程序模仿购物平台，针对手机购买用户，基于flask和postgresql开发，一共收集576部十大品牌（诺基亚、摩托罗拉、三星、索尼、苹果、谷歌、华为、小米、一加、华硕）的手机。
用户可通过ASIN号、品牌、型号、价位来查找手机，通过价位升序/降序、评分降序查看。还可以进入某手机的网页进行评论或查看他人评论，并通过本网站提供的亚马逊购买链接购买

用import.py将其导入postgre数据库的phones表。整个程序代码采用Flask框架
使得python与Postgresql能够交互，实现登录、查找和评论的功能
同时使用javascript对部分html组件进行控制，使程序更好地运行

js代码直接被包含在两个html文件里
数据库URL为postgresql://postgres:zyh@localhost:5432/postgres
