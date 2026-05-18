# FastapiAdmin 数据库表结构说明

## 一、概述

本项目是一个 RBAC（基于角色的访问控制）权限管理系统，核心围绕 **用户-角色-菜单-部门** 四大模块展开。

## 二、表结构总览

| 表名 | 中文名 | 类型 |
|------|--------|------|
| sys_user | 用户表 | 核心 |
| sys_role | 角色表 | 核心 |
| sys_menu | 菜单表 | 核心 |
| sys_dept | 部门表 | 核心 |
| sys_position | 岗位表 | 辅助 |
| sys_dict_type | 字典类型表 | 辅助 |
| sys_dict_data | 字典数据表 | 辅助 |
| sys_param | 系统参数表 | 辅助 |
| sys_notice | 通知公告表 | 辅助 |
| sys_log | 系统日志表 | 辅助 |
| sys_user_roles | 用户角色关联表 | 中间表 |
| sys_user_positions | 用户岗位关联表 | 中间表 |
| sys_role_menus | 角色菜单关联表 | 中间表 |
| sys_role_depts | 角色部门关联表 | 中间表 |

## 三、基础模型设计

所有业务表都继承自基础模型，保证统一的审计字段：

### ModelMixin（通用字段）

| 字段 | 类型 | 说明 |
|------|------|------|
| id | Integer | 主键ID，自增 |
| uuid | String(64) | UUID全局唯一标识 |
| status | String(10) | 是否启用(0:启用 1:禁用) |
| description | Text | 备注/描述 |
| created_time | DateTime | 创建时间 |
| updated_time | DateTime | 更新时间 |

### UserMixin（审计字段）

| 字段 | 类型 | 说明 |
|------|------|------|
| created_id | Integer | 创建人ID（外键→sys_user.id） |
| updated_id | Integer | 更新人ID（外键→sys_user.id） |
| created_by | UserModel | 创建人对象（关联关系） |
| updated_by | UserModel | 更新人对象（关联关系） |

**设计意图：**
- `ModelMixin`：所有业务表都继承，保证每张表都有统一的审计字段
- `UserMixin`：记录数据的创建者和修改者，用于"仅本人数据权限"控制

## 四、核心表详解

### 4.1 用户表（sys_user）

**文件：** `backend/app/api/v1/module_system/user/model.py`

| 字段 | 类型 | 说明 |
|------|------|------|
| username | String(64) | 登录账号（唯一） |
| password | String(255) | 密码哈希 |
| name | String(32) | 昵称 |
| mobile | String(11) | 手机号（唯一） |
| email | String(64) | 邮箱（唯一） |
| gender | String(1) | 性别(0:男 1:女 2:未知) |
| avatar | String(255) | 头像URL |
| is_superuser | Boolean | 是否超级管理员 |
| last_login | DateTime | 最后登录时间 |
| gitee_login | String(32) | Gitee登录标识 |
| github_login | String(32) | GitHub登录标识 |
| wx_login | String(32) | 微信登录标识 |
| qq_login | String(32) | QQ登录标识 |
| dept_id | Integer | 所属部门ID（外键→sys_dept.id） |

**关联关系：**
- 一个用户属于 **一个部门**（`dept_id` 外键）
- 一个用户可以有 **多个角色**（通过 `sys_user_roles` 中间表）
- 一个用户可以有 **多个岗位**（通过 `sys_user_positions` 中间表）

### 4.2 角色表（sys_role）

**文件：** `backend/app/api/v1/module_system/role/model.py`

| 字段 | 类型 | 说明 |
|------|------|------|
| name | String(64) | 角色名称 |
| code | String(16) | 角色编码（唯一） |
| order | Integer | 显示排序 |
| data_scope | Integer | 数据权限范围：1:仅本人 2:本部门 3:本部门及以下 4:全部 5:自定义 |

**关联关系：**
- 一个角色包含 **多个菜单**（通过 `sys_role_menus` 中间表）→ 控制**功能权限**
- 一个角色可以绑定 **多个部门**（通过 `sys_role_depts` 中间表）→ 当 `data_scope=5` 时使用
- 一个角色可以被 **多个用户** 拥有

### 4.3 菜单表（sys_menu）

**文件：** `backend/app/api/v1/module_system/menu/model.py`

| 字段 | 类型 | 说明 |
|------|------|------|
| name | String(50) | 菜单名称 |
| type | Integer | 菜单类型：1:目录 2:菜单 3:按钮/权限 4:外部链接 |
| order | Integer | 显示排序 |
| permission | String(100) | 权限标识（如：module_system:user:create） |
| icon | String(50) | 菜单图标 |
| route_name | String(100) | 路由名称（Vue Router用） |
| route_path | String(200) | 路由路径（如：/system/user） |
| component_path | String(200) | 组件路径（如：module_system/user/index） |
| redirect | String(200) | 重定向地址 |
| hidden | Boolean | 是否隐藏 |
| keep_alive | Boolean | 是否缓存页面 |
| always_show | Boolean | 是否始终显示 |
| title | String(50) | 菜单标题 |
| params | JSON | 路由参数 |
| affix | Boolean | 是否固定标签页 |
| parent_id | Integer | 父菜单ID（自关联，树形结构） |

**设计意图：**
- 菜单表不仅是导航菜单，还承担了**权限控制**的职责
- `type=3` 的按钮类型，用于前端按钮级权限控制（`v-hasPerm`）
- `permission` 字段是权限控制的核心标识

### 4.4 部门表（sys_dept）

**文件：** `backend/app/api/v1/module_system/dept/model.py`

| 字段 | 类型 | 说明 |
|------|------|------|
| name | String(64) | 部门名称 |
| order | Integer | 显示排序 |
| code | String(16) | 部门编码（唯一） |
| leader | String(32) | 部门负责人 |
| phone | String(11) | 联系电话 |
| email | String(64) | 联系邮箱 |
| parent_id | Integer | 父部门ID（自关联，树形结构） |

**关联关系：**
- 部门是**树形结构**（通过 `parent_id` 自关联）
- 一个部门有 **多个用户**
- 一个部门可以被 **多个角色** 绑定（自定义数据权限时使用）

## 五、辅助表详解

### 5.1 岗位表（sys_position）

**文件：** `backend/app/api/v1/module_system/position/model.py`

| 字段 | 类型 | 说明 |
|------|------|------|
| name | String(64) | 岗位名称 |
| order | Integer | 显示排序 |

**作用：**
- 岗位是对用户职位的描述，与角色（权限）是不同维度的概念
- 一个用户可以有多个岗位

### 5.2 字典类型表（sys_dict_type）

**文件：** `backend/app/api/v1/module_system/dict/model.py`

| 字段 | 类型 | 说明 |
|------|------|------|
| dict_name | String(64) | 字典名称 |
| dict_type | String(255) | 字典类型（唯一） |

### 5.3 字典数据表（sys_dict_data）

| 字段 | 类型 | 说明 |
|------|------|------|
| dict_sort | Integer | 排序 |
| dict_label | String(255) | 显示标签 |
| dict_value | String(255) | 实际值 |
| css_class | String(255) | 样式类 |
| list_class | String(255) | 表格回显样式 |
| is_default | Boolean | 是否默认 |
| dict_type | String(255) | 所属字典类型 |
| dict_type_id | Integer | 字典类型ID（外键→sys_dict_type.id） |

**作用：**
- 用于存储系统中各种下拉选项的数据（如：性别、状态、公告类型等）
- 前端下拉框、标签显示都从这里取数据
- 避免硬编码，方便维护

### 5.4 系统参数表（sys_param）

**文件：** `backend/app/api/v1/module_system/params/model.py`

| 字段 | 类型 | 说明 |
|------|------|------|
| config_name | String(64) | 参数名称 |
| config_key | String(500) | 参数键名 |
| config_value | String(500) | 参数键值 |
| config_type | Boolean | 是否系统内置 |

**作用：**
- 存储系统运行时的配置项（如：网站标题、Logo、登录背景图等）
- 可以在管理后台动态修改，无需重启服务

### 5.5 通知公告表（sys_notice）

**文件：** `backend/app/api/v1/module_system/notice/model.py`

| 字段 | 类型 | 说明 |
|------|------|------|
| notice_title | String(64) | 公告标题 |
| notice_type | String(1) | 公告类型（1:通知 2:公告） |
| notice_content | Text | 公告内容 |

### 5.6 系统日志表（sys_log）

**文件：** `backend/app/api/v1/module_system/log/model.py`

| 字段 | 类型 | 说明 |
|------|------|------|
| type | Integer | 日志类型（1:登录日志 2:操作日志） |
| request_path | String(255) | 请求路径 |
| request_method | String(10) | 请求方式 |
| request_payload | Text/LONGTEXT | 请求体 |
| request_ip | String(50) | 请求IP地址 |
| login_location | String(255) | 登录位置 |
| request_os | String(64) | 操作系统 |
| request_browser | String(64) | 浏览器 |
| response_code | Integer | 响应状态码 |
| response_json | Text/LONGTEXT | 响应体 |
| process_time | String(20) | 处理时间 |

**作用：**
- 记录用户的所有操作，用于审计和安全追踪
- 登录日志记录谁、什么时候、从哪里登录
- 操作日志记录做了什么操作、请求参数、响应结果

## 六、中间关联表详解

### 6.1 用户角色关联表（sys_user_roles）

**文件：** `backend/app/api/v1/module_system/user/model.py`

| 字段 | 类型 | 说明 |
|------|------|------|
| user_id | Integer | 用户ID（联合主键） |
| role_id | Integer | 角色ID（联合主键） |

**关系：用户 ↔ 角色（多对多）**
- 一个用户可以有多个角色
- 一个角色可以被多个用户拥有

### 6.2 用户岗位关联表（sys_user_positions）

| 字段 | 类型 | 说明 |
|------|------|------|
| user_id | Integer | 用户ID（联合主键） |
| position_id | Integer | 岗位ID（联合主键） |

**关系：用户 ↔ 岗位（多对多）**

### 6.3 角色菜单关联表（sys_role_menus）

**文件：** `backend/app/api/v1/module_system/role/model.py`

| 字段 | 类型 | 说明 |
|------|------|------|
| role_id | Integer | 角色ID（联合主键） |
| menu_id | Integer | 菜单ID（联合主键） |

**关系：角色 ↔ 菜单（多对多）**
- 这是**权限控制的核心**
- 角色拥有哪些菜单，就拥有对应的功能权限

### 6.4 角色部门关联表（sys_role_depts）

| 字段 | 类型 | 说明 |
|------|------|------|
| role_id | Integer | 角色ID（联合主键） |
| dept_id | Integer | 部门ID（联合主键） |

**关系：角色 ↔ 部门（多对多）**
- 仅当角色的 `data_scope=5`（自定义数据权限）时使用
- 控制角色可以查看哪些部门的数据

## 七、表关系全景图

```
┌─────────────────────────────────────────────────────────────────┐
│                         用户 (sys_user)                          │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐ │
│  │ username    │  │ is_superuser│  │ dept_id ──────────────┐ │ │
│  │ password    │  │ avatar      │  │ roles ───┐            │ │ │
│  │ name        │  │ status      │  │ positions┘            │ │ │
│  └─────────────┘  └─────────────┘  └─────────────────────────┘ │
└──────────┬────────────────┬─────────────────────────────────────┘
           │                │
           │ 1:N            │ N:1
           ▼                ▼
┌──────────────────┐   ┌──────────────────┐
│   部门 (sys_dept) │   │   岗位 (sys_position) │
│  ┌─────────────┐ │   │  ┌─────────────┐ │
│  │ name        │ │   │  │ name        │ │
│  │ parent_id ──┼─┼───┼──┤ order       │ │
│  │ leader      │ │   │  └─────────────┘ │
│  └─────────────┘ │   └──────────────────┘
└──────────────────┘
           ▲
           │ N:M (sys_user_positions)
           │
           │ N:M (sys_user_roles)
           ▼
┌─────────────────────────────────────────────────────────────┐
│                      角色 (sys_role)                         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐ │
│  │ name        │  │ code        │  │ data_scope          │ │
│  │ order       │  │ status      │  │ (1:本人 2:部门      │ │
│  └─────────────┘  └─────────────┘  │  3:部门及以下 4:全部 │ │
│                                    │  5:自定义)          │ │
│                                    └─────────────────────┘ │
└────────────┬──────────────────────────────┬─────────────────┘
             │ N:M (sys_role_menus)         │ N:M (sys_role_depts)
             ▼                              ▼
┌────────────────────────┐      ┌────────────────────────┐
│     菜单 (sys_menu)     │      │     部门 (sys_dept)     │
│  ┌─────────────────┐   │      │  ┌─────────────────┐   │
│  │ name            │   │      │  │ name            │   │
│  │ type            │   │      │  │ parent_id       │   │
│  │ permission      │◄──┼──────┼──┤ code            │   │
│  │ route_path      │   │      │  └─────────────────┘   │
│  │ component_path  │   │      └────────────────────────┘
│  │ parent_id ──────┼───┼──► 树形子菜单
│  └─────────────────┘   │
└────────────────────────┘
```

## 八、权限控制的数据流转

### 8.1 登录时的权限计算

```
用户登录
    │
    ▼
验证账号密码
    │
    ▼
查询用户角色（sys_user_roles）
    │
    ▼
查询角色绑定的菜单（sys_role_menus）
    │
    ▼
收集所有权限标识（menu.permission）
    │
    ▼
返回给前端：{ userInfo, menus, permissions }
```

### 8.2 数据查询时的权限过滤

```
用户请求查询数据
    │
    ▼
后端检查用户身份
    │
    ▼
is_superuser = True?
    │
   /    \
 是      否
  │      │
  ▼      ▼
返回全部  检查角色的 data_scope
数据      │
         / | \ \ \
        1  2  3  4  5
        │  │  │  │  │
        ▼  ▼  ▼  ▼  ▼
       本人 本部门 本部门及以下 全部 自定义部门
```

## 九、设计亮点总结

| 设计 | 说明 |
|------|------|
| **统一基础字段** | `ModelMixin` + `UserMixin` 保证所有表结构一致 |
| **树形结构** | 部门、菜单都使用 `parent_id` 自关联，支持无限层级 |
| **多对多关联** | 用户-角色、角色-菜单通过中间表解耦 |
| **数据权限** | `data_scope` 字段实现精细化数据隔离 |
| **审计追踪** | `created_id`/`updated_id` 记录操作人 |
| **字典系统** | 避免硬编码，支持动态配置下拉选项 |
