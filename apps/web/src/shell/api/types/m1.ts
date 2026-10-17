// 由 contracts/m1/openapi.yaml 生成，请勿手改。重新生成：pnpm gen:api
export interface paths {
    "/api/m1/v1/rooms": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /**
         * 浏览可用自习室（M1-RSV-01）
         * @description 只返回学生可见（院系专属仅本院系，BR-10）、已开放的自习室。
         */
        get: operations["browse_rooms_api_m1_v1_rooms_get"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/m1/v1/seats/search": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /**
         * 条件搜索座位（M1-SRH-01）
         * @description 结果按自习室分组；标记多选须全部满足；P95 < 1 秒（NFR-14）。
         */
        get: operations["search_seats_api_m1_v1_seats_search_get"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/m1/v1/seats/{seat_id}/timeline": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /**
         * 座位当日各整点时段状态（M1-SRH-02）
         * @description 不显示他人身份，只给状态类别。
         */
        get: operations["seat_timeline_api_m1_v1_seats__seat_id__timeline_get"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/m1/v1/bookings/history": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /**
         * 历史预约（M1-HIS-01）
         * @description 按时间倒序分页；已注销座位仍显示当时的编号与自习室名称。
         */
        get: operations["booking_history_api_m1_v1_bookings_history_get"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/m1/v1/bookings/{booking_id}/rebook": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /**
         * 再次预约该座位前的检查（M1-HIS-02）
         * @description 前端据此预填座位；座位不可用时给出原因并引导回搜索。
         */
        get: operations["rebook_hint_api_m1_v1_bookings__booking_id__rebook_get"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/m1/v1/bookings": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /**
         * 创建预约（M1-RSV-02）
         * @description 按 BR-01 ~ BR-10 与暂停状态校验；规则不满足返回 RULE_VIOLATION 并给出规则编号；同一 Idempotency-Key 只产生一条预约；并发抢同一座位只有一人成功。
         */
        post: operations["create_booking_api_m1_v1_bookings_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/m1/v1/bookings/current": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** 我的当前与即将开始的预约（M1-RSV-04） */
        get: operations["current_bookings_api_m1_v1_bookings_current_get"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/m1/v1/bookings/{booking_id}": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** 预约详情（本人） */
        get: operations["get_booking_api_m1_v1_bookings__booking_id__get"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/m1/v1/bookings/{booking_id}/cancel": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /**
         * 取消预约（M1-RSV-03）
         * @description 签到截止前可取消「待签到」预约，不计违约，座位立即释放（BR-11）。
         */
        post: operations["cancel_booking_api_m1_v1_bookings__booking_id__cancel_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/m1/v1/checkin/candidate": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /**
         * 扫码后找到本人在该室处于签到窗口内的预约（M1-CHK-04）
         * @description 没有时返回 null，前端提示原因并给出「去预约」入口。
         */
        get: operations["checkin_candidate_api_m1_v1_checkin_candidate_get"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/m1/v1/bookings/{booking_id}/checkin": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /**
         * 签到（M1-CHK-03、04）
         * @description 校验：本人、待签到、在窗口内（BR-13）、码属于该室且有效（BR-16）、10 分钟内输错不超过 5 次（BR-17）。
         */
        post: operations["checkin_api_m1_v1_bookings__booking_id__checkin_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/m1/v1/screen/code": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /**
         * 屏幕端获取当前签到码（M1-CHK-02）
         * @description 用请求头 X-Device-Token 鉴权；设备令牌只能取绑定自习室的码，吊销后被拒绝。
         */
        get: operations["screen_code_api_m1_v1_screen_code_get"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/m1/v1/admin/screens": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** 屏幕终端列表 */
        get: operations["list_screens_api_m1_v1_admin_screens_get"];
        put?: never;
        /** 为自习室生成屏幕设备令牌 */
        post: operations["create_screen_api_m1_v1_admin_screens_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/m1/v1/admin/screens/{device_id}/revoke": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /** 吊销屏幕设备令牌 */
        post: operations["revoke_screen_api_m1_v1_admin_screens__device_id__revoke_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/m1/v1/violations/mine": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** 我的违约与处罚状态（M1-VIO-02） */
        get: operations["my_violations_api_m1_v1_violations_mine_get"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/m1/v1/admin/violations": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** 范围内违约查询（M1-VIO-02） */
        get: operations["list_violations_api_m1_v1_admin_violations_get"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/m1/v1/admin/violations/{violation_id}/revoke": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /**
         * 撤销违约（M1-VIO-04）
         * @description 原因必填、写入审计；撤销后重新计算处罚状态。
         */
        post: operations["revoke_violation_api_m1_v1_admin_violations__violation_id__revoke_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/m1/v1/bookings/{booking_id}/checkout": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /**
         * 提前签退（M1-RSV-06）
         * @description 自下一个整点起释放剩余时段，状态为已完成（提前签退）。
         */
        post: operations["checkout_api_m1_v1_bookings__booking_id__checkout_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/m1/v1/rooms/{room_id}/seat-map": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** 座位图（M1-SRH-03） */
        get: operations["seat_map_api_m1_v1_rooms__room_id__seat_map_get"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/m1/v1/seats/{seat_id}/alternatives": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** 替代推荐：同室同标记的可约座位（M1-SRH-04） */
        get: operations["alternatives_api_m1_v1_seats__seat_id__alternatives_get"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/m1/v1/favorites": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** 我的常用座位（M1-HIS-03） */
        get: operations["favorites_api_m1_v1_favorites_get"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/m1/v1/favorites/{seat_id}": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        /** 收藏座位（M1-HIS-03） */
        put: operations["add_favorite_api_m1_v1_favorites__seat_id__put"];
        post?: never;
        /** 取消收藏（M1-HIS-03） */
        delete: operations["remove_favorite_api_m1_v1_favorites__seat_id__delete"];
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/m1/v1/admin/settings": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** 查看 M1 业务参数 */
        get: operations["list_settings_api_m1_v1_admin_settings_get"];
        /**
         * 修改 M1 业务参数（M1-CFG-01）
         * @description 校验取值范围；写入审计；只作用于此后新建的预约（BR-21）。
         */
        put: operations["update_settings_api_m1_v1_admin_settings_put"];
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/m1/v1/admin/bookings/{booking_id}/cancel": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /**
         * 管理员取消预约（M1-RSV-07）
         * @description 限数据范围内；通知学生、不计违约、写入审计。
         */
        post: operations["admin_cancel_api_m1_v1_admin_bookings__booking_id__cancel_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/m1/v1/admin/bookings/{booking_id}/checkin": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /** 管理员补签（M1-CHK-05，P2） */
        post: operations["admin_checkin_api_m1_v1_admin_bookings__booking_id__checkin_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/m1/v1/admin/dashboard": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /**
         * 实时看板（M1-OPS-01）
         * @description 数据延迟 ≤ 1 分钟。
         */
        get: operations["dashboard_api_m1_v1_admin_dashboard_get"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/m1/v1/admin/bookings": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** 预约明细（M1-OPS-02） */
        get: operations["admin_bookings_api_m1_v1_admin_bookings_get"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/m1/v1/admin/stats": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** 统计指标（M1-OPS-03） */
        get: operations["stats_api_m1_v1_admin_stats_get"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/m1/v1/admin/stats/flags": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** 低利用率与紧张自习室（M1-OPS-04） */
        get: operations["stats_flags_api_m1_v1_admin_stats_flags_get"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/m1/v1/admin/export/bookings.csv": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** 导出预约明细 CSV（M1-OPS-05） */
        get: operations["export_bookings_api_m1_v1_admin_export_bookings_csv_get"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/m1/v1/admin/export/stats.csv": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** 导出统计 CSV（M1-OPS-05） */
        get: operations["export_stats_api_m1_v1_admin_export_stats_csv_get"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/m1/v1/admin/trace": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** 座位在某时刻的状态与来源（M1-INT-06） */
        get: operations["seat_trace_api_m1_v1_admin_trace_get"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/m1/v1/admin/trace/history": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** 座位状态变更历史（M1-INT-06） */
        get: operations["seat_trace_history_api_m1_v1_admin_trace_history_get"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/internal/m1/v1/blocks/{source}/{source_ref}": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        /**
         * 写入或更新占用块（M1-INT-01、03）
         * @description 以「写入来源 + 来源单号」幂等。ACTIVE 取消冲突的个人预约并通知（不计违约，BR-19），HOLD 只阻止新预约。仅 M3_REPAIR、ADMIN 可不填结束时间。
         */
        put: operations["upsert_block_internal_m1_v1_blocks__source___source_ref__put"];
        post?: never;
        /**
         * 释放占用块（M1-INT-02）
         * @description 幂等：释放不存在或已释放的块也返回 204。被取消的个人预约不自动恢复。
         */
        delete: operations["release_block_internal_m1_v1_blocks__source___source_ref__delete"];
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/internal/m1/v1/rooms/{room_id}/availability": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /**
         * 自习室在区间内的占用与冲突预约数（M1-INT-04）
         * @description 供 M2 提交、审批前展示冲突；不含学生身份。
         */
        get: operations["room_availability_internal_m1_v1_rooms__room_id__availability_get"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/internal/m1/v1/users/{user_id}/violation-summary": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** 学生近期违约摘要（M1-INT-07，供 M2 准入门槛） */
        get: operations["violation_summary_internal_m1_v1_users__user_id__violation_summary_get"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
}
export type webhooks = Record<string, never>;
export interface components {
    schemas: {
        /** AdminBooking */
        AdminBooking: {
            /** Id */
            id: number;
            /** Seatid */
            seatId: number;
            /** Seatcode */
            seatCode: string;
            /** Roomid */
            roomId: number;
            /** Roomname */
            roomName: string;
            /** Buildingname */
            buildingName: string;
            /**
             * Startsat
             * Format: date-time
             */
            startsAt: string;
            /**
             * Endsat
             * Format: date-time
             */
            endsAt: string;
            status: components["schemas"]["BookingStatus"];
            /**
             * Createdat
             * Format: date-time
             */
            createdAt: string;
            /**
             * Checkinopensat
             * Format: date-time
             * @description 签到窗口开启时刻（BR-13）
             */
            checkinOpensAt: string;
            /**
             * Checkindeadline
             * Format: date-time
             * @description 签到截止时刻 T0 + 15 分钟（BR-12、13）
             */
            checkinDeadline: string;
            /** Checkedinat */
            checkedInAt?: string | null;
            checkinMethod?: components["schemas"]["CheckinMethod"] | null;
            /** Cancelledat */
            cancelledAt?: string | null;
            /** Cancelreason */
            cancelReason?: string | null;
            /** @description 系统取消时的写入来源 */
            cancelSource?: components["schemas"]["BlockSource"] | null;
            /** Cancelsourceref */
            cancelSourceRef?: string | null;
            /** Userid */
            userId: number;
            /**
             * Studentnomasked
             * @description 运营管理员默认看到脱敏学号（NFR-11）
             */
            studentNoMasked: string;
            /**
             * Studentname
             * @description 无查看完整信息的权限时为空
             */
            studentName?: string | null;
        };
        /** BlockBrief */
        BlockBrief: {
            source: components["schemas"]["BlockSource"];
            /** Sourceref */
            sourceRef: string;
            kind: components["schemas"]["BlockKind"];
            scope: components["schemas"]["BlockScope"];
            /**
             * Startsat
             * Format: date-time
             */
            startsAt: string;
            /** Endsat */
            endsAt: string | null;
        };
        /**
         * BlockKind
         * @enum {string}
         */
        BlockKind: "HOLD" | "ACTIVE";
        /** BlockResult */
        BlockResult: {
            /** Blockid */
            blockId: number;
            source: components["schemas"]["BlockSource"];
            /** Sourceref */
            sourceRef: string;
            kind: components["schemas"]["BlockKind"];
            /**
             * Cancelledbookingids
             * @description 因本次写入被系统取消的个人预约（不含学生身份）
             */
            cancelledBookingIds?: number[];
        };
        /**
         * BlockScope
         * @enum {string}
         */
        BlockScope: "ROOM" | "SEATS";
        /**
         * BlockSource
         * @enum {string}
         */
        BlockSource: "M1_BOOKING" | "M2_ROOM_BOOKING" | "M3_REPAIR" | "ADMIN";
        /**
         * BlockUpsert
         * @description PUT /internal/m1/v1/blocks/{source}/{sourceRef}：以「来源 + 来源单号」幂等。
         */
        BlockUpsert: {
            scope: components["schemas"]["BlockScope"];
            /** Roomid */
            roomId: number;
            /**
             * Seatids
             * @description scope=SEATS 时必填
             */
            seatIds?: number[];
            /**
             * Startsat
             * Format: date-time
             */
            startsAt: string;
            /**
             * Endsat
             * @description 为空表示直到释放，仅 M3_REPAIR、ADMIN 允许
             */
            endsAt?: string | null;
            /** @default ACTIVE */
            kind: components["schemas"]["BlockKind"];
            /** Reason */
            reason: string;
        };
        /** BookingCreate */
        BookingCreate: {
            /** Seatid */
            seatId: number;
            /**
             * Date
             * Format: date
             */
            date: string;
            /**
             * Starthour
             * @description 整点（BR-01）
             */
            startHour: number;
            /**
             * Hours
             * @description 实际上限取参数 m1.booking.max_hours（BR-02）
             */
            hours: number;
        };
        /** BookingOut */
        BookingOut: {
            /** Id */
            id: number;
            /** Seatid */
            seatId: number;
            /** Seatcode */
            seatCode: string;
            /** Roomid */
            roomId: number;
            /** Roomname */
            roomName: string;
            /** Buildingname */
            buildingName: string;
            /**
             * Startsat
             * Format: date-time
             */
            startsAt: string;
            /**
             * Endsat
             * Format: date-time
             */
            endsAt: string;
            status: components["schemas"]["BookingStatus"];
            /**
             * Createdat
             * Format: date-time
             */
            createdAt: string;
            /**
             * Checkinopensat
             * Format: date-time
             * @description 签到窗口开启时刻（BR-13）
             */
            checkinOpensAt: string;
            /**
             * Checkindeadline
             * Format: date-time
             * @description 签到截止时刻 T0 + 15 分钟（BR-12、13）
             */
            checkinDeadline: string;
            /** Checkedinat */
            checkedInAt?: string | null;
            checkinMethod?: components["schemas"]["CheckinMethod"] | null;
            /** Cancelledat */
            cancelledAt?: string | null;
            /** Cancelreason */
            cancelReason?: string | null;
            /** @description 系统取消时的写入来源 */
            cancelSource?: components["schemas"]["BlockSource"] | null;
            /** Cancelsourceref */
            cancelSourceRef?: string | null;
        };
        /**
         * BookingStatus
         * @enum {string}
         */
        BookingStatus: "PENDING" | "CHECKED_IN" | "COMPLETED" | "CANCELLED" | "NO_SHOW" | "REVOKED";
        /** CheckinIn */
        CheckinIn: {
            /** Code */
            code: string;
            /**
             * @description CODE 输码 / SCAN 扫码
             * @default CODE
             */
            method: components["schemas"]["CheckinMethod"];
        };
        /**
         * CheckinMethod
         * @enum {string}
         */
        CheckinMethod: "CODE" | "SCAN" | "MANUAL";
        /** Dashboard */
        Dashboard: {
            /**
             * At
             * Format: date-time
             */
            at: string;
            /** Rooms */
            rooms: components["schemas"]["RoomLive"][];
        };
        /** FavoriteSeat */
        FavoriteSeat: {
            /** Seatid */
            seatId: number;
            /** Seatcode */
            seatCode: string;
            /** Roomid */
            roomId: number;
            /** Roomname */
            roomName: string;
        };
        /** HTTPValidationError */
        HTTPValidationError: {
            /** Detail */
            detail?: components["schemas"]["ValidationError"][];
        };
        /** MyViolations */
        MyViolations: {
            /** Records */
            records: components["schemas"]["ViolationOut"][];
            suspension: components["schemas"]["Suspension"];
        };
        /** Page[AdminBooking] */
        Page_AdminBooking_: {
            /** Items */
            items: components["schemas"]["AdminBooking"][];
            /** Total */
            total: number;
            /** Page */
            page: number;
            /** Size */
            size: number;
        };
        /** Page[BookingOut] */
        Page_BookingOut_: {
            /** Items */
            items: components["schemas"]["BookingOut"][];
            /** Total */
            total: number;
            /** Page */
            page: number;
            /** Size */
            size: number;
        };
        /** Page[RoomSeats] */
        Page_RoomSeats_: {
            /** Items */
            items: components["schemas"]["RoomSeats"][];
            /** Total */
            total: number;
            /** Page */
            page: number;
            /** Size */
            size: number;
        };
        /** Page[ViolationOut] */
        Page_ViolationOut_: {
            /** Items */
            items: components["schemas"]["ViolationOut"][];
            /** Total */
            total: number;
            /** Page */
            page: number;
            /** Size */
            size: number;
        };
        /** ReasonIn */
        ReasonIn: {
            /** Reason */
            reason: string;
        };
        /** RebookHint */
        RebookHint: {
            /** Bookingid */
            bookingId: number;
            /** Seatid */
            seatId: number;
            /** Seatcode */
            seatCode: string;
            /** Roomname */
            roomName: string;
            /**
             * Seatusable
             * @description 座位仍存在、启用且本人有权预约
             */
            seatUsable: boolean;
            /**
             * Reason
             * @description 不可用的原因，如「座位已注销」
             */
            reason?: string | null;
        };
        /** RevokeIn */
        RevokeIn: {
            /** Reason */
            reason: string;
        };
        /**
         * RoomAvailability
         * @description GET /internal/m1/v1/rooms/{roomId}/availability（M1-INT-04）。
         */
        RoomAvailability: {
            /** Roomid */
            roomId: number;
            /**
             * Startsat
             * Format: date-time
             */
            startsAt: string;
            /**
             * Endsat
             * Format: date-time
             */
            endsAt: string;
            /** Blocks */
            blocks: components["schemas"]["BlockBrief"][];
            /** Conflictingbookingcount */
            conflictingBookingCount: number;
        };
        /** RoomBrowseItem */
        RoomBrowseItem: {
            /** Roomid */
            roomId: number;
            /** Code */
            code: string;
            /** Name */
            name: string;
            /** Buildingname */
            buildingName: string;
            roomType: components["schemas"]["RoomType"];
            /** Departmentid */
            departmentId: number | null;
            /**
             * Openinghours
             * @description 当日开放时间，如 08:00-22:00；不开放为空串
             */
            openingHours: string;
            /** Totalseats */
            totalSeats: number;
            /**
             * Availableseats
             * @description 所选时段内按 §4.2 可约的座位数
             */
            availableSeats: number;
            /**
             * Tagcounts
             * @description 各标记的座位数
             */
            tagCounts: {
                [key: string]: number;
            };
        };
        /** RoomFlag */
        RoomFlag: {
            /** Roomid */
            roomId: number;
            /** Roomname */
            roomName: string;
            /**
             * Kind
             * @enum {string}
             */
            kind: "LOW_USAGE" | "TIGHT";
            /** Value */
            value: number;
        };
        /** RoomLive */
        RoomLive: {
            /** Roomid */
            roomId: number;
            /** Roomname */
            roomName: string;
            /** Buildingname */
            buildingName: string;
            /** Total */
            total: number;
            /** Unavailable */
            unavailable: number;
            /** Bookednotcheckedin */
            bookedNotCheckedIn: number;
            /** Checkedin */
            checkedIn: number;
            /** Free */
            free: number;
        };
        /** RoomSeats */
        RoomSeats: {
            /** Roomid */
            roomId: number;
            /** Roomcode */
            roomCode: string;
            /** Roomname */
            roomName: string;
            /** Buildingname */
            buildingName: string;
            /** Availablecount */
            availableCount: number;
            /** Seats */
            seats: components["schemas"]["SeatResult"][];
        };
        /**
         * RoomType
         * @enum {string}
         */
        RoomType: "CLASSROOM" | "LIBRARY_STUDY" | "OTHER_STUDY" | "MEETING" | "PUBLIC_AREA";
        /** ScreenCode */
        ScreenCode: {
            /** Roomid */
            roomId: number;
            /** Roomname */
            roomName: string;
            /**
             * Code
             * @description 6 位，去除易混字符，安全随机生成
             */
            code: string;
            /**
             * Qrurl
             * @description 扫码签到网址，含房间与签到码参数
             */
            qrUrl: string;
            /**
             * Validuntil
             * Format: date-time
             */
            validUntil: string;
            /**
             * Refreshseconds
             * @description 屏幕轮询间隔，换码后 30 秒内可见
             */
            refreshSeconds: number;
        };
        /** ScreenDevice */
        ScreenDevice: {
            /** Id */
            id: number;
            /** Roomid */
            roomId: number;
            /** Name */
            name: string;
            /**
             * Createdat
             * Format: date-time
             */
            createdAt: string;
            /** Revokedat */
            revokedAt: string | null;
        };
        /** ScreenDeviceCreate */
        ScreenDeviceCreate: {
            /** Roomid */
            roomId: number;
            /** Name */
            name: string;
        };
        /** ScreenDeviceCreated */
        ScreenDeviceCreated: {
            /** Id */
            id: number;
            /** Roomid */
            roomId: number;
            /** Name */
            name: string;
            /**
             * Createdat
             * Format: date-time
             */
            createdAt: string;
            /** Revokedat */
            revokedAt: string | null;
            /**
             * Token
             * @description 设备令牌，只在创建时返回一次
             */
            token: string;
        };
        /** SeatMap */
        SeatMap: {
            /** Roomid */
            roomId: number;
            /** Rows */
            rows: number;
            /** Cols */
            cols: number;
            /** Cells */
            cells: components["schemas"]["SeatMapCell"][];
        };
        /** SeatMapCell */
        SeatMapCell: {
            /** Row */
            row: number;
            /** Col */
            col: number;
            seat: components["schemas"]["SeatResult"];
        };
        /** SeatResult */
        SeatResult: {
            /** Seatid */
            seatId: number;
            /** Code */
            code: string;
            /** Tags */
            tags: string[];
            state: components["schemas"]["SlotState"];
        };
        /** SeatStateLog */
        SeatStateLog: {
            /** Id */
            id: number;
            /** Seatid */
            seatId: number;
            /** Action */
            action: string;
            source: components["schemas"]["BlockSource"];
            /** Sourceref */
            sourceRef: string;
            kind: components["schemas"]["BlockKind"];
            /**
             * Startsat
             * Format: date-time
             */
            startsAt: string;
            /** Endsat */
            endsAt: string | null;
            /** Writtenby */
            writtenBy: string;
            /**
             * At
             * Format: date-time
             */
            at: string;
        };
        /** SeatTimeline */
        SeatTimeline: {
            /** Seatid */
            seatId: number;
            /** Seatcode */
            seatCode: string;
            /**
             * Date
             * Format: date
             */
            date: string;
            /** Slots */
            slots: components["schemas"]["TimelineSlot"][];
        };
        /** SeatTrace */
        SeatTrace: {
            /** Seatid */
            seatId: number;
            /**
             * At
             * Format: date-time
             */
            at: string;
            state: components["schemas"]["SlotState"];
            source: components["schemas"]["BlockSource"] | null;
            /** Sourceref */
            sourceRef: string | null;
            kind: components["schemas"]["BlockKind"] | null;
            /** Writtenat */
            writtenAt: string | null;
            /** Writtenby */
            writtenBy: string | null;
        };
        /** Setting */
        Setting: {
            /**
             * Key
             * @description 如 m1.booking.max_hours
             */
            key: string;
            /** Value */
            value: number | boolean;
            /** Default */
            default: number | boolean;
            /** Min */
            min?: number | null;
            /** Max */
            max?: number | null;
            /** Description */
            description: string;
        };
        /** SettingsUpdate */
        SettingsUpdate: {
            /**
             * Values
             * @description 要修改的参数键与新值
             */
            values: {
                [key: string]: number | boolean;
            };
        };
        /**
         * SlotState
         * @description 座位在某时段对当前学生的状态，按 §4.2 的优先级取第一个命中项。
         * @enum {string}
         */
        SlotState: "CLOSED" | "DISABLED" | "REPAIR" | "ROOM_OCCUPIED" | "BOOKED" | "AVAILABLE";
        /** Stats */
        Stats: {
            /** Openseathours */
            openSeatHours: number;
            /** Bookingrate */
            bookingRate: number;
            /** Usagerate */
            usageRate: number;
            /** Checkinrate */
            checkinRate: number;
            /** Noshowrate */
            noShowRate: number;
            /** Dailyturnover */
            dailyTurnover: number;
            /**
             * Heatmap
             * @description 7 × 24：星期 × 整点 的预约率
             */
            heatmap: number[][];
        };
        /** Suspension */
        Suspension: {
            /** Active */
            active: boolean;
            /** Until */
            until: string | null;
            /** Recentcount */
            recentCount: number;
            /** Threshold */
            threshold: number;
            /** Windowdays */
            windowDays: number;
        };
        /** TimelineSlot */
        TimelineSlot: {
            /** Hour */
            hour: number;
            state: components["schemas"]["SlotState"];
        };
        /** ValidationError */
        ValidationError: {
            /** Location */
            loc: (string | number)[];
            /** Message */
            msg: string;
            /** Error Type */
            type: string;
            /** Input */
            input?: unknown;
            /** Context */
            ctx?: Record<string, never>;
        };
        /** ViolationOut */
        ViolationOut: {
            /** Id */
            id: number;
            /** Bookingid */
            bookingId: number;
            /** Userid */
            userId: number;
            /**
             * Studentnomasked
             * @description 脱敏学号，如 2621****32（NFR-11）
             */
            studentNoMasked: string;
            /** Roomname */
            roomName: string;
            /** Seatcode */
            seatCode: string;
            /**
             * Startsat
             * Format: date-time
             */
            startsAt: string;
            /**
             * Endsat
             * Format: date-time
             */
            endsAt: string;
            /**
             * Occurredat
             * Format: date-time
             */
            occurredAt: string;
            /** Reason */
            reason: string;
            /** Revokedat */
            revokedAt?: string | null;
            /** Revokereason */
            revokeReason?: string | null;
        };
        /**
         * ViolationSummary
         * @description GET /internal/m1/v1/users/{userId}/violation-summary（M1-INT-07）。
         */
        ViolationSummary: {
            /** Userid */
            userId: number;
            /** Windowdays */
            windowDays: number;
            /** Count */
            count: number;
            /** Suspendeduntil */
            suspendedUntil: string | null;
        };
    };
    responses: never;
    parameters: never;
    requestBodies: never;
    headers: never;
    pathItems: never;
}
export type $defs = Record<string, never>;
export interface operations {
    browse_rooms_api_m1_v1_rooms_get: {
        parameters: {
            query?: {
                /** @description 默认今天（业务时区） */
                date?: string | null;
                /** @description 默认最近可约整点 */
                startHour?: number | null;
                hours?: number;
                campusId?: number | null;
                buildingId?: number | null;
                roomType?: components["schemas"]["RoomType"] | null;
            };
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["RoomBrowseItem"][];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    search_seats_api_m1_v1_seats_search_get: {
        parameters: {
            query?: {
                /** @description 页码，从 1 开始 */
                page?: number;
                /** @description 每页条数 */
                size?: number;
                /** @description 默认今天（业务时区） */
                date?: string | null;
                /** @description 默认最近可约整点 */
                startHour?: number | null;
                hours?: number;
                campusId?: number | null;
                buildingId?: number | null;
                roomId?: number | null;
                roomType?: components["schemas"]["RoomType"] | null;
                /** @description 多选须全部满足 */
                tags?: string[] | null;
                /** @description 快捷条件：有插座（任一类型） */
                anyOutlet?: boolean;
                onlyAvailable?: boolean;
                /** @description 自习室名称或座位编号 */
                keyword?: string | null;
            };
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["Page_RoomSeats_"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    seat_timeline_api_m1_v1_seats__seat_id__timeline_get: {
        parameters: {
            query?: {
                date?: string | null;
            };
            header?: never;
            path: {
                seat_id: number;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["SeatTimeline"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    booking_history_api_m1_v1_bookings_history_get: {
        parameters: {
            query?: {
                /** @description 页码，从 1 开始 */
                page?: number;
                /** @description 每页条数 */
                size?: number;
                status?: components["schemas"]["BookingStatus"][] | null;
                dateFrom?: string | null;
                dateTo?: string | null;
            };
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["Page_BookingOut_"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    rebook_hint_api_m1_v1_bookings__booking_id__rebook_get: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                booking_id: number;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["RebookHint"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    create_booking_api_m1_v1_bookings_post: {
        parameters: {
            query?: never;
            header?: {
                "Idempotency-Key"?: string | null;
            };
            path?: never;
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["BookingCreate"];
            };
        };
        responses: {
            /** @description Successful Response */
            201: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["BookingOut"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    current_bookings_api_m1_v1_bookings_current_get: {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["BookingOut"][];
                };
            };
        };
    };
    get_booking_api_m1_v1_bookings__booking_id__get: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                booking_id: number;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["BookingOut"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    cancel_booking_api_m1_v1_bookings__booking_id__cancel_post: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                booking_id: number;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["BookingOut"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    checkin_candidate_api_m1_v1_checkin_candidate_get: {
        parameters: {
            query: {
                roomId: number;
            };
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["BookingOut"] | null;
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    checkin_api_m1_v1_bookings__booking_id__checkin_post: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                booking_id: number;
            };
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["CheckinIn"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["BookingOut"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    screen_code_api_m1_v1_screen_code_get: {
        parameters: {
            query?: never;
            header: {
                "X-Device-Token": string;
            };
            path?: never;
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["ScreenCode"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    list_screens_api_m1_v1_admin_screens_get: {
        parameters: {
            query?: {
                roomId?: number | null;
            };
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["ScreenDevice"][];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    create_screen_api_m1_v1_admin_screens_post: {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["ScreenDeviceCreate"];
            };
        };
        responses: {
            /** @description Successful Response */
            201: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["ScreenDeviceCreated"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    revoke_screen_api_m1_v1_admin_screens__device_id__revoke_post: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                device_id: number;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["ScreenDevice"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    my_violations_api_m1_v1_violations_mine_get: {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["MyViolations"];
                };
            };
        };
    };
    list_violations_api_m1_v1_admin_violations_get: {
        parameters: {
            query?: {
                /** @description 页码，从 1 开始 */
                page?: number;
                /** @description 每页条数 */
                size?: number;
                userId?: number | null;
                roomId?: number | null;
                dateFrom?: string | null;
                dateTo?: string | null;
            };
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["Page_ViolationOut_"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    revoke_violation_api_m1_v1_admin_violations__violation_id__revoke_post: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                violation_id: number;
            };
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["RevokeIn"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["ViolationOut"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    checkout_api_m1_v1_bookings__booking_id__checkout_post: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                booking_id: number;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["BookingOut"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    seat_map_api_m1_v1_rooms__room_id__seat_map_get: {
        parameters: {
            query?: {
                /** @description 默认今天（业务时区） */
                date?: string | null;
                /** @description 默认最近可约整点 */
                startHour?: number | null;
                hours?: number;
            };
            header?: never;
            path: {
                room_id: number;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["SeatMap"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    alternatives_api_m1_v1_seats__seat_id__alternatives_get: {
        parameters: {
            query?: {
                /** @description 默认今天（业务时区） */
                date?: string | null;
                /** @description 默认最近可约整点 */
                startHour?: number | null;
                hours?: number;
            };
            header?: never;
            path: {
                seat_id: number;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["SeatResult"][];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    favorites_api_m1_v1_favorites_get: {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["FavoriteSeat"][];
                };
            };
        };
    };
    add_favorite_api_m1_v1_favorites__seat_id__put: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                seat_id: number;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            204: {
                headers: {
                    [name: string]: unknown;
                };
                content?: never;
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    remove_favorite_api_m1_v1_favorites__seat_id__delete: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                seat_id: number;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            204: {
                headers: {
                    [name: string]: unknown;
                };
                content?: never;
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    list_settings_api_m1_v1_admin_settings_get: {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["Setting"][];
                };
            };
        };
    };
    update_settings_api_m1_v1_admin_settings_put: {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["SettingsUpdate"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["Setting"][];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    admin_cancel_api_m1_v1_admin_bookings__booking_id__cancel_post: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                booking_id: number;
            };
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["ReasonIn"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["BookingOut"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    admin_checkin_api_m1_v1_admin_bookings__booking_id__checkin_post: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                booking_id: number;
            };
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["ReasonIn"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["BookingOut"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    dashboard_api_m1_v1_admin_dashboard_get: {
        parameters: {
            query?: {
                buildingId?: number | null;
            };
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["Dashboard"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    admin_bookings_api_m1_v1_admin_bookings_get: {
        parameters: {
            query: {
                /** @description 页码，从 1 开始 */
                page?: number;
                /** @description 每页条数 */
                size?: number;
                dateFrom: string;
                dateTo: string;
                buildingId?: number | null;
                roomId?: number | null;
                status?: components["schemas"]["BookingStatus"][] | null;
            };
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["Page_AdminBooking_"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    stats_api_m1_v1_admin_stats_get: {
        parameters: {
            query: {
                dateFrom: string;
                dateTo: string;
                buildingId?: number | null;
                roomId?: number | null;
            };
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["Stats"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    stats_flags_api_m1_v1_admin_stats_flags_get: {
        parameters: {
            query: {
                dateFrom: string;
                dateTo: string;
                buildingId?: number | null;
                roomId?: number | null;
            };
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["RoomFlag"][];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    export_bookings_api_m1_v1_admin_export_bookings_csv_get: {
        parameters: {
            query: {
                /** @description 页码，从 1 开始 */
                page?: number;
                /** @description 每页条数 */
                size?: number;
                dateFrom: string;
                dateTo: string;
                buildingId?: number | null;
                roomId?: number | null;
                status?: components["schemas"]["BookingStatus"][] | null;
            };
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "text/csv": unknown;
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    export_stats_api_m1_v1_admin_export_stats_csv_get: {
        parameters: {
            query: {
                dateFrom: string;
                dateTo: string;
                buildingId?: number | null;
                roomId?: number | null;
            };
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "text/csv": unknown;
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    seat_trace_api_m1_v1_admin_trace_get: {
        parameters: {
            query: {
                seatId: number;
                at: string;
            };
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["SeatTrace"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    seat_trace_history_api_m1_v1_admin_trace_history_get: {
        parameters: {
            query: {
                seatId: number;
                from?: string | null;
                to?: string | null;
            };
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["SeatStateLog"][];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    upsert_block_internal_m1_v1_blocks__source___source_ref__put: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                source: components["schemas"]["BlockSource"];
                source_ref: string;
            };
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["BlockUpsert"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["BlockResult"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    release_block_internal_m1_v1_blocks__source___source_ref__delete: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                source: components["schemas"]["BlockSource"];
                source_ref: string;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            204: {
                headers: {
                    [name: string]: unknown;
                };
                content?: never;
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    room_availability_internal_m1_v1_rooms__room_id__availability_get: {
        parameters: {
            query: {
                startsAt: string;
                endsAt: string;
            };
            header?: never;
            path: {
                room_id: number;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["RoomAvailability"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    violation_summary_internal_m1_v1_users__user_id__violation_summary_get: {
        parameters: {
            query?: {
                days?: number;
            };
            header?: never;
            path: {
                user_id: number;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["ViolationSummary"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
}
