import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def is_vercel_environment():
    """Check if we're running in a Vercel environment"""
    return bool(os.environ.get('VERCEL') or os.environ.get('VERCEL_ENV'))

def load_model_conditionally():
    """Load the CKD model conditionally based on environment"""
    try:
        if is_vercel_environment():
            logger.info("Running in Vercel environment - using lightweight model")
            # Import the lightweight model for Vercel to reduce bundle size
            from .vercel_model import lightweight_model
            return lightweight_model
        else:
            logger.info("Running in local environment - loading full model")
            from .ckd_model import CKDModel
            model = CKDModel()
            # Train the model in local environment
            if model.model is None:
                model.train_model()
            return model
    except Exception as e:
        logger.error(f"Error loading model: {e}")
        # Return a fallback model instance
        try:
            from .vercel_model import lightweight_model
            return lightweight_model
        except:
            from .ckd_model import CKDModel
            return CKDModel()