CREATE database if NOT EXISTS `itsm-admin` default character
set utf8mb4 collate utf8mb4_general_ci;
USE `itsm-admin`;
SET NAMES utf8mb4;

DROP TABLE IF EXISTS `sys_users`;
create table sys_users
(
    user_id     bigint       not null comment '用户id' primary key,
    username    varchar(20)  not null comment '登录用户名',
    password    varchar(200) not null comment '登录密码',
    nickname    varchar(20)  null comment '昵称',
    email       varchar(30)  null comment '邮箱',
is_active   tinyint(1
)
not null comment '是否激活[0未激活/1已激活]',
is_delete tinyint
(
1
)
not null comment '是否删除[0未删除/1已删除]',
create_time datetime not null on
update CURRENT_TIMESTAMP comment '创建时间',
update_time datetime not null on
update CURRENT_TIMESTAMP comment '更新时间',
avatar varchar(200)null comment '头像[CDN链接]',
phone varchar(11)null comment '手机号',
constraint username
unique(username)
);

INSERT INTO `sys_users`(user_id, username, password, nickname, email, is_active, is_delete, create_time, update_time,
avatar, phone)
VALUES (1580216098635255808, 'admin', '$2b$12$IFvqqCMwlLNGA3h6WoTI2..BVKYzEfNow5DsbMMj.Tnl66lT0ph.G', 'admin', null, 1,
0, '2022-10-12 23:17:32', '2022-10-12 23:17:32', null, null);
INSERT INTO `sys_users`(user_id, username, password, nickname, email, is_active, is_delete, create_time, update_time,
avatar, phone)
VALUES (1580435499548545024, 'itsm001', '$2b$12$NFzcxzSdN9KZ9Jc2Ji0Kqur3sPinhj2yJB9.pFz3EqDKrPkt3jOcS', null, null, 1,
0, '2022-10-13 13:49:21', '2022-10-13 13:49:21', null, null);

