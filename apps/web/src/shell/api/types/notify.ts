// 由 contracts/notify/openapi.yaml 生成，请勿手改。重新生成：pnpm gen:api
export interface paths {
    "/api/notify/v1/inbox": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** 我的站内消息（NTF-03） */
        get: operations["inbox_api_notify_v1_inbox_get"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/notify/v1/inbox/unread-count": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** 未读数（NTF-03） */
        get: operations["unread_count_api_notify_v1_inbox_unread_count_get"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/notify/v1/inbox/{message_id}/read": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /** 标记已读（NTF-03） */
        post: operations["mark_read_api_notify_v1_inbox__message_id__read_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/notify/v1/inbox/read-all": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /** 全部标记已读（NTF-03） */
        post: operations["mark_all_read_api_notify_v1_inbox_read_all_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/notify/v1/templates": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** 通知模板列表（NTF-02） */
        get: operations["templates_api_notify_v1_templates_get"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/notify/v1/templates/{event}": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        /** 修改某类事件的模板（NTF-02） */
        put: operations["update_template_api_notify_v1_templates__event__put"];
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/notify/v1/deliveries": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** 投递记录（NTF-04） */
        get: operations["deliveries_api_notify_v1_deliveries_get"];
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
        /** Delivery */
        Delivery: {
            /** Id */
            id: number;
            /** Idempotencykey */
            idempotencyKey: string;
            /** Recipientuserid */
            recipientUserId: number;
            /** Event */
            event: string;
            /**
             * Channel
             * @enum {string}
             */
            channel: "email" | "inbox";
            /**
             * Status
             * @enum {string}
             */
            status: "PENDING" | "SENT" | "FAILED";
            /** Attempts */
            attempts: number;
            /** Lasterror */
            lastError: string | null;
            /**
             * Createdat
             * Format: date-time
             */
            createdAt: string;
            /** Sentat */
            sentAt: string | null;
        };
        /** HTTPValidationError */
        HTTPValidationError: {
            /** Detail */
            detail?: components["schemas"]["ValidationError"][];
        };
        /** InboxMessage */
        InboxMessage: {
            /** Id */
            id: number;
            /** Event */
            event: string;
            /** Title */
            title: string;
            /** Body */
            body: string;
            /** Read */
            read: boolean;
            /**
             * Createdat
             * Format: date-time
             */
            createdAt: string;
        };
        /** Page[Delivery] */
        Page_Delivery_: {
            /** Items */
            items: components["schemas"]["Delivery"][];
            /** Total */
            total: number;
            /** Page */
            page: number;
            /** Size */
            size: number;
        };
        /** Page[InboxMessage] */
        Page_InboxMessage_: {
            /** Items */
            items: components["schemas"]["InboxMessage"][];
            /** Total */
            total: number;
            /** Page */
            page: number;
            /** Size */
            size: number;
        };
        /** Template */
        Template: {
            /**
             * Event
             * @description 事件类型，如 m1.booking.reminder
             */
            event: string;
            /** Title */
            title: string;
            /**
             * Body
             * @description 支持 ${变量} 占位，如 ${roomName}
             */
            body: string;
        };
        /** TemplateIn */
        TemplateIn: {
            /** Title */
            title: string;
            /** Body */
            body: string;
        };
        /** UnreadCount */
        UnreadCount: {
            /** Count */
            count: number;
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
    };
    responses: never;
    parameters: never;
    requestBodies: never;
    headers: never;
    pathItems: never;
}
export type $defs = Record<string, never>;
export interface operations {
    inbox_api_notify_v1_inbox_get: {
        parameters: {
            query?: {
                /** @description 页码，从 1 开始 */
                page?: number;
                /** @description 每页条数 */
                size?: number;
                unreadOnly?: boolean;
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
                    "application/json": components["schemas"]["Page_InboxMessage_"];
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
    unread_count_api_notify_v1_inbox_unread_count_get: {
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
                    "application/json": components["schemas"]["UnreadCount"];
                };
            };
        };
    };
    mark_read_api_notify_v1_inbox__message_id__read_post: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                message_id: number;
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
    mark_all_read_api_notify_v1_inbox_read_all_post: {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
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
        };
    };
    templates_api_notify_v1_templates_get: {
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
                    "application/json": components["schemas"]["Template"][];
                };
            };
        };
    };
    update_template_api_notify_v1_templates__event__put: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                event: string;
            };
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["TemplateIn"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["Template"];
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
    deliveries_api_notify_v1_deliveries_get: {
        parameters: {
            query?: {
                /** @description 页码，从 1 开始 */
                page?: number;
                /** @description 每页条数 */
                size?: number;
                recipientUserId?: number | null;
                event?: string | null;
                status?: ("PENDING" | "SENT" | "FAILED") | null;
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
                    "application/json": components["schemas"]["Page_Delivery_"];
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
