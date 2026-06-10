# Mini Mall — 微型电商项目

基于 **Django + Django REST Framework** 的微型电商项目，后端已完成。

## 技术栈 (实际安装版本)

| 层级 | 技术 | 版本 |
|------|------|------|
| 语言 | Python | 3.10+ |
| 框架 | Django | 5.2.15 |
| API | Django REST Framework | 3.17.1 |
| 认证 | djangorestframework-simplejwt | 5.3+ |
| 跨域 | django-cors-headers | 4.3+ |
| 过滤 | django-filter | 23.5+ |
| 数据库 | SQLite (开发) | 零配置 |
| 测试 | requests | 最新版 |

## 项目状态

- **后端**: ✅ 全部完成，31项测试 29通过
- **后台管理**: ✅ Django Admin 开箱即用
- **H5前端**: 待开发 (API 已就绪)
- **运行中**: `http://localhost:8080`

## 项目结构

```
E:\cc 工作\mini mall\
├── CLAUDE.md                         # 项目说明 (本文件)
├── DESIGN.md                         # 设计方案
├── mini-mall-django/                 # Django 项目
│   ├── manage.py                     # Django 命令入口
│   ├── requirements.txt              # Python 依赖
│   ├── db.sqlite3                    # SQLite 数据库 (含种子数据)
│   ├── mini_mall/                    # 项目配置
│   │   ├── settings.py               # Django 设置
│   │   ├── urls.py                   # 总路由
│   │   ├── wsgi.py
│   │   └── asgi.py
│   ├── apps/                         # 6 个业务 App
│   │   ├── member/                   # 用户 + 收货地址
│   │   ├── goods/                    # 商品 + 分类 + SKU
│   │   ├── cart/                     # 购物车
│   │   ├── order/                    # 订单 + 订单详情
│   │   ├── banner/                   # 轮播图
│   │   └── comment/                  # 商品评价
│   └── media/                        # 上传文件目录
```

## 已录入的种子数据

| 类型 | 数量 | 详情 |
|------|------|------|
| 商品分类 | 8 个 | 5个一级(手机/电脑/电器/服装/食品) + 3个二级 |
| 商品 | 5 个 | iPhone15/Huawei60/Xiaomi14/MacBook/ThinkPad |
| SKU | 9 个 | 颜色/存储/内存等规格组合 |
| Banner | 3 个 | 跳转商品详情或分类列表 |
| 管理员 | 1 个 | admin / admin123 |

## 快速启动

```bash
cd "E:\cc 工作\mini mall\mini-mall-django"

# 安装依赖 (首次)
pip install -r requirements.txt

# 数据库已存在(db.sqlite3)，跳过 migrate
# 如需重建: python manage.py migrate

# 启动服务器
python manage.py runserver 0.0.0.0:8080
```

## 访问地址

| 页面 | URL | 说明 |
|------|-----|------|
| Django Admin | `http://localhost:8080/admin/` | 后台管理系统 (admin/admin123) |
| API 浏览 | `http://localhost:8080/api/goods/page/` | DRF 自带可交互 API 页面 |

## 默认账号

| 用户名 | 密码 | 角色 |
|--------|------|------|
| `admin` | `admin123` | 管理员 (ADMIN) |

## 全部 API (测试通过 ✅)

### 公开接口 (无需登录)
| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/member/register/` | 注册 |
| POST | `/api/member/login/` | 登录，返回 JWT Token |
| GET | `/api/goods/page/` | 商品分页 (?categoryId=&keyword=&sort=price_asc) |
| GET | `/api/goods/detail/{id}/` | 商品详情 (含 SKU 列表) |
| GET | `/api/goods/hot/` | 热卖推荐 Top10 |
| GET | `/api/goods/new/` | 新品推荐 Top10 |
| GET | `/api/goods/category/tree/` | 分类树 (两级) |
| GET | `/api/banner/list/` | 启用 Banner 列表 |
| GET | `/api/comment/goods/{goodsId}/` | 商品评价列表 |

### 需登录 (Header: `Authorization: Bearer <token>`)
| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/member/info/` | 当前用户信息 |
| PUT | `/api/member/info/` | 修改个人信息 |
| GET | `/api/member/address/` | 地址列表 |
| POST | `/api/member/address/` | 新增地址 |
| PUT | `/api/member/address/{id}/` | 修改地址 |
| DELETE | `/api/member/address/{id}/` | 删除地址 (逻辑删) |
| PUT | `/api/member/address/{id}/default/` | 设为默认 |
| GET | `/api/cart/list/` | 购物车列表 |
| POST | `/api/cart/add/` | 加购 {goodsId, skuId, quantity} |
| PUT | `/api/cart/update/` | 改数量 {cartId, quantity} |
| PUT | `/api/cart/check/{id}/` | 选中/取消 |
| DELETE | `/api/cart/remove/{id}/` | 删除购物车项 |
| DELETE | `/api/cart/clear/` | 清空已选中 |
| GET | `/api/cart/count/` | 购物车数量 |
| POST | `/api/order/submit/` | 提交订单 {addressId, remark} |
| POST | `/api/order/pay/` | 模拟支付 {orderId} |
| PUT | `/api/order/cancel/{id}/` | 取消订单 (仅待付款) |
| PUT | `/api/order/confirm/{id}/` | 确认收货 (仅待收货) |
| GET | `/api/order/page/` | 订单列表 (?orderStatus=) |
| GET | `/api/order/detail/{id}/` | 订单详情 (含商品明细) |
| POST | `/api/comment/save/` | 发表评价 {goodsId, orderId, content, star} |

### 统一响应格式

```json
{"code": 200, "msg": "success", "data": {...}}
{"code": 400, "msg": "错误信息"}
```

分页格式：`{"total": N, "pages": N, "current": N, "size": 20, "records": [...]}`

## 关键业务逻辑

### 下单流程 (`apps/order/views.py order_submit`)
1. 校验收货地址
2. 查询购物车 checked 项
3. 事务内：逐个校验 SKU 库存 → 扣库存 → 快照商品信息 → 生成订单号 → 创建订单+明细 → 清空购物车
4. 库存不足则全部回滚

### 订单状态流转
```
0待付款 ──支付──▶ 1待发货 ──发货──▶ 2待收货 ──确认──▶ 3已完成
   │                  │
   └──取消──▶ 4已取消   └──退款──▶ 5已退款
```
- 取消/退款时自动恢复库存

### Django Admin 后台功能
- **商品管理**: CRUD + SKU 内联编辑 + 上下架/热卖/新品标记
- **订单管理**: 列表查看 + 详情 + 批量发货 + 批量退款
- **分类管理**: 查看/编辑两级分类
- **Banner 管理**: 排序 + 启用/禁用 + 跳转类型
- **用户管理**: 查看/启用/禁用 + 角色管理
- **评论管理**: 显示/隐藏
