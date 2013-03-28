WeixinAutoReply
===============

#### 基本架构
使用Django+SAE搭建的一个微信公共主页自动回复服务

#### 参考博文:
[http://blog.csdn.net/liushuaikobe/article/details/8453716](http://blog.csdn.net/liushuaikobe/article/details/8453716)

#### 使用方法:

1.注册微信公共主页帐号 [http://mp.weixin.qq.com/](http://mp.weixin.qq.com/)

2.注册sae帐号 (http://sae.sina.com.cn/)[http://sae.sina.com.cn/]

3.在sae创建应用，并使用svn checkout代码仓库到本地

4.使用django命令生成基本代码 参考[http://python.sinaapp.com/doc/](http://python.sinaapp.com/doc/)

5.添加相应index.wsgi  config.yaml views.py文件，修改urls.py. 

6.将微信公共主页帐号设置为开发模式，并设置URL为sae创建的应用地址，TOKEN设置与views.py中的TOKEN一致

