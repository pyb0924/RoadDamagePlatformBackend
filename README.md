## 智慧公路养护管理系统后端

智慧公路养护管理系统后端是为智慧公路养护管理系统是权限管理系统与业务模块融合的服务。

### 项目迭代文档
[项目迭代文档](https://github.com/pyb0924/RoadDamagePlatformFrontend/tree/dev/docs)

### TODO List
1. 后台管理系统 V1.0 
   - [x] 登录（用户属性、权限缓存）
   - [x] 用户管理（用户新增、用户编辑、用户删除）
   - [x] 接口权限校验

2. 智慧公路养护管理系统 V1.0 
   - [x] 养护事件查询（支持多条件查询，字段包含：病害类型、病害发生地经纬度范围、病害发生地地名、事件状态）
   - [x] 养护事件提交（对接APP端用户提交病害）
   - [x] 养护状态更新（对接Web、APP端的养护事件生成、提交、审核流程）
   
3. 智慧公路养护管理系统 V1.1
   - [x] 模拟数据生成脚本
   - [x] 数据大屏Grafana对接Web iframe

4. 智慧公路养护管理系统 V1.2
   - [x] MQ架构引入
   - [x] 对接AI模块

### 迭代记录

Jan 11, 2023
1. MQ架构引入
2. OSS上传逻辑更新

Nov 27, 2022
1. 调整养护管理部分接口的命名

Nov 20, 2022
1. 修复接口上传图片的bug
2. 新增通过养护事件查询对应历史记录的接口
3. 新增图片后台同步至七牛云OSS的功能

Nov 18, 2022
1. 新增养护事件与用户的关联

Nov 16, 2022
1. 合并dev2内容，即养护管理业务预研结果

Nov 12, 2022
1. 修复用户编辑功能的bug

Nov 7, 2022
1. 修复用户删除的bug
2. 接口权限校验功能上线

Oct 30, 2022
1. 修复当用户没有权限时被无法查出的bug

Oct 26, 2022
1. 新增权限列表接口
2. 修复接口token认证依赖注入的问题

Oct 24, 2022
1. 新增用户管理功能及对应接口

Oct 21, 2022
1. 新增用户新增功能接口
2. 新增支持自定义HTTP异常和自定义Response格式
