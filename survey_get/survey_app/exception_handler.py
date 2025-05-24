from rest_framework.views import exception_handler as drf_default_handler
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError, NotFound, ParseError
from django.db import IntegrityError
from django.core.exceptions import FieldError, ObjectDoesNotExist
import logging

logger = logging.getLogger(__name__)



# (CEH)  for Custom Exception Handler to tag error with my exception_handler



EXCEPTION_MAP = {
    FieldError: {
        'status': status.HTTP_400_BAD_REQUEST,
        'message': '(CEH) Invalid field or query'
    },
    ParseError: {
        'status': status.HTTP_400_BAD_REQUEST,
        'message': '(CEH)  Malformed request'
    },
    NotFound: {
        'status': status.HTTP_404_NOT_FOUND,
        'message': '(CEH) Resource not found'
    },
    IntegrityError: {
        'status': status.HTTP_409_CONFLICT,
        'message': '(CEH) Integrity constraint error'
    },
    ObjectDoesNotExist: {
        'status': status.HTTP_404_NOT_FOUND,
        'message': '(CEH) Object does not exist'
    },
}

def custom_exception_handler(exc, context):
    logger.error(f"[CEH] {str(exc)}", exc_info=True)

    if isinstance(exc, ValidationError):
        return Response({
            'status': 'error',
            'status_code': status.HTTP_400_BAD_REQUEST,
            'message': '(CEH) Validation error',
            'details': exc.detail,
        }, status=status.HTTP_400_BAD_REQUEST)

    for exc_type, config in EXCEPTION_MAP.items():
        if isinstance(exc, exc_type):
            return Response({
                'status': 'error',
                'status_code': config['status'],
                'message': config['message'],
                'details': str(exc),
            }, status=config['status'])

# default error like 4023 and  405 and all standerd error that come from DRF
    # Let DRF handle known ones and still wrap it
    response = drf_default_handler(exc, context)
    if response is not None:
        return Response({
            'status': 'error',
            'status_code': response.status_code,
            'message': '(CEH) An error occurred',
            'details': response.data,
        }, status=response.status_code)
        
# all other errors that we and DRF do not handel in previus code will act as 500
    return Response({
        'status': 'error',
        'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR,
        'message': '(CEH) An unexpected error occurred',
        'details': str(exc),
    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
