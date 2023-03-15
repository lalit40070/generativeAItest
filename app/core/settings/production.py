from app.core.settings.app import AppSettings


class ProdAppSettings(AppSettings):
    
    class Config(AppSettings.Config):
        """use for non docker deployment and testing"""
        #env_file = ".env.prod"

        """ use for docker based deployment and testing"""
        env_prefix = ""