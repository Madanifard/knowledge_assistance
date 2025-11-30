from celery import Celery
from app.config import get_settings

BROKER_URI = get_settings().BROKER_URI
BACKEND_URI = get_settings().BACKEND_URI

from celery import Celery


class CeleryAppFactory:
    """
    یک کلاس سازنده (Factory) برای ساخت و پیکربندی Celery App.
    این ساختار باعث می‌شود بتوانید از چند کانفیگ مختلف در یک پروژه بزرگ استفاده کنید.
    """

    def __init__(
        self,
        name: str = "pdf_tasks",
        broker_url: str = BROKER_URI,
        backend_url: str = BACKEND_URI,
    ):
        self.name = name
        self.broker_url = broker_url
        self.backend_url = backend_url

        # ایجاد شیء Celery
        self.app = Celery(
            self.name,
            broker=self.broker_url,
            backend=self.backend_url
        )

        # اعمال تنظیمات (Config)
        self._configure()

    def _configure(self):
        """تنظیمات Celery اینجا مدیریت می‌شود."""
        self.app.conf.update(
            task_serializer="json",
            result_serializer="json",
            accept_content=["json"],

            # تنظیمات مهم برای OCR Tasks
            worker_prefetch_multiplier=1,
            task_time_limit=1200,       # hard limit
            task_soft_time_limit=1000,  # نرم‌تر و مدیریت‌شده‌تر

            timezone="UTC",
            enable_utc=True,
        )

    def get_app(self):
        """Celery App نهایی را برمی‌گرداند."""
        return self.app


# مقدار استفاده‌ی نهایی
celery_app = CeleryAppFactory().get_app()
