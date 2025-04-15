from django.http import HttpResponse
import logging

logger = logging.getLogger(__name__)

def test_view(request):
    try:
        logger.info("Test view accessed")
        return HttpResponse("Test view working!")
    except Exception as e:
        logger.error(f"Error in test view: {str(e)}")
        return HttpResponse(f"Error: {str(e)}", status=500) 