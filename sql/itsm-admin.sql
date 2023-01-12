create table sys_users
(
    user_id     bigint       not null comment '用户id'
        primary key,
    username    varchar(20)  not null comment '登录用户名',
    password    varchar(200) not null comment '登录密码',
    nickname    varchar(20)  null comment '昵称',
    email       varchar(30)  null comment '邮箱',
    phone       varchar(11)  null comment '手机号',
    is_active   tinyint(1)   not null comment '是否激活[0未激活/1已激活]',
    is_delete   tinyint(1)   not null comment '是否删除[0未删除/1已删除]',
    create_time datetime     not null on update CURRENT_TIMESTAMP comment '创建时间',
    update_time datetime     not null on update CURRENT_TIMESTAMP comment '更新时间',
    avatar      varchar(200) null comment '头像[CDN链接]',
    constraint username
        unique (username)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

INSERT INTO `itsm-admin`.sys_users (user_id, username, password, nickname, email, phone, is_active, is_delete, create_time, update_time, avatar) VALUES (1580216098635255808, 'admin', '$2b$12$IFvqqCMwlLNGA3h6WoTI2..BVKYzEfNow5DsbMMj.Tnl66lT0ph.G', 'admin', null, null, 1, 0, '2022-10-12 23:17:32', '2022-10-12 23:17:32', null);
INSERT INTO `itsm-admin`.sys_users (user_id, username, password, nickname, email, phone, is_active, is_delete, create_time, update_time, avatar) VALUES (1580435499548545024, 'itsm001', '$2b$12$NFzcxzSdN9KZ9Jc2Ji0Kqur3sPinhj2yJB9.pFz3EqDKrPkt3jOcS', null, null, null, 1, 0, '2022-10-13 13:49:21', '2022-11-09 18:30:53', null);
INSERT INTO `itsm-admin`.sys_users (user_id, username, password, nickname, email, phone, is_active, is_delete, create_time, update_time, avatar) VALUES (1584464115051663360, 'admin001', '$2b$12$rMZ2KlRRjBJ4pTghNt.3re9sS7oFjryRYMJp/qtE7WDsX76G5hFkG', null, null, null, 0, 0, '2022-10-24 16:36:27', '2022-11-08 23:12:27', null);
INSERT INTO `itsm-admin`.sys_users (user_id, username, password, nickname, email, phone, is_active, is_delete, create_time, update_time, avatar) VALUES (1584521618812702720, '韩强1', '$2b$12$0eefc3T6LVvAa6Tlva5QF.VZOBQn3.lWiaBWLbRu6gHLFRKsKaUmS', null, null, null, 0, 0, '2022-11-02 10:04:39', '2022-11-08 23:14:40', null);
INSERT INTO `itsm-admin`.sys_users (user_id, username, password, nickname, email, phone, is_active, is_delete, create_time, update_time, avatar) VALUES (1584521627612352512, '韩强12', '$2b$12$M9Htpf.zgUbqGPBaBqWh4OkBUUFLy/CbU.sNuC2rsMHqMCXhZjDYC', null, null, null, 1, 0, '2022-11-02 10:04:39', '2022-11-06 15:24:15', null);
INSERT INTO `itsm-admin`.sys_users (user_id, username, password, nickname, email, phone, is_active, is_delete, create_time, update_time, avatar) VALUES (1584521637322166272, '韩强312', '$2b$12$RQS4UfSTuQKhUm7IeC7UUeKxcmrZ8jA.UuZMcPcJX6PCYKc5mchOq', null, null, null, 1, 0, '2022-10-24 20:10:32', '2022-10-24 20:26:12', null);
INSERT INTO `itsm-admin`.sys_users (user_id, username, password, nickname, email, phone, is_active, is_delete, create_time, update_time, avatar) VALUES (1584521647921172480, '韩强3142', '$2b$12$sf45kFmNmtAboQerbGieH.1fbETf2kzRY9H9AYlr/Td30ZoNsqVyK', null, null, null, 1, 0, '2022-10-24 20:10:32', '2022-10-24 20:26:14', null);
INSERT INTO `itsm-admin`.sys_users (user_id, username, password, nickname, email, phone, is_active, is_delete, create_time, update_time, avatar) VALUES (1584521662169223168, '韩强31542', '$2b$12$rJot05QcyoKFx7hH.db/wOYE4hpLNwBCV7Mky3yYE/yAgMJD49Kp.', null, null, null, 1, 0, '2022-10-24 20:10:32', '2022-10-24 20:26:18', null);
INSERT INTO `itsm-admin`.sys_users (user_id, username, password, nickname, email, phone, is_active, is_delete, create_time, update_time, avatar) VALUES (1586291242348711936, 'pyb0924', '$2b$12$lPUTjUPtK7hMSIizIStExOkoCjFReNk0JhZ3F6D0lUF0VpjKcR2XG', null, null, null, 1, 0, '2022-10-26 00:01:41', '2022-11-08 22:28:05', null);
INSERT INTO `itsm-admin`.sys_users (user_id, username, password, nickname, email, phone, is_active, is_delete, create_time, update_time, avatar) VALUES (1586292494910492672, 'test1', '$2b$12$I9dJcYLzb.cLJg6YFLEHHOarSWbobtr4S/nZ7Y63LQ70rv/KQoPBy', null, null, null, 1, 0, '2022-10-26 00:01:41', '2022-10-29 17:42:57', null);
INSERT INTO `itsm-admin`.sys_users (user_id, username, password, nickname, email, phone, is_active, is_delete, create_time, update_time, avatar) VALUES (1586303314671308800, 'test2', '$2b$12$zZHZPFL6XdIwBJ3J6avWMem246ut4ZxrKWkDhbHOSsGHAqev1qmue', null, null, null, 1, 0, '2022-10-26 00:01:41', '2022-10-29 18:25:57', null);
INSERT INTO `itsm-admin`.sys_users (user_id, username, password, nickname, email, phone, is_active, is_delete, create_time, update_time, avatar) VALUES (1586303407843577856, 'test3', '$2b$12$7pp2NsiJrMSoqwqC7BxVUOGMSz56jI5tXgvjJVC0P1/v6ybbsW9ca', null, null, null, 1, 0, '2022-10-26 00:01:41', '2022-10-29 18:26:19', null);
INSERT INTO `itsm-admin`.sys_users (user_id, username, password, nickname, email, phone, is_active, is_delete, create_time, update_time, avatar) VALUES (1587658679329624064, 'admin0001', '$2b$12$fVtRdmjk7O9PhmgGwMCMV.wKLdKSH1R./pfmBy90siBKSZ3zWSIia', null, null, null, 1, 0, '2022-11-01 11:56:17', '2022-11-08 23:18:19', null);
INSERT INTO `itsm-admin`.sys_users (user_id, username, password, nickname, email, phone, is_active, is_delete, create_time, update_time, avatar) VALUES (1589165033236074496, '权限测试', '$2b$12$tPzCnVupTH0/q4fuMA15xe8eoTRsgsIIfsyX7FyfYsxAKHG0def9i', null, null, null, 0, 0, '2022-11-06 15:56:00', '2022-11-06 18:02:17', null);
INSERT INTO `itsm-admin`.sys_users (user_id, username, password, nickname, email, phone, is_active, is_delete, create_time, update_time, avatar) VALUES (1589196937733738496, '权限测试2', '$2b$12$2deBiAmPZ/nw5oqTc4X6nOkmbm7KoO1YVS8UD2kqyfLyOSu6IAreK', null, null, null, 0, 0, '2022-11-06 15:56:00', '2022-11-06 18:05:46', null);
INSERT INTO `itsm-admin`.sys_users (user_id, username, password, nickname, email, phone, is_active, is_delete, create_time, update_time, avatar) VALUES (1589197482364112896, '权限测试3', '$2b$12$9cWjsTfcSUfOI1rZpqaCV.4RxBLjJ0/dCp9eEY/RkU/RxmAT5A79K', null, null, null, 1, 0, '2022-11-06 18:05:24', '2022-11-06 18:06:20', null);
INSERT INTO `itsm-admin`.sys_users (user_id, username, password, nickname, email, phone, is_active, is_delete, create_time, update_time, avatar) VALUES (1592811129033216000, '123min', '$2b$12$NMTxJtMDCKFE7fkjVEUskubmTCgEXDirgxpCPPABHdmbd5pJ6wCYW', null, null, null, 0, 0, '2022-11-08 23:18:11', '2022-11-16 17:26:07', null);
INSERT INTO `itsm-admin`.sys_users (user_id, username, password, nickname, email, phone, is_active, is_delete, create_time, update_time, avatar) VALUES (1592869994735108096, 'test5', '$2b$12$0HVFelMBql9C/kcWhRDrY.nPZvBv.zWsO2/LpcJNsHjNgpN0EpccC', null, null, null, 1, 0, '2022-11-08 23:18:11', '2022-11-16 21:19:35', null);


create table sys_permissions
(
    perm_id     bigint      not null
        primary key,
    perm_name   varchar(32) not null,
    type        int         null,
    perm_pid    bigint      null,
    identifier  varchar(30) null comment '权限标识',
    client_type tinyint     null comment '客户端类型: 0 APP 1 Web/PC',
    is_delete   tinyint(1)  not null,
    create_time datetime    not null,
    update_time datetime    not null,
    constraint identifier
        unique (identifier),
    constraint sys_permissions_perm_name_uindex
        unique (perm_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

INSERT INTO `itsm-admin`.sys_permissions (perm_id, perm_name, type, perm_pid, identifier, client_type, is_delete, create_time, update_time) VALUES (1584446275376517120, '用户管理', 1, null, 'user', 0, 0, '2022-10-24 15:26:44', '2022-10-24 15:26:44');
INSERT INTO `itsm-admin`.sys_permissions (perm_id, perm_name, type, perm_pid, identifier, client_type, is_delete, create_time, update_time) VALUES (1584446444692180992, '用户新增', 2, 1584446275376517120, 'user:add', 0, 0, '2022-10-24 15:27:24', '2022-10-24 15:27:24');
INSERT INTO `itsm-admin`.sys_permissions (perm_id, perm_name, type, perm_pid, identifier, client_type, is_delete, create_time, update_time) VALUES (1584446496886099968, '用户编辑', 2, 1584446275376517120, 'user:edit', 0, 0, '2022-10-24 15:27:37', '2022-10-24 15:27:37');
INSERT INTO `itsm-admin`.sys_permissions (perm_id, perm_name, type, perm_pid, identifier, client_type, is_delete, create_time, update_time) VALUES (1584446603446587392, '用户删除', 2, 1584446275376517120, 'user:delete', 0, 0, '2022-10-24 15:28:02', '2022-10-24 15:28:02');
INSERT INTO `itsm-admin`.sys_permissions (perm_id, perm_name, type, perm_pid, identifier, client_type, is_delete, create_time, update_time) VALUES (1589987633008873472, '数据地图', 0, null, 'map', 0, 0, '2022-11-08 22:26:06', '2022-11-08 22:26:06');


create table sys_user_permission
(
    id          bigint            not null comment '用户权限关系ID'
        primary key,
    user_id     bigint            not null comment '用户ID',
    perm_id     bigint            not null comment '权限ID',
    is_delete   tinyint default 0 not null,
    create_time datetime          not null comment '创建时间',
    update_time datetime          not null comment '更新时间',
    constraint sys_user_permission_user_id_perm_id_uindex
        unique (user_id, perm_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 comment '用户权限关系表';

INSERT INTO `itsm-admin`.sys_user_permission (id, user_id, perm_id, is_delete, create_time, update_time) VALUES (1584450702380503040, 1580216098635255808, 1584446275376517120, 0, '2022-10-24 15:44:19', '2022-10-24 15:44:19');
INSERT INTO `itsm-admin`.sys_user_permission (id, user_id, perm_id, is_delete, create_time, update_time) VALUES (1584452350712614912, 1580216098635255808, 1584446444692180992, 0, '2022-10-24 15:50:52', '2022-10-24 15:50:52');
INSERT INTO `itsm-admin`.sys_user_permission (id, user_id, perm_id, is_delete, create_time, update_time) VALUES (1584452375194767360, 1580216098635255808, 1584446496886099968, 0, '2022-10-24 15:50:58', '2022-10-24 15:50:58');
INSERT INTO `itsm-admin`.sys_user_permission (id, user_id, perm_id, is_delete, create_time, update_time) VALUES (1584452414793191424, 1580216098635255808, 1584446603446587392, 0, '2022-10-24 15:51:07', '2022-10-24 15:51:08');
INSERT INTO `itsm-admin`.sys_user_permission (id, user_id, perm_id, is_delete, create_time, update_time) VALUES (1584452432719646720, 1580216098635255808, 1584446902865367040, 0, '2022-10-24 15:51:12', '2022-10-24 15:51:12');
INSERT INTO `itsm-admin`.sys_user_permission (id, user_id, perm_id, is_delete, create_time, update_time) VALUES (1584452457008861184, 1580216098635255808, 1584447577754046464, 0, '2022-10-24 15:51:17', '2022-10-24 15:51:18');
INSERT INTO `itsm-admin`.sys_user_permission (id, user_id, perm_id, is_delete, create_time, update_time) VALUES (1584452482547978240, 1580216098635255808, 1584447631415971840, 0, '2022-10-24 15:51:24', '2022-10-24 15:51:24');
INSERT INTO `itsm-admin`.sys_user_permission (id, user_id, perm_id, is_delete, create_time, update_time) VALUES (1584452505679564800, 1580216098635255808, 1584447850501246976, 0, '2022-10-24 15:51:29', '2022-10-24 15:51:29');
INSERT INTO `itsm-admin`.sys_user_permission (id, user_id, perm_id, is_delete, create_time, update_time) VALUES (1587665183940153344, 1587665182820274176, 1584446444692180992, 0, '2022-11-01 11:56:17', '2022-11-02 12:37:31');
INSERT INTO `itsm-admin`.sys_user_permission (id, user_id, perm_id, is_delete, create_time, update_time) VALUES (1587665183948541952, 1587665182820274176, 1584446496886099968, 0, '2022-11-01 11:56:17', '2022-11-02 12:37:31');


