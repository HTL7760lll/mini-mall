# Mini Mall 微型电商项目 — 技术设计方案

## 项目概述

基于 **waynboot-mall** 技术栈（https://github.com/wayn111/waynboot-mall），实现一个精简的微型电商项目 **mini mall**。

保留 waynboot-mall 的核心架构思想（Spring Boot 3 + JDK 17 + MyBatis-Plus + Spring Security + JWT），去掉过重中间件（Elasticsearch、RabbitMQ、xxl-job 等），简化为单体应用。

---

## 一、项目根目录与整体结构

```
E:\cc 工作\mini mall/
├── mini-mall-server/          # Spring Boot 后端
├── mini-mall-h5/              # Vue 3 H5 商城前台
└── mini-mall-admin/           # Vue 3 运营后台
```

---

## 二、技术栈与版本

| 层级 | 技术 | 版本 | 说明 |
|------|------|------|------|
| **JDK** | Java | **17** | 长期支持版本 |
| **后端框架** | Spring Boot | **3.2.x** | 参考 waynboot-mall 3.1.4 |
| **ORM** | MyBatis-Plus | **3.5.x** | 简化 CRUD |
| **数据库** | MySQL | **8.0** | 主数据库 |
| **缓存** | Redis + Lettuce | **7.x** | 验证码存储、Token 缓存 |
| **安全框架** | Spring Security | **6.x** | 认证授权 |
| **JWT** | auth0 java-jwt | **4.4.x** | 无状态 Token |
| **工具库** | Hutool | **5.8.x** | 通用工具 |
| **验证码** | Easy-Captcha | **1.6.x** | 图形验证码 |
| **API 文档** | Knife4j | **4.x** | Swagger 增强 |
| **H5 前端框架** | Vue 3 + Vite | **3.4+ / 5.x** | Composition API |
| **H5 UI 组件** | Vant | **4.x** | 移动端组件库 |
| **后台前端框架** | Vue 3 + Vite | **3.4+ / 5.x** | Composition API |
| **后台 UI 组件** | Element Plus | **2.x** | 桌面端组件库 |
| **状态管理** | Pinia | **2.x** | Vue 3 官方推荐 |
| **路由** | Vue Router | **4.x** | — |
| **HTTP 客户端** | Axios | latest | 请求拦截器注入 JWT |
| **富文本编辑器** | @wangeditor/editor | latest | 商品详情编辑 |

### 与 waynboot-mall 的差异（刻意简化的部分）

| waynboot-mall 组件 | mini mall 替代方案 | 原因 |
|-------------------|-------------------|------|
| Elasticsearch | MySQL LIKE 查询 | 微型项目数据量不大 |
| RabbitMQ | 同步处理 | 简化部署和开发 |
| xxl-job | @Scheduled 定时任务 | 任务量少，不需要分布式调度 |
| Spring Boot Admin | 无 | 单机项目无需服务监控 |
| OpenResty/Nginx | 无 | 开发阶段无需网关 |
| Maven 多模块 | 单体项目 + 包内模块 | 简化项目结构 |

---

## 三、后端源码目录（`mini-mall-server`）

```
mini-mall-server/
├── pom.xml
├── src/main/java/com/minimall/
│   ├── MiniMallApplication.java              # Spring Boot 启动类
│   │
│   ├── common/                                # ===== 通用层 =====
│   │   ├── base/
│   │   │   └── BaseEntity.java               # 基础实体 (id/createTime/updateTime/deleted)
│   │   ├── config/
│   │   │   ├── MyBatisPlusConfig.java         # MyBatis-Plus 分页插件 + 逻辑删除
│   │   │   ├── RedisConfig.java               # Redis 序列化配置
│   │   │   ├── Knife4jConfig.java             # API 文档配置
│   │   │   └── WebMvcConfig.java              # CORS 跨域配置
│   │   ├── constant/
│   │   │   └── Constants.java                 # 通用常量
│   │   ├── enums/
│   │   │   ├── OrderStatusEnum.java           # 订单状态枚举
│   │   │   ├── PayStatusEnum.java             # 支付状态枚举
│   │   │   └── ResultCode.java                # 统一返回码
│   │   ├── exception/
│   │   │   ├── BusinessException.java         # 业务异常
│   │   │   └── GlobalExceptionHandler.java    # 全局异常处理 (@RestControllerAdvice)
│   │   ├── dto/
│   │   │   └── PageResult.java                # 分页结果封装
│   │   ├── util/
│   │   │   ├── JwtUtil.java                   # JWT 签发/验证工具
│   │   │   ├── RedisUtil.java                 # Redis 操作工具
│   │   │   └── OrderNoUtil.java               # 订单号生成工具
│   │   └── wrapper/
│   │       └── R.java                         # 统一响应 { code, msg, data }
│   │
│   ├── security/                              # ===== 安全模块 =====
│   │   ├── SecurityConfig.java                # Spring Security 核心配置
│   │   ├── JwtAuthenticationFilter.java       # JWT 过滤器 (OncePerRequestFilter)
│   │   ├── JwtAuthenticationEntryPoint.java   # 未认证处理器
│   │   ├── JwtAccessDeniedHandler.java        # 权限拒绝处理器
│   │   └── LoginUser.java                     # Spring Security UserDetails 实现
│   │
│   ├── module/                                # ===== 业务模块(按领域分包) =====
│   │   │
│   │   ├── member/                            # 用户模块
│   │   │   ├── entity/Member.java
│   │   │   ├── mapper/MemberMapper.java
│   │   │   ├── service/MemberService.java
│   │   │   ├── service/impl/MemberServiceImpl.java
│   │   │   ├── controller/
│   │   │   │   ├── MemberController.java      # H5前台: 注册/登录/个人信息
│   │   │   │   └── AdminMemberController.java # 后台: 用户管理
│   │   │   ├── dto/
│   │   │   │   ├── RegisterDTO.java
│   │   │   │   ├── LoginDTO.java
│   │   │   │   └── MemberVO.java
│   │   │   └── request/
│   │   │       ├── RegisterRequest.java
│   │   │       └── LoginRequest.java
│   │   │
│   │   ├── address/                           # 收货地址模块
│   │   │   ├── entity/Address.java
│   │   │   ├── mapper/AddressMapper.java
│   │   │   ├── service/AddressService.java
│   │   │   ├── service/impl/AddressServiceImpl.java
│   │   │   ├── controller/AddressController.java
│   │   │   ├── dto/AddressVO.java
│   │   │   └── request/AddressRequest.java
│   │   │
│   │   ├── goods/                             # 商品模块
│   │   │   ├── entity/
│   │   │   │   ├── Goods.java                 # 商品 SPU
│   │   │   │   ├── GoodsSku.java              # 商品 SKU
│   │   │   │   └── GoodsCategory.java         # 商品分类
│   │   │   ├── mapper/
│   │   │   │   ├── GoodsMapper.java
│   │   │   │   ├── GoodsSkuMapper.java
│   │   │   │   └── GoodsCategoryMapper.java
│   │   │   ├── service/
│   │   │   │   ├── GoodsService.java
│   │   │   │   ├── GoodsSkuService.java
│   │   │   │   ├── GoodsCategoryService.java
│   │   │   │   └── impl/
│   │   │   │       ├── GoodsServiceImpl.java
│   │   │   │       ├── GoodsSkuServiceImpl.java
│   │   │   │       └── GoodsCategoryServiceImpl.java
│   │   │   ├── controller/
│   │   │   │   ├── GoodsController.java       # H5前台: 商品浏览/搜索/详情
│   │   │   │   ├── AdminGoodsController.java  # 后台: 商品CRUD
│   │   │   │   └── AdminCategoryController.java # 后台: 分类管理
│   │   │   ├── dto/
│   │   │   │   ├── GoodsVO.java
│   │   │   │   ├── GoodsDetailVO.java
│   │   │   │   ├── GoodsSkuVO.java
│   │   │   │   └── CategoryVO.java
│   │   │   └── request/
│   │   │       ├── GoodsPageRequest.java
│   │   │       ├── GoodsSearchRequest.java
│   │   │       └── GoodsSaveRequest.java
│   │   │
│   │   ├── cart/                              # 购物车模块
│   │   │   ├── entity/Cart.java
│   │   │   ├── mapper/CartMapper.java
│   │   │   ├── service/CartService.java
│   │   │   ├── service/impl/CartServiceImpl.java
│   │   │   ├── controller/CartController.java
│   │   │   ├── dto/CartVO.java
│   │   │   └── request/CartRequest.java
│   │   │
│   │   ├── order/                             # 订单模块
│   │   │   ├── entity/
│   │   │   │   ├── Order.java
│   │   │   │   └── OrderDetail.java
│   │   │   ├── mapper/
│   │   │   │   ├── OrderMapper.java
│   │   │   │   └── OrderDetailMapper.java
│   │   │   ├── service/
│   │   │   │   ├── OrderService.java
│   │   │   │   ├── OrderDetailService.java
│   │   │   │   └── impl/
│   │   │   │       ├── OrderServiceImpl.java  # ↓ 核心下单事务
│   │   │   │       └── OrderDetailServiceImpl.java
│   │   │   ├── controller/
│   │   │   │   ├── OrderController.java       # H5前台: 下单/支付/订单列表
│   │   │   │   └── AdminOrderController.java  # 后台: 订单管理
│   │   │   ├── dto/
│   │   │   │   ├── OrderVO.java
│   │   │   │   ├── OrderDetailVO.java
│   │   │   │   └── OrderSubmitVO.java
│   │   │   └── request/
│   │   │       ├── OrderSubmitRequest.java
│   │   │       ├── OrderPageRequest.java
│   │   │       └── PayRequest.java
│   │   │
│   │   ├── comment/                           # 评价模块
│   │   │   ├── entity/Comment.java
│   │   │   ├── mapper/CommentMapper.java
│   │   │   ├── service/CommentService.java
│   │   │   ├── service/impl/CommentServiceImpl.java
│   │   │   ├── controller/CommentController.java
│   │   │   ├── dto/CommentVO.java
│   │   │   └── request/CommentRequest.java
│   │   │
│   │   └── banner/                            # Banner 模块
│   │       ├── entity/Banner.java
│   │       ├── mapper/BannerMapper.java
│   │       ├── service/BannerService.java
│   │       ├── service/impl/BannerServiceImpl.java
│   │       ├── controller/
│   │       │   ├── BannerController.java      # H5前台: 获取Banner
│   │       │   └── AdminBannerController.java # 后台: Banner管理
│   │       ├── dto/BannerVO.java
│   │       └── request/BannerRequest.java
│   │
│   └── task/                                  # 定时任务
│       └── OrderTimeoutTask.java              # 超时未支付订单自动取消
│
├── src/main/resources/
│   ├── application.yml                        # 主配置
│   ├── application-dev.yml                    # 开发环境
│   └── mapper/                                # MyBatis XML (复杂SQL)
│       └── GoodsMapper.xml
│
└── db-init/
    └── init.sql                               # 建表脚本 + 种子数据
```

---

## 四、数据库设计

### 4.1 表关系

```
member  1 ──── N  address          (一个用户多个收货地址)
member  1 ──── N  cart             (一个用户多个购物车项)
member  1 ──── N  order            (一个用户多个订单)
member  1 ──── N  comment          (一个用户多个评价)

goods_category  1 ──── N  goods    (一个分类多个商品)
goods  1 ──── N  goods_sku         (一个商品多个 SKU)
goods  1 ──── N  cart              (一个商品被多人加入购物车)
goods  1 ──── N  comment           (一个商品多个评价)

order  1 ──── N  order_detail      (一个订单多个商品明细)
order  1 ──── 1  address           (订单快照收货地址)

banner  (独立)
```

### 4.2 建表 SQL

```sql
-- ==================== 用户表 ====================
CREATE TABLE `member` (
  `id`              BIGINT       NOT NULL AUTO_INCREMENT COMMENT '用户ID',
  `username`        VARCHAR(50)  NOT NULL COMMENT '用户名',
  `password`        VARCHAR(128) NOT NULL COMMENT '密码 (BCrypt加密)',
  `nickname`        VARCHAR(50)  DEFAULT NULL COMMENT '昵称',
  `avatar`          VARCHAR(255) DEFAULT NULL COMMENT '头像URL',
  `gender`          TINYINT      DEFAULT 0 COMMENT '性别 0未知 1男 2女',
  `phone`           VARCHAR(20)  DEFAULT NULL COMMENT '手机号',
  `role`            VARCHAR(20)  DEFAULT 'USER' COMMENT '角色 USER/ADMIN',
  `status`          TINYINT      DEFAULT 1 COMMENT '状态 1正常 0禁用',
  `last_login_time` DATETIME     DEFAULT NULL COMMENT '最后登录时间',
  `create_time`     DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time`     DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `deleted`         TINYINT      DEFAULT 0 COMMENT '逻辑删除 0未删 1已删',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户表';

-- ==================== 收货地址表 ====================
CREATE TABLE `address` (
  `id`             BIGINT       NOT NULL AUTO_INCREMENT,
  `member_id`      BIGINT       NOT NULL COMMENT '用户ID',
  `receiver_name`  VARCHAR(30)  NOT NULL COMMENT '收货人姓名',
  `receiver_phone` VARCHAR(20)  NOT NULL COMMENT '收货人电话',
  `province`       VARCHAR(20)  NOT NULL COMMENT '省',
  `city`           VARCHAR(20)  NOT NULL COMMENT '市',
  `district`       VARCHAR(50)  NOT NULL COMMENT '区',
  `detail`         VARCHAR(200) NOT NULL COMMENT '详细地址',
  `is_default`     TINYINT      DEFAULT 0 COMMENT '是否默认 1是 0否',
  `create_time`    DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time`    DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `deleted`        TINYINT      DEFAULT 0,
  PRIMARY KEY (`id`),
  KEY `idx_member_id` (`member_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='收货地址表';

-- ==================== 商品分类表 ====================
CREATE TABLE `goods_category` (
  `id`          BIGINT      NOT NULL AUTO_INCREMENT,
  `parent_id`   BIGINT      DEFAULT 0 COMMENT '父级ID, 0=一级分类',
  `name`        VARCHAR(50) NOT NULL COMMENT '分类名称',
  `icon`        VARCHAR(255) DEFAULT NULL COMMENT '图标URL',
  `sort`        INT         DEFAULT 0 COMMENT '排序值(升序)',
  `status`      TINYINT     DEFAULT 1 COMMENT '状态 1启用 0禁用',
  `create_time` DATETIME    NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` DATETIME    NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `deleted`     TINYINT     DEFAULT 0,
  PRIMARY KEY (`id`),
  KEY `idx_parent_id` (`parent_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='商品分类表';

-- ==================== 商品表 (SPU) ====================
CREATE TABLE `goods` (
  `id`             BIGINT        NOT NULL AUTO_INCREMENT COMMENT '商品ID (SPU)',
  `category_id`    BIGINT        NOT NULL COMMENT '分类ID',
  `name`           VARCHAR(200)  NOT NULL COMMENT '商品名称',
  `subtitle`       VARCHAR(500)  DEFAULT NULL COMMENT '副标题/简介',
  `main_image`     VARCHAR(255)  DEFAULT NULL COMMENT '主图URL',
  `images`         TEXT          DEFAULT NULL COMMENT '详情图URL列表 (JSON数组)',
  `detail`         LONGTEXT      DEFAULT NULL COMMENT '商品详情 (富文本HTML)',
  `price`          DECIMAL(10,2) NOT NULL COMMENT '最低售价 (展示用)',
  `original_price` DECIMAL(10,2) DEFAULT NULL COMMENT '原价/划线价',
  `stock`          INT           NOT NULL DEFAULT 0 COMMENT '总库存',
  `sales`          INT           DEFAULT 0 COMMENT '累计销量',
  `status`         TINYINT       DEFAULT 1 COMMENT '状态 1上架 0下架',
  `is_hot`         TINYINT       DEFAULT 0 COMMENT '是否热卖',
  `is_new`         TINYINT       DEFAULT 0 COMMENT '是否新品',
  `sort`           INT           DEFAULT 0 COMMENT '排序值(升序)',
  `create_time`    DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time`    DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `deleted`        TINYINT       DEFAULT 0,
  PRIMARY KEY (`id`),
  KEY `idx_category_id` (`category_id`),
  KEY `idx_status` (`status`),
  KEY `idx_name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='商品表(SPU)';

-- ==================== 商品SKU表 ====================
CREATE TABLE `goods_sku` (
  `id`          BIGINT        NOT NULL AUTO_INCREMENT,
  `goods_id`    BIGINT        NOT NULL COMMENT '商品ID (SPU)',
  `specs`       VARCHAR(500)  NOT NULL COMMENT '规格描述 (如: "颜色:白;尺寸:M")',
  `price`       DECIMAL(10,2) NOT NULL COMMENT 'SKU售价',
  `stock`       INT           NOT NULL DEFAULT 0 COMMENT 'SKU库存',
  `image`       VARCHAR(255)  DEFAULT NULL COMMENT 'SKU配图URL',
  `status`      TINYINT       DEFAULT 1 COMMENT '状态 1有效 0无效',
  `create_time` DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `deleted`     TINYINT       DEFAULT 0,
  PRIMARY KEY (`id`),
  KEY `idx_goods_id` (`goods_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='商品SKU表';

-- ==================== 购物车表 ====================
CREATE TABLE `cart` (
  `id`          BIGINT   NOT NULL AUTO_INCREMENT,
  `member_id`   BIGINT   NOT NULL COMMENT '用户ID',
  `goods_id`    BIGINT   NOT NULL COMMENT '商品ID (SPU)',
  `sku_id`      BIGINT   NOT NULL COMMENT 'SKU ID',
  `quantity`    INT      NOT NULL DEFAULT 1 COMMENT '数量',
  `checked`     TINYINT  DEFAULT 1 COMMENT '是否选中 1是 0否',
  `create_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_member_sku` (`member_id`, `sku_id`),
  KEY `idx_member_id` (`member_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='购物车表';

-- ==================== 订单表 ====================
CREATE TABLE `order` (
  `id`               BIGINT        NOT NULL AUTO_INCREMENT,
  `order_no`         VARCHAR(32)   NOT NULL COMMENT '订单号 (全局唯一)',
  `member_id`        BIGINT        NOT NULL COMMENT '用户ID',
  `total_price`      DECIMAL(10,2) NOT NULL COMMENT '商品总价',
  `freight`          DECIMAL(10,2) DEFAULT 0.00 COMMENT '运费',
  `pay_amount`       DECIMAL(10,2) NOT NULL COMMENT '实付金额',
  `pay_type`         TINYINT       DEFAULT 1 COMMENT '支付方式 1模拟支付',
  `pay_status`       TINYINT       DEFAULT 0 COMMENT '支付状态 0未支付 1已支付',
  `pay_time`         DATETIME      DEFAULT NULL COMMENT '支付时间',
  `order_status`     TINYINT       DEFAULT 0 COMMENT '订单状态 0待付款 1待发货 2待收货 3已完成 4已取消 5已退款',
  `receiver_name`    VARCHAR(30)   NOT NULL COMMENT '收货人 (下单快照)',
  `receiver_phone`   VARCHAR(20)   NOT NULL COMMENT '收货电话 (下单快照)',
  `receiver_address` VARCHAR(300)  NOT NULL COMMENT '收货地址 (下单快照)',
  `remark`           VARCHAR(500)  DEFAULT NULL COMMENT '用户备注',
  `create_time`      DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time`      DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `deleted`          TINYINT       DEFAULT 0,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_order_no` (`order_no`),
  KEY `idx_member_id` (`member_id`),
  KEY `idx_order_status` (`order_status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='订单表';

-- ==================== 订单详情表 ====================
CREATE TABLE `order_detail` (
  `id`           BIGINT        NOT NULL AUTO_INCREMENT,
  `order_id`     BIGINT        NOT NULL COMMENT '订单ID',
  `order_no`     VARCHAR(32)   NOT NULL COMMENT '订单号 (冗余)',
  `goods_id`     BIGINT        NOT NULL COMMENT '商品ID (SPU)',
  `sku_id`       BIGINT        NOT NULL COMMENT 'SKU ID',
  `goods_name`   VARCHAR(200)  NOT NULL COMMENT '商品名称 (下单快照)',
  `goods_image`  VARCHAR(255)  DEFAULT NULL COMMENT '商品主图 (下单快照)',
  `sku_specs`    VARCHAR(500)  NOT NULL COMMENT 'SKU规格 (下单快照)',
  `price`        DECIMAL(10,2) NOT NULL COMMENT '单价 (下单快照)',
  `quantity`     INT           NOT NULL COMMENT '数量',
  `total_price`  DECIMAL(10,2) NOT NULL COMMENT '小计',
  `create_time`  DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_order_id` (`order_id`),
  KEY `idx_order_no` (`order_no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='订单详情表';

-- ==================== 商品评价表 ====================
CREATE TABLE `comment` (
  `id`          BIGINT        NOT NULL AUTO_INCREMENT,
  `goods_id`    BIGINT        NOT NULL COMMENT '商品ID',
  `order_id`    BIGINT        DEFAULT NULL COMMENT '订单ID',
  `member_id`   BIGINT        NOT NULL COMMENT '用户ID',
  `content`     VARCHAR(1000) NOT NULL COMMENT '评价内容',
  `star`        TINYINT       NOT NULL COMMENT '评分 1-5',
  `images`      TEXT          DEFAULT NULL COMMENT '评价图片 (JSON数组)',
  `is_show`     TINYINT       DEFAULT 1 COMMENT '是否显示 1是 0否',
  `create_time` DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `deleted`     TINYINT       DEFAULT 0,
  PRIMARY KEY (`id`),
  KEY `idx_goods_id` (`goods_id`),
  KEY `idx_member_id` (`member_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='商品评价表';

-- ==================== Banner轮播图表 ====================
CREATE TABLE `banner` (
  `id`          BIGINT       NOT NULL AUTO_INCREMENT,
  `title`       VARCHAR(100) DEFAULT NULL COMMENT '标题',
  `image_url`   VARCHAR(255) NOT NULL COMMENT '图片URL',
  `link_url`    VARCHAR(255) DEFAULT NULL COMMENT '跳转链接',
  `link_type`   TINYINT      DEFAULT 1 COMMENT '跳转类型 1不跳转 2商品详情 3分类',
  `link_target` VARCHAR(100) DEFAULT NULL COMMENT '跳转参数 (商品ID/分类ID)',
  `sort`        INT          DEFAULT 0 COMMENT '排序',
  `status`      TINYINT      DEFAULT 1 COMMENT '1启用 0禁用',
  `create_time` DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `deleted`     TINYINT      DEFAULT 0,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Banner轮播图表';

-- ==================== 管理员种子数据 ====================
-- 密码: admin123 (BCrypt加密)
INSERT INTO `member` (`username`, `password`, `nickname`, `role`, `status`)
VALUES ('admin', '$2a$10$N.zmdr9k7uOCQb376NoUnuTJ8iAt6Z5EHsM8lE9lBOsl7iAt6Z5Eh', '管理员', 'ADMIN', 1);
```

### 4.3 设计要点

- **地址快照**：`order` 表冗余 `receiver_name/receiver_phone/receiver_address`，防止用户修改地址影响历史订单
- **商品快照**：`order_detail` 表冗余 `goods_name/goods_image/sku_specs/price`，保证历史订单数据与下单时一致
- **逻辑删除**：所有表使用 `deleted` 字段，MyBatis-Plus `@TableLogic` 自动过滤
- **库存**：`goods.stock` 为各 SKU 库存之和（冗余），实际扣减在 `goods_sku.stock` 上执行
- **搜索**：对 `goods.name` 建立索引 `idx_name`，MySQL LIKE 在数据量不大的情况下性能可接受

---

## 五、API 接口设计

### 5.1 接口规范

- H5 前台基础路径：`/api/**`
- 运营后台基础路径：`/admin-api/**`
- 请求方式：RESTful
- 数据格式：JSON
- 认证方式：Header `Authorization: Bearer <jwt_token>`
- 分页参数：`?page=1&pageSize=20`
- 分页响应：`{ code:200, data: { total, pages, records: [...] } }`
- API 文档：Knife4j，访问 `http://localhost:8080/doc.html`

---

### 5.2 H5 商城前台接口

#### 用户模块

| 方法 | 路径 | 说明 | 认证 |
|------|------|------|------|
| POST | `/api/member/register` | 用户注册 | 否 |
| POST | `/api/member/login` | 用户登录（返回 JWT Token） | 否 |
| GET | `/api/member/info` | 获取当前用户信息 | 是 |
| PUT | `/api/member/profile` | 修改个人信息 | 是 |
| GET | `/api/captcha` | 获取图形验证码 | 否 |

#### 商品模块

| 方法 | 路径 | 说明 | 认证 |
|------|------|------|------|
| GET | `/api/goods/page` | 商品分页列表（?categoryId=&sort=price_asc\|price_desc\|sales） | 否 |
| GET | `/api/goods/detail/{id}` | 商品详情（含 SKU 列表 + 评价列表） | 否 |
| GET | `/api/goods/search` | 商品搜索（?keyword=&categoryId=&sort=） | 否 |
| GET | `/api/goods/hot` | 热卖商品推荐 | 否 |
| GET | `/api/goods/new` | 新品推荐 | 否 |
| GET | `/api/category/tree` | 商品分类树 | 否 |

#### 购物车模块

| 方法 | 路径 | 说明 | 认证 |
|------|------|------|------|
| GET | `/api/cart/list` | 我的购物车列表（含商品/SKU 信息） | 是 |
| POST | `/api/cart/add` | 加入购物车（已存在则数量+1） | 是 |
| PUT | `/api/cart/update` | 修改数量 | 是 |
| PUT | `/api/cart/check` | 选中/取消选中 | 是 |
| DELETE | `/api/cart/remove/{id}` | 删除购物车项 | 是 |
| DELETE | `/api/cart/clear` | 清空已选中项 | 是 |
| GET | `/api/cart/count` | 购物车总件数 | 是 |

#### 地址模块

| 方法 | 路径 | 说明 | 认证 |
|------|------|------|------|
| GET | `/api/address/list` | 我的地址列表 | 是 |
| POST | `/api/address/save` | 新增/修改地址 | 是 |
| GET | `/api/address/{id}` | 地址详情 | 是 |
| DELETE | `/api/address/delete/{id}` | 删除地址 | 是 |
| PUT | `/api/address/default/{id}` | 设为默认地址 | 是 |

#### 订单模块

| 方法 | 路径 | 说明 | 认证 |
|------|------|------|------|
| POST | `/api/order/submit` | 提交订单（从购物车选中项生成） | 是 |
| POST | `/api/order/pay` | 模拟支付 | 是 |
| GET | `/api/order/page` | 订单分页列表（?orderStatus=） | 是 |
| GET | `/api/order/detail/{id}` | 订单详情（含订单商品明细） | 是 |
| PUT | `/api/order/cancel/{id}` | 取消订单（仅待付款状态可取消） | 是 |
| PUT | `/api/order/confirm/{id}` | 确认收货 | 是 |

#### 评价模块

| 方法 | 路径 | 说明 | 认证 |
|------|------|------|------|
| POST | `/api/comment/save` | 发表评价 | 是 |
| GET | `/api/comment/goods/{goodsId}` | 商品评价列表 | 否 |

#### Banner

| 方法 | 路径 | 说明 | 认证 |
|------|------|------|------|
| GET | `/api/banner/list` | 获取启用的 Banner 列表 | 否 |

---

### 5.3 运营后台接口

#### 商品管理

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/admin-api/goods/page` | 商品列表（?keyword=&status=&categoryId=） |
| POST | `/admin-api/goods/save` | 新增/编辑商品（含 SKU 列表） |
| GET | `/admin-api/goods/detail/{id}` | 商品详情（含 SKU） |
| PUT | `/admin-api/goods/status` | 批量上下架 `{ ids:[], status:1\|0 }` |
| DELETE | `/admin-api/goods/delete/{id}` | 逻辑删除商品 |

#### 分类管理

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/admin-api/category/tree` | 分类树 |
| POST | `/admin-api/category/save` | 新增/编辑分类 |
| DELETE | `/admin-api/category/delete/{id}` | 删除分类（无子分类时） |

#### 订单管理

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/admin-api/order/page` | 订单列表（?orderNo=&orderStatus=&page=&pageSize=） |
| GET | `/admin-api/order/detail/{id}` | 订单详情 |
| PUT | `/admin-api/order/ship` | 发货 `{ orderId, expressNo }` |
| PUT | `/admin-api/order/refund/{id}` | 同意退款 |

#### 用户管理

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/admin-api/member/page` | 用户列表（?keyword=） |
| PUT | `/admin-api/member/status` | 启用/禁用 `{ id, status }` |

#### Banner 管理

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/admin-api/banner/page` | Banner 分页列表 |
| POST | `/admin-api/banner/save` | 新增/编辑 Banner |
| DELETE | `/admin-api/banner/delete/{id}` | 删除 Banner |

#### 评论管理

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/admin-api/comment/page` | 评论列表（?goodsName=） |
| PUT | `/admin-api/comment/toggle/{id}` | 显示/隐藏评论 |

#### 文件上传

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/admin-api/upload/image` | 图片上传（返回 URL） |

#### 仪表盘

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/admin-api/dashboard/stats` | 今日订单数/销售额/新增用户/总商品数 |

---

## 六、认证方案（Spring Security + JWT）

### 6.1 认证流程

```
┌──────────┐   POST /api/member/login       ┌──────────────┐
│  前端     │ ───────────────────────────────> │  后端         │
│ (H5/后台) │ <─────────────────────────────── │  Login API   │
│          │   { code:200, data:{token, ...} }│              │
│          │                                  │  验证账号密码  │
│          │   GET /api/cart/list             │  BCrypt比对   │
│          │   Authorization: Bearer <token>  │  生成 JWT    │
│          │ ───────────────────────────────> │              │
│          │                                  │  JWT Filter  │
│          │ <─────────────────────────────── │  解析Token   │
│          │   { code:200, data:[...] }       │  设置Security │
│          │                                  │  Context     │
│          │                                  │              │
│          │   Token过期 or 无Token           │              │
│          │ ───────────────────────────────> │              │
│          │ <─────────────────────────────── │              │
│          │   { code:401, msg:"未认证" }      │  返回 401    │
└──────────┘                                  └──────────────┘
```

### 6.2 SecurityConfig 核心配置

```java
@Configuration
@EnableWebSecurity
@EnableMethodSecurity  // 启用 @PreAuthorize
public class SecurityConfig {

    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http
            .csrf(AbstractHttpConfigurer::disable)
            .sessionManagement(s -> s.sessionCreationPolicy(SessionCreationPolicy.STATELESS))
            .authorizeHttpRequests(auth -> auth
                // 公开接口
                .requestMatchers("/api/member/register", "/api/member/login", "/api/captcha").permitAll()
                .requestMatchers(HttpMethod.GET,
                    "/api/goods/**", "/api/category/**",
                    "/api/banner/**", "/api/comment/goods/**").permitAll()
                // 后台接口需要 ADMIN 角色
                .requestMatchers("/admin-api/**").hasRole("ADMIN")
                // 其余接口需要登录
                .anyRequest().authenticated()
            )
            .exceptionHandling(ex -> ex
                .authenticationEntryPoint(jwtAuthenticationEntryPoint)
                .accessDeniedHandler(jwtAccessDeniedHandler)
            )
            .addFilterBefore(jwtAuthenticationFilter, UsernamePasswordAuthenticationFilter.class);
        return http.build();
    }

    @Bean
    public PasswordEncoder passwordEncoder() {
        return new BCryptPasswordEncoder();
    }
}
```

### 6.3 JWT 载荷设计

```java
// 生成 Token
String token = JWT.create()
    .withClaim("userId", member.getId())
    .withClaim("username", member.getUsername())
    .withClaim("role", member.getRole())   // "USER" 或 "ADMIN"
    .withExpiresAt(new Date(System.currentTimeMillis() + 7200 * 1000))  // 2小时
    .sign(Algorithm.HMAC256(secret));
```

### 6.4 角色权限矩阵

| 角色 | 来源 | 可访问路径 | 说明 |
|------|------|-----------|------|
| USER | H5 注册/登录 | `/api/**` | 浏览商品、购物车、下单 |
| ADMIN | 种子数据初始化 | `/admin-api/**` + `/api/**` | 后台管理（需 `hasRole('ADMIN')`) |

---

## 七、关键业务逻辑

### 7.1 下单事务 `OrderServiceImpl.submitOrder()`

```
@Transactional(rollbackFor = Exception.class)
submitOrder(request, memberId):
  1. 校验收货地址存在且属于当前用户
  2. 查询购物车 checked=1 的记录
     → 若为空 → 抛异常 "请选择商品"
  3. 遍历购物车项:
     a) 查 goods_sku，悲观锁锁行 (SELECT ... FOR UPDATE)
     b) 校验 stock >= quantity → 否则抛异常 "XX商品库存不足"
     c) 查 goods 快照名称/图片/价格
     d) 累加 totalPrice
  4. 生成订单号 (OrderNoUtil: 时间戳 + 随机数)
  5. 创建 order 记录 (含地址快照)
  6. 批量创建 order_detail 记录 (含商品快照)
  7. 扣减 goods_sku.stock (stock = stock - quantity)
  8. 更新 goods.stock (各SKU求和)
  9. 删除购物车已下单记录
  10. 返回 OrderSubmitVO (orderId, orderNo, payAmount)
```

### 7.2 模拟支付 `OrderServiceImpl.pay()`

```
pay(memberId, payRequest):
  1. 查 order → 校验属于当前用户
  2. 校验 orderStatus == 0 (待付款) → 否则抛 "订单状态不正确"
  3. 更新:
     pay_status = 1 (已支付)
     pay_time = now()
     order_status = 1 (待发货)
  4. 返回 ok
```

### 7.3 订单状态流转

```
待付款(0) ──支付──> 待发货(1) ──发货──> 待收货(2) ──确认收货──> 已完成(3)
    │                    │
    └─ 取消/超时 ────────> 已取消(4)
                         
待付款(0) ──退款──> 已退款(5)
```

### 7.4 超时未支付自动取消

```java
@Component
public class OrderTimeoutTask {
    @Scheduled(fixedDelay = 60000) // 每60秒执行一次
    public void cancelTimeoutOrders() {
        // UPDATE `order` SET order_status = 4, update_time = NOW()
        // WHERE order_status = 0 AND create_time < NOW() - INTERVAL 30 MINUTE
    }
}
```

### 7.5 MySQL LIKE 搜索

```xml
<!-- GoodsMapper.xml -->
<select id="searchGoods" resultType="com.minimall.module.goods.entity.Goods">
    SELECT * FROM goods
    WHERE deleted = 0 AND status = 1
    <if test="keyword != null and keyword != ''">
        AND name LIKE CONCAT('%', #{keyword}, '%')
    </if>
    <if test="categoryId != null">
        AND category_id = #{categoryId}
    </if>
    ORDER BY
    <choose>
        <when test="sort == 'price_asc'">price ASC</when>
        <when test="sort == 'price_desc'">price DESC</when>
        <when test="sort == 'sales'">sales DESC</when>
        <otherwise>sort ASC, create_time DESC</otherwise>
    </choose>
</select>
```

---

## 八、前端架构

### 8.1 H5 商城前端（`mini-mall-h5`）

```
mini-mall-h5/
├── package.json
├── vite.config.ts
├── index.html
├── src/
│   ├── main.ts                   # 入口，注册 Pinia/Router/Vant
│   ├── App.vue
│   ├── router/index.ts           # Hash 模式路由
│   ├── stores/                   # Pinia
│   │   ├── user.ts               # 用户登录态 (token/userInfo)
│   │   └── cart.ts               # 购物车数量
│   ├── api/                      # 接口封装
│   │   ├── request.ts            # Axios 实例 + JWT 拦截器
│   │   ├── goods.ts
│   │   ├── member.ts
│   │   ├── cart.ts
│   │   ├── order.ts
│   │   ├── address.ts
│   │   └── comment.ts
│   ├── views/                    # 页面
│   │   ├── home/index.vue        # 首页 (Banner + 分类 + 热卖)
│   │   ├── goods/
│   │   │   ├── list.vue          # 商品列表 (无限滚动/分页)
│   │   │   ├── detail.vue        # 商品详情 (SKU 选择 + 加购)
│   │   │   └── search.vue        # 搜索结果
│   │   ├── cart/index.vue        # 购物车
│   │   ├── order/
│   │   │   ├── confirm.vue       # 确认订单 (选地址 + 提交)
│   │   │   ├── pay.vue           # 模拟支付
│   │   │   ├── list.vue          # 订单列表 (Tab 切换状态)
│   │   │   └── detail.vue        # 订单详情
│   │   ├── member/
│   │   │   ├── login.vue         # 登录
│   │   │   ├── register.vue      # 注册
│   │   │   └── profile.vue       # 个人中心
│   │   └── address/list.vue      # 地址管理
│   ├── components/               # 公共组件
│   │   ├── NavBar.vue            # 顶部导航栏
│   │   ├── TabBar.vue            # 底部 Tab 栏
│   │   ├── GoodsCard.vue         # 商品卡片
│   │   └── SkuSelector.vue       # SKU 选择弹窗
│   └── utils/index.ts
```

### 8.2 运营后台（`mini-mall-admin`）

```
mini-mall-admin/
├── package.json
├── vite.config.ts
├── index.html
├── src/
│   ├── main.ts
│   ├── App.vue
│   ├── router/index.ts           # History 模式 + 路由守卫
│   ├── stores/
│   │   └── user.ts               # 管理员登录态
│   ├── api/
│   │   ├── request.ts            # Axios + JWT 拦截器
│   │   ├── goods.ts
│   │   ├── order.ts
│   │   ├── category.ts
│   │   ├── member.ts
│   │   ├── banner.ts
│   │   ├── comment.ts
│   │   └── upload.ts
│   ├── views/
│   │   ├── login/index.vue       # 后台登录
│   │   ├── dashboard/index.vue   # 仪表盘 (ECharts)
│   │   ├── goods/
│   │   │   ├── list.vue          # 商品列表
│   │   │   └── edit.vue          # 新增/编辑商品 (含 SKU 编辑器)
│   │   ├── category/list.vue     # 分类管理 (树形表格)
│   │   ├── order/
│   │   │   ├── list.vue          # 订单列表
│   │   │   └── detail.vue        # 订单详情 (可操作发货)
│   │   ├── member/list.vue       # 用户列表
│   │   ├── banner/list.vue       # Banner 管理
│   │   └── comment/list.vue      # 评论管理
│   ├── components/
│   │   ├── Sidebar.vue           # 侧边菜单
│   │   ├── HeaderBar.vue         # 顶栏
│   │   ├── SkuEditor.vue         # SKU 编辑器组件
│   │   └── ImageUpload.vue       # 图片上传组件
│   └── utils/index.ts
```

### 8.3 Axios 拦截器（H5 示例）

```typescript
// mini-mall-h5/src/api/request.ts
import axios from 'axios';
import { showToast } from 'vant';
import router from '@/router';

const request = axios.create({
  baseURL: '/api',
  timeout: 15000,
});

// 请求拦截：自动注入 JWT
request.interceptors.request.use(config => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// 响应拦截：统一错误处理
request.interceptors.response.use(
  res => {
    const { code, msg, data } = res.data;
    if (code === 200) return data;
    showToast(msg || '请求失败');
    return Promise.reject(new Error(msg));
  },
  err => {
    if (err.response?.status === 401) {
      localStorage.removeItem('token');
      router.push('/login');
    }
    showToast('网络异常');
    return Promise.reject(err);
  }
);

export default request;
```

---

## 九、配置文件

### `application-dev.yml`

```yaml
server:
  port: 8080

spring:
  datasource:
    url: jdbc:mysql://localhost:3306/mini_mall?useUnicode=true&characterEncoding=utf8mb4&serverTimezone=Asia/Shanghai
    username: root
    password: root
    driver-class-name: com.mysql.cj.jdbc.Driver

  data:
    redis:
      host: localhost
      port: 6379

  servlet:
    multipart:
      max-file-size: 10MB

mybatis-plus:
  global-config:
    db-config:
      logic-delete-field: deleted
      logic-delete-value: 1
      logic-not-delete-value: 0
  mapper-locations: classpath:mapper/**/*.xml
  configuration:
    log-impl: org.apache.ibatis.logging.stdout.StdOutImpl

jwt:
  secret: mini-mall-jwt-secret-key-2024-must-be-256-bits-at-least!!
  expiration: 7200

knife4j:
  enable: true

upload:
  path: ./uploads/
```

---

## 十、实施计划

| Phase | 内容 | 预估 | 关键产出 |
|-------|------|------|---------|
| **1. 项目骨架** | Maven 项目创建、依赖导入、启动类、配置文件、建表 SQL | 0.5天 | `pom.xml`, `MiniMallApplication`, `init.sql` |
| **2. 通用层** | R.java, BaseEntity, GlobalExceptionHandler, 枚举, 配置类, JwtUtil, RedisUtil | 0.5天 | `common/*` 全部 |
| **3. 安全模块** | SecurityConfig, JWT Filter, Login/UserDetails, 注册登录接口 | 1天 | `security/*`, `MemberController` |
| **4. 商品模块** | 分类 CRUD, 商品 CRUD, SKU, MySQL LIKE 搜索 + H5 列表/详情/搜索页 | 2天 | `module/goods/*`, H5 goods 页面 |
| **5. 用户+地址** | 注册登录前端、Token 存储、个人中心、地址管理 CRUD | 1天 | `module/member`, `module/address`, H5 页面 |
| **6. 购物车** | 购物车 CRUD + H5 购物车页面 | 1天 | `module/cart/*`, H5 cart 页面 |
| **7. 订单+支付** | 下单事务、模拟支付、订单状态流转、超时取消 | 2天 | `module/order/*`, `task/*`, H5 order 页面 |
| **8. 后台管理** | 商品/分类/订单/用户/Banner/评论管理 + 仪表盘 + 图片上传 | 2天 | Admin*Controller, `mini-mall-admin` 全部 |
| **9. 首页+Banner+评价** | H5 首页装修、Banner 前后端、商品评价、管理员种子数据 | 1天 | `module/banner`, `module/comment`, H5 首页 |
| **总计** | | **11天** | |

---

## 十一、验证步骤

1. **数据库**：启动 MySQL + Redis → 执行 `init.sql` 建表 → 确认表结构和种子数据
2. **后端启动**：`mvn spring-boot:run` → 访问 `http://localhost:8080/doc.html` 确认 Knife4j 可用
3. **接口测试**（Knife4j）：注册用户 → 登录获取 Token → 测试各业务接口
4. **H5 前端**：`npm install && npm run dev` → 浏览商品 → 注册登录 → 加购 → 下单 → 模拟支付 → 查看订单
5. **后台前端**：`npm install && npm run dev` → 管理员 admin/admin123 登录 → 管理商品/分类/订单
6. **超时取消**：创建订单不支付 → 等 30 分钟 → 确认订单自动取消
