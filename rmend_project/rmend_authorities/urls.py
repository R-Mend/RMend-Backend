from django.urls import path
from .views import AuthorityManagerLoginView, AuthorityIssueTypeGroupView, AuthorityIssueTypeView, IssueTypeGroupView


app_name = 'rmend_authorities'

urlpatterns = [
    path('authority/', AuthorityManagerLoginView),
    path('authority/issue-groups', AuthorityIssueTypeGroupView.as_view()),
    path('authority/issue-types', AuthorityIssueTypeView.as_view()),
    path('issue-groups/', IssueTypeGroupView.as_view())
]