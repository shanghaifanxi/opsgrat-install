# Opsgrat安装手册

## 服务器环境要求

*   CentOS 7或Red Hat 7
*   python2.7

## 服务器配置要求

*   Cpu >=4Core
*   内存 >=8G

## 依赖中间件

1.   MySQL5.5+：部署OpsGrat前需要先提供MySQL数据库，并准备好可以创建数据库的用户
2.   Redis3.0+：OpsGrat执行ansible-playbook产生的中间日志先记录在Redis中因此需要提供可以访问的Redis
3.   RabbitMQ：OpsGrat使用RabbitMQ作为消息队列异步执行作业，所以部署前需要先准备好可以访问的RabbitMQ

## OpsGrat和SSO使用python版本

*   python3.6

## OpsGrat程序的组成

1.   sso：单点登录，包括用户管理、部门管理、角色管理、菜单管理等基础内容
2.   sso-worker：celery异步任务进程，用于从ldap同步用户信息
3.   opsgrat：OpsGrat系统，提供OpsGrat的api和web操作界面，只能单节点部署
4.   opsgrat-worker：celery异步任务进程，主要用于异步执行自动化作业和工作流，opsgrat-worker可以部署多个节点
5.   notification-worker：通知进程，用于通过邮件或钉钉通知用户自动化作业的执行结果，notification-worker可以部署多个节点
6.   opsgrat-beat：定时任务进程，用于生成计划任务交给opsgrat-worker执行，只能单节点部署和opsgrat web程序部署在同一台主机上即可

## OpsGrat安装

### 安装

1.   进入opsgrat-install目录
2.   运行setup.sh
```
sh setup.sh
```
3.   在浏览器中打开：http://ip:8000/
4.   按照步骤进行OpsGrat安装

## 初始化配置

## sso配置

1.   opsgrat安装完成后在浏览器上访问sso，本文的地址为：http://ip:8081/ (根据实际配置修改ip和端口)  
  - 管理用户为：admin
  - 初始密码为：admin
2.   修改sso和opsgrat的访问地址：
  - 点击菜单管理-》子系统管理
  - 修改OpsGrat和sso的访问路径

## 导入License

1.   申请试用或者购买的时候会将License发送到填写的邮箱，先将License文件下载到本地
2.   进入opsgrat系统，由于首次安装还未导入License，系统会跳转到License导入页面，本地opsgrat地址为：http://ip:8080/
3.   点击“导入”按钮，选择License文件后点击上传即可


