// 后端统一错误结构（NFR-12）：{ code, message, details, traceId }

export type ApiError = {
  code: string;
  message: string;
  details?: Record<string, unknown>;
  traceId?: string;
};

function isApiError(value: unknown): value is ApiError {
  return (
    typeof value === "object" &&
    value !== null &&
    typeof (value as ApiError).code === "string" &&
    typeof (value as ApiError).message === "string"
  );
}

/** 把任意错误转成给用户看的一句话。 */
export function errorMessage(error: unknown): string {
  if (isApiError(error)) {
    if (error.code === "NOT_IMPLEMENTED") {
      return `该功能尚未实现（任务 ${String(error.details?.task ?? "")}）`;
    }
    return error.traceId ? `${error.message}（traceId ${error.traceId}）` : error.message;
  }
  if (error instanceof Error) return error.message;
  return "请求失败，请稍后再试";
}
