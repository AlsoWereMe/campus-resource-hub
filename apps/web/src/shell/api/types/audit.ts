// 由 contracts/audit/openapi.yaml 生成，请勿手改。重新生成：pnpm gen:api
export interface paths {
    "/api/audit/v1/logs": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /**
         * 审计查询（AUD-02）
         * @description 审计记录只增不改，任何角色都不能修改或删除。
         */
        get: operations["logs_api_audit_v1_logs_get"];
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
        /** AuditLogOut */
        AuditLogOut: {
            /** Id */
            id: number;
            /** Actortype */
            actorType: string;
            /** Actorid */
            actorId: string;
            /** Actorname */
            actorName: string | null;
            /** Action */
            action: string;
            /** Targettype */
            targetType: string;
            /** Targetid */
            targetId: string;
            /** Before */
            before: {
                [key: string]: unknown;
            } | null;
            /** After */
            after: {
                [key: string]: unknown;
            } | null;
            /** Result */
            result: string;
            /**
             * Occurredat
             * Format: date-time
             */
            occurredAt: string;
            /** Traceid */
            traceId: string | null;
        };
        /** HTTPValidationError */
        HTTPValidationError: {
            /** Detail */
            detail?: components["schemas"]["ValidationError"][];
        };
        /** Page[AuditLogOut] */
        Page_AuditLogOut_: {
            /** Items */
            items: components["schemas"]["AuditLogOut"][];
            /** Total */
            total: number;
            /** Page */
            page: number;
            /** Size */
            size: number;
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
    logs_api_audit_v1_logs_get: {
        parameters: {
            query?: {
                /** @description 页码，从 1 开始 */
                page?: number;
                /** @description 每页条数 */
                size?: number;
                actorId?: string | null;
                action?: string | null;
                targetType?: string | null;
                targetId?: string | null;
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
                    "application/json": components["schemas"]["Page_AuditLogOut_"];
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
