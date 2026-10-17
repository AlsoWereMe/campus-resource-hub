// 由 contracts/m2/openapi.yaml 生成，请勿手改。重新生成：pnpm gen:api
export interface paths {
    "/api/m2/v1/rooms": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /**
         * 可申请房间检索（M2-ROOM-01）
         * @description 只返回申请人有资格申请的可整间预约房间（BR-M2-17），并说明不可申请的原因。
         */
        get: operations["search_rooms_api_m2_v1_rooms_get"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/m2/v1/rooms/{room_id}/calendar": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** 房间占用日历（M2-ROOM-02，P1） */
        get: operations["room_calendar_api_m2_v1_rooms__room_id__calendar_get"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/m2/v1/rooms/{room_id}/conflicts": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /**
         * 冲突预检（M2-INT-02）
         * @description 调用 M1 可用性查询。提交前查询失败则不可提交；审批页查询失败只提示。
         */
        get: operations["room_conflicts_api_m2_v1_rooms__room_id__conflicts_get"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/m2/v1/applications/check": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /** 提交前预检准入门槛（M2-ELG-01 ~ 05） */
        post: operations["check_eligibility_api_m2_v1_applications_check_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/m2/v1/applications": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /**
         * 提交整间申请（M2-APP-01）
         * @description 准入校验（M2-T02）→ 冲突校验（BR-M2-04、05）→ 匹配并固化审批链 → 写回 HOLD → 通知第 1 级审批人。同一 Idempotency-Key 只产生一条申请。
         */
        post: operations["submit_application_api_m2_v1_applications_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/m2/v1/applications/mine": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** 我的申请（M2-QRY-01） */
        get: operations["my_applications_api_m2_v1_applications_mine_get"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/m2/v1/applications/{application_id}": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** 申请详情：审批时间线、截止时刻、写回状态（M2-APV-04） */
        get: operations["get_application_api_m2_v1_applications__application_id__get"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/m2/v1/applications/{application_id}/withdraw": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /** 撤回审批中的申请（M2-APP-03） */
        post: operations["withdraw_application_api_m2_v1_applications__application_id__withdraw_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/m2/v1/applications/{application_id}/cancel": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /**
         * 取消已通过、未开始的申请（M2-APP-04）
         * @description 释放占用；被 M1 取消的个人预约不恢复。开始后不能取消（BR-M2-13）。
         */
        post: operations["cancel_application_api_m2_v1_applications__application_id__cancel_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/m2/v1/admin/applications/{application_id}/writeback/retry": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /** 手动重试失败的写回（M2-INT-03） */
        post: operations["retry_writeback_api_m2_v1_admin_applications__application_id__writeback_retry_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/m2/v1/approvals/pending": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /**
         * 待我审批（M2-APV-01）
         * @description 按截止时刻升序；不含本人提交的申请与本人已审批过的申请（M2-APV-05）。
         */
        get: operations["pending_approvals_api_m2_v1_approvals_pending_get"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/m2/v1/approvals/done": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** 我已审批 */
        get: operations["done_approvals_api_m2_v1_approvals_done_get"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/m2/v1/applications/{application_id}/approve": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /**
         * 通过当前级别（M2-APV-02）
         * @description 有下一级则进入下一级并通知；末级通过则写回 ACTIVE 并通知申请人。
         */
        post: operations["approve_api_m2_v1_applications__application_id__approve_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/m2/v1/applications/{application_id}/reject": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /** 驳回（M2-APV-03） */
        post: operations["reject_api_m2_v1_applications__application_id__reject_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/m2/v1/applications/{application_id}/transfer": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /** 转交同级审批人（M2-APV-06，P2） */
        post: operations["transfer_api_m2_v1_applications__application_id__transfer_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/m2/v1/admin/flows": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** 审批链规则列表（M2-FLOW-01） */
        get: operations["list_flows_api_m2_v1_admin_flows_get"];
        put?: never;
        /**
         * 新增审批链规则（M2-FLOW-02）
         * @description 只影响此后提交的申请（M2-APP-02）；写入审计。
         */
        post: operations["create_flow_api_m2_v1_admin_flows_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/m2/v1/admin/flows/{flow_id}": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        /** 修改审批链规则（M2-FLOW-02） */
        put: operations["update_flow_api_m2_v1_admin_flows__flow_id__put"];
        post?: never;
        /** 删除审批链规则（M2-FLOW-02） */
        delete: operations["delete_flow_api_m2_v1_admin_flows__flow_id__delete"];
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/m2/v1/admin/settings": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** 查看 M2 参数 */
        get: operations["list_settings_api_m2_v1_admin_settings_get"];
        /** 修改 M2 参数（BR-M2-19：只作用于新申请） */
        put: operations["update_settings_api_m2_v1_admin_settings_put"];
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/m2/v1/admin/applications": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** 范围内全部申请（M2-QRY-02） */
        get: operations["list_applications_api_m2_v1_admin_applications_get"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/m2/v1/admin/applications/{application_id}/revoke": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /**
         * 撤销已通过的申请（M2-APP-06）
         * @description 理由必填、写入审计；释放占用并通知申请人。
         */
        post: operations["revoke_application_api_m2_v1_admin_applications__application_id__revoke_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/m2/v1/admin/stats": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** 申请统计（M2-QRY-03，P2） */
        get: operations["stats_api_m2_v1_admin_stats_get"];
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
        /** ApplicableRoom */
        ApplicableRoom: {
            /** Roomid */
            roomId: number;
            /** Code */
            code: string;
            /** Name */
            name: string;
            /** Buildingname */
            buildingName: string;
            roomType: components["schemas"]["RoomType"];
            /** Capacity */
            capacity: number;
            /** Facilities */
            facilities: string[];
            /** Openinghours */
            openingHours: string;
            /**
             * Applicable
             * @description 所选时段是否可申请
             */
            applicable: boolean;
            /**
             * Reason
             * @description 不可申请的原因：已有申请 / 维修下架 / 不在开放时间
             */
            reason?: string | null;
        };
        /**
         * ApplicantType
         * @enum {string}
         */
        ApplicantType: "STAFF" | "STUDENT_LEADER";
        /** ApplicationCreate */
        ApplicationCreate: {
            /** Roomid */
            roomId: number;
            /**
             * Date
             * Format: date
             */
            date: string;
            /**
             * Starthour
             * @description 整点（BR-M2-01）
             */
            startHour: number;
            /**
             * Hours
             * @description 实际上限取参数 m2.max_duration_hours
             */
            hours: number;
            /**
             * Title
             * @description 活动名称
             */
            title: string;
            /** Purpose */
            purpose: string;
            /**
             * Attendees
             * @description 预计人数，不得超过房间容量（BR-M2-06）
             */
            attendees: number;
            /**
             * Contactname
             * @description 默认本人
             */
            contactName?: string | null;
            /** Contactphone */
            contactPhone?: string | null;
            /** Remark */
            remark?: string | null;
        };
        /** ApplicationOut */
        ApplicationOut: {
            /** Id */
            id: number;
            /** Roomid */
            roomId: number;
            /** Roomcode */
            roomCode: string;
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
            /** Title */
            title: string;
            /** Purpose */
            purpose: string;
            /** Attendees */
            attendees: number;
            /** Contactname */
            contactName: string;
            /** Contactphone */
            contactPhone: string | null;
            /** Remark */
            remark: string | null;
            /** Applicantid */
            applicantId: number;
            /** Applicantname */
            applicantName: string;
            status: components["schemas"]["ApplicationStatus"];
            /**
             * Currentlevel
             * @description 审批中时的当前级别
             */
            currentLevel: number | null;
            /**
             * Deadline
             * @description 当前级别的审批截止时刻（BR-M2-11）
             */
            deadline: string | null;
            /**
             * Chain
             * @description 提交时固化的审批链快照（M2-APP-02）
             */
            chain: components["schemas"]["ApprovalLevel"][];
            /** Records */
            records: components["schemas"]["ApprovalRecord"][];
            /**
             * Writeback
             * @description 在 M1 中的占用同步状态（M2-INT-03）
             * @enum {string}
             */
            writeback: "NONE" | "SYNCING" | "SYNCED" | "FAILED";
            /**
             * Createdat
             * Format: date-time
             */
            createdAt: string;
        };
        /**
         * ApplicationStatus
         * @enum {string}
         */
        ApplicationStatus: "PENDING" | "APPROVED" | "REJECTED" | "WITHDRAWN" | "EXPIRED" | "CANCELLED" | "REVOKED" | "COMPLETED";
        /** ApprovalLevel */
        ApprovalLevel: {
            /** Level */
            level: number;
            /**
             * Role
             * @description 审批角色，如 dept_approver、room_admin、resource_admin
             */
            role: string;
            scopeFrom: components["schemas"]["ScopeFrom"];
        };
        /** ApprovalRecord */
        ApprovalRecord: {
            /** Level */
            level: number;
            /** Approverid */
            approverId: number;
            /** Approvername */
            approverName: string;
            /**
             * Action
             * @enum {string}
             */
            action: "APPROVE" | "REJECT" | "TRANSFER";
            /** Comment */
            comment: string | null;
            /**
             * At
             * Format: date-time
             */
            at: string;
        };
        /** ApproveIn */
        ApproveIn: {
            /** Comment */
            comment?: string | null;
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
        /** CalendarItem */
        CalendarItem: {
            /**
             * Startsat
             * Format: date-time
             */
            startsAt: string;
            /** Endsat */
            endsAt: string | null;
            /**
             * Kind
             * @enum {string}
             */
            kind: "APPLICATION" | "REPAIR" | "PERSONAL_BOOKINGS";
            /**
             * Status
             * @description 整间申请的状态；不显示申请人
             */
            status?: string | null;
            /**
             * Count
             * @description 个人预约数量
             */
            count?: number | null;
        };
        /** ConflictPreview */
        ConflictPreview: {
            /**
             * Personalbookingcount
             * @description 审批通过后将被取消的个人预约数
             */
            personalBookingCount: number;
            /** Blocks */
            blocks: components["schemas"]["BlockBrief"][];
            /** Cansubmit */
            canSubmit: boolean;
            /** Reason */
            reason?: string | null;
        };
        /** EligibilityResult */
        EligibilityResult: {
            /** Eligible */
            eligible: boolean;
            /** Violations */
            violations: components["schemas"]["Violation"][];
        };
        /** FlowCondition */
        FlowCondition: {
            /**
             * Applicanttypes
             * @description 空表示不限
             */
            applicantTypes?: components["schemas"]["ApplicantType"][];
            /**
             * Minattendees
             * @description 预计人数大于该值时命中
             */
            minAttendees?: number | null;
            /**
             * Minhours
             * @description 时长大于该值时命中
             */
            minHours?: number | null;
            /** Roomtypes */
            roomTypes?: components["schemas"]["RoomType"][];
            roomOwner?: components["schemas"]["OwnerType"] | null;
        };
        /** FlowRule */
        FlowRule: {
            /** Name */
            name: string;
            /**
             * Priority
             * @description 数字越小越优先，取第一条命中的规则（BR-M2-09）
             */
            priority: number;
            condition: components["schemas"]["FlowCondition"];
            /** Levels */
            levels: components["schemas"]["ApprovalLevel"][];
            /**
             * Enabled
             * @default true
             */
            enabled: boolean;
            /** Id */
            id: number;
        };
        /** FlowRuleIn */
        FlowRuleIn: {
            /** Name */
            name: string;
            /**
             * Priority
             * @description 数字越小越优先，取第一条命中的规则（BR-M2-09）
             */
            priority: number;
            condition: components["schemas"]["FlowCondition"];
            /** Levels */
            levels: components["schemas"]["ApprovalLevel"][];
            /**
             * Enabled
             * @default true
             */
            enabled: boolean;
        };
        /** HTTPValidationError */
        HTTPValidationError: {
            /** Detail */
            detail?: components["schemas"]["ValidationError"][];
        };
        /**
         * OwnerType
         * @enum {string}
         */
        OwnerType: "SCHOOL" | "DEPARTMENT";
        /** Page[ApplicableRoom] */
        Page_ApplicableRoom_: {
            /** Items */
            items: components["schemas"]["ApplicableRoom"][];
            /** Total */
            total: number;
            /** Page */
            page: number;
            /** Size */
            size: number;
        };
        /** Page[ApplicationOut] */
        Page_ApplicationOut_: {
            /** Items */
            items: components["schemas"]["ApplicationOut"][];
            /** Total */
            total: number;
            /** Page */
            page: number;
            /** Size */
            size: number;
        };
        /** RejectIn */
        RejectIn: {
            /**
             * Reason
             * @description 驳回理由必填（BR-M2-10）
             */
            reason: string;
        };
        /** RevokeIn */
        RevokeIn: {
            /** Reason */
            reason: string;
        };
        /** RoomStats */
        RoomStats: {
            /** Roomid */
            roomId: number;
            /** Roomname */
            roomName: string;
            /** Month */
            month: string;
            /** Submitted */
            submitted: number;
            /** Approvalrate */
            approvalRate: number;
            /** Avgapprovalhours */
            avgApprovalHours: number;
            /** Expiredrate */
            expiredRate: number;
        };
        /**
         * RoomType
         * @enum {string}
         */
        RoomType: "CLASSROOM" | "LIBRARY_STUDY" | "OTHER_STUDY" | "MEETING" | "PUBLIC_AREA";
        /**
         * ScopeFrom
         * @description 审批人数据范围的取法。
         * @enum {string}
         */
        ScopeFrom: "APPLICANT_DEPARTMENT" | "ROOM_SCOPE" | "ALL";
        /** Setting */
        Setting: {
            /**
             * Key
             * @description 如 m2.level_timeout_hours
             */
            key: string;
            /** Value */
            value: number;
            /** Default */
            default: number;
            /** Min */
            min?: number | null;
            /** Max */
            max?: number | null;
            /** Description */
            description: string;
        };
        /** SettingsUpdate */
        SettingsUpdate: {
            /** Values */
            values: {
                [key: string]: number;
            };
        };
        /** TransferIn */
        TransferIn: {
            /** Touserid */
            toUserId: number;
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
        /** Violation */
        Violation: {
            /**
             * Rule
             * @description 规则编号，如 BR-M2-03
             */
            rule: string;
            /** Message */
            message: string;
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
    search_rooms_api_m2_v1_rooms_get: {
        parameters: {
            query?: {
                /** @description 页码，从 1 开始 */
                page?: number;
                /** @description 每页条数 */
                size?: number;
                date?: string | null;
                startHour?: number | null;
                hours?: number | null;
                buildingId?: number | null;
                roomType?: components["schemas"]["RoomType"] | null;
                /** @description 预计人数 */
                minCapacity?: number | null;
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
                    "application/json": components["schemas"]["Page_ApplicableRoom_"];
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
    room_calendar_api_m2_v1_rooms__room_id__calendar_get: {
        parameters: {
            query: {
                dateFrom: string;
                dateTo: string;
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
                    "application/json": components["schemas"]["CalendarItem"][];
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
    room_conflicts_api_m2_v1_rooms__room_id__conflicts_get: {
        parameters: {
            query: {
                date: string;
                startHour: number;
                hours: number;
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
                    "application/json": components["schemas"]["ConflictPreview"];
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
    check_eligibility_api_m2_v1_applications_check_post: {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["ApplicationCreate"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["EligibilityResult"];
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
    submit_application_api_m2_v1_applications_post: {
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
                "application/json": components["schemas"]["ApplicationCreate"];
            };
        };
        responses: {
            /** @description Successful Response */
            201: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["ApplicationOut"];
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
    my_applications_api_m2_v1_applications_mine_get: {
        parameters: {
            query?: {
                /** @description 页码，从 1 开始 */
                page?: number;
                /** @description 每页条数 */
                size?: number;
                status?: components["schemas"]["ApplicationStatus"][] | null;
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
                    "application/json": components["schemas"]["Page_ApplicationOut_"];
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
    get_application_api_m2_v1_applications__application_id__get: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                application_id: number;
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
                    "application/json": components["schemas"]["ApplicationOut"];
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
    withdraw_application_api_m2_v1_applications__application_id__withdraw_post: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                application_id: number;
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
                    "application/json": components["schemas"]["ApplicationOut"];
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
    cancel_application_api_m2_v1_applications__application_id__cancel_post: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                application_id: number;
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
                    "application/json": components["schemas"]["ApplicationOut"];
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
    retry_writeback_api_m2_v1_admin_applications__application_id__writeback_retry_post: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                application_id: number;
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
                    "application/json": components["schemas"]["ApplicationOut"];
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
    pending_approvals_api_m2_v1_approvals_pending_get: {
        parameters: {
            query?: {
                /** @description 页码，从 1 开始 */
                page?: number;
                /** @description 每页条数 */
                size?: number;
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
                    "application/json": components["schemas"]["Page_ApplicationOut_"];
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
    done_approvals_api_m2_v1_approvals_done_get: {
        parameters: {
            query?: {
                /** @description 页码，从 1 开始 */
                page?: number;
                /** @description 每页条数 */
                size?: number;
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
                    "application/json": components["schemas"]["Page_ApplicationOut_"];
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
    approve_api_m2_v1_applications__application_id__approve_post: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                application_id: number;
            };
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["ApproveIn"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["ApplicationOut"];
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
    reject_api_m2_v1_applications__application_id__reject_post: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                application_id: number;
            };
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["RejectIn"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["ApplicationOut"];
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
    transfer_api_m2_v1_applications__application_id__transfer_post: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                application_id: number;
            };
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["TransferIn"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["ApplicationOut"];
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
    list_flows_api_m2_v1_admin_flows_get: {
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
                    "application/json": components["schemas"]["FlowRule"][];
                };
            };
        };
    };
    create_flow_api_m2_v1_admin_flows_post: {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["FlowRuleIn"];
            };
        };
        responses: {
            /** @description Successful Response */
            201: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["FlowRule"];
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
    update_flow_api_m2_v1_admin_flows__flow_id__put: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                flow_id: number;
            };
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["FlowRuleIn"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["FlowRule"];
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
    delete_flow_api_m2_v1_admin_flows__flow_id__delete: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                flow_id: number;
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
    list_settings_api_m2_v1_admin_settings_get: {
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
    update_settings_api_m2_v1_admin_settings_put: {
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
    list_applications_api_m2_v1_admin_applications_get: {
        parameters: {
            query?: {
                /** @description 页码，从 1 开始 */
                page?: number;
                /** @description 每页条数 */
                size?: number;
                status?: components["schemas"]["ApplicationStatus"][] | null;
                roomId?: number | null;
                applicantId?: number | null;
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
                    "application/json": components["schemas"]["Page_ApplicationOut_"];
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
    revoke_application_api_m2_v1_admin_applications__application_id__revoke_post: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                application_id: number;
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
                    "application/json": components["schemas"]["ApplicationOut"];
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
    stats_api_m2_v1_admin_stats_get: {
        parameters: {
            query: {
                dateFrom: string;
                dateTo: string;
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
                    "application/json": components["schemas"]["RoomStats"][];
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
