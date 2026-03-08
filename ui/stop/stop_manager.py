from PySide6.QtCore import QObject

class StopManager(QObject):
    """
    یک کلاس کمکی برای مدیریت توقف امن Timerها و انیمیشن‌ها
    تا وقتی ویو حذف شد، crash نده.
    """

    @staticmethod
    def safe_stop(timer):
        """
        Timer را اگر فعال است متوقف می‌کند
        """
        if timer is not None and timer.isActive():
            timer.stop()

    @staticmethod
    def stop_animation(animation):
        """
        HomeAnimation یا هر شی مشابه را با متد stop ایمن متوقف می‌کند
        """
        if animation is not None and hasattr(animation, "stop"):
            animation.stop()
