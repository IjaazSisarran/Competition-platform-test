# blue prints are imported 
# explicitly instead of using *
from .user_views import user_views
from .student_views import student_views
from .admin_views import admin_views
from .competition_views import competition_views
from .results_views import results_views
from .admin import setup_admin


views = [
    user_views,
    student_views,
    admin_views,
    competition_views,
    results_views
]
# blueprints must be added to this list