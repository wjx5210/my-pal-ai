from app.context_service import select_context_by_intent
from app.pal_service import find_pals_by_name

pal = find_pals_by_name("棉悠悠")[0]


result = select_context_by_intent(
    "location",
    pal
)


print(result)