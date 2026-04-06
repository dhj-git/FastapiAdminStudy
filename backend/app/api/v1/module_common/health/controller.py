from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.common.response import ResponseSchema, SuccessResponse

HealthRouter = APIRouter(prefix="/health", tags=["健康检查"])


@HealthRouter.get(
    "/",
    summary="健康检查",
    description="检查系统健康状态",
    response_model=ResponseSchema[dict],
)
async def health_check() -> JSONResponse:
    """
    健康检查接口

    返回:
    - JSONResponse: 包含健康状态的JSON响应
    """
    return SuccessResponse(data=True, msg="系统健康")

# 定义了一个“健康检查”的路由”，它本身并没有做任何实际的系统状态检查逻辑。
# 它只是返回了一个固定的 JSON 响应 {"data": True, "msg": "系统健康", ...}，表示系统“健康”
# 没有实际检查 CPU、内存、磁盘、数据库连接、依赖服务等状态