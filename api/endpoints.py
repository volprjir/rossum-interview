import logging

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBasicCredentials

from exceptions.postbin import PostbinException
from exceptions.rossum import (NoRossumDataError, RossumExportError,
                               RossumLoginError)
from models.http_models import XMLConversionBody
from services.authorization_service import AuthorizationService
from services.converter_service import ConverterService
from services.postbin_service import PostbinService
from services.rossum_service import RossumService

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/export/")
async def export(
    body: XMLConversionBody,
    credentials: HTTPBasicCredentials = Depends(
        AuthorizationService.verify_credentials
    ),
):
    try:
        logger.debug("Starting export process")
        rossum_data = RossumService().export_queue(body.queue_id, body.annotation_id)
        processed_xml = ConverterService.process_xml(rossum_data)
        PostbinService.send_data(processed_xml)
        logger.debug("Export process completed successfully")
        return JSONResponse(content={"success": True})
    except NoRossumDataError as e:
        # This looks to be a happy path => warning log and success response
        logger.warning(f"No Rossum data to process.")
        return JSONResponse(content={"success": True, "error": str(e)})
    except RossumExportError as e:
        logger.error(f"Rossum export error: {e}")
        return JSONResponse(content={"success": False, "error": str(e)})
    except RossumLoginError as e:
        logger.error(f"Rossum login error: {e}")
        return JSONResponse(content={"success": False, "error": str(e)})
    except PostbinException as e:
        logger.error(f"Postbin error: {e}")
        return JSONResponse(content={"success": False, "error": str(e)})
    except Exception as e:
        logger.error(f"Unknown error: {e}")
        return JSONResponse(content={"success": False, "error": "Unknown error"})
