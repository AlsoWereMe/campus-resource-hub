// 由 contracts/space/openapi.yaml 生成，请勿手改。重新生成：pnpm gen:api
export interface paths {
    "/api/space/v1/campuses": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** 校区列表 */
        get: operations["campuses_api_space_v1_campuses_get"];
        put?: never;
        /** 新增校区 */
        post: operations["create_campus_api_space_v1_campuses_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/space/v1/buildings": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** 楼宇列表 */
        get: operations["buildings_api_space_v1_buildings_get"];
        put?: never;
        /** 新增楼宇 */
        post: operations["create_building_api_space_v1_buildings_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/space/v1/rooms": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** 房间列表（含公共区域，可按条件筛选） */
        get: operations["rooms_api_space_v1_rooms_get"];
        put?: never;
        /** 新增房间（SPC-ROOM-01） */
        post: operations["create_room_api_space_v1_rooms_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/space/v1/rooms/{room_id}": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** 房间详情（含开放时间、整间预约属性） */
        get: operations["room_api_space_v1_rooms__room_id__get"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        /** 修改房间属性（SPC-ROOM-01、04） */
        patch: operations["update_room_api_space_v1_rooms__room_id__patch"];
        trace?: never;
    };
    "/api/space/v1/rooms/{room_id}/seats": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** 房间内的座位 */
        get: operations["room_seats_api_space_v1_rooms__room_id__seats_get"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/space/v1/seats/{seat_id}": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** 座位详情 */
        get: operations["seat_api_space_v1_seats__seat_id__get"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        /** 修改座位平面位置（SPC-SEAT-03，P2） */
        patch: operations["update_seat_api_space_v1_seats__seat_id__patch"];
        trace?: never;
    };
    "/api/space/v1/tags": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** 座位标记字典 */
        get: operations["tags_api_space_v1_tags_get"];
        put?: never;
        /** 扩展标记字典（SPC-TAG-01，P2） */
        post: operations["create_tag_api_space_v1_tags_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/space/v1/rooms/{room_id}/study": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /**
         * 开放为自习室或关闭自习（SPC-ROOM-02）
         * @description 关闭时若有未结束预约，先返回影响预览；确认后执行，受影响学生收到通知且不计违约。
         */
        post: operations["set_study_open_api_space_v1_rooms__room_id__study_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/space/v1/rooms/{room_id}/status": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /** 启用、停用、注销房间（SPC-ROOM-01、02） */
        post: operations["set_room_status_api_space_v1_rooms__room_id__status_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/space/v1/rooms/{room_id}/booking-policy": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        /** 整间预约属性（SPC-ROOM-05） */
        put: operations["set_booking_policy_api_space_v1_rooms__room_id__booking_policy_put"];
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/space/v1/rooms/{room_id}/facilities": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        /** 房间设施（SPC-ROOM-06，P2） */
        put: operations["set_facilities_api_space_v1_rooms__room_id__facilities_put"];
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/space/v1/rooms/{room_id}/opening-hours": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        /**
         * 设置按星期的开放时间（SPC-ROOM-03）
         * @description 非整点被拒绝（BR-22）；缩短开放时间时按 SPC-ROOM-02 的确认流程处理受影响预约。
         */
        put: operations["set_opening_hours_api_space_v1_rooms__room_id__opening_hours_put"];
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/space/v1/rooms/{room_id}/closures": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** 闭馆日列表（P1） */
        get: operations["list_closures_api_space_v1_rooms__room_id__closures_get"];
        put?: never;
        /** 新增闭馆日（P1） */
        post: operations["add_closure_api_space_v1_rooms__room_id__closures_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/space/v1/rooms/{room_id}/closures/{closure_id}": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        post?: never;
        /** 删除闭馆日（P1） */
        delete: operations["delete_closure_api_space_v1_rooms__room_id__closures__closure_id__delete"];
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/space/v1/seats": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /** 登记座位（SPC-SEAT-01） */
        post: operations["create_seat_api_space_v1_seats_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/space/v1/rooms/{room_id}/seats/batch": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /** 批量生成座位（SPC-SEAT-01，P1） */
        post: operations["create_seats_batch_api_space_v1_rooms__room_id__seats_batch_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/space/v1/rooms/{room_id}/seats/import": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /** CSV 导入座位（SPC-SEAT-01，P2） */
        post: operations["import_seats_api_space_v1_rooms__room_id__seats_import_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/space/v1/seats/status": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /**
         * 停用、恢复、注销座位（SPC-SEAT-01、02）
         * @description 停用在 M1 中表现为写入来源 ADMIN 的占用块；受影响预约按 BR-19 处理。
         */
        post: operations["set_seats_status_api_space_v1_seats_status_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/space/v1/seats/tags": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /** 批量添加、移除座位标记（SPC-TAG-01） */
        post: operations["set_seat_tags_api_space_v1_seats_tags_post"];
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
        /**
         * ApplicantType
         * @enum {string}
         */
        ApplicantType: "STAFF" | "STUDENT_LEADER";
        /** Body_import_seats_api_space_v1_rooms__room_id__seats_import_post */
        Body_import_seats_api_space_v1_rooms__room_id__seats_import_post: {
            /** File */
            file: string;
        };
        /** BookingPolicyIn */
        BookingPolicyIn: {
            /** Wholeroombookable */
            wholeRoomBookable: boolean;
            /** Allowedapplicanttypes */
            allowedApplicantTypes?: components["schemas"]["ApplicantType"][];
        };
        /** Building */
        Building: {
            /** Id */
            id: number;
            /** Campusid */
            campusId: number;
            /** Code */
            code: string;
            /** Name */
            name: string;
        };
        /** BuildingIn */
        BuildingIn: {
            /** Campusid */
            campusId: number;
            /** Code */
            code: string;
            /** Name */
            name: string;
        };
        /** Campus */
        Campus: {
            /** Id */
            id: number;
            /** Code */
            code: string;
            /** Name */
            name: string;
        };
        /** CampusIn */
        CampusIn: {
            /** Code */
            code: string;
            /** Name */
            name: string;
        };
        /** ClosureIn */
        ClosureIn: {
            /**
             * Date
             * Format: date
             */
            date: string;
            /** Reason */
            reason: string;
        };
        /** ClosureOut */
        ClosureOut: {
            /**
             * Date
             * Format: date
             */
            date: string;
            /** Reason */
            reason: string;
            /** Id */
            id: number;
        };
        /** FacilitiesIn */
        FacilitiesIn: {
            /**
             * Facilities
             * @description 如 PROJECTOR、SPEAKER、MICROPHONE（SPC-ROOM-06，P2）
             */
            facilities: string[];
        };
        /** HTTPValidationError */
        HTTPValidationError: {
            /** Detail */
            detail?: components["schemas"]["ValidationError"][];
        };
        /** ImpactPreview */
        ImpactPreview: {
            /**
             * Affectedbookingcount
             * @description 将被系统取消的未结束预约数（BR-19）
             */
            affectedBookingCount: number;
            /**
             * Executed
             * @description confirm=false 时只预览，不执行
             */
            executed: boolean;
            room?: components["schemas"]["RoomInfo"] | null;
        };
        /** OpeningHoursIn */
        OpeningHoursIn: {
            /**
             * Rules
             * @description 起止必须为整点，同一天的区间不得重叠
             */
            rules: components["schemas"]["OpeningRule"][];
            /**
             * Confirm
             * @description 缩短导致冲突时先预览，确认后执行
             * @default false
             */
            confirm: boolean;
        };
        /** OpeningRule */
        OpeningRule: {
            /**
             * Weekday
             * @description 1=周一 … 7=周日
             */
            weekday: number;
            /** Starthour */
            startHour: number;
            /**
             * Endhour
             * @description 不含；起止均为整点（BR-22）
             */
            endHour: number;
        };
        /**
         * OwnerType
         * @enum {string}
         */
        OwnerType: "SCHOOL" | "DEPARTMENT";
        /** Page[RoomInfo] */
        Page_RoomInfo_: {
            /** Items */
            items: components["schemas"]["RoomInfo"][];
            /** Total */
            total: number;
            /** Page */
            page: number;
            /** Size */
            size: number;
        };
        /** RoomIn */
        RoomIn: {
            /** Buildingid */
            buildingId: number;
            /**
             * Code
             * @description 全局唯一（SPC-ROOM-01）
             */
            code: string;
            /** Name */
            name: string;
            /** Floor */
            floor?: number | null;
            roomType: components["schemas"]["RoomType"];
            /** Capacity */
            capacity: number;
            /** @default SCHOOL */
            ownerType: components["schemas"]["OwnerType"];
            /**
             * Departmentid
             * @description owner_type=DEPARTMENT 时必填
             */
            departmentId?: number | null;
        };
        /** RoomInfo */
        RoomInfo: {
            /** Id */
            id: number;
            /** Code */
            code: string;
            /** Name */
            name: string;
            /** Campusid */
            campusId: number;
            /** Buildingid */
            buildingId: number;
            /** Buildingname */
            buildingName: string;
            /** Floor */
            floor?: number | null;
            roomType: components["schemas"]["RoomType"];
            /** Capacity */
            capacity: number;
            ownerType: components["schemas"]["OwnerType"];
            /**
             * Departmentid
             * @description 归属院系；校级房间为空
             */
            departmentId?: number | null;
            status: components["schemas"]["Status"];
            /**
             * Studyopen
             * @description 是否开放为自习室（SPC-ROOM-02）
             */
            studyOpen: boolean;
            /**
             * Wholeroombookable
             * @description 是否允许整间预约（SPC-ROOM-05）
             */
            wholeRoomBookable: boolean;
            /** Allowedapplicanttypes */
            allowedApplicantTypes?: components["schemas"]["ApplicantType"][];
            /** Facilities */
            facilities?: string[];
            /** Openingrules */
            openingRules?: components["schemas"]["OpeningRule"][];
            /**
             * Closures
             * @description 闭馆日期（P1）
             */
            closures?: string[];
        };
        /** RoomPatch */
        RoomPatch: {
            /** Name */
            name?: string | null;
            /** Floor */
            floor?: number | null;
            roomType?: components["schemas"]["RoomType"] | null;
            /** Capacity */
            capacity?: number | null;
            ownerType?: components["schemas"]["OwnerType"] | null;
            /** Departmentid */
            departmentId?: number | null;
        };
        /**
         * RoomType
         * @enum {string}
         */
        RoomType: "CLASSROOM" | "LIBRARY_STUDY" | "OTHER_STUDY" | "MEETING" | "PUBLIC_AREA";
        /** SeatBatchIn */
        SeatBatchIn: {
            /**
             * Count
             * @description 按序号自动编号，与已有座位不冲突（P1）
             */
            count: number;
            /**
             * Perrow
             * @default 8
             */
            perRow: number;
        };
        /** SeatIn */
        SeatIn: {
            /** Roomid */
            roomId: number;
            /**
             * Code
             * @description 全局唯一，建议「房间编号-序号」
             */
            code: string;
            /** Row */
            row?: number | null;
            /** Col */
            col?: number | null;
            /** Tags */
            tags?: string[];
        };
        /** SeatInfo */
        SeatInfo: {
            /** Id */
            id: number;
            /** Roomid */
            roomId: number;
            /** Code */
            code: string;
            status: components["schemas"]["Status"];
            /** Tags */
            tags?: string[];
            /** Row */
            row?: number | null;
            /** Col */
            col?: number | null;
        };
        /** SeatPatch */
        SeatPatch: {
            /** Row */
            row?: number | null;
            /** Col */
            col?: number | null;
        };
        /** SeatStatusIn */
        SeatStatusIn: {
            /** Seatids */
            seatIds: number[];
            status: components["schemas"]["Status"];
            /**
             * Reason
             * @description 停用原因必填（SPC-SEAT-02）
             */
            reason: string;
            /**
             * Confirm
             * @default false
             */
            confirm: boolean;
        };
        /** SeatTagsIn */
        SeatTagsIn: {
            /** Seatids */
            seatIds: number[];
            /** Add */
            add?: string[];
            /** Remove */
            remove?: string[];
        };
        /**
         * Status
         * @enum {string}
         */
        Status: "ENABLED" | "DISABLED" | "DELETED";
        /** StatusIn */
        StatusIn: {
            status: components["schemas"]["Status"];
            /**
             * Confirm
             * @default false
             */
            confirm: boolean;
        };
        /** StudyOpenIn */
        StudyOpenIn: {
            /** Studyopen */
            studyOpen: boolean;
            /**
             * Confirm
             * @default false
             */
            confirm: boolean;
        };
        /** TagIn */
        TagIn: {
            /** Code */
            code: string;
            /** Name */
            name: string;
        };
        /** TagOut */
        TagOut: {
            /** Code */
            code: string;
            /** Name */
            name: string;
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
    campuses_api_space_v1_campuses_get: {
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
                    "application/json": components["schemas"]["Campus"][];
                };
            };
        };
    };
    create_campus_api_space_v1_campuses_post: {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["CampusIn"];
            };
        };
        responses: {
            /** @description Successful Response */
            201: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["Campus"];
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
    buildings_api_space_v1_buildings_get: {
        parameters: {
            query?: {
                campusId?: number | null;
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
                    "application/json": components["schemas"]["Building"][];
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
    create_building_api_space_v1_buildings_post: {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["BuildingIn"];
            };
        };
        responses: {
            /** @description Successful Response */
            201: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["Building"];
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
    rooms_api_space_v1_rooms_get: {
        parameters: {
            query?: {
                /** @description 页码，从 1 开始 */
                page?: number;
                /** @description 每页条数 */
                size?: number;
                campusId?: number | null;
                buildingId?: number | null;
                roomType?: components["schemas"]["RoomType"] | null;
                /** @description 只看已开放为自习室的房间 */
                studyOpen?: boolean | null;
                /** @description 只看允许整间预约的房间 */
                wholeRoomBookable?: boolean | null;
                departmentId?: number | null;
                /** @description 匹配房间编号或名称 */
                keyword?: string | null;
                /** @description 按 ID 批量查询 */
                ids?: number[] | null;
                /** @description 包含已注销的房间（用于历史展示） */
                includeDeleted?: boolean;
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
                    "application/json": components["schemas"]["Page_RoomInfo_"];
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
    create_room_api_space_v1_rooms_post: {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["RoomIn"];
            };
        };
        responses: {
            /** @description Successful Response */
            201: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["RoomInfo"];
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
    room_api_space_v1_rooms__room_id__get: {
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
                    "application/json": components["schemas"]["RoomInfo"];
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
    update_room_api_space_v1_rooms__room_id__patch: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                room_id: number;
            };
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["RoomPatch"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["RoomInfo"];
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
    room_seats_api_space_v1_rooms__room_id__seats_get: {
        parameters: {
            query?: {
                /** @description 须带全部所列标记 */
                tag?: string[] | null;
                includeDisabled?: boolean;
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
                    "application/json": components["schemas"]["SeatInfo"][];
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
    seat_api_space_v1_seats__seat_id__get: {
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
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["SeatInfo"];
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
    update_seat_api_space_v1_seats__seat_id__patch: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                seat_id: number;
            };
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["SeatPatch"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["SeatInfo"];
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
    tags_api_space_v1_tags_get: {
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
                    "application/json": components["schemas"]["TagOut"][];
                };
            };
        };
    };
    create_tag_api_space_v1_tags_post: {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["TagIn"];
            };
        };
        responses: {
            /** @description Successful Response */
            201: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["TagOut"];
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
    set_study_open_api_space_v1_rooms__room_id__study_post: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                room_id: number;
            };
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["StudyOpenIn"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["ImpactPreview"];
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
    set_room_status_api_space_v1_rooms__room_id__status_post: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                room_id: number;
            };
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["StatusIn"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["ImpactPreview"];
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
    set_booking_policy_api_space_v1_rooms__room_id__booking_policy_put: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                room_id: number;
            };
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["BookingPolicyIn"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["RoomInfo"];
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
    set_facilities_api_space_v1_rooms__room_id__facilities_put: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                room_id: number;
            };
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["FacilitiesIn"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["RoomInfo"];
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
    set_opening_hours_api_space_v1_rooms__room_id__opening_hours_put: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                room_id: number;
            };
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["OpeningHoursIn"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["ImpactPreview"];
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
    list_closures_api_space_v1_rooms__room_id__closures_get: {
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
                    "application/json": components["schemas"]["ClosureOut"][];
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
    add_closure_api_space_v1_rooms__room_id__closures_post: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                room_id: number;
            };
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["ClosureIn"];
            };
        };
        responses: {
            /** @description Successful Response */
            201: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["ClosureOut"];
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
    delete_closure_api_space_v1_rooms__room_id__closures__closure_id__delete: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                room_id: number;
                closure_id: number;
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
    create_seat_api_space_v1_seats_post: {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["SeatIn"];
            };
        };
        responses: {
            /** @description Successful Response */
            201: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["SeatInfo"];
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
    create_seats_batch_api_space_v1_rooms__room_id__seats_batch_post: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                room_id: number;
            };
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["SeatBatchIn"];
            };
        };
        responses: {
            /** @description Successful Response */
            201: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["SeatInfo"][];
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
    import_seats_api_space_v1_rooms__room_id__seats_import_post: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                room_id: number;
            };
            cookie?: never;
        };
        requestBody: {
            content: {
                "multipart/form-data": components["schemas"]["Body_import_seats_api_space_v1_rooms__room_id__seats_import_post"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["SeatInfo"][];
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
    set_seats_status_api_space_v1_seats_status_post: {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["SeatStatusIn"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["ImpactPreview"];
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
    set_seat_tags_api_space_v1_seats_tags_post: {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["SeatTagsIn"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["SeatInfo"][];
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
