#app/utils/errorlo.py
import traceback
import socket
from datetime import datetime
from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.errorlog import ErrorLog

async def log_error_to_db(request: Request, error: Exception, db: AsyncSession):
    try:
        tb = traceback.format_exc()
        pc_name = socket.gethostname()
        method = request.method
        path = request.url.path

        error_log = ErrorLog(
            error=type(error).__name__,
            reason=tb,
            pc_name=pc_name,
            method=method,
            path=path,
            timestamp=datetime.utcnow()
        )

        db.add(error_log)
        await db.commit()

    except Exception as logging_exception:
        print("Error while logging the error:", logging_exception)
