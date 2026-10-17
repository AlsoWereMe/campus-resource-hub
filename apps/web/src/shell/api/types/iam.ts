// 由 contracts/iam/openapi.yaml 生成，请勿手改。重新生成：pnpm gen:api
export interface paths {
    "/api/iam/v1/auth/login": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /**
         * 账号登录（IAM-AUTH-01）
         * @description 连续失败达到上限后锁定一段时间；用户不存在与口令错误返回同一种错误。
         */
        post: operations["login_api_iam_v1_auth_login_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/iam/v1/auth/refresh": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /**
         * 用刷新令牌换取新令牌（IAM-AUTH-01）
         * @description 刷新令牌一次性使用：换取新令牌后旧刷新令牌立即失效。
         */
        post: operations["refresh_api_iam_v1_auth_refresh_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/iam/v1/auth/logout": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /** 登出（IAM-AUTH-01） */
        post: operations["logout_api_iam_v1_auth_logout_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/iam/v1/auth/password": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /**
         * 修改口令（IAM-AUTH-01）
         * @description 修改成功后，该用户所有刷新令牌失效。
         */
        post: operations["change_password_api_iam_v1_auth_password_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/iam/v1/me": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** 当前用户、角色与权限点 */
        get: operations["me_api_iam_v1_me_get"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/internal/iam/v1/jwks": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** 令牌验签公钥（JWKS） */
        get: operations["jwks_internal_iam_v1_jwks_get"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/internal/iam/v1/service-token": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /** 用服务凭证换取服务令牌 */
        post: operations["service_token_internal_iam_v1_service_token_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/internal/iam/v1/users": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /**
         * 按角色与数据范围查询有效用户（IAM-USER-02）
         * @description 返回拥有该角色、且该授权的数据范围覆盖给定院系或楼宇的启用用户；全校范围总是覆盖。
         */
        get: operations["users_by_role_internal_iam_v1_users_get"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/internal/iam/v1/users/batch": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** 按 ID 批量查询用户摘要（展示姓名、发送通知） */
        get: operations["users_by_ids_internal_iam_v1_users_batch_get"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/iam/v1/users": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** 用户列表 */
        get: operations["list_users_api_iam_v1_users_get"];
        put?: never;
        /** 新建用户（默认授予学生或教职工角色） */
        post: operations["create_user_api_iam_v1_users_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/iam/v1/users/import": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /**
         * CSV 批量导入用户（IAM-AUTH-02）
         * @description 列：学号、姓名、院系编码、邮箱、初始角色。全部校验通过才导入，否则按行号列出全部错误。
         */
        post: operations["import_users_api_iam_v1_users_import_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/iam/v1/users/{user_id}": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** 用户详情 */
        get: operations["get_user_api_iam_v1_users__user_id__get"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        /**
         * 修改用户（IAM-USER-01）
         * @description 院系变更后可见的院系专属自习室随之变化，已有预约不受影响。
         */
        patch: operations["update_user_api_iam_v1_users__user_id__patch"];
        trace?: never;
    };
    "/api/iam/v1/users/{user_id}/disable": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /**
         * 停用账号（IAM-AUTH-02）
         * @description 立即不能登录，刷新令牌全部失效；已签发访问令牌在有效期（≤ 15 分钟）后失效。
         */
        post: operations["disable_user_api_iam_v1_users__user_id__disable_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/iam/v1/users/{user_id}/enable": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /** 启用账号 */
        post: operations["enable_user_api_iam_v1_users__user_id__enable_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/iam/v1/departments": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** 院系列表（IAM-USER-01） */
        get: operations["list_departments_api_iam_v1_departments_get"];
        put?: never;
        /** 新增院系 */
        post: operations["create_department_api_iam_v1_departments_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/iam/v1/departments/{department_id}": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        /** 修改院系 */
        patch: operations["update_department_api_iam_v1_departments__department_id__patch"];
        trace?: never;
    };
    "/api/iam/v1/permissions": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** 权限点清单（IAM-ROLE-01，只读） */
        get: operations["permissions_api_iam_v1_permissions_get"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/iam/v1/roles": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** 角色列表 */
        get: operations["list_roles_api_iam_v1_roles_get"];
        put?: never;
        /** 新建角色（IAM-ROLE-02） */
        post: operations["create_role_api_iam_v1_roles_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/iam/v1/roles/{role_id}": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** 角色详情 */
        get: operations["get_role_api_iam_v1_roles__role_id__get"];
        put?: never;
        post?: never;
        /**
         * 删除角色（IAM-ROLE-02）
         * @description 仍有用户绑定时拒绝并提示人数；系统管理员角色不可删除。
         */
        delete: operations["delete_role_api_iam_v1_roles__role_id__delete"];
        options?: never;
        head?: never;
        /**
         * 修改角色（IAM-ROLE-02）
         * @description 系统管理员角色不可减少权限；权限点必须来自清单；写入审计。
         */
        patch: operations["update_role_api_iam_v1_roles__role_id__patch"];
        trace?: never;
    };
    "/api/iam/v1/users/{user_id}/roles": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** 用户的角色与数据范围（IAM-ROLE-03） */
        get: operations["user_roles_api_iam_v1_users__user_id__roles_get"];
        /**
         * 设置用户的角色与数据范围（IAM-ROLE-03、04）
         * @description 整体替换；一人可多角色，权限取并集；写入审计。
         */
        put: operations["set_user_roles_api_iam_v1_users__user_id__roles_put"];
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
        /** Body_import_users_api_iam_v1_users_import_post */
        Body_import_users_api_iam_v1_users_import_post: {
            /** File */
            file: string;
        };
        /** DepartmentIn */
        DepartmentIn: {
            /** Code */
            code: string;
            /** Name */
            name: string;
        };
        /** DepartmentOut */
        DepartmentOut: {
            /** Id */
            id: number;
            /** Code */
            code: string;
            /** Name */
            name: string;
        };
        /** HTTPValidationError */
        HTTPValidationError: {
            /** Detail */
            detail?: components["schemas"]["ValidationError"][];
        };
        /** ImportIssue */
        ImportIssue: {
            /** Line */
            line: number;
            /** Message */
            message: string;
        };
        /** ImportResult */
        ImportResult: {
            /** Imported */
            imported: number;
            /**
             * Errors
             * @description 有任何错误则整批不导入（IAM-AUTH-02）
             */
            errors: components["schemas"]["ImportIssue"][];
        };
        /** Jwks */
        Jwks: {
            /** Keys */
            keys: {
                [key: string]: unknown;
            }[];
        };
        /** LoginIn */
        LoginIn: {
            /** Username */
            username: string;
            /** Password */
            password: string;
        };
        /** MeOut */
        MeOut: {
            /** Id */
            id: number;
            /** Username */
            username: string;
            /** Name */
            name: string;
            /** Usertype */
            userType: string;
            /** Departmentid */
            departmentId: number | null;
            /** Departmentname */
            departmentName: string | null;
            /** Email */
            email: string | null;
            /** Roles */
            roles: string[];
            /** Permissions */
            permissions: string[];
        };
        /** Page[UserOut] */
        Page_UserOut_: {
            /** Items */
            items: components["schemas"]["UserOut"][];
            /** Total */
            total: number;
            /** Page */
            page: number;
            /** Size */
            size: number;
        };
        /** PasswordChangeIn */
        PasswordChangeIn: {
            /** Oldpassword */
            oldPassword: string;
            /** Newpassword */
            newPassword: string;
        };
        /** PermissionOut */
        PermissionOut: {
            /** Code */
            code: string;
            /** Description */
            description: string;
        };
        /** RefreshIn */
        RefreshIn: {
            /** Refreshtoken */
            refreshToken: string;
        };
        /** RoleGrant */
        RoleGrant: {
            /** Roleid */
            roleId: number;
            /**
             * Scopeall
             * @default false
             */
            scopeAll: boolean;
            /** Buildingids */
            buildingIds?: number[];
            /** Departmentids */
            departmentIds?: number[];
        };
        /** RoleIn */
        RoleIn: {
            /** Code */
            code: string;
            /** Name */
            name: string;
            /**
             * Description
             * @default
             */
            description: string;
            /** Permissions */
            permissions: string[];
            /**
             * Enabled
             * @default true
             */
            enabled: boolean;
        };
        /** RoleOut */
        RoleOut: {
            /** Id */
            id: number;
            /** Code */
            code: string;
            /** Name */
            name: string;
            /** Description */
            description: string;
            /** Builtin */
            builtin: boolean;
            /** Enabled */
            enabled: boolean;
            /** Permissions */
            permissions: string[];
            /** Usercount */
            userCount: number;
        };
        /** RolePatch */
        RolePatch: {
            /** Name */
            name?: string | null;
            /** Description */
            description?: string | null;
            /** Permissions */
            permissions?: string[] | null;
            /** Enabled */
            enabled?: boolean | null;
        };
        /** ServiceTokenRequest */
        ServiceTokenRequest: {
            /** Clientid */
            clientId: string;
            /** Clientsecret */
            clientSecret: string;
        };
        /** TokenResponse */
        TokenResponse: {
            /** Accesstoken */
            accessToken: string;
            /**
             * Tokentype
             * @default Bearer
             * @constant
             */
            tokenType: "Bearer";
            /** Expiresin */
            expiresIn: number;
            /** Refreshtoken */
            refreshToken?: string | null;
        };
        /** UserBrief */
        UserBrief: {
            /** Id */
            id: number;
            /** Username */
            username: string;
            /** Name */
            name: string;
            /**
             * Usertype
             * @enum {string}
             */
            userType: "student" | "staff";
            /** Departmentid */
            departmentId: number | null;
            /** Email */
            email: string | null;
        };
        /** UserCreate */
        UserCreate: {
            /** Username */
            username: string;
            /** Name */
            name: string;
            /**
             * Usertype
             * @enum {string}
             */
            userType: "student" | "staff";
            /** Departmentid */
            departmentId?: number | null;
            /** Email */
            email?: string | null;
            /** Phone */
            phone?: string | null;
            /** Initialpassword */
            initialPassword: string;
        };
        /** UserOut */
        UserOut: {
            /** Id */
            id: number;
            /**
             * Username
             * @description 学号或工号
             */
            username: string;
            /** Name */
            name: string;
            /**
             * Usertype
             * @enum {string}
             */
            userType: "student" | "staff";
            /** Departmentid */
            departmentId: number | null;
            /** Departmentname */
            departmentName: string | null;
            /** Email */
            email: string | null;
            /** Phone */
            phone: string | null;
            /**
             * Status
             * @enum {string}
             */
            status: "ACTIVE" | "DISABLED";
            /** Roles */
            roles: string[];
            /**
             * Createdat
             * Format: date-time
             */
            createdAt: string;
        };
        /** UserUpdate */
        UserUpdate: {
            /** Name */
            name?: string | null;
            /** Departmentid */
            departmentId?: number | null;
            /** Email */
            email?: string | null;
            /** Phone */
            phone?: string | null;
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
    login_api_iam_v1_auth_login_post: {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["LoginIn"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["TokenResponse"];
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
    refresh_api_iam_v1_auth_refresh_post: {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["RefreshIn"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["TokenResponse"];
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
    logout_api_iam_v1_auth_logout_post: {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["RefreshIn"];
            };
        };
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
    change_password_api_iam_v1_auth_password_post: {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["PasswordChangeIn"];
            };
        };
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
    me_api_iam_v1_me_get: {
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
                    "application/json": components["schemas"]["MeOut"];
                };
            };
        };
    };
    jwks_internal_iam_v1_jwks_get: {
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
                    "application/json": components["schemas"]["Jwks"];
                };
            };
        };
    };
    service_token_internal_iam_v1_service_token_post: {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["ServiceTokenRequest"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["TokenResponse"];
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
    users_by_role_internal_iam_v1_users_get: {
        parameters: {
            query: {
                /** @description 角色编码，如 technician */
                role: string;
                /** @description 数据范围须覆盖该院系 */
                departmentId?: number | null;
                /** @description 数据范围须覆盖该楼宇 */
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
                    "application/json": components["schemas"]["UserBrief"][];
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
    users_by_ids_internal_iam_v1_users_batch_get: {
        parameters: {
            query: {
                ids: number[];
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
                    "application/json": components["schemas"]["UserBrief"][];
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
    list_users_api_iam_v1_users_get: {
        parameters: {
            query?: {
                /** @description 页码，从 1 开始 */
                page?: number;
                /** @description 每页条数 */
                size?: number;
                /** @description 学号、工号或姓名 */
                keyword?: string | null;
                departmentId?: number | null;
                role?: string | null;
                status?: ("ACTIVE" | "DISABLED") | null;
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
                    "application/json": components["schemas"]["Page_UserOut_"];
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
    create_user_api_iam_v1_users_post: {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["UserCreate"];
            };
        };
        responses: {
            /** @description Successful Response */
            201: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["UserOut"];
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
    import_users_api_iam_v1_users_import_post: {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody: {
            content: {
                "multipart/form-data": components["schemas"]["Body_import_users_api_iam_v1_users_import_post"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["ImportResult"];
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
    get_user_api_iam_v1_users__user_id__get: {
        parameters: {
            query?: never;
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
                    "application/json": components["schemas"]["UserOut"];
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
    update_user_api_iam_v1_users__user_id__patch: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                user_id: number;
            };
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["UserUpdate"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["UserOut"];
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
    disable_user_api_iam_v1_users__user_id__disable_post: {
        parameters: {
            query?: never;
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
                    "application/json": components["schemas"]["UserOut"];
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
    enable_user_api_iam_v1_users__user_id__enable_post: {
        parameters: {
            query?: never;
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
                    "application/json": components["schemas"]["UserOut"];
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
    list_departments_api_iam_v1_departments_get: {
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
                    "application/json": components["schemas"]["DepartmentOut"][];
                };
            };
        };
    };
    create_department_api_iam_v1_departments_post: {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["DepartmentIn"];
            };
        };
        responses: {
            /** @description Successful Response */
            201: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["DepartmentOut"];
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
    update_department_api_iam_v1_departments__department_id__patch: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                department_id: number;
            };
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["DepartmentIn"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["DepartmentOut"];
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
    permissions_api_iam_v1_permissions_get: {
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
                    "application/json": components["schemas"]["PermissionOut"][];
                };
            };
        };
    };
    list_roles_api_iam_v1_roles_get: {
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
                    "application/json": components["schemas"]["RoleOut"][];
                };
            };
        };
    };
    create_role_api_iam_v1_roles_post: {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["RoleIn"];
            };
        };
        responses: {
            /** @description Successful Response */
            201: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["RoleOut"];
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
    get_role_api_iam_v1_roles__role_id__get: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                role_id: number;
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
                    "application/json": components["schemas"]["RoleOut"];
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
    delete_role_api_iam_v1_roles__role_id__delete: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                role_id: number;
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
    update_role_api_iam_v1_roles__role_id__patch: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                role_id: number;
            };
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["RolePatch"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["RoleOut"];
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
    user_roles_api_iam_v1_users__user_id__roles_get: {
        parameters: {
            query?: never;
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
                    "application/json": components["schemas"]["RoleGrant"][];
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
    set_user_roles_api_iam_v1_users__user_id__roles_put: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                user_id: number;
            };
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["RoleGrant"][];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["RoleGrant"][];
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
