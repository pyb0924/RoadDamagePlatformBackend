## 智慧公路养护管理系统后端

智慧公路养护管理系统后端是为智慧公路养护管理系统是权限管理系统与业务模块融合的服务。

### 项目启动

1. 创建虚拟环境(通过venv或conda)
2. 安装依赖 `pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple`
3. 启动一个MySQL服务，导入`sql/itsm-admin.sql`
4. 修改数据库配置`common/db.py`
5. 直接启动`main.py`

### TODO List

1. 后台管理系统 V1.0

- [ ] 用户管理
- [ ] 角色管理
- [ ] 权限管理
- [ ] 菜单管理