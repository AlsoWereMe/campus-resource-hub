// 由 contracts/m3/openapi.yaml 生成，请勿手改。重新生成：pnpm gen:api
export interface paths {
    "/api/m3/v1/categories": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** 故障类别字典（BR-M3-02） */
        get: operations["categories_api_m3_v1_categories_get"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/m3/v1/workorders/duplicates": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** 同房间同类别的未关闭工单，上报前提示可能重复（M3-RPT-03，P1） */
        get: operations["duplicates_api_m3_v1_workorders_duplicates_get"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/m3/v1/workorders": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /**
         * 工单工作台（M3-QRY-02）
         * @description 调度员看范围内、维修人员看 assignedToMe、物业主管看全部；已升级的置顶。
         */
        get: operations["workbench_api_m3_v1_workorders_get"];
        put?: never;
        /**
         * 故障上报（M3-RPT-01）
         * @description 状态为待受理，计算受理截止，通知范围内调度员。同一 Idempotency-Key 只产生一张工单。
         */
        post: operations["report_api_m3_v1_workorders_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/m3/v1/workorders/mine": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** 我的报修（M3-QRY-01） */
        get: operations["my_work_orders_api_m3_v1_workorders_mine_get"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/m3/v1/workorders/{work_order_id}": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** 工单详情与时间线（M3-QRY-01） */
        get: operations["get_work_order_api_m3_v1_workorders__work_order_id__get"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        /** 调整类别或紧急程度（M3-DSP-01、M3-ESC-03） */
        patch: operations["patch_work_order_api_m3_v1_workorders__work_order_id__patch"];
        trace?: never;
    };
    "/api/m3/v1/workorders/{work_order_id}/cancel": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /**
         * 取消工单（M3-RPT-04）
         * @description 只能在待受理、已派单时取消；维修中只能由调度员关闭（BR-M3-09）。
         */
        post: operations["cancel_api_m3_v1_workorders__work_order_id__cancel_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/m3/v1/admin/stats": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** 工单统计（M3-QRY-03，P1） */
        get: operations["stats_api_m3_v1_admin_stats_get"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/m3/v1/admin/rooms/{room_id}/workorders": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** 按房间查历史工单（M3-QRY-04，P1） */
        get: operations["room_history_api_m3_v1_admin_rooms__room_id__workorders_get"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/m3/v1/workorders/{work_order_id}/attachments": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /**
         * 上传图片附件（M3-RPT-02，P1）
         * @description 每张工单至多 3 张，每张 ≤ 5 MB，仅 jpg / png（BR-M3-14）；文件存挂载卷（决策 Q24）。
         */
        post: operations["upload_attachment_api_m3_v1_workorders__work_order_id__attachments_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/m3/v1/attachments/{attachment_id}": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** 下载图片附件（M3-RPT-02） */
        get: operations["download_attachment_api_m3_v1_attachments__attachment_id__get"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/m3/v1/technicians": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /**
         * 范围覆盖该楼宇的维修人员及在办数（M3-DSP-01）
         * @description 人员来自 IAM-USER-02（按角色与范围查询用户）。
         */
        get: operations["technicians_api_m3_v1_technicians_get"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/m3/v1/workorders/{work_order_id}/assign": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /** 受理并派单（M3-DSP-01） */
        post: operations["assign_api_m3_v1_workorders__work_order_id__assign_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/m3/v1/workorders/{work_order_id}/reassign": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /**
         * 改派（M3-DSP-02）
         * @description 已派单、维修中可改派；不影响下架状态与当前阶段截止时刻。
         */
        post: operations["reassign_api_m3_v1_workorders__work_order_id__reassign_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/m3/v1/workorders/{work_order_id}/return": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /** 维修人员退回工单（M3-DSP-03，P1） */
        post: operations["return_work_order_api_m3_v1_workorders__work_order_id__return_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/m3/v1/workorders/{work_order_id}/close": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /**
         * 关闭无效、重复或无需维修的工单（M3-DSP-05）
         * @description 若在维修中则同时释放 M1 下架。
         */
        post: operations["close_api_m3_v1_workorders__work_order_id__close_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/m3/v1/workorders/{work_order_id}/start": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /**
         * 开始维修，写回下架（M3-WRK-01、M3-INT-01）
         * @description 影响范围默认整间（决策 Q7）；只有定位到房间的工单才写回。
         */
        post: operations["start_api_m3_v1_workorders__work_order_id__start_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/m3/v1/workorders/{work_order_id}/impact": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        /** 调整影响范围（M3-WRK-02，P1） */
        put: operations["change_impact_api_m3_v1_workorders__work_order_id__impact_put"];
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/m3/v1/workorders/{work_order_id}/notes": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /** 追加进度备注（M3-WRK-03，P1） */
        post: operations["add_note_api_m3_v1_workorders__work_order_id__notes_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/m3/v1/workorders/{work_order_id}/complete": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /**
         * 完工提交（M3-WRK-04）
         * @description 进入待验收；下架保持到验收通过（BR-M3-07）。
         */
        post: operations["complete_api_m3_v1_workorders__work_order_id__complete_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/m3/v1/admin/workorders/{work_order_id}/writeback/retry": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /** 手动重试失败的写回（M3-INT-03） */
        post: operations["retry_writeback_api_m3_v1_admin_workorders__work_order_id__writeback_retry_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/m3/v1/workorders/{work_order_id}/accept": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /**
         * 验收与评价（M3-ACC-01、02）
         * @description 通过：已完成并释放下架；不通过：回到维修中，修复时限重新计算。评价只能提交一次。
         */
        post: operations["accept_api_m3_v1_workorders__work_order_id__accept_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/m3/v1/workorders/{work_order_id}/accept-on-behalf": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /** 调度员代验收（M3-ACC-04，P1） */
        post: operations["accept_on_behalf_api_m3_v1_workorders__work_order_id__accept_on_behalf_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/m3/v1/admin/settings": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** 查看处理时限等 M3 参数 */
        get: operations["list_settings_api_m3_v1_admin_settings_get"];
        /**
         * 修改处理时限（M3-ESC-04）
         * @description 只影响此后进入新阶段的工单（BR-M3-16）；写入审计。
         */
        put: operations["update_settings_api_m3_v1_admin_settings_put"];
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/m3/v1/admin/categories": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        /** 维护故障类别字典（BR-M3-02） */
        put: operations["upsert_categories_api_m3_v1_admin_categories_put"];
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
        /** AcceptIn */
        AcceptIn: {
            /** Passed */
            passed: boolean;
            /**
             * Reason
             * @description 不通过时必填（BR-M3-10）
             */
            reason?: string | null;
            /**
             * Rating
             * @description 通过时可评 1 ~ 5 星（BR-M3-12）
             */
            rating?: number | null;
            /** Comment */
            comment?: string | null;
        };
        /** AssignIn */
        AssignIn: {
            /** Technicianid */
            technicianId: number;
            /** Categorycode */
            categoryCode?: string | null;
            urgency?: components["schemas"]["Urgency"] | null;
        };
        /** AttachmentOut */
        AttachmentOut: {
            /** Id */
            id: number;
            /** Filename */
            fileName: string;
            /** Url */
            url: string;
            /**
             * Uploadedat
             * Format: date-time
             */
            uploadedAt: string;
        };
        /** Body_upload_attachment_api_m3_v1_workorders__work_order_id__attachments_post */
        Body_upload_attachment_api_m3_v1_workorders__work_order_id__attachments_post: {
            /** File */
            file: string;
        };
        /** Category */
        Category: {
            /** Code */
            code: string;
            /** Name */
            name: string;
        };
        /** CategoryIn */
        CategoryIn: {
            /** Code */
            code: string;
            /** Name */
            name: string;
            /**
             * Enabled
             * @default true
             */
            enabled: boolean;
        };
        /** CompleteIn */
        CompleteIn: {
            /**
             * Resolution
             * @description 处理说明必填
             */
            resolution: string;
            /** Attachmentids */
            attachmentIds?: number[];
        };
        /** HTTPValidationError */
        HTTPValidationError: {
            /** Detail */
            detail?: components["schemas"]["ValidationError"][];
        };
        /** ImpactIn */
        ImpactIn: {
            /** @default ROOM */
            impactScope: components["schemas"]["ImpactScope"];
            /**
             * Seatids
             * @description impact_scope=SEATS 时必填
             */
            seatIds?: number[];
        };
        /**
         * ImpactScope
         * @enum {string}
         */
        ImpactScope: "ROOM" | "SEATS";
        /** NoteIn */
        NoteIn: {
            /** Content */
            content: string;
        };
        /** Page[WorkOrderOut] */
        Page_WorkOrderOut_: {
            /** Items */
            items: components["schemas"]["WorkOrderOut"][];
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
        /** ReassignIn */
        ReassignIn: {
            /** Technicianid */
            technicianId: number;
            /** Reason */
            reason: string;
        };
        /** Setting */
        Setting: {
            /**
             * Key
             * @description 如 m3.sla.accept.normal_minutes
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
        /**
         * Stage
         * @enum {string}
         */
        Stage: "ACCEPT" | "RESPOND" | "REPAIR";
        /** StatsRow */
        StatsRow: {
            /** Key */
            key: string;
            /** Total */
            total: number;
            /** Avgacceptminutes */
            avgAcceptMinutes: number;
            /** Avgrespondminutes */
            avgRespondMinutes: number;
            /** Avgrepairminutes */
            avgRepairMinutes: number;
            /** Slarate */
            slaRate: number;
            /** Avgrating */
            avgRating: number | null;
        };
        /** TechnicianLoad */
        TechnicianLoad: {
            /** Userid */
            userId: number;
            /** Name */
            name: string;
            /**
             * Opencount
             * @description 在办工单数
             */
            openCount: number;
        };
        /** TimelineEntry */
        TimelineEntry: {
            /**
             * At
             * Format: date-time
             */
            at: string;
            /** Actorid */
            actorId: string;
            /** Actorname */
            actorName: string;
            /**
             * Action
             * @description 如 SUBMIT、ASSIGN、START、NOTE、COMPLETE、ESCALATE、ACCEPT
             */
            action: string;
            /** Detail */
            detail?: string | null;
        };
        /**
         * Urgency
         * @enum {string}
         */
        Urgency: "NORMAL" | "URGENT";
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
        /** WorkOrderBrief */
        WorkOrderBrief: {
            /** Id */
            id: number;
            /** Roomname */
            roomName: string | null;
            /** Categoryname */
            categoryName: string;
            status: components["schemas"]["WorkOrderStatus"];
            /**
             * Createdat
             * Format: date-time
             */
            createdAt: string;
        };
        /** WorkOrderCreate */
        WorkOrderCreate: {
            /** Buildingid */
            buildingId: number;
            /**
             * Roomid
             * @description 可选，含公共区域
             */
            roomId?: number | null;
            /**
             * Seatid
             * @description 可选，须属于所选房间（BR-M3-01）
             */
            seatId?: number | null;
            /** Categorycode */
            categoryCode: string;
            /** @default NORMAL */
            urgency: components["schemas"]["Urgency"];
            /** Description */
            description: string;
            /** Contactphone */
            contactPhone?: string | null;
        };
        /** WorkOrderOut */
        WorkOrderOut: {
            /** Id */
            id: number;
            /** Buildingid */
            buildingId: number;
            /** Buildingname */
            buildingName: string;
            /** Roomid */
            roomId: number | null;
            /** Roomname */
            roomName: string | null;
            /** Seatid */
            seatId: number | null;
            /** Seatcode */
            seatCode: string | null;
            /** Categorycode */
            categoryCode: string;
            /** Categoryname */
            categoryName: string;
            urgency: components["schemas"]["Urgency"];
            /** Description */
            description: string;
            /** Contactphone */
            contactPhone: string | null;
            /** Reporterid */
            reporterId: number;
            /** Reportername */
            reporterName: string;
            /** Assigneeid */
            assigneeId: number | null;
            /** Assigneename */
            assigneeName: string | null;
            status: components["schemas"]["WorkOrderStatus"];
            stage: components["schemas"]["Stage"] | null;
            /**
             * Stagedeadline
             * @description 当前处理阶段的截止时刻（BR-M3-04）
             */
            stageDeadline: string | null;
            /**
             * Escalationlevel
             * @description 0 未升级；1 已通知调度员；2 已通知物业主管
             */
            escalationLevel: number;
            impactScope: components["schemas"]["ImpactScope"] | null;
            /** Impactseatids */
            impactSeatIds: number[];
            /** Resolution */
            resolution: string | null;
            /** Rating */
            rating: number | null;
            /** Comment */
            comment: string | null;
            /** Attachments */
            attachments: components["schemas"]["AttachmentOut"][];
            /** Timeline */
            timeline: components["schemas"]["TimelineEntry"][];
            /**
             * Writeback
             * @description 在 M1 中的下架同步状态（M3-INT-03）
             * @enum {string}
             */
            writeback: "NONE" | "SYNCING" | "SYNCED" | "FAILED";
            /**
             * Createdat
             * Format: date-time
             */
            createdAt: string;
        };
        /** WorkOrderPatch */
        WorkOrderPatch: {
            /** Categorycode */
            categoryCode?: string | null;
            urgency?: components["schemas"]["Urgency"] | null;
        };
        /**
         * WorkOrderStatus
         * @enum {string}
         */
        WorkOrderStatus: "SUBMITTED" | "ASSIGNED" | "IN_REPAIR" | "PENDING_ACCEPTANCE" | "COMPLETED" | "CANCELLED" | "CLOSED";
    };
    responses: never;
    parameters: never;
    requestBodies: never;
    headers: never;
    pathItems: never;
}
export type $defs = Record<string, never>;
export interface operations {
    categories_api_m3_v1_categories_get: {
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
                    "application/json": components["schemas"]["Category"][];
                };
            };
        };
    };
    duplicates_api_m3_v1_workorders_duplicates_get: {
        parameters: {
            query: {
                roomId: number;
                categoryCode: string;
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
                    "application/json": components["schemas"]["WorkOrderBrief"][];
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
    workbench_api_m3_v1_workorders_get: {
        parameters: {
            query?: {
                /** @description 页码，从 1 开始 */
                page?: number;
                /** @description 每页条数 */
                size?: number;
                status?: components["schemas"]["WorkOrderStatus"][] | null;
                categoryCode?: string | null;
                buildingId?: number | null;
                urgency?: components["schemas"]["Urgency"] | null;
                escalated?: boolean | null;
                assignedToMe?: boolean;
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
                    "application/json": components["schemas"]["Page_WorkOrderOut_"];
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
    report_api_m3_v1_workorders_post: {
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
                "application/json": components["schemas"]["WorkOrderCreate"];
            };
        };
        responses: {
            /** @description Successful Response */
            201: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["WorkOrderOut"];
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
    my_work_orders_api_m3_v1_workorders_mine_get: {
        parameters: {
            query?: {
                /** @description 页码，从 1 开始 */
                page?: number;
                /** @description 每页条数 */
                size?: number;
                status?: components["schemas"]["WorkOrderStatus"][] | null;
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
                    "application/json": components["schemas"]["Page_WorkOrderOut_"];
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
    get_work_order_api_m3_v1_workorders__work_order_id__get: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                work_order_id: number;
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
                    "application/json": components["schemas"]["WorkOrderOut"];
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
    patch_work_order_api_m3_v1_workorders__work_order_id__patch: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                work_order_id: number;
            };
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["WorkOrderPatch"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["WorkOrderOut"];
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
    cancel_api_m3_v1_workorders__work_order_id__cancel_post: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                work_order_id: number;
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
                    "application/json": components["schemas"]["WorkOrderOut"];
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
    stats_api_m3_v1_admin_stats_get: {
        parameters: {
            query: {
                dateFrom: string;
                dateTo: string;
                groupBy?: "building" | "category" | "technician";
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
                    "application/json": components["schemas"]["StatsRow"][];
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
    room_history_api_m3_v1_admin_rooms__room_id__workorders_get: {
        parameters: {
            query?: never;
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
                    "application/json": components["schemas"]["WorkOrderBrief"][];
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
    upload_attachment_api_m3_v1_workorders__work_order_id__attachments_post: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                work_order_id: number;
            };
            cookie?: never;
        };
        requestBody: {
            content: {
                "multipart/form-data": components["schemas"]["Body_upload_attachment_api_m3_v1_workorders__work_order_id__attachments_post"];
            };
        };
        responses: {
            /** @description Successful Response */
            201: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["AttachmentOut"];
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
    download_attachment_api_m3_v1_attachments__attachment_id__get: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                attachment_id: number;
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
                    "image/jpeg": unknown;
                    "image/png": unknown;
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
    technicians_api_m3_v1_technicians_get: {
        parameters: {
            query: {
                buildingId: number;
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
                    "application/json": components["schemas"]["TechnicianLoad"][];
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
    assign_api_m3_v1_workorders__work_order_id__assign_post: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                work_order_id: number;
            };
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["AssignIn"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["WorkOrderOut"];
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
    reassign_api_m3_v1_workorders__work_order_id__reassign_post: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                work_order_id: number;
            };
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["ReassignIn"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["WorkOrderOut"];
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
    return_work_order_api_m3_v1_workorders__work_order_id__return_post: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                work_order_id: number;
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
                    "application/json": components["schemas"]["WorkOrderOut"];
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
    close_api_m3_v1_workorders__work_order_id__close_post: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                work_order_id: number;
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
                    "application/json": components["schemas"]["WorkOrderOut"];
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
    start_api_m3_v1_workorders__work_order_id__start_post: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                work_order_id: number;
            };
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["ImpactIn"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["WorkOrderOut"];
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
    change_impact_api_m3_v1_workorders__work_order_id__impact_put: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                work_order_id: number;
            };
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["ImpactIn"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["WorkOrderOut"];
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
    add_note_api_m3_v1_workorders__work_order_id__notes_post: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                work_order_id: number;
            };
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["NoteIn"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["WorkOrderOut"];
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
    complete_api_m3_v1_workorders__work_order_id__complete_post: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                work_order_id: number;
            };
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["CompleteIn"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["WorkOrderOut"];
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
    retry_writeback_api_m3_v1_admin_workorders__work_order_id__writeback_retry_post: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                work_order_id: number;
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
                    "application/json": components["schemas"]["WorkOrderOut"];
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
    accept_api_m3_v1_workorders__work_order_id__accept_post: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                work_order_id: number;
            };
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["AcceptIn"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["WorkOrderOut"];
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
    accept_on_behalf_api_m3_v1_workorders__work_order_id__accept_on_behalf_post: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                work_order_id: number;
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
                    "application/json": components["schemas"]["WorkOrderOut"];
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
    list_settings_api_m3_v1_admin_settings_get: {
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
    update_settings_api_m3_v1_admin_settings_put: {
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
    upsert_categories_api_m3_v1_admin_categories_put: {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["CategoryIn"][];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["CategoryIn"][];
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
